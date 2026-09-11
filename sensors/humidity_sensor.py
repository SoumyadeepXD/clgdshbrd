from .dht_sensor import DHTSensor
import config

class HumiditySensor(DHTSensor):
    """
    Backward-compatible wrapper for HumiditySensor.
    Now backed directly by DHTSensor on Raspberry Pi GPIO (default GPIO 4).
    """
    def __init__(self, adc_reader=None, channel=None, pin=config.DHT_PIN, **kwargs):
        super().__init__(pin=pin, **kwargs)
