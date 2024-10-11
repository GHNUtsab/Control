import subprocess
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Function to start the scripts by running startup.bat
def start_scripts():
    try:
        # Run startup.bat file
        subprocess.Popen(['startup.bat'], shell=True)
        start_time = time.time()  # Record start time
        update_timer(start_time)  # Start the timer
        messagebox.showinfo("Info", "Scripts started successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start scripts: {e}")

# Function to stop the scripts by running stop.bat
def stop_scripts():
    try:
        # Run stop.bat file
        subprocess.Popen(['stop.bat'], shell=True)
        reset_timer()  # Reset the timer when stopped
        messagebox.showinfo("Info", "Scripts stopped successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to stop scripts: {e}")

# Function to update the timer
def update_timer(start_time):
    def _update_timer():
        while timer_running:
            elapsed_time = time.time() - start_time
            formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
            timer_label.config(text=formatted_time)
            time.sleep(1)
    
    global timer_running
    timer_running = True
    threading.Thread(target=_update_timer, daemon=True).start()

# Function to reset the timer
def reset_timer():
    global timer_running
    timer_running = False
    timer_label.config(text="00:00:00")  # Reset timer to zero

# Create the main window
root = tk.Tk()
root.title("Script Manager")
root.geometry("300x150")

# Create and place Start button
start_button = tk.Button(root, text="Start", command=start_scripts, width=10, height=2)
start_button.pack(pady=10)

# Create and place Stop button
stop_button = tk.Button(root, text="Stop", command=stop_scripts, width=10, height=2)
stop_button.pack(pady=10)

# Create and place Timer label
timer_label = tk.Label(root, text="00:00:00", font=("Helvetica", 24))
timer_label.pack(pady=10)

# Flag to control the timer
timer_running = False

# Run the GUI loop
root.mainloop()
