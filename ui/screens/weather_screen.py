import pygame
import config
from ui.glass_ui import draw_glass_panel

class WeatherScreen:
    """
    Screen 2: Weather of Kolkata (New Town) View.
    Fully responsive layout scaling proportionally to any display resolution.
    """
    def __init__(self, surface: pygame.Surface, fonts: dict):
        self.surface = surface
        self.fonts = fonts

    def draw(self, weather_data: dict):
        rect = self.surface.get_rect()
        w, h = rect.width, rect.height
        
        card_w, card_h = int(w * 0.84), int(h * 0.68)
        card_rect = pygame.Rect((w - card_w) // 2, (h - card_h) // 2, card_w, card_h)
        
        draw_glass_panel(self.surface, card_rect, border_radius=int(h * 0.05), bg_alpha=140, border_alpha=35, glow_alpha=100)
        
        # Location Label
        city_str = str(weather_data.get('city', 'KOLKATA (NEW TOWN)')).upper()
        city_surf = self.fonts["badge"].render(city_str, True, config.TEXT_MUTED)
        self.surface.blit(city_surf, (card_rect.centerx - city_surf.get_width() // 2, card_rect.top + int(card_h * 0.08)))
        
        # Giant Responsive Temperature
        temp_str = str(weather_data.get("temp", "--"))
        temp_surf = self.fonts["giant_clock"].render(temp_str, True, config.TEXT_PRIMARY)
        self.surface.blit(temp_surf, (card_rect.centerx - temp_surf.get_width() // 2, card_rect.top + int(card_h * 0.18)))
        
        # Condition Description
        cond_str = str(weather_data.get('condition', 'CLEAR')).upper()
        cond_surf = self.fonts["heading"].render(cond_str, True, config.TEXT_SECONDARY)
        self.surface.blit(cond_surf, (card_rect.centerx - cond_surf.get_width() // 2, card_rect.top + int(card_h * 0.65)))
        
        # High / Low Range
        hi_lo_str = f"HIGH {weather_data.get('temp_max', '--')}   ·   LOW {weather_data.get('temp_min', '--')}"
        hi_lo_surf = self.fonts["small"].render(hi_lo_str, True, config.TEXT_MUTED)
        self.surface.blit(hi_lo_surf, (card_rect.centerx - hi_lo_surf.get_width() // 2, card_rect.top + int(card_h * 0.80)))
