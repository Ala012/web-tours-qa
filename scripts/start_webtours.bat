@echo off
setlocal
set "WEBTOURS_HOME=D:\web tours\WebTours"

if not exist "%WEBTOURS_HOME%\bin\httpd.exe" (
    echo [ERREUR] WebTours introuvable dans "%WEBTOURS_HOME%".
    exit /b 1
)

tasklist /FI "IMAGENAME eq httpd.exe" 2>nul | find /I "httpd.exe" >nul
if not errorlevel 1 (
    echo WebTours est deja demarre.
    exit /b 0
)

echo Demarrage de WebTours...
start "WebTours" /MIN "%WEBTOURS_HOME%\bin\httpd.exe" -d "%WEBTOURS_HOME%"

echo Attente du port 1080...
for /L %%i in (1,1,30) do (
    powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:1080/WebTours/index.htm' -UseBasicParsing -TimeoutSec 2; if ($r.StatusCode -eq 200) { exit 0 } } catch { }; exit 1" >nul 2>&1
    if not errorlevel 1 (
        echo WebTours est pret sur http://127.0.0.1:1080/WebTours/index.htm
        exit /b 0
    )
    timeout /t 1 /nobreak >nul
)

echo [ERREUR] WebTours ne repond pas sur le port 1080.
exit /b 1
