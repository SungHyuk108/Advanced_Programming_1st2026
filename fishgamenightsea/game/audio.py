import os
import pygame

current_bgm = None
# s

def play_bgm(filename):
    global current_bgm

    # mixer 초기화
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    path = os.path.join(
        os.path.dirname(__file__),
        "music",
        filename
    )

    # 같은 음악이 이미 재생 중이면 다시 재생하지 않음
    if current_bgm == path and pygame.mixer.music.get_busy():
        return

    current_bgm = path

    print("music path =", path)

    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)


def stop_bgm():
    global current_bgm
    pygame.mixer.music.stop()
    current_bgm = None


def pause_bgm():
    pygame.mixer.music.pause()


def unpause_bgm():
    pygame.mixer.music.unpause()


def set_volume(volume):
    pygame.mixer.music.set_volume(volume)