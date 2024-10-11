Explanation:

Chat.py: Your main script that captures screenshots, tracks mouse and keyboard events, and logs activities.

secondary_script.py: Another Python script that runs as a subprocess from Chat.py.

requirements.txt: List of Python dependencies (e.g., psutil, pynput, etc.).

easy.bat: A setup script to install Python (if necessary), set up a virtual environment, install dependencies, and run the Python scripts.

startup.bat: A script to start both Python scripts (Chat.py and secondary_script.py) after setting up the environment.

stop.bat: A script to stop all running Python processes that are started by startup.bat.

venv/: The virtual environment created by easy.bat. This contains Python and your dependencies.

screenshots/: A folder where the screenshots captured by the script will be stored.

activity_log.txt: A file where activity events (mouse, keyboard) will be logged.

Useage.txt: A file where activity percentage and screen change score are logged.

appdetails.txt: A file where active app usage is logged.


Steps to Run:

Run easy.bat:
It will check if Python is installed, set up a virtual environment, install dependencies, and run the scripts.

Use startup.bat:
If Python is already installed and the environment is set up, use startup.bat to directly start the scripts.

Stop the Scripts:
Use stop.bat to terminate all Python processes started by the startup.bat script.

This structure should make it easy to manage and run your project on any machine. Let me know if you'd like to make any modifications!

Project_Folder/
│
├── Chat.py                     # Your main Python script
├── secondary_script.py          # Secondary Python script
├── requirements.txt             # List of dependencies
├── easy.bat                     # Batch script to install dependencies and run the project
├── startup.bat                  # Batch script to start the Python scripts
├── stop.bat                     # Batch script to stop the running Python scripts
├── venv/                        # Virtual environment folder (created by easy.bat)
│   ├── Scripts/
│   ├── Include/
│   ├── Lib/
│   └── ...
├── screenshots/                 # Folder where screenshots will be saved
├── activity_log.txt             # File where activity logs will be written
├── Useage.txt                   # File where usage data will be logged
└── appdetails.txt               # File to log app usage details
