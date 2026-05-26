"""낚시 플레이 로직·렌더링."""
import math
import random
import pygame

from game.assets import background_imgs, fish_images
from game.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STATE_IDLE,
    STATE_CASTING,
    STATE_WAITING,
    STATE_BITE,
    STATE_CATCHING,
    STATE_RESULT,
    WHITE,
    BLACK,
    GRAY,
    GREEN,
    BRIGHT_GREEN,
    DARK_GREEN,
    RED,
    BRIGHT_RED,
    YELLOW,
    BRIGHT_YELLOW,
    DARK_GRAY,
)
from game.data import RARITY_COLORS, RARITY_KR
from game.drawing import (
    draw_pixel_bobber,
    draw_pixel_fishing_line,
    draw_pixel_cylinder,
    draw_pixel_bar,
    draw_splash_particle,
)
from game.fonts import font_large, font_medium, font_small, font_tiny


class FishingMixin:

    def reset_game(self):
        self.power           = 0
        self.power_direction = 1
        self.perfect_zone_start = random.randint(60, 80)
        self.perfect_zone_end   = self.perfect_zone_start + 15
        self.is_perfect_cast    = False

        self.wait_time     = 0
        self.max_wait_time = random.uniform(3, 6)
        self.bobber_bob    = 0
        self.splash_particles = []

        self.bite_timer     = 0
        self.bite_time_limit= 2.0

        self.bar_y        = 200
        self.bar_height   = 70
        self.bar_velocity = 0
        self.bar_max_speed    = 6 * self.get_reel_multiplier()
        self.bar_accel_time   = 0.5
        self.bar_accel_rate   = self.bar_max_speed / self.bar_accel_time

        self.fish_y         = 150
        self.fish_direction = 1
        self.fish_speed     = 3
        self.catch_progress = 50
        self.current_fish   = None
        self.caught_fish    = None
        self.result_timer   = 0

    # --------------------------------------------------
    # 물고기 선택
    # --------------------------------------------------

    def select_fish(self):
        weights = [15, 10, 25, 20, 12, 8, 5, 3, 1.5, 0.4, 0.1]
        if self.is_perfect_cast:
            weights = [5, 5, 20, 20, 18, 15, 10, 4, 2, 0.7, 0.3]
        if self.bait:
            bait_effect = self.bait["effect"]
            for i in range(4):
                weights[i] /= bait_effect
            for i in range(4, len(weights)):
                weights[i] *= bait_effect
            self.bait_count -= 1
            if self.bait_count <= 0:
                self.bait       = None
                self.bait_count = 0
        total = sum(weights)
        r     = random.uniform(0, total)
        cumulative = 0
        for i, w in enumerate(weights):
            cumulative += w
            if r <= cumulative:
                return FISH_DATA[i].copy()
        return FISH_DATA[0].copy()

    # --------------------------------------------------
    # 파티클
    # --------------------------------------------------

    def add_splash_particle(self, x, y):
        for _ in range(3):
            self.splash_particles.append({
                'x': x + random.randint(-15, 15),
                'y': y,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-6, -3),
                'life': 1.0,
                'size': random.randint(3, 6),
            })

    def update_splash_particles(self, dt):
        for p in self.splash_particles[:]:
            p['x']   += p['vx']
            p['y']   += p['vy']
            p['vy']  += 12 * dt
            p['life'] -= dt * 1.5
            if p['life'] <= 0:
                self.splash_particles.remove(p)

    # --------------------------------------------------
    # 업데이트
    # --------------------------------------------------

    def update_fishing(self, dt, action_pressed):
        if self.state == STATE_CASTING:
            self.power += self.power_direction * 100 * dt
            if self.power >= 100:
                self.power = 100
                self.power_direction = -1
            elif self.power <= 0:
                self.power = 0
                self.power_direction = 1

        elif self.state == STATE_WAITING:
            self.wait_time  += dt
            self.bobber_bob  = math.sin(self.wait_time * 3) * 4
            bobber_x = 450 + (self.power / 100) * 300
            if random.random() < 0.15:
                self.add_splash_particle(bobber_x, 365)
            self.update_splash_particles(dt)
            if self.wait_time >= self.max_wait_time:
                self.state      = STATE_BITE
                self.bite_timer = 0

        elif self.state == STATE_BITE:
            self.bite_timer += dt
            self.update_splash_particles(dt)
            bobber_x = 450 + (self.power / 100) * 300
            if random.random() < 0.4:
                self.add_splash_particle(bobber_x, 380)
            if self.bite_timer >= self.bite_time_limit:
                self.state        = STATE_RESULT
                self.caught_fish  = None
                self.result_timer = 0

        elif self.state == STATE_CATCHING:
            if action_pressed:
                self.bar_velocity -= self.bar_accel_rate * dt
            else:
                self.bar_velocity += (self.bar_accel_rate / 1.5) * dt
            self.bar_velocity = max(-self.bar_max_speed, min(self.bar_max_speed, self.bar_velocity))
            self.bar_y += self.bar_velocity

            cylinder_top    = 80
            cylinder_bottom = 420
            if self.bar_y <= cylinder_top:
                self.bar_y        = cylinder_top
                self.bar_velocity = 0
            elif self.bar_y >= cylinder_bottom - self.bar_height:
                self.bar_y        = cylinder_bottom - self.bar_height
                self.bar_velocity = 0

            self.fish_y += self.fish_direction * self.fish_speed
            if random.random() < 0.02:
                self.fish_direction *= -1
            fish_size = 40
            if self.fish_y <= cylinder_top:
                self.fish_y         = cylinder_top
                self.fish_direction = 1
            elif self.fish_y >= cylinder_bottom - fish_size:
                self.fish_y         = cylinder_bottom - fish_size
                self.fish_direction = -1

            hook_mult = self.get_hook_multiplier()
            line_mult = self.get_line_multiplier()
            fish_center = self.fish_y + fish_size / 2
            if self.bar_y <= fish_center <= self.bar_y + self.bar_height:
                self.catch_progress += 35 * hook_mult * dt
            else:
                self.catch_progress -= 18 * line_mult * dt
            self.catch_progress = max(0, min(100, self.catch_progress))

            if self.catch_progress >= 100:
                self.caught_fish = self.current_fish
                # =========================================================
                # 물고기 잡았을 때 업적 체크
                # update() 안
                # catch_progress >= 100 부분에 추가
                # =========================================================

                self.on_fish_caught()
                self.state        = STATE_RESULT
                self.result_timer = 0
            elif self.catch_progress <= 0:
                self.caught_fish  = None
                self.state        = STATE_RESULT
                self.result_timer = 0
            self.update_splash_particles(dt)

        elif self.state == STATE_RESULT:
            self.result_timer += dt
            if self.result_timer >= 3:
                self.state = STATE_IDLE
                self.reset_game()

    def handle_action(self):
        if self.state == STATE_IDLE:
            self.state           = STATE_CASTING
            self.power           = 0
            self.power_direction = 1
        # =========================================================
        # PERFECT 횟수 증가
        # handle_action() 안
        # STATE_CASTING 부분 수정
        # =========================================================

        elif self.state == STATE_CASTING:

            self.is_perfect_cast = (
                self.perfect_zone_start <= self.power <= self.perfect_zone_end
        )

            if self.is_perfect_cast:
                self.perfect_count += 1

            self.state = STATE_WAITING
            # 낚시 시도 카운트 → 3번마다 배경 전환
            self.cast_count += 1
            if self.cast_count % 3 == 0:
                self.bg_index = (self.bg_index + 1) % len(background_imgs)
        elif self.state == STATE_BITE:
            self.current_fish    = self.select_fish()
            self.fish_speed      = self.current_fish["speed"]
            self.bar_y           = 200
            self.bar_velocity    = 0
            self.fish_y          = random.randint(100, 350)
            self.catch_progress  = 50
            self.state           = STATE_CATCHING


    def draw_idle(self, screen):
        text     = font_medium.render("SPACE/클릭으로 낚시 시작!", True, WHITE)
        text_rect= text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        box_rect = pygame.Rect(text_rect.x - 15, text_rect.y - 10, text_rect.width + 30, text_rect.height + 20)
        pygame.draw.rect(screen, (30, 30, 50), box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)
        screen.blit(text, text_rect)

    # --------------------------------------------------
    # 낚시 - CASTING
    # --------------------------------------------------

    def draw_casting(self, screen):
        gauge_x     = SCREEN_WIDTH // 2 - 150
        gauge_y     = 80
        gauge_width = 300
        gauge_height= 28

        pygame.draw.rect(screen, (30, 30, 50), (gauge_x-6, gauge_y-6, gauge_width+12, gauge_height+12))
        pygame.draw.rect(screen, (60, 60, 80), (gauge_x-6, gauge_y-6, gauge_width+12, gauge_height+12), 3)
        pygame.draw.rect(screen, DARK_GRAY,    (gauge_x, gauge_y, gauge_width, gauge_height))

        perfect_x     = gauge_x + (self.perfect_zone_start / 100) * gauge_width
        perfect_width = ((self.perfect_zone_end - self.perfect_zone_start) / 100) * gauge_width
        pygame.draw.rect(screen, BRIGHT_YELLOW, (perfect_x, gauge_y, perfect_width, gauge_height))
        pygame.draw.rect(screen, YELLOW,        (perfect_x, gauge_y + gauge_height - 4, perfect_width, 4))

        power_width = (self.power / 100) * gauge_width
        pygame.draw.rect(screen, GREEN,       (gauge_x, gauge_y, power_width, gauge_height))
        pygame.draw.rect(screen, BRIGHT_GREEN,(gauge_x, gauge_y, power_width, 4))
        pygame.draw.rect(screen, DARK_GREEN,  (gauge_x, gauge_y + gauge_height - 4, power_width, 4))

        line_x = gauge_x + power_width
        pygame.draw.rect(screen, WHITE, (line_x - 2, gauge_y - 6, 4, gauge_height + 12))

        text = font_small.render(f"파워: {int(self.power)}%", True, WHITE)
        screen.blit(text, (gauge_x, gauge_y + gauge_height + 10))

    # --------------------------------------------------
    # 낚시 - WAITING
    # --------------------------------------------------

    def draw_waiting(self, screen):
        bobber_x = 450 + (self.power / 100) * 300
        bobber_y = 355 + self.bobber_bob
        draw_pixel_fishing_line(screen, (380, 260), (bobber_x, bobber_y - 15), tension=30)
        draw_pixel_bobber(screen, int(bobber_x), int(bobber_y))
        draw_splash_particle(screen, self.splash_particles)

        if self.is_perfect_cast:
            text   = font_large.render("PERFECT!", True, YELLOW)
            shadow = font_large.render("PERFECT!", True, BLACK)
            tr     = text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            screen.blit(shadow, (tr.x + 2, tr.y + 2))
            screen.blit(text, tr)

        dots = "." * (int(self.wait_time * 2) % 4)
        text = font_small.render(f"기다리는 중{dots}", True, WHITE)
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, 50)))

    # --------------------------------------------------
    # 낚시 - BITE
    # --------------------------------------------------

    def draw_bite(self, screen):
        bobber_x = 450 + (self.power / 100) * 300
        bobber_y = 380 + math.sin(self.bite_timer * 25) * 3
        draw_pixel_fishing_line(screen, (380, 260), (bobber_x, bobber_y), tension=40)
        draw_pixel_bobber(screen, int(bobber_x), int(bobber_y), submerged=True)
        draw_splash_particle(screen, self.splash_particles)

        remaining = self.bite_time_limit - self.bite_timer
        color     = RED if remaining < 1 else YELLOW
        if int(self.bite_timer * 10) % 2 == 0:
            text     = font_large.render("!! SPACE/클릭 !!", True, color)
            text_rect= text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            box_rect = pygame.Rect(text_rect.x - 15, text_rect.y - 8, text_rect.width + 30, text_rect.height + 16)
            pygame.draw.rect(screen, (50, 20, 20), box_rect)
            pygame.draw.rect(screen, color, box_rect, 3)
            screen.blit(text, text_rect)

        time_text = font_medium.render(f"{remaining:.1f}초", True, WHITE)
        screen.blit(time_text, time_text.get_rect(center=(SCREEN_WIDTH // 2, 150)))

    # --------------------------------------------------
    # 낚시 - CATCHING
    # --------------------------------------------------

    def draw_catching(self, screen):
        cyl_x = SCREEN_WIDTH - 130
        cyl_y = 80
        cyl_w = 70
        cyl_h = 340

        draw_pixel_cylinder(screen, cyl_x, cyl_y, cyl_w, cyl_h)
        bar_active = self.is_fish_in_bar()
        draw_pixel_bar(screen, cyl_x + 6, int(self.bar_y), cyl_w - 12, self.bar_height, bar_active)

        fish_name  = self.current_fish["name"]
        fish_img   = fish_images.get(fish_name)
        scaled_img = pygame.transform.scale(fish_img, (50, 50))
        if self.fish_direction < 0:
            scaled_img = pygame.transform.flip(scaled_img, True, False)
        screen.blit(scaled_img, (cyl_x + 10, int(self.fish_y) - 5))

        prog_x = cyl_x - 50
        prog_w = 25
        prog_h = cyl_h
        pygame.draw.rect(screen, (30, 30, 50), (prog_x-4, cyl_y-4, prog_w+8, prog_h+8))
        pygame.draw.rect(screen, (60, 60, 80), (prog_x-4, cyl_y-4, prog_w+8, prog_h+8), 3)
        pygame.draw.rect(screen, DARK_GRAY,    (prog_x, cyl_y, prog_w, prog_h))

        fill_h = (self.catch_progress / 100) * prog_h
        fill_y = cyl_y + prog_h - fill_h
        if   self.catch_progress > 70: pc, lc = GREEN,  BRIGHT_GREEN
        elif self.catch_progress > 30: pc, lc = YELLOW, BRIGHT_YELLOW
        else:                          pc, lc = RED,    BRIGHT_RED
        pygame.draw.rect(screen, pc, (prog_x, fill_y, prog_w, fill_h))
        pygame.draw.rect(screen, lc, (prog_x, fill_y, 4, fill_h))

        bobber_x = 450 + (self.power / 100) * 300
        bobber_y = 370 + math.sin(pygame.time.get_ticks() / 80) * 4
        draw_pixel_fishing_line(screen, (380, 260), (bobber_x, bobber_y - 10), tension=35)
        draw_pixel_bobber(screen, int(bobber_x), int(bobber_y), submerged=True)
        if random.random() < 0.3:
            self.add_splash_particle(bobber_x, 370)
        draw_splash_particle(screen, self.splash_particles)

        info_box = pygame.Rect(30, 100, 200, 80)
        pygame.draw.rect(screen, (30, 30, 50), info_box)
        pygame.draw.rect(screen, WHITE, info_box, 2)
        screen.blit(font_medium.render(self.current_fish["name"], True, WHITE), (45, 110))
        rarity     = self.current_fish["rarity"]
        rarity_txt = font_small.render(f"[{RARITY_KR[rarity]}]", True, RARITY_COLORS[rarity])
        screen.blit(rarity_txt, (45, 145))
        screen.blit(font_tiny.render("SPACE/클릭: 올라가기", True, WHITE), (30, SCREEN_HEIGHT - 40))

    def is_fish_in_bar(self):
        if not self.current_fish:
            return False
        return self.bar_y <= self.fish_y + 20 <= self.bar_y + self.bar_height

    # --------------------------------------------------
    # 낚시 - RESULT
    # --------------------------------------------------

    def draw_result(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))

        if self.caught_fish:
            rarity = self.caught_fish["rarity"]
            label  = "뭔가를 건졌다..." if rarity == "trash" else "물고기를 잡았다!"
            color  = GRAY if rarity == "trash" else GREEN
            screen.blit(font_large.render(label, True, color),
                        font_large.render(label, True, color).get_rect(center=(SCREEN_WIDTH//2, 150)))
            screen.blit(font_large.render(self.caught_fish["name"], True, WHITE),
                        font_large.render(self.caught_fish["name"], True, WHITE).get_rect(center=(SCREEN_WIDTH//2, 210)))
            rtxt = font_medium.render(f"[{RARITY_KR[rarity]}] - {self.caught_fish['price']}G",
                                      True, RARITY_COLORS[rarity])
            screen.blit(rtxt, rtxt.get_rect(center=(SCREEN_WIDTH//2, 260)))
            if len(self.inventory) >= self.get_bag_size():
                ft = font_small.render("가방이 가득 찼습니다!", True, RED)
                screen.blit(ft, ft.get_rect(center=(SCREEN_WIDTH//2, 420)))
            img = pygame.transform.scale(fish_images[self.caught_fish["name"]], (120, 120))
            screen.blit(img, (SCREEN_WIDTH//2 - 60, 290))
        else:
            t = font_large.render("놓쳤다...", True, RED)
            screen.blit(t, t.get_rect(center=(SCREEN_WIDTH//2, 220)))

        ct = font_tiny.render("잠시 후 자동으로 계속됩니다...", True, GRAY)
        screen.blit(ct, ct.get_rect(center=(SCREEN_WIDTH//2, 450)))
