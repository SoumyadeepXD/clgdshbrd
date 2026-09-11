import os

# ==============================================================================
# DISPLAY & ROTATION CONFIGURATION
# ==============================================================================
ROTATION_INTERVAL = 10  # 10 seconds per screen
FPS = 30

# Resolution setup
FULLSCREEN = os.environ.get("PI_DASHBOARD_FULLSCREEN", "False").lower() == "true"
SCREEN_WIDTH = int(os.environ.get("PI_DASHBOARD_WIDTH", "800"))
SCREEN_HEIGHT = int(os.environ.get("PI_DASHBOARD_HEIGHT", "480"))

# ==============================================================================
# WEATHER API CONFIGURATION (Kolkata New Town Coordinates)
# ==============================================================================
WEATHER_LATITUDE = float(os.environ.get("WEATHER_LAT", "22.5833"))
WEATHER_LONGITUDE = float(os.environ.get("WEATHER_LON", "88.4667"))
WEATHER_CITY_NAME = os.environ.get("WEATHER_CITY", "Kolkata (New Town)")
WEATHER_UPDATE_INTERVAL = 600  # 10 minutes

# ==============================================================================
# HARDWARE & SENSOR CONFIGURATION (DIRECT RASPBERRY PI GPIO PINS)
# DHT Sensor: GPIO 4
# Smoke Sensor: Pin 11 (Digital DO)
# Mic / Sound Sensor: Pin 13 (Digital DO)
# ==============================================================================
FORCE_MOCK_SENSORS = os.environ.get("FORCE_MOCK_SENSORS", "False").lower() == "true"

# Pin Numbering Mode: Default is BCM GPIO numbers (GPIO 4, GPIO 11, GPIO 13).
# If you wired directly to Physical Header Pins on the Raspberry Pi board:
#   Physical Pin 7  -> BCM GPIO 4
#   Physical Pin 11 -> BCM GPIO 17
#   Physical Pin 13 -> BCM GPIO 27
# Set USE_PHYSICAL_PINS = True to automatically map physical pins 11 and 13 to BCM 17 and 27.
USE_PHYSICAL_PINS = os.environ.get("USE_PHYSICAL_PINS", "False").lower() == "true"

# DHT Sensor (Temperature & Humidity)
DHT_PIN = int(os.environ.get("DHT_PIN", "4"))           # Default: GPIO 4 (Physical Pin 7)
DHT_TYPE = int(os.environ.get("DHT_TYPE", "11"))         # 11 for DHT11, 22 for DHT22 / AM2302

# Smoke / Gas Sensor (Digital DO Pin)
SMOKE_PIN = int(os.environ.get("SMOKE_PIN", "11"))       # Default: Pin 11
SMOKE_ACTIVE_LOW = os.environ.get("SMOKE_ACTIVE_LOW", "True").lower() == "true"  # DO goes LOW on smoke detect

# Microphone / Sound Sensor (Digital DO Pin)
MIC_PIN = int(os.environ.get("MIC_PIN", "13"))           # Default: Pin 13
MIC_ACTIVE_LOW = os.environ.get("MIC_ACTIVE_LOW", "True").lower() == "true"      # DO goes LOW on sound detect

# Backward-compatibility fallback variables (Deprecated ADC settings)
ADS1115_GAIN = 1
HUMIDITY_CHANNEL = 0
MQ_CHANNEL = 1
SOUND_CHANNEL = 3
MQ_CLEAN_AIR_RO = 10.0
SOUND_V_REF = 0.005
SOUND_DB_OFFSET = 45.0

# ==============================================================================
# MINIMALIST GLASSMORPHISM PALETTE (Monochrome)
# ==============================================================================
COLOR_BG = (10, 13, 20)            # Deep Matte Dark
COLOR_GLASS_BG = (20, 26, 38)      # Translucent Frosted Glass Card
COLOR_GLASS_BORDER = (45, 55, 75)  # Subtle Border
COLOR_GLASS_GLOW = (80, 95, 120)   # Refractive Edge Highlight

TEXT_PRIMARY = (255, 255, 255)     # Pure White
TEXT_SECONDARY = (160, 174, 192)   # Soft Gray
TEXT_MUTED = (113, 128, 150)       # Dim Slate Gray
