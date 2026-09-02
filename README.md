# Raspberry Pi Local Standalone Dashboard

A native, lightweight Python dashboard built specifically for **Raspberry Pi** that runs **100% locally without any external web browser** (no Chromium, no Electron).

It cycles between 3 screens (10s each):
1. **Time & Date**
2. **Weather of Kolkata (New Town)**
3. **Local Hardware Room Telemetry (Noise dB, Local Humidity %, Air Quality AQI/PPM)**

---

## 🤖 How to Boot Directly into Dashboard on Raspberry Pi Startup (Kiosk Configuration)

Follow these steps to configure your Raspberry Pi so it automatically boots directly into your `main.py` dashboard file upon power-up:

### Step 1: Enable Desktop Auto-Login
1. Open terminal on your Raspberry Pi and run:
   ```bash
   sudo raspi-config
   ```
2. Navigate to **1 System Options** $\rightarrow$ **S5 Boot / Auto Login**.
3. Choose **B4 Desktop Autologin** (or **B2 Console Autologin** if using CLI mode).
4. Select **Finish** to save.

---

### Step 2: Configure Systemd Kiosk Service with Your File Path

1. Copy the included systemd kiosk service file:
   ```bash
   sudo cp systemd/pi-dashboard.service /etc/systemd/system/
   ```

2. Open the service file in `nano` to set your Raspberry Pi username and project file path:
   ```bash
   sudo nano /etc/systemd/system/pi-dashboard.service
   ```

3. Ensure `User`, `WorkingDirectory`, and `ExecStart` match your project file location:
   ```ini
   [Unit]
   Description=Raspberry Pi Kiosk Dashboard
   After=network-online.target graphical.target
   Wants=network-online.target

   [Service]
   Type=simple

   # Your Raspberry Pi username (default: pi or your custom username)
   User=pi

   # Path to your project folder
   WorkingDirectory=/home/pi/clgdshbrd

   # Path to your Python virtual environment + your dashboard file
   ExecStart=/home/pi/clgdshbrd/.venv/bin/python main.py

   Environment=PI_DASHBOARD_FULLSCREEN=True
   Environment=DISPLAY=:0
   Environment=XAUTHORITY=/home/pi/.Xauthority
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=graphical.target
   ```
   *(Press `Ctrl+O`, `Enter` to save, and `Ctrl+X` to exit)*

---

### Step 3: Enable Service and Test Reboot

1. Reload systemd and enable the autostart daemon:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable pi-dashboard.service
   sudo systemctl start pi-dashboard.service
   ```

2. Reboot your Raspberry Pi:
   ```bash
   sudo reboot
   ```

---

## 🔌 Hardware Wiring Schematic & Pinout Guide

### Complete Pin-to-Pin Connection Diagram

```
       RASPBERRY PI 40-PIN GPIO HEADER
      ┌──────────────────────────────────┐
      │  (1) 3.3V  [PWR]  │ (2) 5V  [PWR]┼───────────┐ (5V Power Rail)
      │  (3) GPIO 2 [SDA] │ (4) 5V  [PWR]│           │
      │  (5) GPIO 3 [SCL] │ (6) GND [GND]┼────┐      │
      └───────┬──────┬──────────┬────────┘    │      │
              │      │          │             │      │
       ┌──────┘      │          └──────┐      │ (GND Rail)
       │ (SDA Line)  │ (SCL Line)      │      │      │
       ▼             ▼                 ▼      ▼      ▼
   ┌────────────────────────────────────────────────────────┐
   │             ADS1115 / ADS1116 I2C ADC                  │
   ├─────────┬─────────┬─────────┬──────────┬───────────────┤
   │   VDD   │   GND   │   SCL   │   SDA    │  ADDR         │
   └────┬────┴────┬────┴────┬────┴────┬─────┴───┬───────────┘
        │         │         │         │         │
    (3.3V Pin1) (GND Pin6) (SCL Pin5)(SDA Pin3)(GND Pin6)
                  │
                  │              ┌──────────────────────────┐
                  ├─────────────►│ MQ GAS SENSOR            │
                  │              ├──────────────────────────┤
                  │              │ VCC  ◄─── 5V (Pi Pin 2)  │
                  │              │ GND  ◄─── GND (Pi Pin 6) │
   ┌──────────────┼─────────────►│ AOUT ───► ADS1115 A0     │
   │              │              └──────────────────────────┘
   │              │              ┌──────────────────────────┐
   │              │              │ SOUND SENSOR             │
   │              │              ├──────────────────────────┤
   │              │              │ VCC  ◄─── 3.3V (Pi Pin 1)│
   │              │              │ GND  ◄─── GND (Pi Pin 6) │
   │              ├─────────────►│ AOUT ───► ADS1115 A1     │
   │              │              └──────────────────────────┘
   │              │              ┌──────────────────────────┐
   │              │              │ HUMIDITY SENSOR          │
   │              │              ├──────────────────────────┤
   │              │              │ VCC  ◄─── 3.3V (Pi Pin 1)│
   │              │              │ GND  ◄─── GND (Pi Pin 6) │
   │              └─────────────►│ AOUT ───► ADS1115 A2     │
   │                             └──────────────────────────┘
   ▼
 ADS1115 Analog Input Channels:
   • Channel A0 ◄─── MQ Gas Sensor AOUT
   • Channel A1 ◄─── Sound Sensor AOUT
   • Channel A2 ◄─── Humidity Sensor AOUT
```

---

## 📌 Pinout Table

### 1. ADS1115 / ADS1116 ADC $\rightarrow$ Raspberry Pi
| ADS1115 Pin | Raspberry Pi GPIO Pin | Physical Pin # | Description |
| :--- | :--- | :--- | :--- |
| **VDD** | 3.3V Power | **Pin 1** | Power Supply |
| **GND** | Ground | **Pin 6** | Ground Line |
| **SCL** | **GPIO 3 (SCL)** | **Pin 5** | **I2C Clock Line** |
| **SDA** | **GPIO 2 (SDA)** | **Pin 3** | **I2C Data Line** |
| **ADDR** | Ground | **Pin 6** | Sets I2C Address `0x48` |

### 2. Local Hardware Sensors to ADS1115 Channels
| Sensor | Sensor Pin | ADS1115 Channel | Description |
| :--- | :--- | :--- | :--- |
| **MQ Gas Sensor** | **AOUT** | **Channel A0** | Air Quality / Gas PPM Signal |
| **Sound Sensor** | **AOUT** | **Channel A1** | Noise Decibel (dB) Signal |
| **Humidity Sensor** | **AOUT** | **Channel A2** | Local Room Humidity (% RH) Signal |

---

## ⚙️ Enabling I2C on Raspberry Pi

1. Open terminal on Raspberry Pi and run:
   ```bash
   sudo raspi-config
   ```
2. Go to **Interface Options** $\rightarrow$ **I2C** $\rightarrow$ **Enable**.
3. Reboot: `sudo reboot`
4. Test I2C detection:
   ```bash
   sudo i2cdetect -y 1
   ```
   *(You should see `48` at address `0x48`)*
