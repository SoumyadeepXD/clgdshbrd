import time
import math
import config
from .ads_reader import ADS1115Reader

class HumiditySensor:
    """
    Driver for local Analog Humidity Sensor connected to ADS1115 channel A0.
    Converts raw analog voltage into local relative humidity percentage (% RH).
    """
    def __init__(self, adc_reader: ADS1115Reader, channel=config.HUMIDITY_CHANNEL):
        self.adc = adc_reader
        self.channel = channel

    def get_readings(self) -> dict:
        voltage = self.adc.read_voltage(self.channel)
        
        # Standard analog humidity sensor conversion (0.1V - 3.3V -> 0% - 100% RH)
        v_signal = max(0.0, min(3.3, voltage))
        rh_percent = (v_signal / 3.3) * 100.0
        
        # Simulated fallback signal if ADC in mock mode or unpowered
        if self.adc.is_mock or voltage <= 0.05:
            t = time.time()
            rh_percent = 55.0 + 8.0 * math.sin(t / 20.0)
            
        rh_int = int(max(10, min(95, rh_percent)))
        
        if rh_int < 35:
            status = "DRY"
        elif rh_int <= 65:
            status = "COMFORTABLE"
        else:
            status = "HUMID"

        return {
            "voltage": round(voltage, 3),
            "humidity": f"{rh_int}%",
            "val": rh_int,
            "display": f"{rh_int}%",
            "status": status,
            "subtext": f"{round(voltage, 2)}V  ·  {status}",
            "color": config.TEXT_PRIMARY
        }
