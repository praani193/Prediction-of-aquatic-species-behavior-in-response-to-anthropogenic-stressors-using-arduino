import serial
import time

# Configure the serial port
ser = serial.Serial('COM5', 9600)  # Change 'COM3' to the correct port name

# Create and open the data files
temp_file = open('temp.data', 'w')
freq_file = open('freq.data', 'w')

try:
    while True:
        # Read data from Arduino
        data = ser.readline().decode().strip()
        if data:
            if data.startswith("Temperature (C):"):
                temperature = data.split(":")[1].strip()
                temp_file.write(temperature + '\n')
                print(temperature)
            elif data.startswith("Sound Value:"):
                sound_value = data.split(":")[1].strip()
                freq_file.write(sound_value + '\n')
except KeyboardInterrupt:
    print("Data collection stopped.")

# Close the data files and serial connection
temp_file.close()
freq_file.close()
ser.close()
