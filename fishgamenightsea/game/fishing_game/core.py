"""게임 공통: 초기화, HUD, 타이틀, draw 라우팅."""
import pygame
print("CORE LOADED 999999")
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
    STATE_HELP,
    WHITE,
    YELLOW,
    LIGHT_GRAY,
    GRAY,
    BROWN,
    LIGHT_BROWN,
    DARK_BROWN,
)
from game.data import SHOP_DATA
from game.drawing import draw_pixel_button
from game.fonts import font_small, font_tiny, font_medium, MENU_FONT
from game.title_ui import button_rects, menu_buttons

HELP_TABS = [
    "낚시 방법",
    "단축키",
    "가방 및 상점",
    "업적 및 도감",
]

HELP_CONTENT = {
    0: [
        "1. SPACE 또는 클릭으로 낚시 시작",
        "",
        "2. 미끼 물면 SPACE 또는 클릭 다시 누르기",
        "",
        "3. SPACE 또는 클릭으로 스크롤을 조절하여 물고기와 겹치게 하기",
        "",
        "4. 초록색 게이지가 다 올라가면 낚시 성공!",
    ],

    1: [
        "[SPACE] 낚시",
        "[I] 가방",
        "[P] 상점",
        "[S] 가방에서 물고기 일괄 판매",
    ],

    2: [
        "가방에는 잡은 물고기가 저장되며, 물고기 판매가 가능합니다.",
        "상점에서는 번 돈으로 각종 낚시 장비와 미끼를 구매할 수 있습니다!",
    ],

    3: [
        "새로운 물고기를 발견할 때마다 도감에 추가됩니다.",
        "특정 조건을 달성하면 업적이 해금되고, 그에 따른 보상을 받을 수 있습니다.",
    ],
}


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
        self.help_tab = 0
        self.help_rects = []
        
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
            self.draw_collection(screen, self.codex_scroll)
        elif self.state == STATE_ACHIEVEMENT:
            self.draw_achievement(screen)
        elif self.state == STATE_HELP:
            self.draw_help(screen)
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
                    # 도움말 버튼
            help_hovered = title_ui.help_button_rect.collidepoint(mouse_pos)
            draw_pixel_button(
                screen,
                title_ui.help_button_rect,
                "도움말",
                font_tiny,
                hovered=help_hovered,
                is_main=False,
            )

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

    def draw_help(self, screen):
        
        screen.fill((20, 30, 50))

        panel = pygame.Rect(80, 40, 860, 500)

        pygame.draw.rect(screen, (40, 60, 90), panel)
        pygame.draw.rect(screen, (120, 180, 255), panel, 4)

        title = font_medium.render("도움말", True, WHITE)
        screen.blit(title, (470, 60))

        self.help_rects = []

        for i, tab in enumerate(HELP_TABS):

            rect = pygame.Rect(
                110,
                120 + i * 70,
                180,
                50
            )

            self.help_rects.append(rect)

            if i == self.help_tab:
                color = (100, 170, 255)
            else:
                color = (60, 90, 130)

            pygame.draw.rect(screen, color, rect)

            txt = font_small.render(tab, True, WHITE)
            screen.blit(txt, (rect.x + 10, rect.y + 15))

        y = 130

        for line in HELP_CONTENT[self.help_tab]:

            txt = font_small.render(line, True, WHITE)
            screen.blit(txt, (340, y))

            y += 35

        close = font_tiny.render(
            "[ESC] 닫기",
            True,
            LIGHT_GRAY
        )

        screen.blit(close, (100, 500))