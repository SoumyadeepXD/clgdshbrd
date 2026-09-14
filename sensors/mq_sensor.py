import config
from .ads_reader import ADS1115Reader

class MQSensor:
    """
    Driver & math processor for MQ Series Gas Sensors (MQ-2, MQ-135, MQ-7, etc.)
    connected to ADS1115 channel A1.
    Calculates real-time numeric gas concentration in PPM and voltage telemetry.
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
        ppm = int(max(10.0, min(2000.0, ppm)))
        
        if ppm < 250:
            status = "GOOD AIR"
        elif ppm < 500:
            status = "MODERATE"
        elif ppm < 800:
            status = "ELEVATED"
        else:
            status = "HIGH GAS"

        return {
            "voltage": round(voltage, 3),
            "ratio": round(ratio, 2),
            "ppm": ppm,
            "display": f"{ppm} PPM",
            "status": status,
            "subtext": f"{round(voltage, 2)}V  ·  {status}",
            "color": config.TEXT_PRIMARY
        }
