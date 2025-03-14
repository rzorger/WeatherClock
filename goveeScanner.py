from bluepy import btle
import binascii
import time

# Replace these with the MAC addresses of your sensors
SENSORS = {
    "Inside": "A4:C1:38:95:A6:EE".lower(),
    "Outside": "A4:C1:38:6B:3D:27".lower()
}

class GoveeDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        #print(dev.addr)
        if dev.addr in SENSORS.values():
            #print("Device discovered...")
            #print(dev.getScanData())
            for (adtype, desc, data) in dev.getScanData():

                if adtype == 255:  # Manufacturer Specific Data
                    hex_data = binascii.unhexlify(data)
                    
                    if len(hex_data) >= 7:  # Ensure correct data length
                        temp_raw = int.from_bytes(hex_data[3:5], byteorder='little', signed=True)  # Adjusted byte range
                        humidity_raw = hex_data[5]  # Adjusted byte index

                        temp_c = temp_raw / 100.0  # Convert to °C
                        temp_f = (temp_c * 9/5) + 32
                        humidity = humidity_raw  # Already percentage

                        if -40 <= temp_c <= 60:  # Sanity check (valid range for indoor/outdoor temps)
                            location = list(SENSORS.keys())[list(SENSORS.values()).index(dev.addr)]
                            print(f"{location}: {temp_c:.2f}°C, {humidity}%")
                            print(f"{location}: {temp_f:.2f}°F, {humidity}%")
                            print(f"{location}: {temp_c:.2f}°C / {temp_f:.2f}°F, {humidity}%")
                        else:
                            print(f"Invalid temperature reading from {dev.addr}: {temp_c}°C")


def scan_govee():
    print("Startng a new bluepy btle scan...")
    scanner = btle.Scanner().withDelegate(GoveeDelegate())
    scanner.scan(10.0)  # Scan for 10 seconds

if __name__ == "__main__":
    while True:
        #print(SENSORS.values())
        scan_govee()
        time.sleep(10)  # Scan every minute

