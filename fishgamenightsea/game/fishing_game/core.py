"""게임 공통: 초기화, HUD, 타이틀, draw 라우팅."""
import pygame

from game import title_ui
from game.assets import background_imgs, title_bg_img, fisherman_img, title_img
from game.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STATE_TITLE,
    STATE_IDLE,
    STATE_CASTING,
    STATE_WAITING,
    STATE_BITE,
    STATE_CATCHING,
    STATE_RESULT,
    STATE_INVENTORY,
    STATE_SHOP_MAIN,
    STATE_SHOP_CATEGORY,
    STATE_COLLECTION,
    STATE_ACHIEVEMENT,
    WHITE,
    YELLOW,
    LIGHT_GRAY,
    BROWN,
    LIGHT_BROWN,
    DARK_BROWN,
)
from game.data import SHOP_DATA
from game.drawing import draw_pixel_button
from game.fonts import font_small, font_tiny, font_medium, MENU_FONT
from game.title_ui import button_rects, menu_buttons


class CoreMixin:

    def __init__(self):
        self.state        = STATE_TITLE
        self.inventory    = []
        self.total_money  = 500
        self.max_inventory= 10
        self.discovered   = set()   # 도감: 발견한 물고기 이름 저장

        # 배경 전환 시스템
        self.bg_index   = 0   # 0: 아침, 1: 저녁, 2: 밤
        self.cast_count = 0   # 낚시 시도 횟수 (3번마다 배경 전환)

        self.equipment = {
            "릴": 0, "낚싯바늘": 0, "낚싯줄": 0, "가방": 0,
        }
        self.bait       = None
        self.bait_count = 0

        self.shop_category = None
        self.shop_scroll   = 0

        self.category_rects = []
        self.item_rects     = []

        # 도감 스크롤
        self.codex_scroll = 0
        # =========================================================
# 업적 데이터
# FishingGame.__init__ 안에 추가
# =========================================================

        self.init_achievement_state()

        self.reset_game()
    def get_reel_multiplier(self):
        lv = self.equipment["릴"]
        return 1.0 if lv == 0 else SHOP_DATA["릴"]["effects"][lv - 1]

    def get_hook_multiplier(self):
        lv = self.equipment["낚싯바늘"]
        return 1.0 if lv == 0 else SHOP_DATA["낚싯바늘"]["effects"][lv - 1]

    def get_line_multiplier(self):
        lv = self.equipment["낚싯줄"]
        return 1.0 if lv == 0 else SHOP_DATA["낚싯줄"]["effects"][lv - 1]

    def get_bag_size(self):
        lv = self.equipment["가방"]
        return 10 if lv == 0 else SHOP_DATA["가방"]["effects"][lv - 1]

    def draw(self, screen):
        if self.state == STATE_TITLE:
            self.draw_title(screen)
        elif self.state in [STATE_SHOP_MAIN, STATE_SHOP_CATEGORY]:
            self.draw_shop(screen)
        elif self.state == STATE_COLLECTION:
            self.draw_collection(screen)
        elif self.state == STATE_ACHIEVEMENT:
            self.draw_achievement(screen)
        else:
            self.draw_background(screen)
            if self.state == STATE_IDLE:
                self.draw_idle(screen)
            elif self.state == STATE_CASTING:
                self.draw_casting(screen)
            elif self.state == STATE_WAITING:
                self.draw_waiting(screen)
            elif self.state == STATE_BITE:
                self.draw_bite(screen)
            elif self.state == STATE_CATCHING:
                self.draw_catching(screen)
            elif self.state == STATE_RESULT:
                self.draw_result(screen)
            elif self.state == STATE_INVENTORY:
                self.draw_inventory(screen)
            self.draw_ui(screen)

    def draw_title(self, screen):
        screen.blit(title_bg_img, (0, 0))

        # 타이틀 내려오는 애니메이션
        if title_ui.title_y < title_ui.title_target_y:
            title_ui.title_y += title_ui.title_speed
        else:
            title_ui.show_menu = True

        title_rect = title_img.get_rect(
            center=(SCREEN_WIDTH // 2, title_ui.title_y)
        )

        screen.blit(title_img, title_rect)

        if title_ui.show_menu:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(button_rects):
                hovered  = rect.collidepoint(mouse_pos)
                is_main  = (i == 0)
                btn_font = MENU_FONT if is_main else font_medium
                draw_pixel_button(screen, rect, menu_buttons[i]["text"],
                                  btn_font, hovered=hovered, is_main=is_main)

        hint = font_tiny.render("ESC: 타이틀로 돌아가기", True, (200, 230, 255))
        screen.blit(hint, (10, SCREEN_HEIGHT - 25))

    def draw_background(self, screen):
        screen.blit(background_imgs[self.bg_index], (0, 0))
        screen.blit(fisherman_img, (295, 205))

    def draw_ui(self, screen):
        ui_box = pygame.Rect(15, 15, 160, 35)
        pygame.draw.rect(screen, (30, 30, 50),  ui_box)
        pygame.draw.rect(screen, (60, 60, 80),  ui_box, 3)
        pygame.draw.rect(screen, (80, 80, 100), (17, 17, 156, 2))
        money_text = font_small.render(f"소지금: {self.total_money}G", True, YELLOW)
        screen.blit(money_text, (25, 22))

        if self.bait:
            bait_box = pygame.Rect(15, 55, 160, 30)
            pygame.draw.rect(screen, (50, 30, 30), bait_box)
            pygame.draw.rect(screen, (100, 60, 60), bait_box, 2)
            bait_text = font_tiny.render(f"미끼: {self.bait['name']} x{self.bait_count}", True, (255, 180, 100))
            screen.blit(bait_text, (25, 60))

        bag_rect = pygame.Rect(SCREEN_WIDTH - 70, 15, 55, 50)
        pygame.draw.rect(screen, BROWN,       bag_rect)
        pygame.draw.rect(screen, LIGHT_BROWN, (SCREEN_WIDTH - 68, 17, 51, 3))
        pygame.draw.rect(screen, DARK_BROWN,  bag_rect, 3)
        pygame.draw.rect(screen, DARK_BROWN,  (SCREEN_WIDTH - 55, 10, 25, 8))
        bag_text = font_small.render(f"{len(self.inventory)}/{self.get_bag_size()}", True, WHITE)
        screen.blit(bag_text, (SCREEN_WIDTH - 65, 35))

        if self.state == STATE_IDLE:
            hint = font_tiny.render("[I] 가방  [P] 상점  [ESC] 타이틀", True, LIGHT_GRAY)
            screen.blit(hint, (SCREEN_WIDTH - 190, 70))

        self.draw_achievement_popup(screen)

    def update(self, dt, action_pressed):
        self.update_fishing(dt, action_pressed)
        self.update_achievement_popup(dt)

