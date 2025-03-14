import tkinter as tk
import time

# Path to the Govee sensor data file
DATA_FILE = "/home/zorger/govee_data.txt"

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
    current_time = time.strftime("%I:%M %p")  # Format time as HH:MM AM/PM
    indoor, outdoor = read_sensor_data()

    clock_label.config(text=current_time)
    indoor_label.config(text=f"In: {indoor}")
    outdoor_label.config(text=f"Out: {outdoor}")

    root.after(1000, update_display)  # Refresh every second

# Initialize tkinter
root = tk.Tk()
root.title("Weather Display")
root.configure(bg="black")
root.attributes('-fullscreen', True)  # Fullscreen mode
root.bind('<Escape>', lambda e: root.destroy())  # Exit on Esc key

# Configure labels
font_large = ("Helvetica", 80, "bold")
font_medium = ("Helvetica", 50, "bold")

clock_label = tk.Label(root, text="", font=font_large, fg="white", bg="black")
clock_label.pack(pady=20)

indoor_label = tk.Label(root, text="In: N/A", font=font_medium, fg="white", bg="black")
indoor_label.pack(pady=10)

outdoor_label = tk.Label(root, text="Out: N/A", font=font_medium, fg="white", bg="black")
outdoor_label.pack(pady=10)

# Start updating display
update_display()

# Run the tkinter main loop
root.mainloop()

