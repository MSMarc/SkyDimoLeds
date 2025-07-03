import serial
import time
import numpy as np
import mss
import os
from dotenv import load_dotenv

load_dotenv()

NUM_LEDS = 65
PORT = 'COM3'
BAUD_RATE = 115200
SMOOTHING_ALPHA = 0.25

prefix = b'Ada' + bytes([
    (NUM_LEDS >> 8) & 0xFF,
    NUM_LEDS & 0xFF,
    ((NUM_LEDS >> 8) & 0xFF) ^ (NUM_LEDS & 0xFF)
])

ser = serial.Serial(PORT, BAUD_RATE)
prev_colors = np.zeros((NUM_LEDS, 3), dtype=np.float32)

def average_color(region):
    """Get average color of a screen region."""
    img = np.array(region)
    if img.ndim == 3:
        rgb = img[:, :, :3]
        return rgb.mean(axis=(0, 1))
    return [0, 0, 0]

def get_led_colors(sct, screen):
    h = screen['height']
    w = screen['width']
    top = screen['top']
    left = screen['left']

    colors = []

    for i in reversed(range(17)):
        region = {
            'top': top + int(i * h / 17),
            'left': left,
            'width': 10,
            'height': int(h / 17)
        }
        colors.append(average_color(sct.grab(region)))

    for i in range(31):
        region = {
            'top': top,
            'left': left + int(i * w / 31),
            'width': int(w / 31),
            'height': 10
        }
        colors.append(average_color(sct.grab(region)))

    for i in range(17):
        region = {
            'top': top + int(i * h / 17),
            'left': left + w - 10,
            'width': 10,
            'height': int(h / 17)
        }
        colors.append(average_color(sct.grab(region)))

    return np.array(colors)




try:
    with mss.mss() as sct:
        monitor = sct.monitors[2]
        prev_time = time.perf_counter()
        while True:
            new_colors = get_led_colors(sct, monitor)
            prev_colors = prev_colors * (1 - SMOOTHING_ALPHA) + new_colors * SMOOTHING_ALPHA
            led_data = prev_colors.astype(np.uint8).flatten().tolist()
            frame = prefix + bytes(led_data)
            ser.write(frame)
            elapsed = time.perf_counter() - prev_time
            delay = max(0, (1/60) - elapsed)
            time.sleep(delay)
            prev_time = time.perf_counter()


except KeyboardInterrupt:
    off_data = [0, 0, 0] * NUM_LEDS
    ser.write(prefix + bytes(off_data))
    ser.close()
