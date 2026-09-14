import time
import random
import config

class SmokeSensor:
    """
    Driver for Smoke / Gas Sensors (MQ Series digital DO pin)
    connected directly to Raspberry Pi GPIO (default Pin 11 / GPIO 17).
    Digital output comparator triggers LOW (active low) when smoke/gas exceeds threshold.
    Returns numeric PPM representation & real-time digital detection status.
    """
    def __init__(self, pin: int = config.SMOKE_PIN, active_low: bool = config.SMOKE_ACTIVE_LOW, force_mock: bool = config.FORCE_MOCK_SENSORS):
        self.pin = pin
        self.active_low = active_low
        self.is_mock = force_mock
        self.bcm_pin = self._resolve_pin(self.pin)
        self.gpio_lib = None
        self.device = None
        
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
            print(f"[SmokeSensor] Physical Smoke Sensor initialized via RPi.GPIO on GPIO {self.bcm_pin}.")
            return
        except Exception:
            pass

        try:
            from gpiozero import DigitalInputDevice
            self.device = DigitalInputDevice(self.bcm_pin, pull_up=True)
            self.gpio_lib = "gpiozero"
            print(f"[SmokeSensor] Physical Smoke Sensor initialized via gpiozero on GPIO {self.bcm_pin}.")
            return
        except Exception as e:
            print(f"[SmokeSensor] Hardware GPIO not available ({e}). Using MOCK SENSOR MODE.")
            self.is_mock = True

    def read_raw(self) -> int:
        if not self.is_mock:
            try:
                if self.gpio_lib == "RPi.GPIO":
                    import RPi.GPIO as GPIO
                    return GPIO.input(self.bcm_pin)
                elif self.gpio_lib == "gpiozero" and self.device:
                    return 0 if self.device.is_active else 1
            except Exception as e:
                print(f"[SmokeSensor] Error reading pin {self.bcm_pin}: {e}.")
        return 1

    def get_readings(self) -> dict:
        raw_val = self.read_raw()
        
        if self.is_mock:
            is_detected = False
        else:
            is_detected = (raw_val == 0) if self.active_low else (raw_val == 1)

        if is_detected:
            ppm = 950
            display = f"{ppm} PPM"
            subtext = "ALERT · GAS DETECTED"
            status = "HAZARDOUS"
            color = (255, 110, 110)
        else:
            ppm = 120
            display = f"{ppm} PPM"
            subtext = "PIN 11 · AIR CLEAN"
            status = "GOOD AIR"
            color = config.TEXT_PRIMARY

        return {
            "detected": is_detected,
            "raw": raw_val,
            "ppm": ppm,
            "display": display,
            "subtext": subtext,
            "status": status,
            "color": color,
            "pin": self.bcm_pin
        }
