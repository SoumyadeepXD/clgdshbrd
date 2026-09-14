import pygame
import config
from ui.glass_ui import draw_glass_panel

class SensorScreen:
    """
    Screen 3: Full-Screen Local Hardware Environment & Room Metrics View.
    Maximized container displaying 3 large glass metric cards with GIANT BOLD numeric readouts:
    1. Local Room Humidity (% RH)
    2. Air Quality AQI / Smoke (PPM)
    3. Sound & Noise Level (dB)
    """
    def __init__(self, surface: pygame.Surface, fonts: dict):
        self.surface = surface
        self.fonts = fonts

    def draw(self, mq_data: dict = None, sound_data: dict = None, humidity_data: dict = None,
             smoke_data: dict = None, mic_data: dict = None, dht_data: dict = None, **kwargs):
        rect = self.surface.get_rect()
        w, h = rect.width, rect.height
        
        card_w, card_h = int(w * 0.94), int(h * 0.88)
        card_rect = pygame.Rect((w - card_w) // 2, (h - card_h) // 2, card_w, card_h)
        
        draw_glass_panel(self.surface, card_rect, border_radius=int(h * 0.05), bg_alpha=140, border_alpha=35, glow_alpha=100)
        
        title_surf = self.fonts["badge"].render("REAL-TIME HARDWARE SENSORS TELEMETRY", True, config.TEXT_MUTED)
        self.surface.blit(title_surf, (card_rect.centerx - title_surf.get_width() // 2, card_rect.top + int(card_h * 0.05)))
        
        # Smart Dictionary Resolver to handle ADC sensors or direct GPIO sensors
        hum = humidity_data or dht_data or kwargs.get('sensor_dht', {}) or {}
        mq = mq_data or smoke_data or kwargs.get('sensor_smoke', {}) or {}
        snd = sound_data or mic_data or kwargs.get('sensor_mic', {}) or {}

        # 1. Humidity Display (Numeric %)
        hum_num = hum.get('display', f"{hum.get('humidity', '--')}%")
        if not str(hum_num).endswith('%') and hum_num != '--':
            hum_num = f"{hum_num}%"
        hum_sub = hum.get('subtext', f"{hum.get('status', 'COMFORTABLE')}")

        # 2. Air Quality / MQ Display (Numeric PPM)
        mq_num = mq.get('display', f"{mq.get('ppm', '--')} PPM")
        mq_sub = mq.get('subtext', f"{mq.get('status', 'GOOD')}")

        # 3. Sound / Mic Display (Numeric dB)
        snd_num = snd.get('display', f"{snd.get('db', '--')} dB")
        snd_sub = snd.get('subtext', f"{snd.get('status', 'QUIET')}")

        # 3 Side-by-Side Large Glass Metric Cards
        col_w = int(card_rect.width * 0.29)
        col_h = int(card_rect.height * 0.76)
        gap = int(card_rect.width * 0.03)
        start_x = card_rect.left + (card_rect.width - (col_w * 3 + gap * 2)) // 2
        card_y = card_rect.top + int(card_h * 0.16)
        
        metrics = [
            ("ROOM HUMIDITY", hum_num, hum_sub),
            ("AIR QUALITY (AQI)", mq_num, mq_sub),
            ("NOISE LEVEL", snd_num, snd_sub)
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
            
            # Secondary Subtext Status
            s_surf = self.fonts["small"].render(str(subtext_val), True, config.TEXT_SECONDARY)
            self.surface.blit(s_surf, (col_rect.centerx - s_surf.get_width() // 2, col_rect.bottom - int(col_h * 0.20)))
