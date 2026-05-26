"""상점 로직·렌더링."""
import pygame

from game.assets import shop_img
from game.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STATE_SHOP_MAIN,
    STATE_SHOP_CATEGORY,
    WHITE,
    GREEN,
    YELLOW,
    LIGHT_GRAY,
    CYAN,
    GRAY,
)
from game.data import SHOP_DATA
from game.fonts import font_medium, font_small, font_tiny


class ShopMixin:

    def buy_item(self, category, item_index):
        data  = SHOP_DATA[category]
        price = data["prices"][item_index]
        if self.total_money < price:
            return False
        if data["consumable"]:
            self.total_money -= price
            self.bait         = {"name": data["items"][item_index], "effect": data["effects"][item_index]}
            self.bait_count  += 5
            return True
        else:
            current_level = self.equipment[category]
            if current_level >= item_index + 1:
                return False
            if current_level != item_index:
                return False
            self.total_money     -= price
            self.equipment[category] = item_index + 1
            if category == "가방":
                self.max_inventory = self.get_bag_size()
            return True

    def handle_shop_click(self, pos):
        if self.state == STATE_SHOP_MAIN:
            for rect, cat in self.category_rects:
                if rect.collidepoint(pos):
                    self.shop_category = cat
                    self.state         = STATE_SHOP_CATEGORY
                    return
        elif self.state == STATE_SHOP_CATEGORY:
            for rect, idx in self.item_rects:
                if rect.collidepoint(pos):
                    self.buy_item(self.shop_category, idx)
                    return

    def draw_shop(self, screen):
        screen.blit(shop_img, (0, 0))
        if self.state == STATE_SHOP_MAIN:
            self.draw_shop_main(screen)
        elif self.state == STATE_SHOP_CATEGORY:
            self.draw_shop_category(screen)

    def draw_shop_main(self, screen):
        money_box = pygame.Rect(SCREEN_WIDTH - 180, 15, 165, 35)
        pygame.draw.rect(screen, (30, 30, 50), money_box)
        pygame.draw.rect(screen, YELLOW, money_box, 2)
        screen.blit(font_small.render(f"소지금: {self.total_money}G", True, YELLOW), (SCREEN_WIDTH - 170, 22))

        categories = ["미끼", "릴", "낚싯바늘", "낚싯줄", "가방"]
        btn_w, btn_h = 140, 45
        sx = (SCREEN_WIDTH - btn_w) // 2
        sy = 350
        self.category_rects = []
        for i, cat in enumerate(categories):
            rect = pygame.Rect(sx, sy + i * 55, btn_w, btn_h)
            self.category_rects.append((rect, cat))
            pygame.draw.rect(screen, (50, 40, 30), rect)
            pygame.draw.rect(screen, (80, 60, 40), (rect.x, rect.y, rect.width, 4))
            pygame.draw.rect(screen, (30, 25, 20), (rect.x, rect.y + rect.height - 4, rect.width, 4))
            pygame.draw.rect(screen, (100, 80, 60), rect, 2)
            if cat != "미끼":
                lv  = self.equipment[cat]
                lbl = f"{cat} [{SHOP_DATA[cat]['items'][lv-1]}]" if lv > 0 else cat
                cat_txt = font_small.render(lbl, True, WHITE)
            else:
                lbl     = f"{cat} ({self.bait_count})" if self.bait else cat
                cat_txt = font_small.render(lbl, True, (255, 180, 100) if self.bait else WHITE)
            screen.blit(cat_txt, cat_txt.get_rect(center=rect.center))

        hint = font_tiny.render("[P/ESC] 나가기", True, LIGHT_GRAY)
        screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 20)))

    def draw_shop_category(self, screen):
        cat  = self.shop_category
        data = SHOP_DATA[cat]

        money_box = pygame.Rect(SCREEN_WIDTH - 180, 15, 165, 35)
        pygame.draw.rect(screen, (30, 30, 50), money_box)
        pygame.draw.rect(screen, YELLOW, money_box, 2)
        screen.blit(font_small.render(f"소지금: {self.total_money}G", True, YELLOW), (SCREEN_WIDTH - 170, 22))

        title_box = pygame.Rect(15, 15, 200, 35)
        pygame.draw.rect(screen, (30, 30, 50), title_box)
        pygame.draw.rect(screen, WHITE, title_box, 2)
        screen.blit(font_medium.render(cat, True, WHITE), (25, 18))
        screen.blit(font_tiny.render(data["description"], True, LIGHT_GRAY), (25, 55))

        self.item_rects = []
        sy = 350
        for i, (item_name, price, effect) in enumerate(zip(data["items"], data["prices"], data["effects"])):
            rect = pygame.Rect(80, sy + i * 50, SCREEN_WIDTH - 160, 42)
            self.item_rects.append((rect, i))

            can_buy = self.total_money >= price
            already_owned = False
            if not data["consumable"]:
                lv            = self.equipment[cat]
                already_owned = lv >= i + 1
                can_buy       = can_buy and lv == i

            if already_owned:
                bg, border = (40, 60, 40), GREEN
            elif can_buy:
                bg, border = (50, 40, 30), (100, 80, 60)
            else:
                bg, border = (40, 35, 35), (80, 60, 60)

            pygame.draw.rect(screen, bg,     rect)
            pygame.draw.rect(screen, border, rect, 2)

            if already_owned:
                name_txt = font_small.render(f"{item_name} [보유중]", True, GREEN)
            else:
                name_txt = font_small.render(item_name, True, WHITE if can_buy else GRAY)
            screen.blit(name_txt, (rect.x + 15, rect.y + 5))

            effect_strs = {
                "미끼": f"희귀확률 x{effect}", "릴": f"속도 x{effect}",
                "낚싯바늘": f"증가속도 x{effect}", "낚싯줄": f"감소속도 x{effect}",
                "가방": f"크기 {effect}칸",
            }
            eff_txt = font_tiny.render(effect_strs[cat], True, CYAN if can_buy else GRAY)
            screen.blit(eff_txt, (rect.x + 15, rect.y + 25))

            if not already_owned:
                pt = font_small.render(f"{price}G", True, YELLOW if can_buy else (100, 80, 60))
                screen.blit(pt, pt.get_rect(right=rect.right - 15, centery=rect.centery))

        hint = font_tiny.render("[ESC] 뒤로  |  숫자키(1~5)로 구매", True, LIGHT_GRAY)
        screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 20)))

