@echo off
title Detener Servidor Python

echo Deteniendo servidor Flask...
taskkill /f /im python.exe >nul 2>&1

echo.
echo Servidor detenido.
pause