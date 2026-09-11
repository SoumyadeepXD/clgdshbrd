# Raspberry Pi Local Standalone Dashboard

A native, lightweight Python dashboard built specifically for **Raspberry Pi** that runs **100% locally without any external web browser** (no Chromium, no Electron).

It cycles between 3 screens (10s each):
1. **Time & Date**
2. **Weather of Kolkata (New Town)**
3. **Local Hardware Room Telemetry (DHT Sensor GPIO 4, Smoke Sensor Pin 11, Mic Sensor Pin 13)**

---

## 🔌 Hardware Wiring Schematic & Pinout Guide (Direct GPIO)

No external ADC (ADS1115) required! All sensors connect directly to the Raspberry Pi 40-pin GPIO header.

### Complete Pin-to-Pin Connection Diagram

```
       RASPBERRY PI 40-PIN GPIO HEADER
      ┌─────────────────────────────────────────┐
      │  (1) 3.3V [PWR]   │  (2) 5V  [PWR]──────┼──────────┐ (5V Power Rail)
      │  (3) GPIO 2       │  (4) 5V  [PWR]      │          │
      │  (5) GPIO 3       │  (6) GND [GND]──────┼────┐     │
      │  (7) GPIO 4──────┐│  (8) GPIO 14        │    │     │
      │  (9) GND         ││ (10) GPIO 15        │    │     │
      │ (11) PIN 11 ─────┼┼─┐(12) GPIO 18       │    │     │
      │ (13) PIN 13 ──┐  ││ │                   │    │     │
      └───────┬───────┼──┼┴─┼───────────────────┘    │     │
              │       │  │  │ (Pin 11 Signal)        │     │
              │       │  │  ▼                        │     │
              │       │  │  ┌────────────────────────┴───┐ │
              │       │  │  │ SMOKE SENSOR (MQ Series)   │ │
              │       │  │  ├────────────────────────────┤ │
              │       │  │  │ VCC ◄─── 5V (Pi Pin 2) ────┼─┘
              │       │  │  │ GND ◄─── GND (Pi Pin 6) ───┤
              │       │  │  │ DO  ───► Pi Pin 11         │
              │       │  │  └────────────────────────────┘
              │       │  │                           │
              │       │  │ (GPIO 4 Signal)           │
              │       │  ▼                           │
              │       │  ┌───────────────────────────┴───┐
              │       │  │ DHT SENSOR (DHT11 / DHT22)    │
              │       │  ├───────────────────────────────┤
              │       │  │ VCC ◄─── 3.3V (Pi Pin 1) ─────┤
              │       │  │ GND ◄─── GND (Pi Pin 6) ──────┤
              │       │  │ DATA ──► Pi GPIO 4 (Pin 7)    │
              │       │  └───────────────────────────────┘
              │       │                              │
              │ (Pin 13 Signal)                      │
              ▼                                      │
              ┌──────────────────────────────────────┴───┐
              │ MICROPHONE / SOUND SENSOR (KY-037/038)   │
              ├──────────────────────────────────────────┤
              │ VCC  ◄─── 3.3V (Pi Pin 1)                │
              │ GND  ◄─── GND (Pi Pin 6) ────────────────┤
              │ DO   ───► Pi Pin 13                      │
              └──────────────────────────────────────────┘
```

---

## 📌 Pinout Table

### Sensor Pin Connections

| Sensor | Sensor Pin | Raspberry Pi Pin | Description |
| :--- | :--- | :--- | :--- |
| **DHT11 / DHT22** | **VCC** | **Pin 1 (3.3V)** | Power Supply |
| | **GND** | **Pin 6 (GND)** | Ground |
| | **DATA / OUT** | **GPIO 4 (Physical Pin 7)** | 1-Wire Digital Climate Telemetry |
| **Smoke Sensor (MQ)**| **VCC** | **Pin 2 (5V)** | Power Supply (MQ heater requires 5V) |
| | **GND** | **Pin 6 (GND)** | Ground |
| | **DO (Digital Out)** | **Pin 11** | Gas / Smoke Detection Trigger |
| **Mic / Sound Sensor** | **VCC** | **Pin 1 (3.3V)** | Power Supply |
| | **GND** | **Pin 6 (GND)** | Ground |
| | **DO (Digital Out)** | **Pin 13** | Acoustic / Sound Detection Trigger |

> [!NOTE]
> **Pin Numbering Mode**:
> - By default, pins are interpreted as **BCM GPIO numbers** (DHT = GPIO 4, Smoke = GPIO 11, Mic = GPIO 13).
> - If you wired by **Physical Board Pin numbers** (Pin 11 = BCM 17, Pin 13 = BCM 27), you can enable automatic physical pin translation by running with `USE_PHYSICAL_PINS=true` or changing the setting in `config.py`.

---

## 🚀 Installation & Setup on Raspberry Pi

1. Install system prerequisites (if needed for GPIO / DHT on Raspberry Pi OS):
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-pygame python3-gpiozero libgpiod2
   ```

2. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Run the dashboard:
   ```bash
   python3 main.py
   ```

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
