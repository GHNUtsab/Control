@echo off

:: Find the PID of the Python process running Chat.py
for /f "tokens=2 delims=," %%A in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH') do (
    echo Stopping Python script with PID %%A
    :: Send Ctrl+C to the Python process
    wmic process where ProcessID=%%A call terminate
)

echo All Python scripts sent termination signal.
pause
