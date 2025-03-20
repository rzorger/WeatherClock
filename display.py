import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import time
import urllib.request
import os

# Path to the Govee sensor data file
DATA_FILE = "/home/zorger/govee_data.txt"
RADAR_URL = "https://radar.weather.gov/ridge/standard/KDOX_loop.gif"
RADAR_FILE = "/tmp/radar.gif"

# Cropping configuration: (left, upper, right, lower)
CROP_BOX = (0, 0, 600, 480)  # Crop to 600px width, full height

def read_sensor_data():
    """Reads the latest sensor data from the file."""
    try:
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
            data = {}
            for line in lines:
                parts = line.strip().split(": ")
                if len(parts) == 2:
                    key, value = parts
                    data[key] = value
            return data.get("In", "N/A"), data.get("Out", "N/A")
    except FileNotFoundError:
        return "N/A", "N/A"

def update_display():
    """Updates the clock, sensor data, and radar animation on the display."""
    current_time = time.strftime("%I:%M %p")  # Format time as HH:MM AM/PM
    indoor, outdoor = read_sensor_data()

    clock_label.config(text=current_time)
    indoor_label.config(text=f"In: {indoor}")
    outdoor_label.config(text=f"Out: {outdoor}")

    # Refresh the radar every 5 minutes
    if int(time.time()) % 300 == 0:
        update_radar()

    root.after(1000, update_display)  # Refresh every second

def update_radar():
    """Downloads and updates the radar animation with cropping."""
    try:
        urllib.request.urlretrieve(RADAR_URL, RADAR_FILE)
        
        # Open the downloaded radar GIF
        radar_image = Image.open(RADAR_FILE)

        # Crop the image (CROP_BOX is (left, upper, right, lower))
        radar_image_cropped = radar_image.crop(CROP_BOX)

        # Convert the cropped image to PhotoImage for tkinter
        radar_photo = ImageTk.PhotoImage(radar_image_cropped)

        radar_label.config(image=radar_photo)
        radar_label.image = radar_photo  # Prevent garbage collection
        print("Radar updated successfully.")
    except Exception as e:
        print(f"Failed to update radar: {e}")

# Initialize tkinter
root = tk.Tk()
root.title("Weather Display")
root.configure(bg="black")
root.attributes('-fullscreen', True)  # Fullscreen mode
root.bind('<Escape>', lambda e: root.destroy())  # Exit on Esc key

# Configure labels
font_large = ("Helvetica", 50, "bold")
font_medium = ("Helvetica", 20, "bold")
font_small = ("Helvetica", 5, "bold")

clock_label = tk.Label(root, text="", font=font_large, fg="white", bg="black")
clock_label.pack(pady=2)

indoor_label = tk.Label(root, text="In: N/A", font=font_small, fg="white", bg="black")
indoor_label.pack(pady=2)

outdoor_label = tk.Label(root, text="Out: N/A", font=font_medium, fg="white", bg="black")
outdoor_label.pack(pady=2)

# Add radar placeholder
radar_label = tk.Label(root, bg="black")
radar_label.pack(pady=10)

# Update radar on startup
update_radar()

# Start updating display
update_display()

# Run the tkinter main loop
root.mainloop()

