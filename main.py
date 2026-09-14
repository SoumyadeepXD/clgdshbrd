#!/usr/bin/env python3
"""
Raspberry Pi Standalone Local Dashboard
Runs locally without external browser dependencies.
Cycles between Time (10s), Weather (10s), and Real-time Numeric Telemetry Sensors (10s).
"""
import sys
import time
import signal
import config
from sensors import ADS1115Reader, MQSensor, SoundSensor, HumiditySensor
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
    print(f"Humidity Sensor: ADS1115 Channel A{config.HUMIDITY_CHANNEL}")
    print(f"MQ Gas Sensor (AQI): ADS1115 Channel A{config.MQ_CHANNEL}")
    print(f"Noise Sensor (Decibel dB): ADS1115 Channel A{config.SOUND_CHANNEL}")
    print("======================================================")
    
    # 1. Initialize Hardware ADC (ADS1115 / ADS1116)
    adc = ADS1115Reader(gain=config.ADS1115_GAIN)
    
    # 2. Initialize Hardware Sensors (A0: Humidity, A1: MQ Gas AQI, A3: Sound dB)
    humidity_sensor = HumiditySensor(adc, channel=config.HUMIDITY_CHANNEL)
    mq_sensor = MQSensor(adc, channel=config.MQ_CHANNEL)
    sound_sensor = SoundSensor(adc, channel=config.SOUND_CHANNEL)
    
    # 3. Initialize Background Weather Fetcher
    weather = WeatherService(
        lat=config.WEATHER_LATITUDE,
        lon=config.WEATHER_LONGITUDE,
        city=config.WEATHER_CITY_NAME
    )
    
    # 4. Launch Pygame Display Manager
    try:
        app = DisplayManager(
            sensor_mq=mq_sensor,
            sensor_sound=sound_sensor,
            sensor_humidity=humidity_sensor,
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
