import pygame
import config
from ui.glass_ui import draw_glass_panel

class SensorScreen:
    """
    Screen 3: Full-Screen Local Hardware Environment & Room Metrics View.
    Maximized container displaying 3 large glass metric cards with GIANT BOLD numeric readouts:
    1. Local Room Humidity (A0): e.g. 58%
    2. Air Quality AQI (A1): e.g. 145 PPM
    3. Noise Level (A3): e.g. 58 dB
    """
    def __init__(self, surface: pygame.Surface, fonts: dict):
        self.surface = surface
        self.fonts = fonts

    def draw(self, mq_data: dict = None, sound_data: dict = None, humidity_data: dict = None, **kwargs):
        rect = self.surface.get_rect()
        w, h = rect.width, rect.height
        
        card_w, card_h = int(w * 0.94), int(h * 0.88)
        card_rect = pygame.Rect((w - card_w) // 2, (h - card_h) // 2, card_w, card_h)
        
        draw_glass_panel(self.surface, card_rect, border_radius=int(h * 0.05), bg_alpha=140, border_alpha=35, glow_alpha=100)
        
        title_surf = self.fonts["badge"].render("REAL-TIME HARDWARE SENSORS TELEMETRY", True, config.TEXT_MUTED)
        self.surface.blit(title_surf, (card_rect.centerx - title_surf.get_width() // 2, card_rect.top + int(card_h * 0.05)))
        
        # Support both current sensor dictionary names and kwargs fallback
        hum = humidity_data or kwargs.get('dht_data', {}) or {}
        mq = mq_data or kwargs.get('smoke_data', {}) or {}
        snd = sound_data or kwargs.get('mic_data', {}) or {}

        # Extract numeric display strings
        hum_num = hum.get('display', f"{hum.get('humidity', '--')}")
        if not str(hum_num).endswith('%') and hum_num != '--':
            hum_num = f"{hum_num}%"
        hum_sub = hum.get('subtext', f"{hum.get('voltage', '--')}V  ·  {hum.get('status', 'NORMAL')}")

        mq_num = mq.get('display', f"{mq.get('ppm', '--')} PPM")
        mq_sub = mq.get('subtext', f"{mq.get('voltage', '--')}V  ·  {mq.get('status', 'GOOD')}")

        snd_num = snd.get('display', f"{snd.get('db', '--')} dB")
        snd_sub = snd.get('subtext', f"{snd.get('voltage', '--')}V  ·  {snd.get('status', 'QUIET')}")

        # 3 Side-by-Side Large Glass Metric Cards
        col_w = int(card_rect.width * 0.29)
        col_h = int(card_rect.height * 0.76)
        gap = int(card_rect.width * 0.03)
        start_x = card_rect.left + (card_rect.width - (col_w * 3 + gap * 2)) // 2
        card_y = card_rect.top + int(card_h * 0.16)
        
        metrics = [
            (f"ROOM HUMIDITY (A0)", hum_num, hum_sub),
            (f"AIR QUALITY (A1)", mq_num, mq_sub),
            (f"NOISE LEVEL (A3)", snd_num, snd_sub)
        ]
        
        for i, (col_title, num_val, subtext_val) in enumerate(metrics):
            col_rect = pygame.Rect(start_x + i * (col_w + gap), card_y, col_w, col_h)
            draw_glass_panel(self.surface, col_rect, border_radius=int(col_h * 0.08), bg_alpha=100, border_alpha=30, glow_alpha=60)
            
            # Metric Card Title Badge
            t_surf = self.fonts["badge"].render(col_title, True, config.TEXT_MUTED)
            self.surface.blit(t_surf, (col_rect.centerx - t_surf.get_width() // 2, col_rect.top + int(col_h * 0.08)))
            
            # Giant Bold Numeric Reading
            v_surf = self.fonts["heading"].render(str(num_val), True, config.TEXT_PRIMARY)
            self.surface.blit(v_surf, (col_rect.centerx - v_surf.get_width() // 2, col_rect.top + int(col_h * 0.32)))
            
            # Secondary Subtext Status & Voltage
            s_surf = self.fonts["small"].render(str(subtext_val), True, config.TEXT_SECONDARY)
            self.surface.blit(s_surf, (col_rect.centerx - s_surf.get_width() // 2, col_rect.bottom - int(col_h * 0.20)))
