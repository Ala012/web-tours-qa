# Lance Jenkins en local (Windows) pour le mini-projet QA WebTours.
#
#   powershell -ExecutionPolicy Bypass -File ci\jenkins\run-jenkins.ps1
#
# Le JENKINS_HOME est place hors du depot (par defaut D:\web tours\jenkins)
# pour ne jamais commiter les donnees Jenkins ni le mot de passe admin.

param(
    [string]$JenkinsHome = "D:\web tours\jenkins",
    [int]$Port = 8080
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path $JenkinsHome | Out-Null
$war = Join-Path $JenkinsHome "jenkins.war"
if (-not (Test-Path $war)) {
    Write-Host "Telechargement de Jenkins LTS..."
    Invoke-WebRequest -Uri "https://get.jenkins.io/war-stable/latest/jenkins.war" -OutFile $war
}

$home = Join-Path $JenkinsHome "home"
$initDir = Join-Path $home "init.groovy.d"
New-Item -ItemType Directory -Force -Path $initDir | Out-Null
Copy-Item (Join-Path $PSScriptRoot "init.groovy.d\01-admin.groovy") `
    (Join-Path $initDir "01-admin.groovy") -Force

$pwFile = Join-Path $JenkinsHome "admin-password.txt"
if (-not (Test-Path $pwFile)) {
    $pw = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 20 | ForEach-Object { [char]$_ })
    Set-Content -Path $pwFile -Value $pw -NoNewline
    Write-Host "Mot de passe admin genere : $pwFile"
}

# Jenkins LTS recent exige Java 21+ : on utilise un JDK 21 local si besoin.
$jdkRoot = Join-Path $JenkinsHome "jdk21"
$javaDir = Get-ChildItem $jdkRoot -Directory -ErrorAction SilentlyContinue |
    Select-Object -First 1
if (-not $javaDir) {
    $zip = Join-Path $JenkinsHome "jdk21.zip"
    if (-not (Test-Path $zip)) {
        Write-Host "Telechargement de Temurin JDK 21..."
        Invoke-WebRequest -Uri "https://api.adoptium.net/v3/binary/latest/21/ga/windows/x64/jdk/hotspot/normal/eclipse?project=jdk" -OutFile $zip
    }
    Expand-Archive -Path $zip -DestinationPath $jdkRoot -Force
    $javaDir = Get-ChildItem $jdkRoot -Directory | Select-Object -First 1
}
$java = Join-Path $javaDir.FullName "bin\java.exe"

$env:JENKINS_HOME = $home
$env:JENKINS_ADMIN_PASSWORD = Get-Content $pwFile -Raw
$env:JAVA_TOOL_OPTIONS = '-Djenkins.install.runSetupWizard=false'

Write-Host "Jenkins demarre sur http://127.0.0.1:$Port (utilisateur : admin)"
Write-Host "Mot de passe : $pwFile"
& $java -jar $war --httpPort=$Port
