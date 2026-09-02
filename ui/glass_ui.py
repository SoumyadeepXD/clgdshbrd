import pygame
import config

def draw_ambient_background(surface: pygame.Surface):
    """
    Renders a deep dark background with soft ambient light gradients that shine
    through translucent glass panels.
    """
    w, h = surface.get_size()
    
    # Base Deep Canvas (#0B0F17)
    surface.fill((11, 15, 23))
    
    # Ambient Light Orbs (Pre-rendered translucent glow shapes)
    glow_top_left = pygame.Surface((350, 350), pygame.SRCALPHA)
    for r in range(175, 0, -5):
        alpha = int(12 * (r / 175))
        pygame.draw.circle(glow_top_left, (70, 90, 130, alpha), (175, 175), r)
    surface.blit(glow_top_left, (-80, -80))
    
    glow_bottom_right = pygame.Surface((400, 400), pygame.SRCALPHA)
    for r in range(200, 0, -5):
        alpha = int(15 * (r / 200))
        pygame.draw.circle(glow_bottom_right, (90, 110, 150, alpha), (200, 200), r)
    surface.blit(glow_bottom_right, (w - 250, h - 250))

def draw_glass_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    border_radius: int = 20,
    bg_alpha: int = 150,
    border_alpha: int = 50,
    glow_alpha: int = 110
):
    """
    Renders an authentic Glassmorphism panel with RGBA surface blending,
    frosted backdrop transparency, drop shadow, and light-reflecting edges.
    """
    w, h = rect.width, rect.height
    
    # 1. Drop Shadow Surface
    shadow_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 80), (0, 4, w, h - 4), border_radius=border_radius)
    surface.blit(shadow_surf, (rect.left, rect.top + 2))
    
    # 2. Translucent Glass Body Surface
    glass_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(glass_surf, (22, 28, 42, bg_alpha), (0, 0, w, h), border_radius=border_radius)
    
    # 3. Glass Outer Rim (Subtle Translucent White)
    pygame.draw.rect(glass_surf, (255, 255, 255, border_alpha), (0, 0, w, h), width=1, border_radius=border_radius)
    
    # 4. Top & Left Refractive Glass Bevel Highlights
    top_line = pygame.Rect(border_radius, 0, max(1, w - (border_radius * 2)), 1)
    pygame.draw.rect(glass_surf, (255, 255, 255, glow_alpha), top_line)
    
    left_line = pygame.Rect(0, border_radius, 1, max(1, h - (border_radius * 2)))
    pygame.draw.rect(glass_surf, (255, 255, 255, glow_alpha // 2), left_line)
    
    surface.blit(glass_surf, rect.topleft)
