"""업적 로직·렌더링."""
import copy
import pygame

from game.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    GRAY,
    GREEN,
    RED,
    YELLOW,
    DARK_GRAY,
    LIGHT_GRAY,
)
from game.data import FISH_DATA
from game.fonts import font_large, font_medium, font_small, font_tiny
from game.fishing_game.achievement.data import DEFAULT_ACHIEVEMENTS


class AchievementMixin:

    def init_achievement_state(self):
        self.achievements = copy.deepcopy(DEFAULT_ACHIEVEMENTS)

        self.total_catches = 0
        self.perfect_count = 0

        self.achievement_popup = None
        self.achievement_timer = 0

        # 도감용
        self.discovered = set()


    def on_fish_caught(self):

        # 잡은 물고기 기록
        self.discovered.add(self.caught_fish["name"])

        self.total_catches += 1

        # 전체 물고기 수 계산
        total_fish_count = len(FISH_DATA)

        # 업적 체크
        if self.total_catches >= 1:
            self.unlock_achievement("first_fish")

        if self.perfect_count >= 10:
            self.unlock_achievement("perfect_10")

        if self.caught_fish["rarity"] == "legendary":
            self.unlock_achievement("first_legendary")

        # 도감 마스터
        if len(self.discovered) >= total_fish_count:
            self.unlock_achievement("codex_master")

        if self.total_money >= 1000:
            self.unlock_achievement("rich_1000")

        # 인벤토리 추가
        if len(self.inventory) < self.get_bag_size():
            self.inventory.append(self.caught_fish)

        # 디버그 출력
        print("현재 도감:", len(self.discovered))
        print("전체 물고기:", total_fish_count)

    def unlock_achievement(self, key):

        achievement = self.achievements[key]

        if achievement["unlocked"]:
            return

        achievement["unlocked"] = True

        reward = achievement["reward"]
        self.total_money += reward

        self.achievement_popup = f"[업적 달성] {achievement['name']} (+{reward}G)"
        self.achievement_timer = 4

        print(self.achievement_popup)


    def update_achievement_popup(self, dt):
        if self.achievement_timer > 0:
            self.achievement_timer -= dt
            if self.achievement_timer <= 0:
                self.achievement_popup = None

    def draw_achievement_popup(self, screen):
        if not self.achievement_popup:
            return
        popup_rect = pygame.Rect(SCREEN_WIDTH // 2 - 220, 20, 440, 50)
        pygame.draw.rect(screen, (40, 30, 20), popup_rect)
        pygame.draw.rect(screen, YELLOW, popup_rect, 3)
        txt = font_small.render(self.achievement_popup, True, WHITE)
        screen.blit(txt, txt.get_rect(center=popup_rect.center))

    def draw_achievement(self, screen):

        screen.fill((25, 20, 35))

        title = font_large.render("업적", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 40)))

        y = 100

        for key, achievement in self.achievements.items():

            unlocked = achievement["unlocked"]

            rect = pygame.Rect(120, y, 780, 70)

            bg = (40, 60, 40) if unlocked else (35, 35, 40)
            border = GREEN if unlocked else DARK_GRAY

            pygame.draw.rect(screen, bg, rect)
            pygame.draw.rect(screen, border, rect, 3)

            # 이름
            name_color = YELLOW if unlocked else GRAY

            name_txt = font_medium.render(
                achievement["name"],
                True,
                name_color
            )

            screen.blit(name_txt, (140, y + 10))

            # 설명
            desc_txt = font_small.render(
                achievement["desc"],
                True,
                LIGHT_GRAY
            )

            screen.blit(desc_txt, (140, y + 38))

            # 상태
            status = "달성 완료" if unlocked else "미달성"

            status_color = GREEN if unlocked else RED

            status_txt = font_small.render(
                status,
                True,
                status_color
            )

            screen.blit(status_txt, (760, y + 22))

            y += 85

        close_txt = font_tiny.render(
            "[ESC] 닫기",
            True,
            GRAY
        )

        screen.blit(
            close_txt,
            close_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        )
    # --------------------------------------------------
