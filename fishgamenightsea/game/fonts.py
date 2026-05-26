"""한글 폰트 로드."""
import pygame
from game.config import WHITE

def get_korean_font(size):
    font_names = [
        "malgun gothic", "malgungothic", "AppleGothic", "Apple SD Gothic Neo",
        "NanumGothic", "NanumBarunGothic", "gulim", "dotum", "batang",
    ]
    for font_name in font_names:
        try:
            font = pygame.font.SysFont(font_name, size)
            test_surface = font.render("테스트", True, WHITE)
            if test_surface.get_width() > 10:
                return font
        except:
            continue
    return pygame.font.Font(None, size)

font_large  = get_korean_font(40)
font_medium = get_korean_font(28)
font_small  = get_korean_font(20)
font_tiny   = get_korean_font(16)

TITLE_FONT = get_korean_font(80)
MENU_FONT  = get_korean_font(30)
