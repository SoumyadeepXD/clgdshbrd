import pygame
import config
from ui.glass_ui import draw_glass_panel

class SensorScreen:
    """
    Screen 3: Full-Screen Local Hardware Environment & Room Metrics View.
    Maximized container filling 95% of the display with 3 large glass metric cards.
    """
    def __init__(self, surface: pygame.Surface, fonts: dict):
        self.surface = surface
        self.fonts = fonts

    def draw(self, mq_data: dict, sound_data: dict, humidity_data: dict):
        rect = self.surface.get_rect()
        w, h = rect.width, rect.height
        
        card_w, card_h = int(w * 0.94), int(h * 0.88)
        card_rect = pygame.Rect((w - card_w) // 2, (h - card_h) // 2, card_w, card_h)
        
        draw_glass_panel(self.surface, card_rect, border_radius=int(h * 0.05), bg_alpha=140, border_alpha=35, glow_alpha=100)
        
        title_surf = self.fonts["badge"].render("HARDWARE SENSORS & ROOM TELEMETRY", True, config.TEXT_MUTED)
        self.surface.blit(title_surf, (card_rect.centerx - title_surf.get_width() // 2, card_rect.top + int(card_h * 0.05)))
        
        # 3 Side-by-Side Large Glass Metric Cards
        col_w = int(card_rect.width * 0.29)
        col_h = int(card_rect.height * 0.76)
        gap = int(card_rect.width * 0.03)
        start_x = card_rect.left + (card_rect.width - (col_w * 3 + gap * 2)) // 2
        card_y = card_rect.top + int(card_h * 0.16)
        
        metrics = [
            ("ROOM HUMIDITY (A0)", humidity_data.get('humidity', '--'), humidity_data.get('status', 'COMFORTABLE')),
            ("AIR QUALITY (A1)", f"{mq_data.get('ppm', '--')} PPM", mq_data.get('status', 'GOOD')),
            ("NOISE LEVEL (A3)", f"{sound_data.get('db', '--')} dB", sound_data.get('status', 'NORMAL'))
        ]
        
        for i, (title, main_val, status_val) in enumerate(metrics):
            col_rect = pygame.Rect(start_x + i * (col_w + gap), card_y, col_w, col_h)
            draw_glass_panel(self.surface, col_rect, border_radius=int(col_h * 0.08), bg_alpha=100, border_alpha=30, glow_alpha=60)
            
            t_surf = self.fonts["badge"].render(title, True, config.TEXT_MUTED)
            self.surface.blit(t_surf, (col_rect.centerx - t_surf.get_width() // 2, col_rect.top + int(col_h * 0.08)))
            
            v_surf = self.fonts["heading"].render(str(main_val), True, config.TEXT_PRIMARY)
            self.surface.blit(v_surf, (col_rect.centerx - v_surf.get_width() // 2, col_rect.top + int(col_h * 0.35)))
            
            s_surf = self.fonts["small"].render(str(status_val), True, config.TEXT_SECONDARY)
            self.surface.blit(s_surf, (col_rect.centerx - s_surf.get_width() // 2, col_rect.bottom - int(col_h * 0.20)))
