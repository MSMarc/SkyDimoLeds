import serial
import time
from dotenv import load_dotenv

load_dotenv()

NUM_LEDS = 65
PORT = 'COM8'
BAUD_RATE = 115200

ser = serial.Serial(PORT, BAUD_RATE)

prefix = b'Ada' + bytes([
    (NUM_LEDS >> 8) & 0xFF,
    NUM_LEDS & 0xFF,
    ((NUM_LEDS >> 8) & 0xFF) ^ (NUM_LEDS & 0xFF)
])

led_data = [255, 255, 255] * NUM_LEDS
frame = prefix + bytes(led_data)

try:
    while True:
        ser.write(frame)
        time.sleep(1)
except KeyboardInterrupt:
    off_data = [0, 0, 0] * NUM_LEDS
    ser.write(prefix + bytes(off_data))
    ser.close()