"""이미지 에셋 로드 (디스플레이 초기화 후 load_all_assets 호출)."""
import os

import pygame

from game.config import SCREEN_HEIGHT, SCREEN_WIDTH

ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

background_imgs = []
title_bg_img = None
fisherman_img = None
shop_img = None
title_img = None
fish_images = {}

_loaded = False


def load_image(path, scale=None):
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


def load_image_jpg(path, scale=None):
    img = pygame.image.load(path).convert()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img


def load_all_assets():
    """pygame.display.set_mode() 이후에 호출해야 합니다."""
    global background_imgs, title_bg_img, fisherman_img, shop_img, title_img, fish_images, _loaded

    if _loaded:
        return

    background_imgs = [
        load_image(os.path.join(ASSETS_PATH, "morning_day.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        load_image(os.path.join(ASSETS_PATH, "evening_day.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
        load_image(os.path.join(ASSETS_PATH, "night_day.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)),
    ]
    title_bg_img = load_image(
        os.path.join(ASSETS_PATH, "background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    fisherman_img = load_image(os.path.join(ASSETS_PATH, "fisherman.png"), (128, 128))
    shop_img = load_image_jpg(os.path.join(ASSETS_PATH, "shop.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    title_img = load_image(os.path.join(ASSETS_PATH, "title.png"), (700, 260))
    fish_images = {
        "해초": load_image(os.path.join(ASSETS_PATH, "seaweed.png")),
        "바다장어": load_image(os.path.join(ASSETS_PATH, "conger_eel.png")),
        "황새치": load_image(os.path.join(ASSETS_PATH, "swordfish.png")),
        "참치": load_image(os.path.join(ASSETS_PATH, "tuna.png")),
        "연어": load_image(os.path.join(ASSETS_PATH, "salmon.png")),
        "숭어": load_image(os.path.join(ASSETS_PATH, "mullet.png")),
        "상어": load_image(os.path.join(ASSETS_PATH, "shark.png")),
        "돌고래": load_image(os.path.join(ASSETS_PATH, "dolphin.png")),
        "날치": load_image(os.path.join(ASSETS_PATH, "flying_fish.png")),
        "쓰레기": load_image(os.path.join(ASSETS_PATH, "trash.png")),
        "멸치": load_image(os.path.join(ASSETS_PATH, "anchovy.png")),
        "게": load_image(os.path.join(ASSETS_PATH, "crab.png")),
        "가오리": load_image(os.path.join(ASSETS_PATH, "stingray.png")),
        "새우": load_image(os.path.join(ASSETS_PATH, "shrimp.png")),
        "복어": load_image(os.path.join(ASSETS_PATH, "pufferfish.png")),
        "피라냐": load_image(os.path.join(ASSETS_PATH, "piranha.png")),
        "문어": load_image(os.path.join(ASSETS_PATH, "octopus.png")),
        "황금잉어": load_image(os.path.join(ASSETS_PATH, "golden_carp.png")),
    }
    _loaded = True
