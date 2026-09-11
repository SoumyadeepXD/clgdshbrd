from .mic_sensor import MicSensor
import config

class SoundSensor(MicSensor):
    """
    Backward-compatible wrapper for SoundSensor.
    Now backed directly by MicSensor on Raspberry Pi GPIO (default Pin 13).
    """
    def __init__(self, adc_reader=None, channel=None, pin=config.MIC_PIN, **kwargs):
        super().__init__(pin=pin, **kwargs)
