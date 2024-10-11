import time
import re
import pygetwindow as gw
import atexit
import signal
import sys

# Dictionary to store the time spent on each website
website_time = {}

# Create a file to store website visit data
website_data_file = "website_data.txt"

# Function to get the active browser window (Chrome or Edge)
def get_active_browser_window():
    try:
        # Print all window titles for debugging
        windows = gw.getAllTitles()
        print("All window titles:", windows)
        
        # Check for Chrome or Edge windows in the foreground
        windows = gw.getWindowsWithTitle("Google Chrome") + gw.getWindowsWithTitle("Microsoft Edge")
        if windows:
            print("Active browser window title:", windows[0].title)  # Print the active browser window title
            return windows[0]  # Return the first match (active window)
        print("No active browser window detected")
        return None
    except Exception as e:
        print(f"Error getting active window: {e}")
        return None

# Function to extract the website (URL or title) from the browser window title
def get_website_from_title(title):
    try:
        # Modify the regular expression to capture titles that end with " - Google Chrome" or " - Microsoft Edge"
        match = re.search(r'(.+?) - Google Chrome|(.+?) - Microsoft Edge', title)
        if match:
            return match.group(1)  # Extract the website name from the window title
        return None
    except Exception as e:
        print(f"Error extracting website from title: {e}")
        return None

# Function to log the website visit to the file in real-time
def log_website_visit(site, time_spent):
    try:
        with open(website_data_file, "a") as f:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - Visited: {site} - Time Spent: {time_spent:.2f} seconds\n")
        print(f"Logged: {site} with time spent {time_spent:.2f} seconds to file.")
    except Exception as e:
        print(f"Error logging website visit: {e}")

# Function to track website usage time
def track_website_usage():
    current_site = None
    site_start_time = time.time()

    while True:
        # Get the active browser window
        active_window = get_active_browser_window()

        if active_window and active_window.title:
            # Get the website (from the title)
            website = get_website_from_title(active_window.title)
            if website:
                # If a new site is detected
                if website != current_site:
                    # If there's an ongoing site being tracked, calculate time spent
                    if current_site:
                        time_spent = time.time() - site_start_time
                        website_time[current_site] = website_time.get(current_site, 0) + time_spent
                        log_website_visit(current_site, time_spent)

                    # Update the current site and reset the start time
                    current_site = website
                    site_start_time = time.time()

        # Sleep for a bit before checking again
        time.sleep(2)

# Function to log the website usage when the script is interrupted
def log_final_website_usage():
    try:
        with open(website_data_file, "a") as f:
            for site, time_spent in website_time.items():
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} - Final Log: {site} - Time Spent: {time_spent:.2f} seconds\n")
        print("Final website usage logged.")
    except Exception as e:
        print(f"Error logging final website usage: {e}")

# Handle exit by writing final logs
def exit_handler():
    log_final_website_usage()

# Handle termination signals
def signal_handler(sig, frame):
    print(f"Received signal {sig}. Logging final website usage before exit.")
    log_final_website_usage()
    sys.exit(0)

if __name__ == "__main__":
    # Register exit handlers
    atexit.register(exit_handler)
    
    # Register signal handlers for termination signals
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Handle termination signals (e.g., kill command)

    try:
        track_website_usage()
    except KeyboardInterrupt:
        print("Tracking stopped. Logging final website usage.")
        log_final_website_usage()
