import sys
import time
import pygame
import config
from ui.glass_ui import draw_ambient_background
from .screens import TimeScreen, WeatherScreen, SensorScreen

class DisplayManager:
    """
    3-Screen Rotating Minimalist Glassmorphism UI Manager:
    1. Time & Date (10s)
    2. Weather of Kolkata (New Town) (10s)
    3. Noise, Room Humidity & Air Quality AQI (10s)
    
    100% Emoji-Free typography for clean font rendering across all platforms.
    """
    def __init__(self, sensor_mq, sensor_sound, weather_service):
        pygame.init()
        if hasattr(pygame, 'font') and not pygame.font.get_init():
            pygame.font.init()
        
        self.mq = sensor_mq
        self.sound = sensor_sound
        self.weather = weather_service
        
        flags = pygame.FULLSCREEN if config.FULLSCREEN else pygame.RESIZABLE
        self.surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), flags)
        pygame.display.set_caption("Pi Dashboard - Kolkata New Town")
        
        if config.FULLSCREEN:
            pygame.mouse.set_visible(False)
            
        self.clock = pygame.time.Clock()
        self.running = True
        
        font_name = pygame.font.get_default_font()
        self.fonts = {
            "giant_clock": pygame.font.Font(font_name, 100),
            "heading": pygame.font.Font(font_name, 22),
            "subhead": pygame.font.Font(font_name, 16),
            "small": pygame.font.Font(font_name, 13),
            "badge": pygame.font.Font(font_name, 11)
        }
        
        self.time_screen = TimeScreen(self.surface, self.fonts)
        self.weather_screen = WeatherScreen(self.surface, self.fonts)
        self.sensor_screen = SensorScreen(self.surface, self.fonts)
        
        self.screens = ["TIME", "WEATHER", "SENSORS"]
        self.current_screen_idx = 0
        self.screen_switch_time = time.time()

    def run(self):
        while self.running:
            self._handle_events()
            self._update_rotation()
            self._render()
            self.clock.tick(config.FPS)
            
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    self.running = False
                elif event.key in (pygame.K_SPACE, pygame.K_RIGHT):
                    self._next_screen()
                elif event.key == pygame.K_LEFT:
                    self._prev_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._next_screen()

    def _next_screen(self):
        self.current_screen_idx = (self.current_screen_idx + 1) % len(self.screens)
        self.screen_switch_time = time.time()

    def _prev_screen(self):
        self.current_screen_idx = (self.current_screen_idx - 1) % len(self.screens)
        self.screen_switch_time = time.time()

    def _update_rotation(self):
        elapsed = time.time() - self.screen_switch_time
        if elapsed >= config.ROTATION_INTERVAL:
            self._next_screen()

    def _render(self):
        # Render Ambient Glass Background
        draw_ambient_background(self.surface)
        
        mq_data = self.mq.get_readings()
        sound_data = self.sound.get_readings()
        weather_data = self.weather.get_weather()
        
        # 3-Screen Rotation
        active_screen = self.screens[self.current_screen_idx]
        if active_screen == "TIME":
            self.time_screen.draw(mq_data, sound_data)
        elif active_screen == "WEATHER":
            self.weather_screen.draw(weather_data)
        elif active_screen == "SENSORS":
            self.sensor_screen.draw(mq_data, sound_data, weather_data)
            
        # Subtle 2px Top Timer Progress Line
        w, _ = self.surface.get_size()
        elapsed = time.time() - self.screen_switch_time
        progress = min(1.0, max(0.0, elapsed / config.ROTATION_INTERVAL))
        pygame.draw.rect(self.surface, (255, 255, 255, 140), (0, 0, int(w * progress), 2))
        
        pygame.display.flip()
