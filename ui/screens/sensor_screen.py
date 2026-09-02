import pygame
import config
from ui.glass_ui import draw_glass_panel

class SensorScreen:
    """
    Screen 3: Noise Level, Room Humidity & Air Quality (AQI / PPM) View (10s)
    Clean, minimal, 100% emoji-free typography.
    """
    def __init__(self, surface: pygame.Surface, fonts: dict):
        self.surface = surface
        self.fonts = fonts

    def draw(self, mq_data: dict, sound_data: dict, weather_data: dict):
        rect = self.surface.get_rect()
        
        card_w, card_h = 660, 320
        card_rect = pygame.Rect((rect.width - card_w) // 2, (rect.height - card_h) // 2, card_w, card_h)
        
        # Main Frosted Glass Panel
        draw_glass_panel(self.surface, card_rect, border_radius=28, bg_alpha=140, border_alpha=35, glow_alpha=100)
        
        # Title Header
        title_surf = self.fonts["badge"].render("ENVIRONMENT & ROOM METRICS", True, config.TEXT_MUTED)
        self.surface.blit(title_surf, (card_rect.centerx - title_surf.get_width() // 2, card_rect.top + 25))
        
        # 3 Side-by-Side Glass Metric Cards
        col_w = 185
        col_h = 210
        gap = 20
        start_x = card_rect.left + (card_rect.width - (col_w * 3 + gap * 2)) // 2
        card_y = card_rect.top + 65
        
        metrics = [
            ("NOISE LEVEL", f"{sound_data.get('db', '--')} dB", sound_data.get('status', 'NORMAL')),
            ("HUMIDITY", weather_data.get('humidity', '--'), "ROOM AMBIENT"),
            ("AIR QUALITY", f"{mq_data.get('ppm', '--')} PPM", mq_data.get('status', 'GOOD'))
        ]
        
        for i, (title, main_val, status_val) in enumerate(metrics):
            col_rect = pygame.Rect(start_x + i * (col_w + gap), card_y, col_w, col_h)
            draw_glass_panel(self.surface, col_rect, border_radius=18, bg_alpha=100, border_alpha=30, glow_alpha=60)
            
            # Label
            t_surf = self.fonts["badge"].render(title, True, config.TEXT_MUTED)
            self.surface.blit(t_surf, (col_rect.centerx - t_surf.get_width() // 2, col_rect.top + 20))
            
            # Value
            v_surf = self.fonts["heading"].render(str(main_val), True, config.TEXT_PRIMARY)
            self.surface.blit(v_surf, (col_rect.centerx - v_surf.get_width() // 2, col_rect.top + 75))
            
            # Status
            s_surf = self.fonts["small"].render(str(status_val), True, config.TEXT_SECONDARY)
            self.surface.blit(s_surf, (col_rect.centerx - s_surf.get_width() // 2, col_rect.bottom - 40))
