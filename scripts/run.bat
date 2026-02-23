@echo off
title FiScanPro - Document Scanner
echo Starting FiScanPro...
cd /d "%~dp0.."
python -m src.main
pause
