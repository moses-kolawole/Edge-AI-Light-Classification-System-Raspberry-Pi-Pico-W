# Edge-AI-Light-Classification-System-Raspberry-Pi-Pico-W

## Overview

This project is an Edge AI-inspired light classification system built using the Raspberry Pi Pico W. It continuously reads data from three LDR (Light Dependent Resistor) sensors, performs on-device statistical analysis, automatically calibrates itself, and classifies the surrounding environment into different lighting conditions.

The system provides real-time feedback using a 16x2 I2C LCD display and an RGB LED without requiring any internet connection or cloud processing.

## Features

* Reads light intensity from three LDR sensors
* Automatic startup calibration
* Multi-sensor data fusion
* Dynamic light classification
* Continuous learning using adaptive statistics
* Flicker detection
* Real-time LCD display
* RGB LED status indication
* Runs completely on the Raspberry Pi Pico W

## Hardware Used

* Raspberry Pi Pico W
* 3 × LDR Sensors
* 16×2 I2C LCD Display
* RGB LED (Common Cathode)
* Resistors
* Breadboard
* Jumper Wires
* USB Cable

## Software Used

* MicroPython
* Thonny IDE

## Pin Connections

### LDR Sensors

| Component | Pico Pin    |
| --------- | ----------- |
| LDR 1     | GP26 (ADC0) |
| LDR 2     | GP27 (ADC1) |
| LDR 3     | GP28 (ADC2) |

### I2C LCD

| LCD | Pico Pin |
| --- | -------- |
| SDA | GP0      |
| SCL | GP1      |
| VCC | 3.3V     |
| GND | GND      |

### RGB LED

| LED Color | Pico Pin |
| --------- | -------- |
| Red       | GP16     |
| Green     | GP17     |
| Blue      | GP18     |

## Check out the program Codes

[Click Here to access the projects code](codes)


## How It Works

[Click Here to check out the Demo video](https://youtu.be/K9bCWV1TszI?si=BwJrnmWBc5W49Yja) 

### Step 1

When powered on, the Pico W automatically performs a self-calibration process.

It collects multiple sensor readings to determine:

* Mean
* Variance
* Standard Deviation

These values become the baseline for light classification.

### Step 2

The system continuously reads all three LDR sensors.

Instead of relying on one sensor, it combines all three readings using weighted averaging.

Average Light = (LDR1 × 0.5) + (LDR2 × 0.2) + (LDR3 × 0.3)

This provides a more reliable representation of the surrounding light.

### Step 3

The system analyses:

* Average light intensity
* Sensor spread
* Recent light history

These values are used to classify the environment.

### Step 4

The detected state is displayed on the LCD while the RGB LED changes colour to indicate the current lighting condition.

| State   | RGB LED |
| ------- | ------- |
| Bright  | Green   |
| Dim     | Blue    |
| Dark    | Red     |
| Flicker | Yellow  |

### Step 5

The system continuously updates its statistical model, allowing it to slowly adapt to changes in ambient lighting over time.

## Light Classification Logic

### Bright

Detected when the average light intensity is higher than the calculated upper threshold.

### Dim

Detected when the light level is within the normal operating range.

### Dark

Detected when the average light intensity falls below the lower threshold.

### Flicker

Detected when:

* Sensor readings differ significantly, or
* Rapid light changes occur over a short period.

## Project Highlights

* Edge AI Concepts
* Embedded Systems Programming
* Multi-Sensor Data Fusion
* Statistical Processing
* Adaptive Thresholding
* Continuous Learning
* Decision Tree Classification
* Flicker Detection
* Real-Time Monitoring
* Hardware and Software Integration

## Skills Demonstrated

* Raspberry Pi Pico W Programming
* MicroPython
* ADC Programming
* GPIO Control
* I2C Communication
* LCD Programming
* RGB LED Control
* Embedded System Design
* Sensor Fusion
* Statistical Analysis
* Real-Time Data Processing
* Edge AI Fundamentals

## Project Structure

```text
Edge-AI-Light-Classification-System-Raspberry-Pi-Pico-W/
│
├── main.py
├── lcd_api.py
├── pico_i2c_lcd.py
├── README.md
├── images/
│   ├── hardware.jpg
│   ├── lcd_display.jpg
│   └── wiring.jpg
└── demo.mp4
```

## Future Improvements

* OLED display support
* Data logging to SD card
* Wi-Fi dashboard
* Web-based monitoring
* Machine learning model integration
* Automatic brightness prediction
* Remote monitoring using MQTT
* Sensor health monitoring

## Author

**Moses Olorunfemi Kolawole**

Embedded Systems | Edge AI | IoT | Raspberry Pi Pico W | MicroPython

Always learning, always building.
