import sys
import time
import pygame
import config
from ui.glass_ui import draw_ambient_background
from .screens import TimeScreen, WeatherScreen, SensorScreen

class DisplayManager:
    """
    3-Screen Rotating Minimalist Glassmorphism UI Manager.
    Automatically detects display resolution and dynamically scales font sizes
    and UI cards so elements fill the screen proportionally on ANY display.
    """
    def __init__(self, sensor_mq, sensor_sound, weather_service):
        pygame.init()
        if hasattr(pygame, 'font') and not pygame.font.get_init():
            pygame.font.init()
        
        self.mq = sensor_mq
        self.sound = sensor_sound
        self.weather = weather_service
        
        flags = pygame.FULLSCREEN if config.FULLSCREEN else pygame.RESIZABLE
        
        # 1. Detect native screen resolution for FULLSCREEN or Windowed mode
        if config.FULLSCREEN:
            info = pygame.display.Info()
            self.width = info.current_w if info.current_w > 0 else config.SCREEN_WIDTH
            self.height = info.current_h if info.current_h > 0 else config.SCREEN_HEIGHT
        else:
            self.width = config.SCREEN_WIDTH
            self.height = config.SCREEN_HEIGHT
            
        self.surface = pygame.display.set_mode((self.width, self.height), flags)
        pygame.display.set_caption("Pi Dashboard")
        
        if config.FULLSCREEN:
            pygame.mouse.set_visible(False)
            
        self.clock = pygame.time.Clock()
        self.running = True
        
        # 2. Dynamic Font Scaling relative to screen height
        font_name = pygame.font.get_default_font()
        clock_sz = int(self.height * 0.28)
        heading_sz = int(self.height * 0.065)
        subhead_sz = int(self.height * 0.045)
        small_sz = int(self.height * 0.035)
        badge_sz = int(self.height * 0.028)
        
        self.fonts = {
            "giant_clock": pygame.font.Font(font_name, max(36, clock_sz)),
            "heading": pygame.font.Font(font_name, max(18, heading_sz)),
            "subhead": pygame.font.Font(font_name, max(14, subhead_sz)),
            "small": pygame.font.Font(font_name, max(12, small_sz)),
            "badge": pygame.font.Font(font_name, max(10, badge_sz))
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
        draw_ambient_background(self.surface)
        
        mq_data = self.mq.get_readings()
        sound_data = self.sound.get_readings()
        weather_data = self.weather.get_weather()
        
        active_screen = self.screens[self.current_screen_idx]
        if active_screen == "TIME":
            self.time_screen.draw(mq_data, sound_data)
        elif active_screen == "WEATHER":
            self.weather_screen.draw(weather_data)
        elif active_screen == "SENSORS":
            self.sensor_screen.draw(mq_data, sound_data, weather_data)
            
        # Responsive 2px Top Progress Line
        w, _ = self.surface.get_size()
        elapsed = time.time() - self.screen_switch_time
        progress = min(1.0, max(0.0, elapsed / config.ROTATION_INTERVAL))
        pygame.draw.rect(self.surface, (255, 255, 255, 140), (0, 0, int(w * progress), 3))
        
        pygame.display.flip()
