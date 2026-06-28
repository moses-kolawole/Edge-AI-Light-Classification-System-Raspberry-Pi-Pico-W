from machine import ADC, Pin, I2C
from pico_i2c_lcd import I2cLcd
from collections import deque
import time
import math

# =====================================
# LCD SETUP
# =====================================
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# =====================================
# LDR SETUP
# =====================================
ldr1 = ADC(26)
ldr2 = ADC(27)
ldr3 = ADC(28)

# =====================================
# RGB LED SETUP (Common Cathode)
# =====================================
red   = Pin(16, Pin.OUT)
green = Pin(17, Pin.OUT)
blue  = Pin(18, Pin.OUT)

def rgb_off():
    red.value(0); green.value(0); blue.value(0)

def rgb_red():
    red.value(1); green.value(0); blue.value(0)

def rgb_green():
    red.value(0); green.value(1); blue.value(0)

def rgb_blue():
    red.value(0); green.value(0); blue.value(1)

def rgb_yellow():
    red.value(1); green.value(1); blue.value(0)

# =====================================
# SELF CALIBRATION
# =====================================
lcd.clear()
lcd.putstr("Calibrating...  ")
lcd.move_to(0, 1)
lcd.putstr("Please Wait...  ")

samples = []
for i in range(30):
    l1 = ldr1.read_u16()
    l2 = ldr2.read_u16()
    l3 = ldr3.read_u16()
    avg = (l1 * 0.5) + (l2 * 0.2) + (l3 * 0.3)
    samples.append(avg)
    time.sleep(0.1)  # faster calibration

mean     = sum(samples) / len(samples)
variance = sum((x - mean) ** 2 for x in samples) / len(samples)
std      = math.sqrt(variance)

history = deque((), 10)  # smaller buffer = faster flicker response

lcd.clear()
lcd.putstr("Calibration     ")
lcd.move_to(0, 1)
lcd.putstr("Complete!       ")
time.sleep(1)

print("==============================")
print("Mean  = {:.0f}".format(mean))
print("STD   = {:.0f}".format(std))
print("Upper = {:.0f}".format(mean + std))
print("Lower = {:.0f}".format(mean - std))
print("==============================")

# =====================================
# TRACKING LAST STATE
# only update LCD when state actually changes
# =====================================
last_state = ""

# =====================================
# MAIN LOOP
# =====================================
while True:
    try:
        # --- Read Sensors ---
        l1 = ldr1.read_u16()
        l2 = ldr2.read_u16()
        l3 = ldr3.read_u16()
        avg = (l1 * 0.5) + (l2 * 0.2) + (l3 * 0.3)

        # --- Spread and Flicker ---
        spread = max(l1, l2, l3) - min(l1, l2, l3)
        history.append(avg)
        if len(history) > 1:
            flicker_range = max(history) - min(history)
        else:
            flicker_range = 0

        # --- Decision Tree ---
        if spread > 12000 or flicker_range > 5000:
            state = "FLICKER"
        elif avg > mean + std:
            state = "BRIGHT"
        elif avg < mean - std:
            state = "DARK"
        else:
            state = "DIM"

        # --- RGB updates IMMEDIATELY every loop ---
        if state == "FLICKER":
            rgb_yellow()
        elif state == "BRIGHT":
            rgb_green()
        elif state == "DARK":
            rgb_red()
        else:
            rgb_blue()

        # --- LCD only updates when state changes ---
        if state != last_state:
            lcd.move_to(0, 0)
            lcd.putstr("State:{:<10}".format(state))
            last_state = state

        # --- AVG line updates every loop without clear ---
        lcd.move_to(0, 1)
        lcd.putstr("Avg:{:<12.0f}".format(avg))

        # --- Continuous Learning ---
        mean     = (0.999 * mean)     + (0.001 * avg)
        variance = (0.999 * variance) + (0.001 * (avg - mean) ** 2)
        std      = math.sqrt(variance)

        # --- Serial Monitor ---
        print("L1={:>6} L2={:>6} L3={:>6} AVG={:>7.0f} Spread={:>6.0f} State={}".format(
            l1, l2, l3, avg, spread, state))

        # NO sleep — runs as fast as possible
        # small yield to prevent watchdog issues
        time.sleep_ms(50)

    except Exception as e:
        print("ERROR:", e)
        lcd.clear()
        lcd.putstr("ERR:            ")
        lcd.move_to(0, 1)
        lcd.putstr("{:<16}".format(str(e)[:16]))
        time.sleep(2)

