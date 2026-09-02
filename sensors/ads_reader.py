import time
import math
import random
import config

class ADS1115Reader:
    """
    Hardware abstraction layer for ADS1115 / ADS1015 / ADS1116 I2C ADC.
    Automatically detects physical hardware or gracefully degrades to Mock Mode
    when running on a standard PC/laptop without physical I2C sensors attached.
    """
    def __init__(self, gain=config.ADS1115_GAIN, force_mock=config.FORCE_MOCK_SENSORS):
        self.gain = gain
        self.is_mock = force_mock
        self.i2c = None
        self.ads = None
        self.channels = {}

        if not self.is_mock:
            try:
                import board
                import busio
                import adafruit_ads1x15.ads1115 as ADS
                from adafruit_ads1x15.analog_in import AnalogIn

                self.board = board
                self.ADS = ADS
                self.AnalogIn = AnalogIn
                
                # Initialize I2C bus and ADS1115 ADC
                self.i2c = busio.I2C(board.SCL, board.SDA)
                self.ads = ADS.ADS1115(self.i2c, gain=self.gain)
                print("[ADS1115Reader] Physical ADS1115 ADC initialized via I2C.")
            except Exception as e:
                print(f"[ADS1115Reader] Hardware I2C not available ({e}). Switching to MOCK SENSOR MODE.")
                self.is_mock = True

    def read_voltage(self, channel: int) -> float:
        """
        Reads voltage from specified channel (0: A0, 1: A1, 2: A2, 3: A3).
        Returns voltage in Volts (float).
        """
        if not self.is_mock and self.ads:
            try:
                channel_pin = getattr(self.ADS, f"P{channel}")
                if channel not in self.channels:
                    self.channels[channel] = self.AnalogIn(self.ads, channel_pin)
                return self.channels[channel].voltage
            except Exception as e:
                print(f"[ADS1115Reader] Error reading hardware channel A{channel}: {e}. Falling back to mock.")
        
        # Mock mode fallback with realistic simulated signal
        t = time.time()
        if channel == config.HUMIDITY_CHANNEL:
            # Simulate Humidity sensor voltage on A0 (1.6V ~ 1.8V -> ~52% RH)
            return max(0.5, min(3.3, 1.7 + 0.25 * math.sin(t / 20.0)))

        elif channel == config.MQ_CHANNEL:
            # Simulate MQ gas sensor voltage on A1 (ranges 0.4V to 2.5V)
            base_v = 0.8 + 0.3 * math.sin(t / 15.0)
            noise = random.uniform(-0.02, 0.02)
            surge = 0.8 * math.exp(-((t % 40) - 20)**2 / 10.0) if abs((t % 40) - 20) < 5 else 0
            return max(0.1, min(3.3, base_v + noise + surge))
            
        elif channel == config.SOUND_CHANNEL:
            # Simulate Sound sensor voltage on A3 (ranges 0.05V ambient to 1.2V peak)
            base_v = 0.15 + 0.05 * math.sin(t / 3.0)
            ambient_noise = abs(random.gauss(0, 0.08))
            peak = random.uniform(0.4, 0.9) if (int(t) % 12 == 0) else 0.0
            return max(0.01, min(3.3, base_v + ambient_noise + peak))
            
        else:
            return 1.65 + 0.5 * math.sin(t)

    def read_raw(self, channel: int) -> int:
        """
        Reads raw 16-bit signed integer value from ADC channel (-32768 to 32767).
        """
        voltage = self.read_voltage(channel)
        return int((voltage / 4.096) * 32767)
