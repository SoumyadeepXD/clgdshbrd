import time
import math
import config
from .ads_reader import ADS1115Reader

class SoundSensor:
    """
    Driver & Decibel math processor for Sound Level / Microphonic sensors
    connected to ADS1115 channel A1.
    """
    def __init__(self, adc_reader: ADS1115Reader, channel=config.SOUND_CHANNEL):
        self.adc = adc_reader
        self.channel = channel

    def get_readings(self, sample_duration: float = 0.05) -> dict:
        v_min = 5.0
        v_max = 0.0
        start_time = time.time()
        
        while time.time() - start_time < sample_duration:
            v = self.adc.read_voltage(self.channel)
            if v > v_max:
                v_max = v
            if v < v_min:
                v_min = v
            
        v_pp = max(0.001, v_max - v_min)
        v_rms = v_pp / (2 * math.sqrt(2))
        v_rms = max(0.0001, v_rms)
        
        db = 20.0 * math.log10(v_rms / config.SOUND_V_REF) + config.SOUND_DB_OFFSET
        db = max(30.0, min(120.0, db))
        
        # Minimalist status & subtle monochrome colors
        if db < 55.0:
            status = "QUIET"
            color = config.TEXT_PRIMARY
        elif db < 70.0:
            status = "NORMAL"
            color = config.TEXT_SECONDARY
        elif db < 85.0:
            status = "MODERATE"
            color = config.TEXT_MUTED
        else:
            status = "LOUD"
            color = config.TEXT_PRIMARY

        return {
            "voltage": round(v_max, 3),
            "v_pp": round(v_pp, 3),
            "db": int(db),
            "status": status,
            "color": color
        }
