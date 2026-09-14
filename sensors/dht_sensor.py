import time
import math
import config

class DHTSensor:
    """
    Driver for DHT11 / DHT22 (AM2302) Temperature and Humidity Sensor
    connected directly to Raspberry Pi GPIO (default GPIO 4).
    Includes rate-limiting (2s cache), transient error handling, and mock fallback.
    """
    def __init__(self, pin: int = config.DHT_PIN, sensor_type: int = config.DHT_TYPE, force_mock: bool = config.FORCE_MOCK_SENSORS):
        self.pin = pin
        self.sensor_type = sensor_type
        self.is_mock = force_mock
        
        self.bcm_pin = self._resolve_pin(self.pin)
        self.device = None
        self.last_read_time = 0.0
        self.poll_interval = 2.0
        
        self.last_temp = 25.0
        self.last_humidity = 55
        self.last_status = "COMFORTABLE"
        
        if not self.is_mock:
            self._init_hardware()

    def _resolve_pin(self, pin: int) -> int:
        if getattr(config, "USE_PHYSICAL_PINS", False):
            mapping = {7: 4, 11: 17, 13: 27}
            return mapping.get(pin, pin)
        return pin

    def _init_hardware(self):
        try:
            import board
            import adafruit_dht
            
            pin_attr = f"D{self.bcm_pin}"
            if hasattr(board, pin_attr):
                pin_obj = getattr(board, pin_attr)
            else:
                import microcontroller
                pin_obj = microcontroller.pin.__dict__.get(f"GPIO{self.bcm_pin}")
                
            if self.sensor_type == 22:
                self.device = adafruit_dht.DHT22(pin_obj)
                print(f"[DHTSensor] Physical DHT22 initialized on GPIO {self.bcm_pin}.")
            else:
                self.device = adafruit_dht.DHT11(pin_obj)
                print(f"[DHTSensor] Physical DHT11 initialized on GPIO {self.bcm_pin}.")
        except Exception as e:
            print(f"[DHTSensor] Hardware DHT not available ({e}). Using MOCK SENSOR MODE.")
            self.is_mock = True

    def get_readings(self) -> dict:
        now = time.time()
        
        if not self.is_mock and self.device and (now - self.last_read_time >= self.poll_interval):
            self.last_read_time = now
            try:
                temp = self.device.temperature
                humidity = self.device.humidity
                if temp is not None and humidity is not None:
                    self.last_temp = round(float(temp), 1)
                    self.last_humidity = int(max(5, min(99, humidity)))
            except RuntimeError:
                pass
            except Exception as e:
                print(f"[DHTSensor] Error reading DHT on GPIO {self.bcm_pin}: {e}")

        elif self.is_mock:
            self.last_temp = round(24.5 + 2.0 * math.sin(now / 30.0), 1)
            self.last_humidity = int(max(10, min(90, 54.0 + 8.0 * math.sin(now / 20.0))))

        if self.last_humidity < 35:
            comfort = "DRY"
        elif self.last_humidity <= 65:
            comfort = "COMFORTABLE"
        else:
            comfort = "HUMID"
            
        subtext = f"{self.last_temp}°C  ·  GPIO {self.bcm_pin}  ·  {comfort}"

        return {
            "humidity": self.last_humidity,
            "humidity_str": f"{self.last_humidity}%",
            "temp": self.last_temp,
            "temp_str": f"{self.last_temp}°C",
            "display": f"{self.last_humidity}%",
            "subtext": subtext,
            "status": comfort
        }
