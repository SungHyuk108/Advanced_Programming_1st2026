"""가방·도감 로직·렌더링."""
import pygame

from game.assets import fish_images
from game.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    GRAY,
    GREEN,
    BRIGHT_GREEN,
    DARK_GREEN,
    YELLOW,
    DARK_GRAY,
    LIGHT_GRAY,
)
from game.data import FISH_DATA, RARITY_COLORS, RARITY_KR
from game.fonts import font_large, font_medium, font_small, font_tiny


class BagMixin:

    def sell_all_fish(self):
        for fish in self.inventory:
            self.total_money += fish["price"]
        self.inventory = []

    def draw_inventory(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(220)
        screen.blit(overlay, (0, 0))

        title = font_large.render("가방", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 45)))

        if not self.inventory:
            et = font_medium.render("가방이 비어있습니다", True, GRAY)
            screen.blit(et, et.get_rect(center=(SCREEN_WIDTH//2, 250)))
        else:
            fish_counts = {}
            for fish in self.inventory:
                n = fish["name"]
                if n in fish_counts:
                    fish_counts[n]["count"] += 1
                else:
                    fish_counts[n] = {"fish": fish, "count": 1}

            y_off       = 90
            total_value = 0
            for name, data in fish_counts.items():
                fish  = data["fish"]
                count = data["count"]
                value = fish["price"] * count
                total_value += value
                icon = pygame.transform.scale(fish_images[name], (40, 40))
                screen.blit(icon, (70, y_off - 8))
                screen.blit(font_small.render(f"{name} x{count}", True, RARITY_COLORS[fish["rarity"]]), (125, y_off))
                screen.blit(font_small.render(f"{value}G", True, YELLOW), (350, y_off))
                y_off += 40

            screen.blit(font_medium.render(f"총 가치: {total_value}G", True, YELLOW), (80, y_off + 15))
            sell_rect = pygame.Rect(SCREEN_WIDTH//2 - 90, y_off + 60, 180, 40)
            pygame.draw.rect(screen, GREEN,       sell_rect)
            pygame.draw.rect(screen, BRIGHT_GREEN,(sell_rect.x, sell_rect.y, sell_rect.width, 4))
            pygame.draw.rect(screen, DARK_GREEN,  (sell_rect.x, sell_rect.y + sell_rect.height - 4, sell_rect.width, 4))
            pygame.draw.rect(screen, WHITE, sell_rect, 2)
            st = font_small.render("전부 판매 [S]", True, WHITE)
            screen.blit(st, st.get_rect(center=sell_rect.center))

        ct = font_tiny.render("[ESC] 닫기", True, GRAY)
        screen.blit(ct, ct.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 35)))

    # --------------------------------------------------
    # 도감 화면
    # --------------------------------------------------

    def draw_collection(self, screen):
        screen.fill((15, 25, 40))

        # 제목
        title = font_large.render("도 감", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 38)))

        # 발견 수 표시
        count_txt = font_small.render(
            f"발견한 물고기: {len(self.discovered)} / {len(FISH_DATA)}",
            True, LIGHT_GRAY
        )
        screen.blit(count_txt, count_txt.get_rect(center=(SCREEN_WIDTH // 2, 72)))

        # 구분선
        pygame.draw.line(screen, DARK_GRAY, (40, 90), (SCREEN_WIDTH - 40, 90), 2)

        # 카드 그리드 설정
        CARD_W   = 140
        CARD_H   = 170
        COLS     = 6
        GAP_X    = 20
        GAP_Y    = 20
        START_X  = (SCREEN_WIDTH - (COLS * CARD_W + (COLS - 1) * GAP_X)) // 2
        START_Y  = 108

        for idx, fish in enumerate(FISH_DATA):
            col = idx % COLS
            row = idx // COLS
            cx  = START_X + col * (CARD_W + GAP_X)
            cy  = START_Y + row * (CARD_H + GAP_Y)

            discovered = fish["name"] in self.discovered
            rarity     = fish["rarity"]

            # 카드 배경
            if discovered:
                bg_color     = (30, 40, 60)
                border_color = RARITY_COLORS[rarity]
            else:
                bg_color     = (20, 20, 28)
                border_color = (50, 50, 60)

            card_rect = pygame.Rect(cx, cy, CARD_W, CARD_H)
            pygame.draw.rect(screen, bg_color,     card_rect, border_radius=8)
            pygame.draw.rect(screen, border_color, card_rect, 2, border_radius=8)

            # 물고기 이미지 or 실루엣
            img_size = 72
            img_x    = cx + (CARD_W - img_size) // 2
            img_y    = cy + 14

            if discovered:
                img = pygame.transform.scale(fish_images[fish["name"]], (img_size, img_size))
                screen.blit(img, (img_x, img_y))
            else:
                # 실루엣: 검은 사각형으로 표시
                silhouette = pygame.transform.scale(fish_images[fish["name"]], (img_size, img_size))
                dark_surf  = pygame.Surface((img_size, img_size), pygame.SRCALPHA)
                dark_surf.fill((0, 0, 0, 0))
                # 픽셀 하나하나 어둡게 (간단 실루엣)
                silhouette.set_alpha(40)
                screen.blit(silhouette, (img_x, img_y))
                silhouette.set_alpha(255)
                # ??? 텍스트
                q_text = font_medium.render("???", True, (60, 60, 80))
                screen.blit(q_text, q_text.get_rect(center=(cx + CARD_W // 2, img_y + img_size // 2)))

            # 물고기 이름
            if discovered:
                name_color = WHITE
                name_str   = fish["name"]
            else:
                name_color = (50, 50, 65)
                name_str   = "???"

            name_txt = font_small.render(name_str, True, name_color)
            screen.blit(name_txt, name_txt.get_rect(center=(cx + CARD_W // 2, img_y + img_size + 10)))

            # 희귀도 뱃지
            if discovered:
                rarity_txt = font_tiny.render(RARITY_KR[rarity], True, RARITY_COLORS[rarity])
                screen.blit(rarity_txt, rarity_txt.get_rect(center=(cx + CARD_W // 2, img_y + img_size + 30)))

                # 판매가
                price_txt = font_tiny.render(f"{fish['price']}G", True, YELLOW)
                screen.blit(price_txt, price_txt.get_rect(center=(cx + CARD_W // 2, img_y + img_size + 48)))

        # 닫기 안내
        close_txt = font_tiny.render("[ESC] 닫기", True, GRAY)
        screen.blit(close_txt, close_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 18)))

