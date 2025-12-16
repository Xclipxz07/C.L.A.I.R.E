@echo off
REM Build Claire as a standalone .exe - Simple One-Click Build
title Building Claire.exe...

echo ========================================
echo   Claire - Building Standalone .exe
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create venv if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
) else (
    REM Check if venv has old S.N.O.W path and recreate if needed
    findstr /C:"S.N.O.W" venv\pyvenv.cfg >nul 2>&1
    if not errorlevel 1 (
        echo Detected old venv configuration, recreating...
        rmdir /S /Q venv
        python -m venv venv
        echo.
    )
)

REM Activate and install requirements
call venv\Scripts\activate.bat

echo [1/4] Installing dependencies...
pip install --quiet pyyaml requests PyQt6
echo      Done!
echo.

echo [2/4] Installing PyInstaller...
pip install --quiet pyinstaller
echo      Done!
echo.

REM Build the executable
echo [3/4] Building Claire.exe (takes 2-5 minutes)...
echo      Please wait...
pyinstaller --clean --noconfirm claire.spec
if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)
echo      Done!
echo.

REM Setup distribution folder
echo [4/4] Finalizing...
if not exist "dist\Claire\logs\" mkdir dist\Claire\logs
if not exist "dist\Claire\data\" mkdir dist\Claire\data
copy config.example.yaml dist\Claire\config.yaml >nul 2>&1
echo      Done!
echo.

echo ========================================
echo   SUCCESS! Build Complete!
echo ========================================
echo.
echo Your app is ready: dist\Claire\Claire.exe
echo Size: ~100 MB (includes Python + all dependencies)
echo.
echo WHAT'S NEXT:
echo   1. Go to: dist\Claire\
echo   2. Double-click: Claire.exe
echo   3. That's it!
echo.
echo TO SHARE WITH OTHERS:
echo   - Copy entire "dist\Claire" folder
echo   - They just run Claire.exe
echo   - No Python or setup needed!
echo.
echo NOTE: Make sure Ollama is installed for AI features
echo   Download from: https://ollama.ai
echo.

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $shortcut = $ws.CreateShortcut($env:USERPROFILE + '\Desktop\Claire AI.lnk'); $shortcut.TargetPath = '%~dp0dist\Claire\Claire.exe'; $shortcut.WorkingDirectory = '%~dp0dist\Claire'; $shortcut.Description = 'Claire - Your AI Assistant'; $shortcut.Save()"
echo Desktop shortcut created: "Claire AI"
echo.

echo Press any key to exit...
pause >nul
