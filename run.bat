@echo off
echo Starting Zalo GUI Setup and Run Script...
echo.

REM Check if venv directory exists
if not exist "venv" (
    echo Virtual environment not found. Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment. Make sure Python is installed.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo Virtual environment found.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Virtual environment activated.
echo.

echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements. Make sure requirements.txt exists.
    pause
    exit /b 1
)

echo Requirements installed successfully.
echo.

echo Starting Streamlit application...
streamlit run zalo-gui.py
if errorlevel 1 (
    echo Error: Failed to run Streamlit application. Make sure zalo-gui.py exists.
    pause
    exit /b 1
)

echo.
echo Script completed.
pause