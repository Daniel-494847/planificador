@echo off
title Generador PDC - Servidor Python
color 0A

echo ========================================
echo  INICIANDO GENERADOR DE PDC + PYTORCH
echo ========================================
echo.

cd /d "c:\Users\EQUIPO\Desktop\PLANIFICADOR\backend"

echo [1/3] Activando entorno virtual Python...
call venv\Scripts\activate.bat

echo [2/3] Iniciando servidor Flask + PyTorch en http://localhost:5000
start "Servidor Python" python app.py

echo [3/3] Abriendo navegador...
timeout /t 3 >nul
start "" "http://localhost:5000/"

echo.
echo ========================================
echo  SERVIDOR INICIADO CORRECTAMENTE
echo  - URL: http://localhost:5000/
echo  - Para detener: ejecuta DETENER.bat
echo ========================================
pause