# Raspberry Pi Local Standalone Dashboard

A native, lightweight Python dashboard built specifically for **Raspberry Pi** that runs **100% locally without any external web browser** (no Chromium, no Electron).

It cycles between 3 screens (10s each):
1. **Time & Date**
2. **Weather of Kolkata (New Town)**
3. **Local Hardware Room Telemetry (Local Humidity A0, MQ Gas A1, Noise dB A3)**

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
                  ├─────────────►│ HUMIDITY SENSOR          │
                  │              ├──────────────────────────┤
                  │              │ VCC  ◄─── 3.3V (Pi Pin 1)│
                  │              │ GND  ◄─── GND (Pi Pin 6) │
   ┌──────────────┼─────────────►│ AOUT ───► ADS1115 A0     │
   │              │              └──────────────────────────┘
   │              │              ┌──────────────────────────┐
   │              │              │ MQ GAS SENSOR            │
   │              │              ├──────────────────────────┤
   │              │              │ VCC  ◄─── 5V (Pi Pin 2)  │
   │              │              │ GND  ◄─── GND (Pi Pin 6) │
   │              ├─────────────►│ AOUT ───► ADS1115 A1     │
   │              │              └──────────────────────────┘
   │              │              ┌──────────────────────────┐
   │              │              │ SOUND / NOISE SENSOR     │
   │              │              ├──────────────────────────┤
   │              │              │ VCC  ◄─── 3.3V (Pi Pin 1)│
   │              │              │ GND  ◄─── GND (Pi Pin 6) │
   │              └─────────────►│ AOUT ───► ADS1115 A3     │
   │                             └──────────────────────────┘
   ▼
 ADS1115 Analog Input Channels:
   • Channel A0 ◄─── Humidity Sensor AOUT
   • Channel A1 ◄─── MQ Gas Sensor AOUT
   • Channel A3 ◄─── Sound / Noise Sensor AOUT
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
| **Humidity Sensor** | **AOUT** | **Channel A0** | Local Room Humidity (% RH) Signal |
| **MQ Gas Sensor** | **AOUT** | **Channel A1** | Air Quality / Gas PPM Signal |
| **Sound / Noise Sensor** | **AOUT** | **Channel A3** | Noise Decibel (dB) Signal |

---

## 🤖 How to Boot Directly into Dashboard on Raspberry Pi Startup

1. Copy systemd service file:
   ```bash
   sudo cp systemd/pi-dashboard.service /etc/systemd/system/
   ```
2. Enable and start autostart service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now pi-dashboard.service
   ```
