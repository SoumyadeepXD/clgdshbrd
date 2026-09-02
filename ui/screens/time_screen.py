import time
import datetime
import pygame
import config
from ui.glass_ui import draw_glass_panel

class TimeScreen:
    """
    Screen 1: Time & Date View (10s)
    Clean, minimal, 100% emoji-free typography.
    """
    def __init__(self, surface: pygame.Surface, fonts: dict):
        self.surface = surface
        self.fonts = fonts

    def draw(self, mq_data: dict, sound_data: dict):
        rect = self.surface.get_rect()
        
        card_w, card_h = 640, 320
        card_rect = pygame.Rect((rect.width - card_w) // 2, (rect.height - card_h) // 2, card_w, card_h)
        
        # Centered Frosted Glass Panel
        draw_glass_panel(self.surface, card_rect, border_radius=28, bg_alpha=140, border_alpha=35, glow_alpha=100)
        
        now = datetime.datetime.now()
        
        # Header Label
        lbl_surf = self.fonts["badge"].render("CURRENT TIME", True, config.TEXT_MUTED)
        self.surface.blit(lbl_surf, (card_rect.centerx - lbl_surf.get_width() // 2, card_rect.top + 30))
        
        # Digital Clock (HH:MM:SS)
        time_str = now.strftime("%H:%M:%S")
        time_surf = self.fonts["giant_clock"].render(time_str, True, config.TEXT_PRIMARY)
        self.surface.blit(time_surf, (card_rect.centerx - time_surf.get_width() // 2, card_rect.top + 65))
        
        # Date
        date_str = now.strftime("%A, %d %B %Y").upper()
        date_surf = self.fonts["heading"].render(date_str, True, config.TEXT_SECONDARY)
        self.surface.blit(date_surf, (card_rect.centerx - date_surf.get_width() // 2, card_rect.top + 215))
