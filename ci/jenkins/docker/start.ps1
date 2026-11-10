# Lance Jenkins dans Docker pour le mini-projet QA WebTours.
#
#   powershell -ExecutionPolicy Bypass -File ci\jenkins\docker\start.ps1
#
# - construit l'image (Jenkins + Python + Chrome) ;
# - demarre le conteneur sur http://127.0.0.1:8080 ;
# - demarre WebTours sur l'hote s'il ne tourne pas deja.

param(
    [switch]$NoBuild
)

$ErrorActionPreference = "Stop"

$composeDir = $PSScriptRoot
$repoRoot = Resolve-Path (Join-Path $composeDir "..\..\..")
$envFile = Join-Path $composeDir ".env"
$composeFile = Join-Path $composeDir "docker-compose.yml"

# 1. Mot de passe admin local (jamais versionne).
if (-not (Test-Path $envFile)) {
    $pw = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 24 | ForEach-Object { [char]$_ })
    Set-Content -Path $envFile -Value "JENKINS_ADMIN_PASSWORD=$pw" -NoNewline
    Write-Host "Mot de passe admin genere : $envFile"
}
$password = (Select-String -Path $envFile -Pattern '^JENKINS_ADMIN_PASSWORD=').Line `
    -replace '^JENKINS_ADMIN_PASSWORD=', ''

# 2. WebTours doit tourner sur l'hote Windows.
$webToursUp = $false
try {
    $r = Invoke-WebRequest -Uri "http://127.0.0.1:1080/WebTours/index.htm" -UseBasicParsing -TimeoutSec 3
    $webToursUp = ($r.StatusCode -eq 200)
} catch { }
if (-not $webToursUp) {
    Write-Host "Demarrage de WebTours sur l'hote..."
    & "$repoRoot\scripts\start_webtours.bat"
}

# 3. Construction + demarrage du conteneur.
Push-Location $composeDir
try {
    if ($NoBuild) {
        docker compose up -d
    } else {
        docker compose up -d --build
    }
    if ($LASTEXITCODE -ne 0) {
        throw "docker compose a echoue (code $LASTEXITCODE)"
    }
} finally {
    Pop-Location
}

# 4. Attente de Jenkins.
$ready = $false
for ($i = 0; $i -lt 120; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "http://127.0.0.1:8080/login" -UseBasicParsing -TimeoutSec 3
        if ($r.StatusCode -eq 200) { $ready = $true; break }
    } catch { }
    Start-Sleep -Seconds 2
}

Write-Host ""
if ($ready) {
    Write-Host "Jenkins est pret : http://127.0.0.1:8080"
} else {
    Write-Host "Jenkins met encore du temps a demarrer : docker logs -f webtours-jenkins"
}
Write-Host "Utilisateur : admin"
Write-Host "Mot de passe : $password  (fichier $envFile)"
Write-Host "Job : WebTours-QA (build manuel ou polling SCM toutes les ~5 min)"
