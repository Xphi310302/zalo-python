@echo off
title Python Installer Script
echo ========================================
echo Python Installation Script
echo ========================================
echo.

REM Check if Python is already installed
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python is already installed:
    python --version
    echo.
    pause
    exit /b 0
)

echo Python not found. Starting installation...
echo.

REM Create temp directory for download
if not exist "%TEMP%\python_installer" mkdir "%TEMP%\python_installer"
cd /d "%TEMP%\python_installer"

echo Downloading Python installer...
REM Download Python 3.12.x (latest stable)
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile 'python-installer.exe'"

if not exist "python-installer.exe" (
    echo ERROR: Failed to download Python installer
    pause
    exit /b 1
)

echo.
echo Installing Python...
echo This will install Python with the following options:
echo - Add Python to PATH
echo - Install pip
echo - Install for all users
echo.

REM Install Python silently with common options
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM Wait a moment for installation to complete
timeout /t 5 /nobreak >nul

REM Verify installation
echo.
echo Verifying installation...
python --version
if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo Python installed successfully!
    echo ========================================
    echo.
    echo Checking pip installation...
    pip --version
    echo.
    echo You can now use Python from any command prompt.
    echo Try: python --version
    echo Or:   pip list
) else (
    echo.
    echo ERROR: Python installation may have failed
    echo Please check the installation manually
)

REM Cleanup
cd /d "%TEMP%"
rmdir /s /q "%TEMP%\python_installer" 2>nul

echo.
echo Press any key to exit...
pause >nul