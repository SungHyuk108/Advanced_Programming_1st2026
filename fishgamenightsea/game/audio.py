import os
import pygame

current_bgm = None
current_bgm_file = None
previous_bgm_file = None


def _music_path(filename):
    return os.path.join(os.path.dirname(__file__), "music", filename)


def play_bgm(filename):
    global current_bgm, current_bgm_file

    if not pygame.mixer.get_init():
        pygame.mixer.init()

    path = _music_path(filename)

    if current_bgm == path and pygame.mixer.music.get_busy():
        return

    current_bgm = path
    current_bgm_file = filename

    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1)


def push_bgm(filename):
    """현재 BGM을 저장한 뒤 다른 곡으로 전환."""
    global previous_bgm_file
    previous_bgm_file = current_bgm_file
    play_bgm(filename)


def pop_bgm():
    """push_bgm 이전 곡으로 복구."""
    global previous_bgm_file
    if previous_bgm_file:
        play_bgm(previous_bgm_file)
    previous_bgm_file = None


def stop_bgm():
    global current_bgm, current_bgm_file
    pygame.mixer.music.stop()
    current_bgm = None
    current_bgm_file = None


def pause_bgm():
    pygame.mixer.music.pause()


def unpause_bgm():
    pygame.mixer.music.unpause()


def set_volume(volume):
    pygame.mixer.music.set_volume(volume)
