@echo off
REM Build Claire (New Version) - Enhanced Build Script
title Building Claire.exe (New Build System)...

REM Keep window open on any exit
if not defined IN_SUBPROCESS (cmd /k set IN_SUBPROCESS=1 ^& %0 %*) & exit

echo ========================================
echo   Claire - New Build System v2.0
echo ========================================
echo.

REM Set build timestamp
set BUILD_DATE=%date:~-4%%date:~-10,2%%date:~-7,2%
set BUILD_TIME=%time:~0,2%%time:~3,2%%time:~6,2%
set BUILD_TIME=%BUILD_TIME: =0%

echo Build started: %date% %time%
echo.

REM Check if Python is installed
echo [0/6] Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Display Python version
python --version 2>&1
echo      Python - OK
echo.

REM Check if Ollama is available (optional but recommended)
ollama --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama not detected
    echo      AI features will require Ollama installation
    echo      Download from: https://ollama.ai
    echo.
) else (
    echo      Ollama: Detected - OK
    echo.
)

REM Clean previous builds
if exist "dist\Claire\" (
    echo [1/6] Cleaning previous build...
    rmdir /S /Q dist\Claire 2>nul
    echo      Done!
    echo.
)

if exist "build\claire\" (
    rmdir /S /Q build\claire 2>nul
)

REM Create/Update venv
if not exist "venv\" (
    echo [2/6] Creating virtual environment...
    python -m venv venv
    echo      Done!
    echo.
    goto :activate_venv
)

REM Check if venv has old configuration and recreate if needed
findstr /C:"S.N.O.W" venv\pyvenv.cfg >nul 2>&1
if not errorlevel 1 (
    echo [2/6] Updating virtual environment ^(old config detected^)...
    rmdir /S /Q venv
    python -m venv venv
    echo      Done!
    echo.
    goto :activate_venv
)

echo [2/6] Virtual environment already exists
echo      Skipping...
echo.

:activate_venv
REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo [3/6] Installing dependencies...
echo      Installing core packages...
pip install --quiet --upgrade pip
pip install --quiet pyyaml requests PyQt6
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo      Done!
echo.

REM Install PyInstaller
echo [4/6] Installing PyInstaller...
pip install --quiet pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo      Done!
echo.

REM Build the executable
echo [5/6] Building Claire.exe...
echo      This may take 2-5 minutes, please wait...
echo      Processing modules and dependencies...
echo.

pyinstaller --clean --noconfirm claire.spec
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERROR: Build Failed!
    echo ========================================
    echo.
    echo Check the error messages above for details.
    echo Common issues:
    echo   - Missing dependencies
    echo   - File permission errors
    echo   - Antivirus interference
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo      Build completed successfully!
echo.

REM Setup distribution folder
echo [6/6] Finalizing distribution...
echo      Creating required directories...
if not exist "dist\Claire\logs\" mkdir dist\Claire\logs
if not exist "dist\Claire\data\" mkdir dist\Claire\data

echo      Copying configuration files...
if exist "config.example.yaml" (
    copy config.example.yaml dist\Claire\config.yaml >nul 2>&1
)

REM Copy documentation files
if exist "README.md" (
    copy README.md dist\Claire\ >nul 2>&1
)
if exist "QUICKSTART.md" (
    copy QUICKSTART.md dist\Claire\ >nul 2>&1
)

REM Create build info file
echo Build Information > dist\Claire\BUILD_INFO.txt
echo ================== >> dist\Claire\BUILD_INFO.txt
echo. >> dist\Claire\BUILD_INFO.txt
echo Build Date: %BUILD_DATE% >> dist\Claire\BUILD_INFO.txt
echo Build Time: %BUILD_TIME% >> dist\Claire\BUILD_INFO.txt
echo Python Version: %PYTHON_VERSION% >> dist\Claire\BUILD_INFO.txt
echo Build System: Claire New Build v2.0 >> dist\Claire\BUILD_INFO.txt
echo. >> dist\Claire\BUILD_INFO.txt
echo To run Claire: >> dist\Claire\BUILD_INFO.txt
echo   Double-click Claire.exe >> dist\Claire\BUILD_INFO.txt
echo. >> dist\Claire\BUILD_INFO.txt

echo      Done!
echo.

REM Calculate distribution size
for /f "tokens=3" %%a in ('dir /s "dist\Claire" ^| find "File(s)"') do set SIZE=%%a
echo Distribution size: %SIZE% bytes
echo.

echo ========================================
echo   SUCCESS! Build Complete!
echo ========================================
echo.
echo Build Information:
echo   - Build Date: %BUILD_DATE%
echo   - Build Time: %BUILD_TIME%
echo   - Output: dist\Claire\Claire.exe
echo   - Size: ~100 MB (includes Python + all dependencies)
echo.
echo WHAT'S NEXT:
echo   1. Navigate to: dist\Claire\
echo   2. Double-click: Claire.exe
echo   3. Configure your AI settings (if needed)
echo.
echo TO SHARE WITH OTHERS:
echo   - Copy entire "dist\Claire" folder
echo   - Recipients just run Claire.exe
echo   - No Python installation needed!
echo   - Ollama required for AI features
echo.
echo NOTES:
echo   - Build info saved to: dist\Claire\BUILD_INFO.txt
echo   - Logs will be stored in: dist\Claire\logs\
echo.

REM Offer to create desktop shortcut
echo.
set /p CREATE_SHORTCUT="Create desktop shortcut? (Y/N): "
if /i "%CREATE_SHORTCUT%"=="Y" (
    echo Creating desktop shortcut...
    powershell -Command "$ws = New-Object -ComObject WScript.Shell; $shortcut = $ws.CreateShortcut($env:USERPROFILE + '\Desktop\Claire AI.lnk'); $shortcut.TargetPath = '%~dp0dist\Claire\Claire.exe'; $shortcut.WorkingDirectory = '%~dp0dist\Claire'; $shortcut.Description = 'Claire - Your AI Assistant'; $shortcut.Save()"
    echo Desktop shortcut created: "Claire AI"
    echo.
)

REM Offer to open the distribution folder
echo.
set /p OPEN_FOLDER="Open distribution folder now? (Y/N): "
if /i "%OPEN_FOLDER%"=="Y" (
    explorer "%~dp0dist\Claire"
)

echo.
echo Build process complete!
echo Press any key to exit...
pause >nul
