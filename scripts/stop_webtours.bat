@echo off
taskkill /IM httpd.exe /F >nul 2>&1
if errorlevel 1 (
    echo Aucun processus httpd.exe en cours.
) else (
    echo WebTours arrete.
)
