import config
from .ads_reader import ADS1115Reader

class MQSensor:
    """
    Driver & math processor for MQ Series Gas Sensors (MQ-2, MQ-135, MQ-7, etc.)
    connected to ADS1115 channel A0.
    """
    def __init__(self, adc_reader: ADS1115Reader, channel=config.MQ_CHANNEL):
        self.adc = adc_reader
        self.channel = channel
        self.rl_kohm = 10.0
        self.ro = config.MQ_CLEAN_AIR_RO

    def get_readings(self) -> dict:
        voltage = self.adc.read_voltage(self.channel)
        v_signal = max(0.01, min(4.99, voltage))
        v_supply = 3.3 if v_signal <= 3.3 else 5.0
        
        rs = ((v_supply - v_signal) / v_signal) * self.rl_kohm
        rs = max(0.1, rs)
        ratio = rs / self.ro
        
        ppm = 100.0 * ((ratio) ** -1.5)
        ppm = max(10.0, min(2000.0, ppm))
        
        # Minimalist status & subtle monochrome colors
        if ppm < 250:
            status = "GOOD"
            color = config.TEXT_PRIMARY
        elif ppm < 500:
            status = "MODERATE"
            color = config.TEXT_SECONDARY
        elif ppm < 800:
            status = "ELEVATED"
            color = config.TEXT_MUTED
        else:
            status = "HIGH"
            color = config.TEXT_PRIMARY

        return {
            "voltage": round(voltage, 3),
            "ratio": round(ratio, 2),
            "ppm": int(ppm),
            "status": status,
            "color": color
        }
