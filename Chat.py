import time
import os
from datetime import timedelta
import psutil
import win32gui
import win32process  # To get the process associated with the window
from PIL import ImageGrab, ImageChops
from pynput import mouse, keyboard
import threading
import random
import subprocess
import numpy as np

# Function to run the second script in a separate thread
def run_secondary_script():
    try:
        # Run the secondary script
        subprocess.run(["python", "secondary_script.py"])
    except Exception as e:
        print(f"Failed to run the secondary script: {e}")

# Call the function to run the secondary script in a separate thread
secondary_thread = threading.Thread(target=run_secondary_script)
secondary_thread.start()

# Create directories and files
output_dir = "screenshots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

activity_log = "activity_log.txt"
if not os.path.exists(activity_log):
    with open(activity_log, "w") as f:
        f.write("Time\tEvent\tDetails\n")

usage_file = "Useage.txt"
if not os.path.exists(usage_file):
    with open(usage_file, "w") as f:
        f.write("Timestamp\tActivity Percentage\tScreen Change Score\n")

app_usage_file = "appdetails.txt"

# List of apps to track
APPS_TO_TRACK = ["chrome.exe", "msedge.exe", "AnyDesk.exe", "Code.exe", "notepad.exe"]

# Dictionary to store start times of apps and track their duration since the script started
app_runtime = {}

# Dictionary to accumulate runtime for each app
accumulated_runtime = {app: 0 for app in APPS_TO_TRACK}

# Globals for activity tracking
mouse_active = False
keyboard_active = False
active_seconds = 0
total_seconds = 60  # We track over 60 seconds
last_screenshot = None
screenshot_change_score = 0
last_activity_time = time.time()
screen_width, screen_height = ImageGrab.grab().size
last_mouse_position = None
active_this_second = False

# Function to reset activity flags
def reset_activity():
    global mouse_active, keyboard_active, active_this_second
    mouse_active = False
    keyboard_active = False
    active_this_second = False  # Reset per-second activity tracker

# Function to get the process name of the foreground window
def get_foreground_process():
    try:
        hwnd = win32gui.GetForegroundWindow()  # Get the handle of the foreground window
        _, pid = win32process.GetWindowThreadProcessId(hwnd)  # Get the PID of the process
        process = psutil.Process(pid)  # Get the process using the PID
        return process.name().lower()  # Return the name of the process
    except Exception as e:
        print(f"Error getting foreground process: {e}")
    return None

# Function to track active applications in the foreground and log their runtime
def get_running_apps():
    global app_runtime, accumulated_runtime
    app_log = "Application Usage (hh:mm:ss):\n"

    foreground_process = get_foreground_process()  # Get the foreground process name

    if foreground_process:
        for app in APPS_TO_TRACK:
            if app in foreground_process:  # Match with the foreground app
                if app not in app_runtime:
                    app_runtime[app] = time.time()  # Store the start time

                # Calculate runtime since the last check
                current_time = time.time()
                runtime_seconds = current_time - app_runtime[app]
                accumulated_runtime[app] += runtime_seconds

                # Update the start time for the next check
                app_runtime[app] = current_time

                runtime = str(timedelta(seconds=accumulated_runtime[app]))  # Convert to hh:mm:ss
                app_log += f"{app}: {runtime}\n"

    return app_log

# Function to log running apps to a separate file
def log_app_usage():
    while True:
        app_usage_log = get_running_apps()
        with open(app_usage_file, "a") as f:
            f.write(app_usage_log + "\n")

        print(app_usage_log)
        time.sleep(120)  # Log every 2 minutes to reduce CPU load

# Function to capture random screenshots (2-6 per minute) and check for changes
def capture_screenshots():
    global last_screenshot, screenshot_change_score

    while True:
        num_screenshots = random.randint(2, 6)
        interval = total_seconds // num_screenshots

        for _ in range(num_screenshots):
            timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = f"{output_dir}/screenshot_{timestamp}.png"
            screenshot = ImageGrab.grab(all_screens=True)
            screenshot.save(screenshot_path)

            if last_screenshot:
                diff = ImageChops.difference(screenshot, last_screenshot)
                diff_array = np.array(diff)
                non_zero_diff = np.sum(diff_array > 0)

                change_threshold = 0.01 * diff_array.size
                if non_zero_diff > change_threshold:
                    screenshot_change_score += 1

            last_screenshot = screenshot
            print(f"Screenshot saved at {screenshot_path}")
            time.sleep(interval)

# Function to log mouse and keyboard events
def log_event(event, details):
    global active_seconds, last_activity_time, active_this_second

    current_time = time.time()

    if not active_this_second and current_time - last_activity_time >= 1:
        last_activity_time = current_time
        active_this_second = True
        active_seconds += 1

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(activity_log, "a") as f:
        f.write(f"{timestamp}\t{event}\t{details}\n")

    print(f"{event}: {details}")

# Mouse event handlers with a movement threshold of 20% of the screen
def on_move(x, y):
    global last_mouse_position

    if last_mouse_position is None:
        last_mouse_position = (x, y)
        return

    dx = abs(x - last_mouse_position[0]) / screen_width * 100
    dy = abs(y - last_mouse_position[1]) / screen_height * 100

    if dx >= 20 or dy >= 20:
        log_event("Mouse Move", f"Significant Movement to ({x}, {y})")
        last_mouse_position = (x, y)

def on_click(x, y, button, pressed):
    if pressed:
        log_event("Mouse Click", f"Button {button} at ({x}, {y})")
    else:
        log_event("Mouse Release", f"Button {button} at ({x}, {y})")

def on_scroll(x, y, dx, dy):
    log_event("Mouse Scroll", f"Scrolled ({dx}, {dy}) at ({x}, {y})")

# Keyboard event handlers
def on_press(key):
    log_event("Key Press", "A key was pressed")

def on_release(key):
    log_event("Key Release", "A key was released")
    if key == keyboard.Key.esc:
        return False

# Set up mouse and keyboard listeners
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

# Function to calculate and log activity percentage
def log_activity():
    global active_seconds, total_seconds, screenshot_change_score

    while True:
        time.sleep(total_seconds * 2)  # Now checking every 2 minutes

        activity_percentage = (active_seconds / total_seconds) * 100
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        with open(usage_file, "a") as f:
            f.write(f"{timestamp}\t{activity_percentage:.2f}%\t{screenshot_change_score:.2f}\n")

        print(f"Logged activity: {activity_percentage:.2f}%, Screen Change Score: {screenshot_change_score:.2f}")

        active_seconds = 0
        screenshot_change_score = 0
        reset_activity()

# Start the activity logging thread
activity_thread = threading.Thread(target=log_activity)
activity_thread.daemon = True
activity_thread.start()

# Start the random screenshot capturing and comparison thread
screenshot_thread = threading.Thread(target=capture_screenshots)
screenshot_thread.daemon = True
screenshot_thread.start()

# Start the app usage logging thread
app_usage_thread = threading.Thread(target=log_app_usage)
app_usage_thread.daemon = True
app_usage_thread.start()

try:
    while True:
        time.sleep(1)
        reset_activity()
except KeyboardInterrupt:
    print("Monitoring stopped.")

# Stop listeners when the script ends
mouse_listener.stop()
keyboard_listener.stop()
