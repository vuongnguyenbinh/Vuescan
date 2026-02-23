@echo off
title FiScanPro - Build
echo Building FiScanPro...
cd /d "%~dp0.."
python scripts/build.py
pause
