#!/usr/bin/env python3
"""
Raspberry Pi Standalone Local Dashboard
Runs locally without external browser dependencies.
Cycles between Time (10s), Weather (10s), and Local Hardware GPIO Sensors (10s).
"""
import sys
import time
import signal
import config
from sensors import DHTSensor, SmokeSensor, MicSensor
from weather import WeatherService
from ui import DisplayManager

def main():
    print("======================================================")
    print("      RASPBERRY PI LOCAL STANDALONE DASHBOARD         ")
    print("======================================================")
    print(f"Screen Rotation Interval: {config.ROTATION_INTERVAL} seconds")
    print(f"Target Resolution: {config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}")
    print(f"Weather Location: {config.WEATHER_CITY_NAME} ({config.WEATHER_LATITUDE}, {config.WEATHER_LONGITUDE})")
    print("------------------------------------------------------")
    print(f"DHT Sensor (Temp/Humidity): GPIO {config.DHT_PIN}")
    print(f"Smoke Sensor (Gas/Smoke DO): Pin {config.SMOKE_PIN}")
    print(f"Microphone Sensor (Sound DO): Pin {config.MIC_PIN}")
    print("======================================================")
    
    # 1. Initialize Direct GPIO Sensors
    dht_sensor = DHTSensor(pin=config.DHT_PIN, sensor_type=config.DHT_TYPE)
    smoke_sensor = SmokeSensor(pin=config.SMOKE_PIN, active_low=config.SMOKE_ACTIVE_LOW)
    mic_sensor = MicSensor(pin=config.MIC_PIN, active_low=config.MIC_ACTIVE_LOW)
    
    # 2. Initialize Background Weather Fetcher
    weather = WeatherService(
        lat=config.WEATHER_LATITUDE,
        lon=config.WEATHER_LONGITUDE,
        city=config.WEATHER_CITY_NAME
    )
    
    # 3. Launch Pygame Display Manager
    try:
        app = DisplayManager(
            sensor_smoke=smoke_sensor,
            sensor_mic=mic_sensor,
            sensor_dht=dht_sensor,
            weather_service=weather
        )
        
        # Handle Ctrl+C SIGINT gracefully
        def signal_handler(sig, frame):
            print("\n[Main] Exiting dashboard...")
            weather.stop()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        
        print("[Main] Launching GUI display...")
        app.run()
        
    finally:
        weather.stop()
        print("[Main] Cleanup complete.")

if __name__ == "__main__":
    main()
