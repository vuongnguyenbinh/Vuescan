@echo off
title FiScanPro - Install Dependencies
echo Installing FiScanPro dependencies...
cd /d "%~dp0.."
pip install -r requirements.txt
echo.
echo Dependencies installed successfully!
pause
