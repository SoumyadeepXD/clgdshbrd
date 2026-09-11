from .smoke_sensor import SmokeSensor
import config

class MQSensor(SmokeSensor):
    """
    Backward-compatible wrapper for MQSensor.
    Now backed directly by SmokeSensor on Raspberry Pi GPIO (default Pin 11).
    """
    def __init__(self, adc_reader=None, channel=None, pin=config.SMOKE_PIN, **kwargs):
        super().__init__(pin=pin, **kwargs)
