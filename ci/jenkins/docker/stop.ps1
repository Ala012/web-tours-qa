# Arrete le conteneur Jenkins (le volume de donnees est conserve).
#
#   powershell -ExecutionPolicy Bypass -File ci\jenkins\docker\stop.ps1
#   ... -RemoveVolume   # supprime aussi les donnees Jenkins (reset complet)

param(
    [switch]$RemoveVolume
)

$composeDir = $PSScriptRoot
$composeFile = Join-Path $composeDir "docker-compose.yml"

Push-Location $composeDir
try {
    if ($RemoveVolume) {
        docker compose -f $composeFile down -v
    } else {
        docker compose -f $composeFile down
    }
} finally {
    Pop-Location
}
