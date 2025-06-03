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
    """Reads the latest sensor data from the file and splits values."""
    try:
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
            data = {"in_temp": "N/A", "in_humidity": "N/A",
                    "out_temp": "N/A", "out_humidity": "N/A"}

            for line in lines:
                if line.startswith("In:"):
                    parts = line.strip().split(": ")[1].split(", ")
                    if len(parts) == 2:
                        data["in_temp"], data["in_humidity"] = parts
                elif line.startswith("Out:"):
                    parts = line.strip().split(": ")[1].split(", ")
                    if len(parts) == 2:
                        data["out_temp"], data["out_humidity"] = parts

            return data["in_temp"], data["in_humidity"], data["out_temp"], data["out_humidity"]

    except FileNotFoundError:
        return "N/A", "N/A", "N/A", "N/A"

def update_display():
    """Updates the clock and sensor data on the display."""
    current_time = time.strftime("%I:%M").lstrip("0")  # 12-hour format, no AM/PM, no leading 0
    in_temp, in_humidity, out_temp, out_humidity = read_sensor_data()

    out_temp = out_temp[:-1]
    in_temp = in_temp[:-1]

    clock_label.config(text=current_time)
    in_temp_label.config(text=f"{in_temp}")
#    in_humidity_label.config(text=f"{in_humidity}")
    out_temp_label.config(text=f"{out_temp}")
#    out_humidity_label.config(text=f"{out_humidity}")

    root.after(1000, update_display)

def update_radar():
    """Downloads and displays the latest radar image."""
    try:
        urllib.request.urlretrieve(RADAR_URL, RADAR_FILE)
        radar_image = Image.open(RADAR_FILE)
        cropped_frame = radar_image.crop(CROP_BOX)
        radar_photo = ImageTk.PhotoImage(cropped_frame)
        radar_label.config(image=radar_photo)
        radar_label.image = radar_photo  # Prevent garbage collection
        print("Radar updated successfully.")
    except Exception as e:
        print(f"Failed to update radar: {e}")

    root.after(300000, update_radar)  # Every 5 minutes

# Initialize tkinter
root = tk.Tk()
root.title("Weather Display")
root.configure(bg="black")
root.configure(cursor="none")
root.attributes('-fullscreen', True)
root.bind('<Escape>', lambda e: root.destroy())

# Layout setup
top_frame = tk.Frame(root, bg="black")
top_frame.pack(fill="both", expand=False)

bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(fill="both", expand=True)

left_frame = tk.Frame(bottom_frame, bg="black")
left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)

right_frame = tk.Frame(bottom_frame, bg="black")
right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)

# Clock
font_large = ("Helvetica", 105, "bold")
clock_label = tk.Label(top_frame, text="", font=font_large, fg="white", bg="black")
clock_label.pack(pady=2)

# Indoor/Outdoor Labels
out_temp_label = tk.Label(left_frame, text="Out Temp: N/A", font=font_large, fg="orange", bg="black")
out_temp_label.pack(pady=5, anchor="w")

#font_medium = ("Helvetica", 30, "bold")
#out_humidity_label = tk.Label(left_frame, text="Out Humidity: N/A", font=font_medium, fg="orange", bg="black")
#out_humidity_label.pack(pady=5, anchor="w")

font_medium = ("Helvetica", 40, "bold")
in_temp_label = tk.Label(left_frame, text="N/A", font=font_medium, fg="orange", bg="black")
in_temp_label.pack(pady=5, anchor="w")

#font_medium = ("Helvetica", 30, "bold")
#in_humidity_label = tk.Label(left_frame, text="In Humidity: N/A", font=font_medium, fg="orange", bg="black")
#in_humidity_label.pack(pady=5, anchor="w")

# Radar
radar_label = tk.Label(right_frame, bg="black")
radar_label.pack(pady=10)

# Start everything
update_radar()
update_display()
root.mainloop()

