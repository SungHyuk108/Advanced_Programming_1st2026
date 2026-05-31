"""게임 진입점 — 모든 모듈을 초기화하고 메인 루프를 실행합니다."""

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