# Raspberry Pi Local Standalone Dashboard

A native, lightweight Python dashboard built specifically for **Raspberry Pi** that runs **100% locally without any external web browser** (no Chromium, no Electron).

It cycles between **Time/Clock** for 10 seconds and **Weather Details** for 10 seconds (along with a Hardware Sensor view), while continuously reading data from **MQ Air Quality Gas sensors** and a **Sound Decibel sensor** via an **ADS1115 / ADS1015 I2C ADC**.

---

## 📸 Screenshots & Overview

- **Zero Browser Overhead**: Built on native **Pygame** rendering direct to display (DRM/KGB/X11/Wayland).
- **10-Second Auto-Rotation**: Visual countdown progress bar auto-switches screens every 10s.
- **Always-On Hardware Telemetry**: Live sensor ticker bar at the bottom displaying real-time MQ PPM gas levels and Sound dB noise levels.
- **Automatic Hardware Mock Mode**: If running on a desktop Mac/PC without physical I2C sensors attached, it automatically enters **Mock Mode** using realistic simulated sensor data.

---

## 🔌 Hardware Connections & Wiring Guide

### 1. ADS1115 / ADS1015 I2C ADC Pinouts
| ADS1115 Pin | Raspberry Pi Pin | Description |
| :--- | :--- | :--- |
| **VDD** | **Pin 1 (3.3V)** or **Pin 2 (5V)** | Power Supply |
| **GND** | **Pin 6 (GND)** | Ground |
| **SDA** | **Pin 3 (GPIO 2 / SDA)** | I2C Data |
| **SCL** | **Pin 5 (GPIO 3 / SCL)** | I2C Clock |

### 2. Sensor Connections to ADS1115
| Sensor | Sensor Pin | ADS1115 Channel | Description |
| :--- | :--- | :--- | :--- |
| **MQ Gas Sensor** (MQ2/MQ135/MQ7) | **AOUT** | **Channel A0** | Analog Gas Signal Voltage |
| **Sound Decibel Sensor** | **AOUT** | **Channel A1** | Analog Sound Signal Voltage |

---

## ⚙️ Enabling I2C on Raspberry Pi

1. Open a terminal on your Pi and run:
   ```bash
   sudo raspi-config
   ```
2. Navigate to **Interface Options** $\rightarrow$ **I2C** $\rightarrow$ **Enable**.
3. Reboot your Pi:
   ```bash
   sudo reboot
   ```
4. Verify the ADS1115 address (`0x48`) is detected:
   ```bash
   sudo i2cdetect -y 1
   ```

---

## 🚀 Quick Start Guide

### 1. Environment Setup
```bash
# Clone or navigate to project directory
cd clgdshbrd

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Application
```bash
# Run locally (Windowed or Desktop testing)
python3 main.py

# Force Fullscreen Kiosk Mode:
PI_DASHBOARD_FULLSCREEN=True python3 main.py
```

---

## 🔧 Customization Options (`config.py`)

You can easily adjust parameters in `config.py` or via environment variables:

| Setting | Default | Description |
| :--- | :--- | :--- |
| `ROTATION_INTERVAL` | `10` | Seconds per screen rotation |
| `WEATHER_LATITUDE` | `28.6139` | Latitude for Open-Meteo Weather API |
| `WEATHER_LONGITUDE` | `77.2090` | Longitude for Open-Meteo Weather API |
| `WEATHER_CITY_NAME` | `"New Delhi"` | Display name for location |
| `FORCE_MOCK_SENSORS` | `False` | Force simulated sensor values |

---

## 🤖 Autostart on Pi Boot (Systemd Kiosk)

To make the dashboard automatically launch on Raspberry Pi startup:

1. Copy the systemd service file:
   ```bash
   sudo cp systemd/pi-dashboard.service /etc/systemd/system/
   ```
2. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable pi-dashboard.service
   sudo systemctl start pi-dashboard.service
   ```
3. Check status:
   ```bash
   sudo systemctl status pi-dashboard.service
   ```

---

## 🎮 Keyboard & Touch Controls

- **Spacebar / Right Arrow / Touch Tap**: Instantly skip to the next screen.
- **Left Arrow**: Go back to the previous screen.
- **'q' / ESC**: Exit dashboard application.
