"""픽셀 스타일 그리기 유틸."""
import math
import random
import pygame
from game.config import (
    OFF_WHITE, WHITE, LIGHT_GRAY, BRIGHT_RED, RED, DARK_RED,
    GREEN, BRIGHT_GREEN, DARK_GREEN, YELLOW, BRIGHT_YELLOW,
    LIGHT_CYAN, CYAN,
)

def draw_pixel_bobber(surface, x, y, submerged=False):
    p = 2
    if not submerged:
        pygame.draw.rect(surface, OFF_WHITE,   (x - 3*p, y - 10*p, 6*p, 3*p))
        pygame.draw.rect(surface, WHITE,       (x - 2*p, y - 11*p, 4*p, p))
        pygame.draw.rect(surface, LIGHT_GRAY,  (x - 3*p, y - 7*p,  6*p, p))
        pygame.draw.rect(surface, BRIGHT_RED,  (x - 4*p, y - 6*p,  8*p, 2*p))
        pygame.draw.rect(surface, RED,         (x - 5*p, y - 4*p, 10*p, 6*p))
        pygame.draw.rect(surface, DARK_RED,    (x - 4*p, y + 2*p,  8*p, 3*p))
        pygame.draw.rect(surface, DARK_RED,    (x - 3*p, y + 5*p,  6*p, 2*p))
        pygame.draw.rect(surface, BRIGHT_RED,  (x - 3*p, y - 4*p,  2*p, 4*p))
    else:
        pygame.draw.rect(surface, (180, 80, 80), (x - 3*p, y - 2*p, 6*p, 4*p))


def draw_pixel_fishing_line(surface, start, end, tension=0):
    x1, y1 = start
    x2, y2 = end
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2 + tension
    points = []
    for t in range(21):
        t = t / 20
        px = (1-t)**2 * x1 + 2*(1-t)*t * mid_x + t**2 * x2
        py = (1-t)**2 * y1 + 2*(1-t)*t * mid_y + t**2 * y2
        points.append((int(px), int(py)))
    for i in range(len(points) - 1):
        pygame.draw.line(surface, LIGHT_GRAY, points[i], points[i+1], 2)
        pygame.draw.line(surface, WHITE, (points[i][0], points[i][1]-1),
                         (points[i+1][0], points[i+1][1]-1), 1)


def draw_pixel_cylinder(surface, x, y, width, height):
    p = 2
    pygame.draw.rect(surface, (20, 50, 100), (x - p*2, y - p*2, width + p*4, height + p*4))
    for i in range(0, height, p*4):
        ratio = i / height
        r = int(35 + ratio * 15)
        g = int(100 - ratio * 30)
        b = int(170 - ratio * 30)
        pygame.draw.rect(surface, (r, g, b), (x, y + i, width, p*4))
    wave_time = pygame.time.get_ticks() / 500
    for wy in range(0, height, p*8):
        wave_offset = int(math.sin(wave_time + wy / 20) * p)
        pygame.draw.rect(surface, (50, 120, 190), (x + wave_offset, y + wy, p*2, p*4))
        pygame.draw.rect(surface, (50, 120, 190), (x + width - p*4 + wave_offset, y + wy + p*4, p*2, p*4))
    pygame.draw.rect(surface, (80, 150, 210), (x, y, p*2, height))
    pygame.draw.rect(surface, (20, 60, 120),  (x + width - p*2, y, p*2, height))
    pygame.draw.rect(surface, (60, 90, 140),  (x - p, y - p, width + p*2, p*2))
    pygame.draw.rect(surface, (60, 90, 140),  (x - p, y + height - p, width + p*2, p*2))


def draw_pixel_bar(surface, x, y, width, height, active=False):
    p = 2
    if active:
        main_color  = BRIGHT_GREEN
        light_color = (150, 255, 180)
        dark_color  = DARK_GREEN
    else:
        main_color  = (80, 160, 100)
        light_color = (120, 200, 140)
        dark_color  = (50, 120, 70)
    pygame.draw.rect(surface, main_color,  (x, y, width, height))
    pygame.draw.rect(surface, light_color, (x, y, width, p*2))
    pygame.draw.rect(surface, light_color, (x, y, p*2, height))
    pygame.draw.rect(surface, dark_color,  (x, y + height - p*2, width, p*2))
    pygame.draw.rect(surface, dark_color,  (x + width - p*2, y, p*2, height))
    for py in range(p*4, height - p*4, p*6):
        pygame.draw.rect(surface, light_color, (x + p*4, y + py, width - p*8, p))


def draw_splash_particle(surface, particles):
    for p in particles:
        size = int(p['size'] * p['life'])
        if size > 0:
            pygame.draw.circle(surface, LIGHT_CYAN, (int(p['x']), int(p['y'])), size + 1)
            pygame.draw.circle(surface, CYAN,       (int(p['x']), int(p['y'])), size)
            if size > 2:
                pygame.draw.circle(surface, WHITE, (int(p['x']) - 1, int(p['y']) - 1), size // 2)


def draw_pixel_button(surface, rect, text, font, hovered=False, is_main=False):
    x, y, w, h = rect.x, rect.y, rect.width, rect.height
    B = 4
    if is_main:
        base  = (80, 200, 80)  if hovered else (60, 170, 60)
        light = (160,255,140)  if hovered else (130,230,110)
        dark  = (30, 100, 30)  if hovered else (25,  90, 25)
        shadow= (15,  60, 15)
        txt_c = (255,255,255)
    else:
        base  = (70, 140,220)  if hovered else (50, 110,190)
        light = (150,210,255)  if hovered else (120,180,240)
        dark  = (25,  70,130)  if hovered else (20,  60,120)
        shadow= (8,   35, 75)
        txt_c = (255,255,255)  if hovered else (220,240,255)
    pygame.draw.rect(surface, shadow, (x+B,   y+B,   w,      h     ))
    pygame.draw.rect(surface, dark,   (x,      y,     w,      h     ))
    pygame.draw.rect(surface, base,   (x+B,   y+B,   w-B*2,  h-B*2 ))
    pygame.draw.rect(surface, light,  (x+B,   y+B,   w-B*2,  B*2   ))
    pygame.draw.rect(surface, light,  (x+B,   y+B,   B*2,    h-B*2 ))
    pygame.draw.rect(surface, dark,   (x+B,   y+h-B*3, w-B*2, B*2  ))
    offset   = 2 if hovered else 0
    sh_surf  = font.render(text, True, shadow)
    txt_surf = font.render(text, True, txt_c)
    txt_rect = txt_surf.get_rect(center=(x+w//2, y+h//2+offset))
    surface.blit(sh_surf,  (txt_rect.x+2, txt_rect.y+2))
    surface.blit(txt_surf, txt_rect)
