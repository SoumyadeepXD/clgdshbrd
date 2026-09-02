import pygame
import config
from ui.glass_ui import draw_glass_panel

class WeatherScreen:
    """
    Screen 2: Weather of Kolkata (New Town) View (10s)
    Clean, minimal, 100% emoji-free typography.
    """
    def __init__(self, surface: pygame.Surface, fonts: dict):
        self.surface = surface
        self.fonts = fonts

    def draw(self, weather_data: dict):
        rect = self.surface.get_rect()
        
        card_w, card_h = 640, 320
        card_rect = pygame.Rect((rect.width - card_w) // 2, (rect.height - card_h) // 2, card_w, card_h)
        
        # Centered Frosted Glass Panel
        draw_glass_panel(self.surface, card_rect, border_radius=28, bg_alpha=140, border_alpha=35, glow_alpha=100)
        
        # Location Label
        city_str = str(weather_data.get('city', 'KOLKATA (NEW TOWN)')).upper()
        city_surf = self.fonts["badge"].render(city_str, True, config.TEXT_MUTED)
        self.surface.blit(city_surf, (card_rect.centerx - city_surf.get_width() // 2, card_rect.top + 30))
        
        # Temperature
        temp_str = str(weather_data.get("temp", "--"))
        temp_surf = self.fonts["giant_clock"].render(temp_str, True, config.TEXT_PRIMARY)
        self.surface.blit(temp_surf, (card_rect.centerx - temp_surf.get_width() // 2, card_rect.top + 60))
        
        # Condition Description
        cond_str = str(weather_data.get('condition', 'CLEAR')).upper()
        cond_surf = self.fonts["heading"].render(cond_str, True, config.TEXT_SECONDARY)
        self.surface.blit(cond_surf, (card_rect.centerx - cond_surf.get_width() // 2, card_rect.top + 205))
        
        # High / Low Range
        hi_lo_str = f"HIGH {weather_data.get('temp_max', '--')}   ·   LOW {weather_data.get('temp_min', '--')}"
        hi_lo_surf = self.fonts["small"].render(hi_lo_str, True, config.TEXT_MUTED)
        self.surface.blit(hi_lo_surf, (card_rect.centerx - hi_lo_surf.get_width() // 2, card_rect.top + 250))
