import tkinter as tk
from PIL import Image, ImageTk
import time
import urllib.request

# Path to the Govee sensor data file
DATA_FILE = "/home/zorger/govee_data.txt"
RADAR_URL = "https://radar.weather.gov/ridge/standard/KDOX_0.gif"
RADAR_FILE = "/tmp/radar.gif"

# Cropping configuration: (left, upper, right, lower)
CROP_BOX = (50, 0, 400, 440)  # Crop for better focus

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
    """Updates the clock and sensor data on the display."""
    current_time = time.strftime("%H:%M")  # 24-hour format
    indoor, outdoor = read_sensor_data()

    clock_label.config(text=current_time)
    indoor_label.config(text=f"In: {indoor}")
    outdoor_label.config(text=f"Out: {outdoor}")

    # Refresh display every second
    root.after(1000, update_display)

def update_radar():
    """Downloads and displays the latest radar image."""
    try:
        urllib.request.urlretrieve(RADAR_URL, RADAR_FILE)
        radar_image = Image.open(RADAR_FILE)
        
        # Crop the image if necessary
        cropped_frame = radar_image.crop(CROP_BOX)
        radar_photo = ImageTk.PhotoImage(cropped_frame)

        radar_label.config(image=radar_photo)
        radar_label.image = radar_photo  # Prevent garbage collection
        print("Radar updated successfully.")
    except Exception as e:
        print(f"Failed to update radar: {e}")
    
    # Schedule the next radar update in 5 minutes (300,000 ms)
    root.after(300000, update_radar)

# Initialize tkinter
root = tk.Tk()
root.title("Weather Display")
root.configure(bg="black")
root.attributes('-fullscreen', True)  # Fullscreen mode
root.bind('<Escape>', lambda e: root.destroy())  # Exit on Esc key

# Main container frames
top_frame = tk.Frame(root, bg="black")
top_frame.pack(fill="both", expand=False)

bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(fill="both", expand=True)

left_frame = tk.Frame(bottom_frame, bg="black")
left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

right_frame = tk.Frame(bottom_frame, bg="black")
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Clock label in the top frame
font_large = ("Helvetica", 80, "bold")
clock_label = tk.Label(top_frame, text="", font=font_large, fg="white", bg="black")
clock_label.pack(pady=10)

# Indoor/Outdoor labels in the left frame
font_medium = ("Helvetica", 40, "bold")
indoor_label = tk.Label(left_frame, text="In: N/A", font=font_medium, fg="white", bg="black")
indoor_label.pack(pady=10, anchor="w")

outdoor_label = tk.Label(left_frame, text="Out: N/A", font=font_medium, fg="white", bg="black")
outdoor_label.pack(pady=10, anchor="w")

# Radar placeholder in the right frame
radar_label = tk.Label(right_frame, bg="black")
radar_label.pack(pady=10)

# Update radar and start looping
update_radar()

# Start updating display
update_display()

# Run the tkinter main loop
root.mainloop()

