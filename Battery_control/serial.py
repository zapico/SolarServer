import serial
from datetime import datetime
import time
import json
import os

# Connect to serial
sio = serial.Serial(port='/dev/ttyUSB0',baudrate=19200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=12)
print("connected to: " + sio.portstr)
# Init variables
count=1
kw = 0
battery = 0

# Loop
while True:
    # Check that serial has read both values
    if (kw!=0 and battery!=0) or (battery==100):
        dictionary = {
           "kw": kw,
           "battery": battery,
           "time": str(datetime.now())
        }
        # Save as status json and to history
        with open("/var/www/thehackfarm/html/battery.json", "w") as outfile:
            json.dump(dictionary, outfile)
        # Append to history.json. This dictionary can then be read with:
        # with open('my_file') as f:
        #   my_list = [json.loads(line) for line in f]
        with open('/var/www/thehackfarm/html/history.json', 'a') as f:
            json.dump(dictionary, f)
            f.write(os.linesep)
        # Reset numbers and sleep for 10 minutes
        kw = 0
        battery = 0
        time.sleep(600)

    line = sio.readline().decode('iso-8859-1')
    # read kwh in
    if (-1 != line.find("P	")):
        kw = float(line[2:])
        print(kw)
    # read battery
    if (-1 != line.find("SOC")):
       battery = float(line[4:])/10
       print(battery)
