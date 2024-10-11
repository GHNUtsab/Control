@echo off

:: Activate the virtual environment
call venv\Scripts\activate

:: Run the scripts
echo Starting Chat.py...
start python Chat.py

echo Starting secondary_script.py...
start python secondary_script.py

:: Keep the window open
pause
