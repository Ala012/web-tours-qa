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

# 3. Rotation du compte admin si le mot de passe de .env a change.
#    Le conteneur garde en memoire le mot de passe de sa creation : on supprime
#    le compte (users/admin_<hash>) puis on recree le conteneur pour que
#    init.groovy.d/01-admin.groovy le recree avec le nouveau secret.
$containerName = "webtours-jenkins"
$rotate = $false
$containerExists = (docker ps -a --format "{{.Names}}") -match "^$containerName$"
if ($containerExists) {
    $envLine = docker inspect $containerName --format '{{range .Config.Env}}{{println .}}{{end}}' |
        Select-String '^JENKINS_ADMIN_PASSWORD='
    if ($envLine) {
        $containerPassword = $envLine.Line -replace '^JENKINS_ADMIN_PASSWORD=', ''
        if ($containerPassword -ne $password) {
            Write-Host "Mot de passe admin modifie : rotation du compte..."
            $volume = (docker inspect $containerName --format '{{json .Mounts}}' |
                ConvertFrom-Json |
                Where-Object { $_.Destination -eq '/var/jenkins_home' }).Name
            docker stop $containerName | Out-Null
            docker run --rm -v "${volume}:/var/jenkins_home" alpine `
                sh -c "rm -rf /var/jenkins_home/users/admin_*" | Out-Null
            $rotate = $true
        }
    }
}

# 4. Construction + demarrage du conteneur.
Push-Location $composeDir
try {
    $composeArgs = @("compose", "up", "-d")
    if ($rotate) { $composeArgs += "--force-recreate" }
    if (-not $NoBuild) { $composeArgs += "--build" }
    & docker @composeArgs
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
Write-Host "Mot de passe : voir $envFile (non affiche)"
Write-Host "Job : WebTours-QA (build manuel ou polling SCM toutes les ~5 min)"
