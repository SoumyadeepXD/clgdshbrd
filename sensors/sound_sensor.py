import time
import math
import config
from .ads_reader import ADS1115Reader

class SoundSensor:
    """
    Driver & Decibel math processor for Sound Level / Microphonic sensors
    connected to ADS1115 channel A3.
    Calculates real-time numeric noise SPL level in decibels (dB) and peak voltage telemetry.
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
        db_int = int(max(30.0, min(120.0, db)))
        
        if db_int < 55:
            status = "QUIET"
        elif db_int < 70:
            status = "NORMAL"
        elif db_int < 85:
            status = "MODERATE"
        else:
            status = "LOUD NOISE"

        return {
            "voltage": round(v_max, 3),
            "v_pp": round(v_pp, 3),
            "db": db_int,
            "display": f"{db_int} dB",
            "status": status,
            "subtext": f"{round(v_max, 2)}V PEAK  ·  {status}",
            "color": config.TEXT_PRIMARY
        }
