from bluepy import btle
import binascii
import time

# MAC addresses of the sensors
SENSORS = {
    'In': 'a4:c1:38:95:a6:ee',
    'Out': 'a4:c1:38:6b:3d:27'
}

LOG_FILE = "/home/zorger/govee_data.txt"  # Change path if needed

sensor_data = {key: "Waiting..." for key in SENSORS.keys()}

class GoveeDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr in SENSORS.values():
            for (adtype, desc, data) in dev.getScanData():
                if adtype == 255:  # Manufacturer Specific Data
                    hex_data = binascii.unhexlify(data)

                    if len(hex_data) >= 7:  # Ensure valid data length
                        temp_raw = int.from_bytes(hex_data[3:5], byteorder='little', signed=True)
                        humidity_raw = hex_data[5]

                        temp_c = temp_raw / 100.0
                        temp_f = (temp_c * 9/5) + 32
                        humidity = humidity_raw / 4  # Corrected scaling

                        if -40 <= temp_c <= 60:  # Realistic temp range (-40C to 60C)
                            location = list(SENSORS.keys())[list(SENSORS.values()).index(dev.addr)]
                            sensor_data[location] = f"{temp_f:.1f}°F, {humidity}%"
                            write_to_file()

def write_to_file():
    """Writes the latest sensor data to a file."""
    with open(LOG_FILE, "w") as f:
        for location, data in sensor_data.items():
            f.write(f"{location}: {data}\n")

def scan_govee():
    """Scans for Govee sensor data every 5 seconds."""
    scanner = btle.Scanner().withDelegate(GoveeDelegate())
    while True:
        scanner.scan(5.0)  # Scan for 5 seconds
        time.sleep(30)  # Wait before next scan

if __name__ == "__main__":
    scan_govee()

