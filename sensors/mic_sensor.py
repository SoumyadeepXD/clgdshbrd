import time
import random
import config

class MicSensor:
    """
    Driver for Microphone / Sound Sensor (digital DO pin)
    connected directly to Raspberry Pi GPIO (default Pin 13 / GPIO 27).
    Samples rapid sound trigger pulses and returns numeric decibel dB representation.
    """
    def __init__(self, pin: int = config.MIC_PIN, active_low: bool = config.MIC_ACTIVE_LOW, force_mock: bool = config.FORCE_MOCK_SENSORS):
        self.pin = pin
        self.active_low = active_low
        self.is_mock = force_mock
        self.bcm_pin = self._resolve_pin(self.pin)
        self.gpio_lib = None
        self.device = None
        
        self.active_hold_until = 0.0
        
        if not self.is_mock:
            self._init_hardware()

    def _resolve_pin(self, pin: int) -> int:
        if getattr(config, "USE_PHYSICAL_PINS", False):
            mapping = {7: 4, 11: 17, 13: 27}
            return mapping.get(pin, pin)
        return pin

    def _init_hardware(self):
        try:
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.bcm_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.gpio_lib = "RPi.GPIO"
            print(f"[MicSensor] Physical Mic Sensor initialized via RPi.GPIO on GPIO {self.bcm_pin}.")
            return
        except Exception:
            pass

        try:
            from gpiozero import DigitalInputDevice
            self.device = DigitalInputDevice(self.bcm_pin, pull_up=True)
            self.gpio_lib = "gpiozero"
            print(f"[MicSensor] Physical Mic Sensor initialized via gpiozero on GPIO {self.bcm_pin}.")
            return
        except Exception as e:
            print(f"[MicSensor] Hardware GPIO not available ({e}). Using MOCK SENSOR MODE.")
            self.is_mock = True

    def _read_instant(self) -> int:
        if not self.is_mock:
            try:
                if self.gpio_lib == "RPi.GPIO":
                    import RPi.GPIO as GPIO
                    return GPIO.input(self.bcm_pin)
                elif self.gpio_lib == "gpiozero" and self.device:
                    return 0 if self.device.is_active else 1
            except Exception as e:
                print(f"[MicSensor] Error reading pin {self.bcm_pin}: {e}")
        return 1

    def get_readings(self, sample_duration: float = 0.02) -> dict:
        now = time.time()
        sound_detected = False
        
        if not self.is_mock:
            start_t = time.time()
            while time.time() - start_t < sample_duration:
                val = self._read_instant()
                triggered = (val == 0) if self.active_low else (val == 1)
                if triggered:
                    sound_detected = True
                    break
                time.sleep(0.001)
        else:
            sound_detected = (int(now) % 15 == 0)

        if sound_detected:
            self.active_hold_until = now + 0.8
            
        is_active = (now < self.active_hold_until)

        if is_active:
            db = 78
            display = f"{db} dB"
            subtext = "PIN 13 · SOUND PULSE DETECTED"
            status = "NOISE DETECTED"
            color = config.TEXT_PRIMARY
        else:
            db = 42
            display = f"{db} dB"
            subtext = "PIN 13 · AMBIENT NORMAL"
            status = "QUIET"
            color = config.TEXT_SECONDARY

        return {
            "detected": is_active,
            "db": db,
            "display": display,
            "subtext": subtext,
            "status": status,
            "color": color,
            "pin": self.bcm_pin
        }
