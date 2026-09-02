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
# HARDWARE & SENSOR CONFIGURATION (ADS1115 / ADS1116 I2C ADC)
# Channel Map: A0 = Humidity, A1 = MQ Gas, A3 = Noise
# ==============================================================================
FORCE_MOCK_SENSORS = os.environ.get("FORCE_MOCK_SENSORS", "False").lower() == "true"

ADS1115_GAIN = 1
HUMIDITY_CHANNEL = 0    # A0: Local Humidity Sensor (% RH)
MQ_CHANNEL = 1          # A1: MQ Gas Sensor (AQI / PPM)
SOUND_CHANNEL = 3       # A3: Sound / Noise Sensor (Decibel dB)

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
