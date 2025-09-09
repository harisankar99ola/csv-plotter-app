@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Installer / Launcher for CSV Plotter App
REM 1. Creates a venv (if missing)
REM 2. Upgrades pip & installs/updates the app from git
REM 3. Launches the app

SET REPO_URL=https://github.com/harisankar99ola/csv-plotter-app.git#windows
SET VENV_DIR=.venv

IF NOT EXIST %VENV_DIR% (
    echo Creating virtual environment...
    py -3 -m venv %VENV_DIR%
)

CALL %VENV_DIR%\Scripts\activate.bat

ECHO Upgrading pip...
python -m pip install --upgrade pip

ECHO Installing / updating csv-plotter-app from Git...
pip install --upgrade git+%REPO_URL%

ECHO Creating shortcut on Desktop...
pip install pywin32
csvplotter-shortcut

ECHO Launching app...
csvplotter

ENDLOCAL
