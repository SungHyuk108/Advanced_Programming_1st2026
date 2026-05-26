"""Pygame 디스플레이 초기화."""
import pygame

from game.config import FPS, SCREEN_HEIGHT, SCREEN_WIDTH

screen = None
clock = None


def init_display():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Fishing Game")
    clock = pygame.time.Clock()

    from game.assets import load_all_assets
    load_all_assets()

    return screen, clock
