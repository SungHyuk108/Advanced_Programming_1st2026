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

    def draw_collection(self, screen, scroll_offset=0):
            screen.fill((15, 25, 40))

            # 제목
            title = font_large.render("도 감", True, WHITE)
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 38)))

            # 발견 수
            count_txt = font_small.render(
                f"발견한 물고기: {len(self.discovered)} / {len(FISH_DATA)}",
                True, LIGHT_GRAY
            )
            screen.blit(count_txt, count_txt.get_rect(center=(SCREEN_WIDTH // 2, 72)))

            pygame.draw.line(screen, DARK_GRAY, (40, 90), (SCREEN_WIDTH - 40, 90), 2)

            # 희귀도 순서 (높은 등급 → 낮은 등급)
            RARITY_ORDER = ["legendary", "epic", "rare", "uncommon", "common", "trash"]

            CARD_W  = 130
            CARD_H  = 160
            GAP_X   = 14
            GAP_Y   = 18
            START_X = 40
            START_Y = 108

            # 전체 콘텐츠 높이 계산 (스크롤 max 용)
            total_content_h = 0
            for rarity in RARITY_ORDER:
                fish_in_tier = [f for f in FISH_DATA if f["rarity"] == rarity]
                if not fish_in_tier:
                    continue
                cols = (SCREEN_WIDTH - START_X * 2 + GAP_X) // (CARD_W + GAP_X)
                rows = (len(fish_in_tier) + cols - 1) // cols
                total_content_h += 42 + rows * (CARD_H + GAP_Y) + GAP_Y

            max_scroll    = max(0, total_content_h - (SCREEN_HEIGHT - START_Y - 40))
            scroll_offset = max(0, min(scroll_offset, max_scroll))

            # 클리핑
            clip_rect = pygame.Rect(0, 95, SCREEN_WIDTH, SCREEN_HEIGHT - 95 - 30)
            screen.set_clip(clip_rect)

            COLS = (SCREEN_WIDTH - START_X * 2 + GAP_X) // (CARD_W + GAP_X)
            y_cursor = START_Y - scroll_offset

            for rarity in RARITY_ORDER:
                fish_in_tier = [f for f in FISH_DATA if f["rarity"] == rarity]
                if not fish_in_tier:
                    continue

                tier_color = RARITY_COLORS[rarity]

                # 티어 헤더
                if 95 <= y_cursor <= SCREEN_HEIGHT:
                    # 헤더 배경
                    header_rect = pygame.Rect(START_X, y_cursor, SCREEN_WIDTH - START_X * 2, 34)
                    header_surf = pygame.Surface((header_rect.width, header_rect.height), pygame.SRCALPHA)
                    header_surf.fill((*tier_color[:3], 40) if len(tier_color) == 3 else (80, 80, 80, 40))
                    screen.blit(header_surf, header_rect.topleft)
                    pygame.draw.rect(screen, tier_color, header_rect, 2, border_radius=6)

                    # 티어 이름
                    tier_txt = font_medium.render(RARITY_KR[rarity], True, tier_color)
                    screen.blit(tier_txt, tier_txt.get_rect(midleft=(START_X + 14, y_cursor + 17)))

                    # 발견 수
                    discovered_count = sum(1 for f in fish_in_tier if f["name"] in self.discovered)
                    disc_txt = font_tiny.render(
                        f"{discovered_count}/{len(fish_in_tier)}",
                        True, LIGHT_GRAY
                    )
                    screen.blit(disc_txt, disc_txt.get_rect(midright=(SCREEN_WIDTH - START_X - 10, y_cursor + 17)))

                y_cursor += 42

                # 카드 그리기
                for idx, fish in enumerate(fish_in_tier):
                    col = idx % COLS
                    row = idx // COLS
                    cx  = START_X + col * (CARD_W + GAP_X)
                    cy  = y_cursor + row * (CARD_H + GAP_Y)

                    if cy + CARD_H < 95 or cy > SCREEN_HEIGHT:
                        continue

                    discovered = fish["name"] in self.discovered

                    if discovered:
                        bg_color     = (30, 40, 60)
                        border_color = tier_color
                    else:
                        bg_color     = (20, 20, 28)
                        border_color = (50, 50, 60)

                    card_rect = pygame.Rect(cx, cy, CARD_W, CARD_H)
                    pygame.draw.rect(screen, bg_color,     card_rect, border_radius=8)
                    pygame.draw.rect(screen, border_color, card_rect, 2, border_radius=8)

                    img_size = 64
                    img_x    = cx + (CARD_W - img_size) // 2
                    img_y    = cy + 12

                    if discovered:
                        img = pygame.transform.scale(fish_images[fish["name"]], (img_size, img_size))
                        screen.blit(img, (img_x, img_y))
                    else:
                        silhouette = pygame.transform.scale(fish_images[fish["name"]], (img_size, img_size))
                        silhouette.set_alpha(40)
                        screen.blit(silhouette, (img_x, img_y))
                        silhouette.set_alpha(255)
                        q_text = font_medium.render("???", True, (60, 60, 80))
                        screen.blit(q_text, q_text.get_rect(center=(cx + CARD_W // 2, img_y + img_size // 2)))

                    name_str   = fish["name"] if discovered else "???"
                    name_color = WHITE if discovered else (50, 50, 65)
                    name_txt   = font_small.render(name_str, True, name_color)
                    screen.blit(name_txt, name_txt.get_rect(center=(cx + CARD_W // 2, img_y + img_size + 8)))

                    if discovered:
                        rarity_txt = font_tiny.render(RARITY_KR[rarity], True, tier_color)
                        screen.blit(rarity_txt, rarity_txt.get_rect(center=(cx + CARD_W // 2, img_y + img_size + 26)))
                        price_txt = font_tiny.render(f"{fish['price']}G", True, YELLOW)
                        screen.blit(price_txt, price_txt.get_rect(center=(cx + CARD_W // 2, img_y + img_size + 44)))

                # 다음 티어로 y 이동
                rows = (len(fish_in_tier) + COLS - 1) // COLS
                y_cursor += rows * (CARD_H + GAP_Y) + GAP_Y

            screen.set_clip(None)

            # 스크롤바
            if max_scroll > 0:
                bar_area_h = SCREEN_HEIGHT - 125
                bar_h = max(30, int(bar_area_h * (bar_area_h / total_content_h)))
                bar_y = 95 + int((bar_area_h - bar_h) * (scroll_offset / max_scroll))
                pygame.draw.rect(screen, DARK_GRAY,  (SCREEN_WIDTH - 12, 95, 8, bar_area_h), border_radius=4)
                pygame.draw.rect(screen, LIGHT_GRAY, (SCREEN_WIDTH - 12, bar_y, 8, bar_h),   border_radius=4)

            close_txt = font_tiny.render("[ESC] 닫기  |  [↑↓] 스크롤", True, GRAY)
            screen.blit(close_txt, close_txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 18)))

            self.codex_scroll = scroll_offset