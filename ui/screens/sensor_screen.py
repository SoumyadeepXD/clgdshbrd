import pygame
import config
from ui.glass_ui import draw_glass_panel

class SensorScreen:
    """
    Screen 3: Full-Screen Local Hardware Environment & Room Metrics View.
    Displays 3 large frosted glass cards for GPIO Hardware Sensors:
    1. DHT Sensor (GPIO 4) - Temperature & Humidity
    2. Smoke Sensor (Pin 11) - Digital Smoke / Gas Detector
    3. Mic Sensor (Pin 13) - Digital Microphone / Sound Sensor
    """
    def __init__(self, surface: pygame.Surface, fonts: dict):
        self.surface = surface
        self.fonts = fonts

    def draw(self, smoke_data: dict = None, mic_data: dict = None, dht_data: dict = None, **kwargs):
        rect = self.surface.get_rect()
        w, h = rect.width, rect.height
        
        card_w, card_h = int(w * 0.94), int(h * 0.88)
        card_rect = pygame.Rect((w - card_w) // 2, (h - card_h) // 2, card_w, card_h)
        
        draw_glass_panel(self.surface, card_rect, border_radius=int(h * 0.05), bg_alpha=140, border_alpha=35, glow_alpha=100)
        
        title_surf = self.fonts["badge"].render("HARDWARE GPIO SENSORS & ROOM TELEMETRY", True, config.TEXT_MUTED)
        self.surface.blit(title_surf, (card_rect.centerx - title_surf.get_width() // 2, card_rect.top + int(card_h * 0.05)))
        
        # Smart argument resolution to support any caller signature
        data_list = [d for d in (smoke_data, mic_data, dht_data) if isinstance(d, dict)]
        dht = next((d for d in data_list if 'humidity' in d or 'temp' in d), dht_data or kwargs.get('humidity_data', {}))
        smoke = next((d for d in data_list if ('detected' in d and d.get('pin') == config.SMOKE_PIN) or 'ppm' in d), smoke_data or kwargs.get('mq_data', {}))
        mic = next((d for d in data_list if ('detected' in d and d.get('pin') == config.MIC_PIN) or 'db' in d), mic_data or kwargs.get('sound_data', {}))

        # Fallback if unassigned
        if not dht:
            dht = dht_data or {}
        if not smoke:
            smoke = smoke_data or {}
        if not mic:
            mic = mic_data or {}

        # 3 Side-by-Side Large Glass Metric Cards
        col_w = int(card_rect.width * 0.29)
        col_h = int(card_rect.height * 0.76)
        gap = int(card_rect.width * 0.03)
        start_x = card_rect.left + (card_rect.width - (col_w * 3 + gap * 2)) // 2
        card_y = card_rect.top + int(card_h * 0.16)
        
        dht_val = dht.get('display', f"{dht.get('humidity', '--')}%")
        dht_status = dht.get('status', 'COMFORTABLE')
        dht_color = dht.get('color', config.TEXT_PRIMARY)

        smoke_val = smoke.get('display', smoke.get('status', 'CLEAR'))
        smoke_subtext = smoke.get('subtext', 'AIR CLEAN')
        smoke_color = smoke.get('color', config.TEXT_PRIMARY)

        mic_val = mic.get('display', mic.get('status', 'QUIET'))
        mic_subtext = mic.get('subtext', 'AMBIENT NORMAL')
        mic_color = mic.get('color', config.TEXT_PRIMARY)

        metrics = [
            (f"DHT SENSOR (GPIO {config.DHT_PIN})", dht_val, dht_status, dht_color),
            (f"SMOKE SENSOR (PIN {config.SMOKE_PIN})", smoke_val, smoke_subtext, smoke_color),
            (f"MIC SENSOR (PIN {config.MIC_PIN})", mic_val, mic_subtext, mic_color)
        ]
        
        for i, (col_title, main_val, status_val, val_color) in enumerate(metrics):
            col_rect = pygame.Rect(start_x + i * (col_w + gap), card_y, col_w, col_h)
            draw_glass_panel(self.surface, col_rect, border_radius=int(col_h * 0.08), bg_alpha=100, border_alpha=30, glow_alpha=60)
            
            # Metric Card Title Badge
            t_surf = self.fonts["badge"].render(col_title, True, config.TEXT_MUTED)
            self.surface.blit(t_surf, (col_rect.centerx - t_surf.get_width() // 2, col_rect.top + int(col_h * 0.08)))
            
            # Big Value Typography
            v_surf = self.fonts["heading"].render(str(main_val), True, val_color)
            self.surface.blit(v_surf, (col_rect.centerx - v_surf.get_width() // 2, col_rect.top + int(col_h * 0.35)))
            
            # Status / Subtext
            s_surf = self.fonts["small"].render(str(status_val), True, config.TEXT_SECONDARY)
            self.surface.blit(s_surf, (col_rect.centerx - s_surf.get_width() // 2, col_rect.bottom - int(col_h * 0.20)))
