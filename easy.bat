@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    
    :: Download Python installer (this is for Windows)
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe -OutFile python-installer.exe"
    
    :: Install Python silently
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    :: Clean up installer
    del python-installer.exe
    
    echo Python installed successfully.
) else (
    echo Python is already installed.
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Run Chat.py
echo Running Chat.py...
python Chat.py

:: Run secondary_script.py
echo Running secondary_script.py...
python secondary_script.py

:: Deactivate virtual environment after scripts finish
deactivate
pause
