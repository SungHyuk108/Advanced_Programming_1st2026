import pygame
import random
import math
import os
import sys

pygame.init()

# =========================================================
# 화면 설정
# =========================================================

SCALE = 2
BASE_WIDTH = 512
BASE_HEIGHT = 288
SCREEN_WIDTH = BASE_WIDTH * SCALE   # 1024
SCREEN_HEIGHT = BASE_HEIGHT * SCALE # 576

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Fishing Game")

# =========================================================
# FPS 설정
# =========================================================

clock = pygame.time.Clock()
FPS = 60

# =========================================================
# 색상 팔레트
# =========================================================

WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
RED         = (220, 60, 60)
BRIGHT_RED  = (255, 80, 80)
DARK_RED    = (160, 40, 40)
GREEN       = (60, 179, 113)
BRIGHT_GREEN= (100, 220, 140)
DARK_GREEN  = (40, 130, 80)
YELLOW      = (255, 215, 0)
BRIGHT_YELLOW=(255, 240, 100)
GRAY        = (128, 128, 128)
DARK_GRAY   = (64, 64, 64)
LIGHT_GRAY  = (200, 200, 200)
CYAN        = (100, 200, 255)
LIGHT_CYAN  = (180, 230, 255)
BROWN       = (139, 90, 43)
DARK_BROWN  = (101, 67, 33)
LIGHT_BROWN = (180, 130, 70)
OFF_WHITE   = (240, 240, 240)

BACKGROUND_COLOR  = (120, 190, 255)
BUTTON_COLOR      = (240, 240, 240)
BUTTON_HOVER_COLOR= (180, 220, 255)
TITLE_COLOR       = (255, 255, 255)

# =========================================================
# 한글 폰트 설정
# =========================================================

def get_korean_font(size):
    font_names = [
        "malgun gothic", "malgungothic", "AppleGothic", "Apple SD Gothic Neo",
        "NanumGothic", "NanumBarunGothic", "gulim", "dotum", "batang",
    ]
    for font_name in font_names:
        try:
            font = pygame.font.SysFont(font_name, size)
            test_surface = font.render("테스트", True, WHITE)
            if test_surface.get_width() > 10:
                return font
        except:
            continue
    return pygame.font.Font(None, size)

font_large  = get_korean_font(40)
font_medium = get_korean_font(28)
font_small  = get_korean_font(20)
font_tiny   = get_korean_font(16)

TITLE_FONT = get_korean_font(80)
MENU_FONT  = get_korean_font(30)

# =========================================================
# 게임 상태
# =========================================================

STATE_TITLE     = 0
STATE_IDLE      = 1
STATE_CASTING   = 2
STATE_WAITING   = 3
STATE_BITE      = 4
STATE_CATCHING  = 5
STATE_RESULT    = 6
STATE_INVENTORY = 7
STATE_SHOP_MAIN     = 8
STATE_SHOP_CATEGORY = 9
STATE_COLLECTION    = 10   # 도감
STATE_ACHIEVEMENT   = 11   # 업적

# =========================================================
# 경로 설정
# =========================================================

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

# =========================================================
# 이미지 로드 함수
# =========================================================

def load_image(path, scale=None):
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img

def load_image_jpg(path, scale=None):
    img = pygame.image.load(path).convert()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img

# =========================================================
# 에셋 로드
# =========================================================

background_img = load_image(os.path.join(ASSETS_PATH, "background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
fisherman_img  = load_image(os.path.join(ASSETS_PATH, "fisherman.png"), (128, 128))
shop_img       = load_image_jpg(os.path.join(ASSETS_PATH, "shop.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

fish_images = {
    "해초"    : load_image(os.path.join(ASSETS_PATH, "seaweed.png")),
    "바다장어" : load_image(os.path.join(ASSETS_PATH, "conger_eel.png")),
    "황새치"  : load_image(os.path.join(ASSETS_PATH, "swordfish.png")),
    "참치"    : load_image(os.path.join(ASSETS_PATH, "tuna.png")),
    "연어"    : load_image(os.path.join(ASSETS_PATH, "salmon.png")),
    "숭어"    : load_image(os.path.join(ASSETS_PATH, "mullet.png")),
    "상어"    : load_image(os.path.join(ASSETS_PATH, "shark.png")),
    "돌고래"  : load_image(os.path.join(ASSETS_PATH, "dolphin.png")),
    "날치"    : load_image(os.path.join(ASSETS_PATH, "flying_fish.png")),
    "쓰레기"  : load_image(os.path.join(ASSETS_PATH, "trash.png")),
    "멸치"    : load_image(os.path.join(ASSETS_PATH, "anchovy.png")),
}

# =========================================================
# 물고기 데이터
# =========================================================

FISH_DATA = [
    {"name": "쓰레기",  "rarity": "trash",     "speed": 1.5, "price": 1},
    {"name": "해초",    "rarity": "trash",     "speed": 1,   "price": 2},
    {"name": "멸치",    "rarity": "common",    "speed": 2,   "price": 15},
    {"name": "숭어",    "rarity": "common",    "speed": 2.5, "price": 30},
    {"name": "날치",    "rarity": "uncommon",  "speed": 3,   "price": 60},
    {"name": "연어",    "rarity": "uncommon",  "speed": 3.5, "price": 100},
    {"name": "참치",    "rarity": "rare",      "speed": 4,   "price": 200},
    {"name": "바다장어","rarity": "rare",      "speed": 4.5, "price": 280},
    {"name": "황새치",  "rarity": "epic",      "speed": 5.5, "price": 450},
    {"name": "돌고래",  "rarity": "legendary", "speed": 6,   "price": 800},
    {"name": "상어",    "rarity": "legendary", "speed": 7,   "price": 1200},
]

RARITY_COLORS = {
    "trash"    : GRAY,
    "common"   : WHITE,
    "uncommon" : GREEN,
    "rare"     : (100, 149, 237),
    "epic"     : (186, 85, 211),
    "legendary": YELLOW,
}

RARITY_KR = {
    "trash"    : "잡동사니",
    "common"   : "일반",
    "uncommon" : "고급",
    "rare"     : "희귀",
    "epic"     : "영웅",
    "legendary": "전설",
}

# =========================================================
# 상점 데이터
# =========================================================

SHOP_DATA = {
    "미끼": {
        "items"      : ["두꺼운지렁이", "장수풍뎅이", "소고기", "랍스타", "캐비어"],
        "prices"     : [50, 150, 400, 1000, 3000],
        "effects"    : [1.1, 1.25, 1.5, 1.8, 2.5],
        "description": "희귀 물고기 확률 증가 (소모품)",
        "consumable" : True,
    },
    "릴": {
        "items"      : ["고급", "합금", "카본", "금", "다이아"],
        "prices"     : [200, 600, 1500, 4000, 10000],
        "effects"    : [1.15, 1.3, 1.5, 1.75, 2.0],
        "description": "당기는 속도 증가",
        "consumable" : False,
    },
    "낚싯바늘": {
        "items"      : ["고급", "합금", "카본", "금", "다이아"],
        "prices"     : [200, 600, 1500, 4000, 10000],
        "effects"    : [1.15, 1.3, 1.5, 1.75, 2.0],
        "description": "게이지 증가 속도 증가",
        "consumable" : False,
    },
    "낚싯줄": {
        "items"      : ["고급", "합금", "카본", "금", "다이아"],
        "prices"     : [200, 600, 1500, 4000, 10000],
        "effects"    : [0.9, 0.8, 0.65, 0.5, 0.3],
        "description": "게이지 감소 속도 감소",
        "consumable" : False,
    },
    "가방": {
        "items"      : ["고급", "합금", "카본", "금", "다이아"],
        "prices"     : [300, 800, 2000, 5000, 12000],
        "effects"    : [15, 20, 30, 50, 100],
        "description": "가방 크기 증가",
        "consumable" : False,
    },
}

# =========================================================
# 픽셀 그리기 함수들
# =========================================================

def draw_pixel_bobber(surface, x, y, submerged=False):
    p = 2
    if not submerged:
        pygame.draw.rect(surface, OFF_WHITE,   (x - 3*p, y - 10*p, 6*p, 3*p))
        pygame.draw.rect(surface, WHITE,       (x - 2*p, y - 11*p, 4*p, p))
        pygame.draw.rect(surface, LIGHT_GRAY,  (x - 3*p, y - 7*p,  6*p, p))
        pygame.draw.rect(surface, BRIGHT_RED,  (x - 4*p, y - 6*p,  8*p, 2*p))
        pygame.draw.rect(surface, RED,         (x - 5*p, y - 4*p, 10*p, 6*p))
        pygame.draw.rect(surface, DARK_RED,    (x - 4*p, y + 2*p,  8*p, 3*p))
        pygame.draw.rect(surface, DARK_RED,    (x - 3*p, y + 5*p,  6*p, 2*p))
        pygame.draw.rect(surface, BRIGHT_RED,  (x - 3*p, y - 4*p,  2*p, 4*p))
    else:
        pygame.draw.rect(surface, (180, 80, 80), (x - 3*p, y - 2*p, 6*p, 4*p))


def draw_pixel_fishing_line(surface, start, end, tension=0):
    x1, y1 = start
    x2, y2 = end
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2 + tension
    points = []
    for t in range(21):
        t = t / 20
        px = (1-t)**2 * x1 + 2*(1-t)*t * mid_x + t**2 * x2
        py = (1-t)**2 * y1 + 2*(1-t)*t * mid_y + t**2 * y2
        points.append((int(px), int(py)))
    for i in range(len(points) - 1):
        pygame.draw.line(surface, LIGHT_GRAY, points[i], points[i+1], 2)
        pygame.draw.line(surface, WHITE, (points[i][0], points[i][1]-1),
                         (points[i+1][0], points[i+1][1]-1), 1)


def draw_pixel_cylinder(surface, x, y, width, height):
    p = 2
    pygame.draw.rect(surface, (20, 50, 100), (x - p*2, y - p*2, width + p*4, height + p*4))
    for i in range(0, height, p*4):
        ratio = i / height
        r = int(35 + ratio * 15)
        g = int(100 - ratio * 30)
        b = int(170 - ratio * 30)
        pygame.draw.rect(surface, (r, g, b), (x, y + i, width, p*4))
    wave_time = pygame.time.get_ticks() / 500
    for wy in range(0, height, p*8):
        wave_offset = int(math.sin(wave_time + wy / 20) * p)
        pygame.draw.rect(surface, (50, 120, 190), (x + wave_offset, y + wy, p*2, p*4))
        pygame.draw.rect(surface, (50, 120, 190), (x + width - p*4 + wave_offset, y + wy + p*4, p*2, p*4))
    pygame.draw.rect(surface, (80, 150, 210), (x, y, p*2, height))
    pygame.draw.rect(surface, (20, 60, 120),  (x + width - p*2, y, p*2, height))
    pygame.draw.rect(surface, (60, 90, 140),  (x - p, y - p, width + p*2, p*2))
    pygame.draw.rect(surface, (60, 90, 140),  (x - p, y + height - p, width + p*2, p*2))


def draw_pixel_bar(surface, x, y, width, height, active=False):
    p = 2
    if active:
        main_color  = BRIGHT_GREEN
        light_color = (150, 255, 180)
        dark_color  = DARK_GREEN
    else:
        main_color  = (80, 160, 100)
        light_color = (120, 200, 140)
        dark_color  = (50, 120, 70)
    pygame.draw.rect(surface, main_color,  (x, y, width, height))
    pygame.draw.rect(surface, light_color, (x, y, width, p*2))
    pygame.draw.rect(surface, light_color, (x, y, p*2, height))
    pygame.draw.rect(surface, dark_color,  (x, y + height - p*2, width, p*2))
    pygame.draw.rect(surface, dark_color,  (x + width - p*2, y, p*2, height))
    for py in range(p*4, height - p*4, p*6):
        pygame.draw.rect(surface, light_color, (x + p*4, y + py, width - p*8, p))


def draw_splash_particle(surface, particles):
    for p in particles:
        size = int(p['size'] * p['life'])
        if size > 0:
            pygame.draw.circle(surface, LIGHT_CYAN, (int(p['x']), int(p['y'])), size + 1)
            pygame.draw.circle(surface, CYAN,       (int(p['x']), int(p['y'])), size)
            if size > 2:
                pygame.draw.circle(surface, WHITE, (int(p['x']) - 1, int(p['y']) - 1), size // 2)

# =========================================================
# 타이틀 화면 변수
# =========================================================

title_text   = "FISHING GAME"
title_y      = -150
title_target_y = 100
title_speed  = 5
show_menu    = False

# 메뉴 버튼 설정
button_width  = 250
button_height = 55
button_gap    = 15

menu_buttons = [
    {"text": "낚시",  "scene": STATE_IDLE},
    {"text": "상점",  "scene": STATE_SHOP_MAIN},
    {"text": "가방",  "scene": STATE_INVENTORY},
    {"text": "도감",  "scene": STATE_COLLECTION},
    {"text": "업적",  "scene": STATE_ACHIEVEMENT},
]

button_rects = []
start_y = 220

for i in range(len(menu_buttons)):
    rect = pygame.Rect(
        SCREEN_WIDTH // 2 - button_width // 2,
        start_y + i * (button_height + button_gap),
        button_width,
        button_height,
    )
    button_rects.append(rect)

# =========================================================
# 메인 게임 클래스
# =========================================================

class FishingGame:

    def __init__(self):
        self.state        = STATE_TITLE
        self.inventory    = []
        self.total_money  = 500
        self.max_inventory= 10
        self.discovered   = set()   # 도감: 발견한 물고기 이름 저장

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

        self.reset_game()

    # --------------------------------------------------
    # 장비 배수 헬퍼
    # --------------------------------------------------

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

    # --------------------------------------------------
    # 게임 변수 초기화
    # --------------------------------------------------

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

    def update(self, dt, action_pressed):
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
                self.discovered.add(self.caught_fish["name"])   # 도감 등록
                if len(self.inventory) < self.get_bag_size():
                    self.inventory.append(self.caught_fish)
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

    # --------------------------------------------------
    # 액션 핸들러
    # --------------------------------------------------

    def handle_action(self):
        if self.state == STATE_IDLE:
            self.state           = STATE_CASTING
            self.power           = 0
            self.power_direction = 1
        elif self.state == STATE_CASTING:
            self.is_perfect_cast = (self.perfect_zone_start <= self.power <= self.perfect_zone_end)
            self.state           = STATE_WAITING
            self.wait_time       = 0
            self.max_wait_time   = random.uniform(3, 6)
            self.splash_particles= []
        elif self.state == STATE_BITE:
            self.current_fish    = self.select_fish()
            self.fish_speed      = self.current_fish["speed"]
            self.bar_y           = 200
            self.bar_velocity    = 0
            self.fish_y          = random.randint(100, 350)
            self.catch_progress  = 50
            self.state           = STATE_CATCHING

    def sell_all_fish(self):
        for fish in self.inventory:
            self.total_money += fish["price"]
        self.inventory = []

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

    # --------------------------------------------------
    # 마우스 클릭 처리
    # --------------------------------------------------

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

    # ==================================================
    # 전체 그리기
    # ==================================================

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

    # --------------------------------------------------
    # 타이틀 화면
    # --------------------------------------------------

    def draw_title(self, screen):
        global title_y, show_menu

        screen.fill(BACKGROUND_COLOR)

        # 타이틀 내려오는 애니메이션
        if title_y < title_target_y:
            title_y += title_speed
        else:
            show_menu = True

        title_surface = TITLE_FONT.render(title_text, True, TITLE_COLOR)
        title_rect    = title_surface.get_rect(center=(SCREEN_WIDTH // 2, title_y))
        screen.blit(title_surface, title_rect)

        if show_menu:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(button_rects):
                color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(screen, color, rect, border_radius=15)
                text_surface = MENU_FONT.render(menu_buttons[i]["text"], True, BLACK)
                text_rect    = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

        hint = font_tiny.render("ESC: 타이틀로 돌아가기", True, (200, 230, 255))
        screen.blit(hint, (10, SCREEN_HEIGHT - 25))

    # --------------------------------------------------
    # 배경
    # --------------------------------------------------

    def draw_background(self, screen):
        screen.blit(background_img, (0, 0))
        pygame.draw.rect(screen, (120, 80, 45),  (290, 340, 100, 14))
        pygame.draw.rect(screen, (140, 95, 55),  (290, 340, 100, 4))
        pygame.draw.rect(screen, (90, 60, 35),   (290, 350, 100, 4))
        for px in [300, 340, 375]:
            pygame.draw.rect(screen, (100, 70, 40),  (px, 354, 14, 50))
            pygame.draw.rect(screen, (120, 85, 50),  (px, 354, 4,  50))
            pygame.draw.rect(screen, (80, 55, 30),   (px + 10, 354, 4, 50))
        screen.blit(fisherman_img, (295, 205))

    # --------------------------------------------------
    # HUD
    # --------------------------------------------------

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

    # --------------------------------------------------
    # 낚시 - IDLE
    # --------------------------------------------------

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

    # --------------------------------------------------
    # 가방 화면
    # --------------------------------------------------

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

    # --------------------------------------------------
    # 업적 화면 (임시)
    # --------------------------------------------------

    def draw_achievement(self, screen):
        screen.fill((30, 20, 40))
        t = font_large.render("업적 (준비중)", True, WHITE)
        screen.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        ct = font_tiny.render("[ESC] 닫기", True, GRAY)
        screen.blit(ct, ct.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)))

    # --------------------------------------------------
    # 상점
    # --------------------------------------------------

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


# =========================================================
# 메인 루프
# =========================================================

def main():
    game    = FishingGame()
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        keys          = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        action_pressed= mouse_pressed or keys[pygame.K_SPACE]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # -----------------------------------------------
            # 키 입력
            # -----------------------------------------------
            elif event.type == pygame.KEYDOWN:

                # ESC: 어디서든 타이틀로 돌아가기
                if event.key == pygame.K_ESCAPE:
                    if game.state == STATE_INVENTORY:
                        game.state = STATE_IDLE
                    elif game.state == STATE_SHOP_CATEGORY:
                        game.state = STATE_SHOP_MAIN
                    elif game.state in [STATE_SHOP_MAIN, STATE_COLLECTION, STATE_ACHIEVEMENT]:
                        game.state = STATE_TITLE
                    elif game.state != STATE_TITLE:
                        game.state = STATE_TITLE

                elif event.key == pygame.K_SPACE:
                    if game.state not in [STATE_TITLE, STATE_SHOP_MAIN,
                                          STATE_SHOP_CATEGORY, STATE_COLLECTION, STATE_ACHIEVEMENT]:
                        game.handle_action()

                elif event.key == pygame.K_i:
                    if game.state == STATE_IDLE:
                        game.state = STATE_INVENTORY
                    elif game.state == STATE_INVENTORY:
                        game.state = STATE_IDLE

                elif event.key == pygame.K_p:
                    if game.state == STATE_IDLE:
                        game.state = STATE_SHOP_MAIN
                    elif game.state in [STATE_SHOP_MAIN, STATE_SHOP_CATEGORY]:
                        game.state = STATE_IDLE

                elif event.key == pygame.K_s:
                    if game.state == STATE_INVENTORY:
                        game.sell_all_fish()

                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    if game.state == STATE_SHOP_CATEGORY:
                        game.buy_item(game.shop_category, event.key - pygame.K_1)

            # -----------------------------------------------
            # 마우스 클릭
            # -----------------------------------------------
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.state == STATE_TITLE and show_menu:
                    for i, rect in enumerate(button_rects):
                        if rect.collidepoint(event.pos):
                            game.state = menu_buttons[i]["scene"]
                            break
                elif game.state in [STATE_SHOP_MAIN, STATE_SHOP_CATEGORY]:
                    game.handle_shop_click(event.pos)
                elif game.state not in [STATE_COLLECTION, STATE_ACHIEVEMENT, STATE_INVENTORY]:
                    game.handle_action()

        # ---------------------------------------------------
        # 업데이트 & 그리기
        # ---------------------------------------------------
        game.update(dt, action_pressed)
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()