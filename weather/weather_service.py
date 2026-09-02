import time
import json
import threading
import urllib.request
import urllib.parse
import config

WMO_WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Moderate Showers",
    82: "Violent Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Hail",
    99: "Heavy Thunderstorm"
}

class WeatherService:
    """
    Fetches real-time weather forecasts for Kolkata New Town from Open-Meteo REST API.
    100% Emoji-free for crisp, clean font rendering on any OS.
    """
    def __init__(self, lat=config.WEATHER_LATITUDE, lon=config.WEATHER_LONGITUDE, city=config.WEATHER_CITY_NAME):
        self.lat = lat
        self.lon = lon
        self.city = city
        self.lock = threading.Lock()
        
        self.data = {
            "city": self.city,
            "temp": "--",
            "humidity": "--",
            "wind": "--",
            "condition": "Loading...",
            "temp_max": "--",
            "temp_min": "--",
            "last_updated": "Never"
        }
        
        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def get_weather(self) -> dict:
        """Returns thread-safe copy of latest weather data."""
        with self.lock:
            return dict(self.data)

    def _update_loop(self):
        while self.running:
            try:
                self._fetch_weather()
            except Exception as e:
                print(f"[WeatherService] Error fetching weather: {e}")
            time.sleep(config.WEATHER_UPDATE_INTERVAL)

    def _fetch_weather(self):
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={self.lat}&longitude={self.lon}"
            f"&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            f"&daily=temperature_2m_max,temperature_2m_min,weather_code"
            f"&timezone=auto"
        )
        
        req = urllib.request.Request(url, headers={"User-Agent": "RaspberryPiDashboard/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                raw_json = json.loads(response.read().decode("utf-8"))
                current = raw_json.get("current", {})
                daily = raw_json.get("daily", {})
                
                temp = round(current.get("temperature_2m", 0.0), 1)
                humidity = int(current.get("relative_humidity_2m", 0))
                wind = round(current.get("wind_speed_10m", 0.0), 1)
                w_code = int(current.get("weather_code", 0))
                
                condition = WMO_WEATHER_CODES.get(w_code, "Clear")
                
                temp_max = round(daily.get("temperature_2m_max", [temp])[0], 1) if "temperature_2m_max" in daily else temp
                temp_min = round(daily.get("temperature_2m_min", [temp])[0], 1) if "temperature_2m_min" in daily else temp
                
                with self.lock:
                    self.data = {
                        "city": self.city,
                        "temp": f"{temp}°C",
                        "humidity": f"{humidity}%",
                        "wind": f"{wind} km/h",
                        "condition": condition,
                        "temp_max": f"{temp_max}°C",
                        "temp_min": f"{temp_min}°C",
                        "last_updated": time.strftime("%H:%M")
                    }
                print(f"[WeatherService] Weather updated for {self.city}: {temp}°C, {condition}")

    def stop(self):
        self.running = False
