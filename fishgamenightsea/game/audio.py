import pygame

current_bgm = None


def play_bgm(path, volume=0.4):
    global current_bgm

    # 같은 음악이면 다시 재생 안함
    if current_bgm == path:
        return

    current_bgm = path

    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

import pygame
from game.display import init_display


def main():
    pygame.init()
    pygame.mixer.init()

    init_display()

    from game.loop import run
    run()


if __name__ == "__main__":
    main()

from game.audio import play_bgm

def menu_screen():
    play_bgm("game/assets/music/menu.mp3")

    while True:
        pass

from game.audio import play_bgm

def fishing_screen():
    play_bgm("game/assets/music/fishing.mp3")

    while True:
        pass

from game.audio import play_bgm

def shop_screen():
    play_bgm("game/assets/music/shop.mp3")

    while True:
        pass

