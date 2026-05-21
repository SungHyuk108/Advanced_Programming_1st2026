import pygame
import random
import math
import os

pygame.init()

# 화면 설정 - 배경 이미지 크기에 맞춤 (512x288을 2배로 스케일)
SCALE = 2
BASE_WIDTH = 512
BASE_HEIGHT = 288
SCREEN_WIDTH = BASE_WIDTH * SCALE
SCREEN_HEIGHT = BASE_HEIGHT * SCALE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Fishing Game")

# 색상 팔레트
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
BRIGHT_RED = (255, 80, 80)
DARK_RED = (160, 40, 40)
GREEN = (60, 179, 113)
BRIGHT_GREEN = (100, 220, 140)
DARK_GREEN = (40, 130, 80)
YELLOW = (255, 215, 0)
BRIGHT_YELLOW = (255, 240, 100)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (200, 200, 200)
CYAN = (100, 200, 255)
LIGHT_CYAN = (180, 230, 255)
BROWN = (139, 90, 43)
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (180, 130, 70)
OFF_WHITE = (240, 240, 240)

# 한글 폰트 설정
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

font_large = get_korean_font(40)
font_medium = get_korean_font(28)
font_small = get_korean_font(20)
font_tiny = get_korean_font(16)

# 게임 상태
STATE_IDLE = 0
STATE_CASTING = 1
STATE_WAITING = 2
STATE_BITE = 3
STATE_CATCHING = 4
STATE_RESULT = 5
STATE_INVENTORY = 6
STATE_SHOP_MAIN = 7
STATE_SHOP_CATEGORY = 8

# 경로 설정
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

# 이미지 로드 함수
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

# 배경/캐릭터 이미지
background_img = load_image(os.path.join(ASSETS_PATH, "background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
fisherman_img = load_image(os.path.join(ASSETS_PATH, "fisherman.png"), (128, 128))
shop_img = load_image_jpg(os.path.join(ASSETS_PATH, "shop.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# 물고기 이미지 로드
fish_images = {
    "해초": load_image(os.path.join(ASSETS_PATH, "seaweed.png")),
    "바다장어": load_image(os.path.join(ASSETS_PATH, "conger_eel.png")),
    "황새치": load_image(os.path.join(ASSETS_PATH, "swordfish.png")),
    "참치": load_image(os.path.join(ASSETS_PATH, "tuna.png")),
    "연어": load_image(os.path.join(ASSETS_PATH, "salmon.png")),
    "숭어": load_image(os.path.join(ASSETS_PATH, "mullet.png")),
    "상어": load_image(os.path.join(ASSETS_PATH, "shark.png")),
    "돌고래": load_image(os.path.join(ASSETS_PATH, "dolphin.png")),
    "날치": load_image(os.path.join(ASSETS_PATH, "flying_fish.png")),
    "쓰레기": load_image(os.path.join(ASSETS_PATH, "trash.png")),
    "멸치": load_image(os.path.join(ASSETS_PATH, "anchovy.png")),
}

# 물고기 데이터
FISH_DATA = [
    {"name": "쓰레기", "rarity": "trash", "speed": 1.5, "price": 1},
    {"name": "해초", "rarity": "trash", "speed": 1, "price": 2},
    {"name": "멸치", "rarity": "common", "speed": 2, "price": 15},
    {"name": "숭어", "rarity": "common", "speed": 2.5, "price": 30},
    {"name": "날치", "rarity": "uncommon", "speed": 3, "price": 60},
    {"name": "연어", "rarity": "uncommon", "speed": 3.5, "price": 100},
    {"name": "참치", "rarity": "rare", "speed": 4, "price": 200},
    {"name": "바다장어", "rarity": "rare", "speed": 4.5, "price": 280},
    {"name": "황새치", "rarity": "epic", "speed": 5.5, "price": 450},
    {"name": "돌고래", "rarity": "legendary", "speed": 6, "price": 800},
    {"name": "상어", "rarity": "legendary", "speed": 7, "price": 1200},
]

# 상점 데이터
SHOP_DATA = {
    "미끼": {
        "items": ["두꺼운지렁이", "장수풍뎅이", "소고기", "랍스타", "캐비어"],
        "prices": [50, 150, 400, 1000, 3000],
        "effects": [1.1, 1.25, 1.5, 1.8, 2.5],  # 희귀 물고기 확률 배수
        "description": "희귀 물고기 확률 증가 (소모품)",
        "consumable": True
    },
    "릴": {
        "items": ["고급", "합금", "카본", "금", "다이아"],
        "prices": [200, 600, 1500, 4000, 10000],
        "effects": [1.15, 1.3, 1.5, 1.75, 2.0],  # 최고 속도 배수
        "description": "당기는 속도 증가",
        "consumable": False
    },
    "낚싯바늘": {
        "items": ["고급", "합금", "카본", "금", "다이아"],
        "prices": [200, 600, 1500, 4000, 10000],
        "effects": [1.15, 1.3, 1.5, 1.75, 2.0],  # 게이지 증가 속도 배수
        "description": "게이지 증가 속도 증가",
        "consumable": False
    },
    "낚싯줄": {
        "items": ["고급", "합금", "카본", "금", "다이아"],
        "prices": [200, 600, 1500, 4000, 10000],
        "effects": [0.9, 0.8, 0.65, 0.5, 0.3],  # 게이지 감소 속도 배수
        "description": "게이지 감소 속도 감소",
        "consumable": False
    },
    "가방": {
        "items": ["고급", "합금", "카본", "금", "다이아"],
        "prices": [300, 800, 2000, 5000, 12000],
        "effects": [15, 20, 30, 50, 100],  # 가방 크기
        "description": "가방 크기 증가",
        "consumable": False
    }
}


def draw_pixel_bobber(surface, x, y, submerged=False):
    p = 2
    if not submerged:
        pygame.draw.rect(surface, OFF_WHITE, (x - 3*p, y - 10*p, 6*p, 3*p))
        pygame.draw.rect(surface, WHITE, (x - 2*p, y - 11*p, 4*p, p))
        pygame.draw.rect(surface, LIGHT_GRAY, (x - 3*p, y - 7*p, 6*p, p))
        pygame.draw.rect(surface, BRIGHT_RED, (x - 4*p, y - 6*p, 8*p, 2*p))
        pygame.draw.rect(surface, RED, (x - 5*p, y - 4*p, 10*p, 6*p))
        pygame.draw.rect(surface, DARK_RED, (x - 4*p, y + 2*p, 8*p, 3*p))
        pygame.draw.rect(surface, DARK_RED, (x - 3*p, y + 5*p, 6*p, 2*p))
        pygame.draw.rect(surface, BRIGHT_RED, (x - 3*p, y - 4*p, 2*p, 4*p))
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
        pygame.draw.line(surface, WHITE, (points[i][0], points[i][1]-1), (points[i+1][0], points[i+1][1]-1), 1)


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
    pygame.draw.rect(surface, (20, 60, 120), (x + width - p*2, y, p*2, height))
    pygame.draw.rect(surface, (60, 90, 140), (x - p, y - p, width + p*2, p*2))
    pygame.draw.rect(surface, (60, 90, 140), (x - p, y + height - p, width + p*2, p*2))


def draw_pixel_bar(surface, x, y, width, height, active=False):
    p = 2
    if active:
        main_color = BRIGHT_GREEN
        light_color = (150, 255, 180)
        dark_color = DARK_GREEN
    else:
        main_color = (80, 160, 100)
        light_color = (120, 200, 140)
        dark_color = (50, 120, 70)
    
    pygame.draw.rect(surface, main_color, (x, y, width, height))
    pygame.draw.rect(surface, light_color, (x, y, width, p*2))
    pygame.draw.rect(surface, light_color, (x, y, p*2, height))
    pygame.draw.rect(surface, dark_color, (x, y + height - p*2, width, p*2))
    pygame.draw.rect(surface, dark_color, (x + width - p*2, y, p*2, height))
    
    for py in range(p*4, height - p*4, p*6):
        pygame.draw.rect(surface, light_color, (x + p*4, y + py, width - p*8, p))


def draw_splash_particle(surface, particles):
    for p in particles:
        size = int(p['size'] * p['life'])
        if size > 0:
            pygame.draw.circle(surface, LIGHT_CYAN, (int(p['x']), int(p['y'])), size + 1)
            pygame.draw.circle(surface, CYAN, (int(p['x']), int(p['y'])), size)
            if size > 2:
                pygame.draw.circle(surface, WHITE, (int(p['x']) - 1, int(p['y']) - 1), size // 2)


class FishingGame:
    def __init__(self):
        self.state = STATE_IDLE
        self.inventory = []
        self.total_money = 500  # 시작 자금
        self.max_inventory = 10  # 기본 가방 크기
        
        # 장비 레벨 (0 = 기본, 1~5 = 업그레이드)
        self.equipment = {
            "릴": 0,
            "낚싯바늘": 0,
            "낚싯줄": 0,
            "가방": 0
        }
        
        # 미끼 (소모품)
        self.bait = None  # None 또는 {"name": "...", "effect": ...}
        self.bait_count = 0
        
        # 상점 관련
        self.shop_category = None
        self.shop_scroll = 0
        
        self.reset_game()
        
    def reset_game(self):
        self.power = 0
        self.power_direction = 1
        self.perfect_zone_start = random.randint(60, 80)
        self.perfect_zone_end = self.perfect_zone_start + 15
        self.is_perfect_cast = False
        
        self.wait_time = 0
        self.max_wait_time = random.uniform(3, 6)
        self.bobber_bob = 0
        self.splash_particles = []
        
        self.bite_timer = 0
        self.bite_time_limit = 2.0
        
        self.bar_y = 200
        self.bar_height = 70
        self.bar_velocity = 0
        self.bar_max_speed = 6 * self.get_reel_multiplier()
        self.bar_accel_time = 0.5
        self.bar_accel_rate = self.bar_max_speed / self.bar_accel_time
        
        self.fish_y = 150
        self.fish_direction = 1
        self.fish_speed = 3
        self.catch_progress = 50
        self.current_fish = None
        self.caught_fish = None
        self.result_timer = 0
    
    def get_reel_multiplier(self):
        level = self.equipment["릴"]
        if level == 0:
            return 1.0
        return SHOP_DATA["릴"]["effects"][level - 1]
    
    def get_hook_multiplier(self):
        level = self.equipment["낚싯바늘"]
        if level == 0:
            return 1.0
        return SHOP_DATA["낚싯바늘"]["effects"][level - 1]
    
    def get_line_multiplier(self):
        level = self.equipment["낚싯줄"]
        if level == 0:
            return 1.0
        return SHOP_DATA["낚싯줄"]["effects"][level - 1]
    
    def get_bag_size(self):
        level = self.equipment["가방"]
        if level == 0:
            return 10
        return SHOP_DATA["가방"]["effects"][level - 1]
        
    def select_fish(self):
        weights = [15, 10, 25, 20, 12, 8, 5, 3, 1.5, 0.4, 0.1]
        
        # 퍼펙트 캐스트 보너스
        if self.is_perfect_cast:
            weights = [5, 5, 20, 20, 18, 15, 10, 4, 2, 0.7, 0.3]
        
        # 미끼 보너스 (희귀 물고기 확률 증가)
        if self.bait:
            bait_effect = self.bait["effect"]
            # 일반 이하 감소, 고급 이상 증가
            for i in range(4):  # trash, trash, common, common
                weights[i] /= bait_effect
            for i in range(4, len(weights)):  # uncommon 이상
                weights[i] *= bait_effect
            
            # 미끼 소모
            self.bait_count -= 1
            if self.bait_count <= 0:
                self.bait = None
                self.bait_count = 0
        
        total = sum(weights)
        r = random.uniform(0, total)
        cumulative = 0
        for i, w in enumerate(weights):
            cumulative += w
            if r <= cumulative:
                return FISH_DATA[i].copy()
        return FISH_DATA[0].copy()
    
    def add_splash_particle(self, x, y):
        for _ in range(3):
            self.splash_particles.append({
                'x': x + random.randint(-15, 15),
                'y': y,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-6, -3),
                'life': 1.0,
                'size': random.randint(3, 6)
            })
    
    def update_splash_particles(self, dt):
        for p in self.splash_particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 12 * dt
            p['life'] -= dt * 1.5
            if p['life'] <= 0:
                self.splash_particles.remove(p)
    
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
            self.wait_time += dt
            self.bobber_bob = math.sin(self.wait_time * 3) * 4
            
            bobber_x = 450 + (self.power / 100) * 300
            if random.random() < 0.15:
                self.add_splash_particle(bobber_x, 365)
            self.update_splash_particles(dt)
            
            if self.wait_time >= self.max_wait_time:
                self.state = STATE_BITE
                self.bite_timer = 0
                
        elif self.state == STATE_BITE:
            self.bite_timer += dt
            self.update_splash_particles(dt)
            
            bobber_x = 450 + (self.power / 100) * 300
            if random.random() < 0.4:
                self.add_splash_particle(bobber_x, 380)
            
            if self.bite_timer >= self.bite_time_limit:
                self.state = STATE_RESULT
                self.caught_fish = None
                self.result_timer = 0
                
        elif self.state == STATE_CATCHING:
            if action_pressed:
                self.bar_velocity -= self.bar_accel_rate * dt
            else:
                self.bar_velocity += (self.bar_accel_rate / 1.5) * dt
            
            self.bar_velocity = max(-self.bar_max_speed, min(self.bar_max_speed, self.bar_velocity))
            self.bar_y += self.bar_velocity
            
            cylinder_top = 80
            cylinder_bottom = 420
            if self.bar_y <= cylinder_top:
                self.bar_y = cylinder_top
                self.bar_velocity = 0
            elif self.bar_y >= cylinder_bottom - self.bar_height:
                self.bar_y = cylinder_bottom - self.bar_height
                self.bar_velocity = 0
            
            self.fish_y += self.fish_direction * self.fish_speed
            
            if random.random() < 0.02:
                self.fish_direction *= -1
            
            fish_size = 40
            if self.fish_y <= cylinder_top:
                self.fish_y = cylinder_top
                self.fish_direction = 1
            elif self.fish_y >= cylinder_bottom - fish_size:
                self.fish_y = cylinder_bottom - fish_size
                self.fish_direction = -1
            
            bar_top = self.bar_y
            bar_bottom = self.bar_y + self.bar_height
            fish_center = self.fish_y + fish_size / 2
            
            hook_mult = self.get_hook_multiplier()
            line_mult = self.get_line_multiplier()
            
            if bar_top <= fish_center <= bar_bottom:
                self.catch_progress += 35 * hook_mult * dt
            else:
                self.catch_progress -= 18 * line_mult * dt
            
            self.catch_progress = max(0, min(100, self.catch_progress))
            
            if self.catch_progress >= 100:
                self.caught_fish = self.current_fish
                if len(self.inventory) < self.get_bag_size():
                    self.inventory.append(self.caught_fish)
                self.state = STATE_RESULT
                self.result_timer = 0
            elif self.catch_progress <= 0:
                self.caught_fish = None
                self.state = STATE_RESULT
                self.result_timer = 0
            
            self.update_splash_particles(dt)
                
        elif self.state == STATE_RESULT:
            self.result_timer += dt
            if self.result_timer >= 3:
                self.state = STATE_IDLE
                self.reset_game()
    
    def handle_action(self):
        if self.state == STATE_IDLE:
            self.state = STATE_CASTING
            self.power = 0
            self.power_direction = 1
        elif self.state == STATE_CASTING:
            self.is_perfect_cast = self.perfect_zone_start <= self.power <= self.perfect_zone_end
            self.state = STATE_WAITING
            self.wait_time = 0
            self.max_wait_time = random.uniform(3, 6)
            self.splash_particles = []
        elif self.state == STATE_BITE:
            self.current_fish = self.select_fish()
            self.fish_speed = self.current_fish["speed"]
            self.bar_y = 200
            self.bar_velocity = 0
            self.fish_y = random.randint(100, 350)
            self.catch_progress = 50
            self.state = STATE_CATCHING
        elif self.state == STATE_INVENTORY:
            self.state = STATE_IDLE
    
    def toggle_inventory(self):
        if self.state == STATE_IDLE:
            self.state = STATE_INVENTORY
        elif self.state == STATE_INVENTORY:
            self.state = STATE_IDLE
    
    def toggle_shop(self):
        if self.state == STATE_IDLE:
            self.state = STATE_SHOP_MAIN
            self.shop_category = None
        elif self.state in [STATE_SHOP_MAIN, STATE_SHOP_CATEGORY]:
            self.state = STATE_IDLE
    
    def sell_all_fish(self):
        for fish in self.inventory:
            self.total_money += fish["price"]
        self.inventory = []
    
    def buy_item(self, category, item_index):
        data = SHOP_DATA[category]
        price = data["prices"][item_index]
        
        if self.total_money < price:
            return False
        
        if data["consumable"]:
            # 미끼 구매 (소모품)
            self.total_money -= price
            self.bait = {"name": data["items"][item_index], "effect": data["effects"][item_index]}
            self.bait_count += 5  # 5회 사용
            return True
        else:
            # 장비 업그레이드
            current_level = self.equipment[category]
            if current_level >= item_index + 1:
                return False  # 이미 보유한 등급
            if current_level != item_index:
                return False  # 순서대로 구매해야 함
            
            self.total_money -= price
            self.equipment[category] = item_index + 1
            
            # 가방 크기 업데이트
            if category == "가방":
                self.max_inventory = self.get_bag_size()
            
            return True
    
    def draw(self, screen):
        if self.state in [STATE_SHOP_MAIN, STATE_SHOP_CATEGORY]:
            self.draw_shop(screen)
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
    
    def draw_background(self, screen):
        screen.blit(background_img, (0, 0))
        
        fisherman_x = 295
        fisherman_y = 205
        pygame.draw.rect(screen, (120, 80, 45), (290, 340, 100, 14))
        pygame.draw.rect(screen, (140, 95, 55), (290, 340, 100, 4))
        pygame.draw.rect(screen, (90, 60, 35), (290, 350, 100, 4))
        for px in [300, 340, 375]:
            pygame.draw.rect(screen, (100, 70, 40), (px, 354, 14, 50))
            pygame.draw.rect(screen, (120, 85, 50), (px, 354, 4, 50))
            pygame.draw.rect(screen, (80, 55, 30), (px + 10, 354, 4, 50))
        screen.blit(fisherman_img, (fisherman_x, fisherman_y))
    
    def draw_ui(self, screen):
        ui_box = pygame.Rect(15, 15, 160, 35)
        pygame.draw.rect(screen, (30, 30, 50), ui_box)
        pygame.draw.rect(screen, (60, 60, 80), ui_box, 3)
        pygame.draw.rect(screen, (80, 80, 100), (17, 17, 156, 2))
        money_text = font_small.render(f"소지금: {self.total_money}G", True, YELLOW)
        screen.blit(money_text, (25, 22))
        
        # 미끼 표시
        if self.bait:
            bait_box = pygame.Rect(15, 55, 160, 30)
            pygame.draw.rect(screen, (50, 30, 30), bait_box)
            pygame.draw.rect(screen, (100, 60, 60), bait_box, 2)
            bait_text = font_tiny.render(f"미끼: {self.bait['name']} x{self.bait_count}", True, (255, 180, 100))
            screen.blit(bait_text, (25, 60))
        
        bag_rect = pygame.Rect(SCREEN_WIDTH - 70, 15, 55, 50)
        pygame.draw.rect(screen, BROWN, bag_rect)
        pygame.draw.rect(screen, LIGHT_BROWN, (SCREEN_WIDTH - 68, 17, 51, 3))
        pygame.draw.rect(screen, DARK_BROWN, bag_rect, 3)
        pygame.draw.rect(screen, DARK_BROWN, (SCREEN_WIDTH - 55, 10, 25, 8))
        bag_text = font_small.render(f"{len(self.inventory)}/{self.get_bag_size()}", True, WHITE)
        screen.blit(bag_text, (SCREEN_WIDTH - 65, 35))
        
        if self.state == STATE_IDLE:
            hint = font_tiny.render("[I] 가방  [P] 상점", True, LIGHT_GRAY)
            screen.blit(hint, (SCREEN_WIDTH - 120, 70))
    
    def draw_idle(self, screen):
        text = font_medium.render("SPACE/클릭으로 낚시 시작!", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        box_rect = pygame.Rect(text_rect.x - 15, text_rect.y - 10, text_rect.width + 30, text_rect.height + 20)
        pygame.draw.rect(screen, (30, 30, 50, 200), box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)
        screen.blit(text, text_rect)
    
    def draw_casting(self, screen):
        gauge_x = SCREEN_WIDTH // 2 - 150
        gauge_y = 80
        gauge_width = 300
        gauge_height = 28
        
        pygame.draw.rect(screen, (30, 30, 50), (gauge_x - 6, gauge_y - 6, gauge_width + 12, gauge_height + 12))
        pygame.draw.rect(screen, (60, 60, 80), (gauge_x - 6, gauge_y - 6, gauge_width + 12, gauge_height + 12), 3)
        pygame.draw.rect(screen, DARK_GRAY, (gauge_x, gauge_y, gauge_width, gauge_height))
        
        perfect_x = gauge_x + (self.perfect_zone_start / 100) * gauge_width
        perfect_width = ((self.perfect_zone_end - self.perfect_zone_start) / 100) * gauge_width
        pygame.draw.rect(screen, BRIGHT_YELLOW, (perfect_x, gauge_y, perfect_width, gauge_height))
        pygame.draw.rect(screen, YELLOW, (perfect_x, gauge_y + gauge_height - 4, perfect_width, 4))
        
        power_width = (self.power / 100) * gauge_width
        pygame.draw.rect(screen, GREEN, (gauge_x, gauge_y, power_width, gauge_height))
        pygame.draw.rect(screen, BRIGHT_GREEN, (gauge_x, gauge_y, power_width, 4))
        pygame.draw.rect(screen, DARK_GREEN, (gauge_x, gauge_y + gauge_height - 4, power_width, 4))
        
        line_x = gauge_x + power_width
        pygame.draw.rect(screen, WHITE, (line_x - 2, gauge_y - 6, 4, gauge_height + 12))
        
        text = font_small.render(f"파워: {int(self.power)}%", True, WHITE)
        screen.blit(text, (gauge_x, gauge_y + gauge_height + 10))
    
    def draw_waiting(self, screen):
        bobber_x = 450 + (self.power / 100) * 300
        bobber_y = 355 + self.bobber_bob
        
        draw_pixel_fishing_line(screen, (380, 260), (bobber_x, bobber_y - 15), tension=30)
        draw_pixel_bobber(screen, int(bobber_x), int(bobber_y))
        draw_splash_particle(screen, self.splash_particles)
        
        if self.is_perfect_cast:
            text = font_large.render("PERFECT!", True, YELLOW)
            shadow = font_large.render("PERFECT!", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text, text_rect)
        
        dots = "." * (int(self.wait_time * 2) % 4)
        text = font_small.render(f"기다리는 중{dots}", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(text, text_rect)
    
    def draw_bite(self, screen):
        bobber_x = 450 + (self.power / 100) * 300
        bobber_y = 380 + math.sin(self.bite_timer * 25) * 3
        
        draw_pixel_fishing_line(screen, (380, 260), (bobber_x, bobber_y), tension=40)
        draw_pixel_bobber(screen, int(bobber_x), int(bobber_y), submerged=True)
        draw_splash_particle(screen, self.splash_particles)
        
        remaining = self.bite_time_limit - self.bite_timer
        color = RED if remaining < 1 else YELLOW
        
        if int(self.bite_timer * 10) % 2 == 0:
            text = font_large.render("!! SPACE/클릭 !!", True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            box_rect = pygame.Rect(text_rect.x - 15, text_rect.y - 8, text_rect.width + 30, text_rect.height + 16)
            pygame.draw.rect(screen, (50, 20, 20), box_rect)
            pygame.draw.rect(screen, color, box_rect, 3)
            screen.blit(text, text_rect)
        
        time_text = font_medium.render(f"{remaining:.1f}초", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(time_text, time_rect)
    
    def draw_catching(self, screen):
        cylinder_x = SCREEN_WIDTH - 130
        cylinder_y = 80
        cylinder_width = 70
        cylinder_height = 340
        
        draw_pixel_cylinder(screen, cylinder_x, cylinder_y, cylinder_width, cylinder_height)
        
        bar_active = self.is_fish_in_bar()
        draw_pixel_bar(screen, cylinder_x + 6, int(self.bar_y), cylinder_width - 12, self.bar_height, bar_active)
        
        # 물고기 이미지 그리기
        fish_name = self.current_fish["name"]
        fish_img = fish_images.get(fish_name)
        scaled_img = pygame.transform.scale(fish_img, (50, 50))
        if self.fish_direction < 0:
            scaled_img = pygame.transform.flip(scaled_img, True, False)
        screen.blit(scaled_img, (cylinder_x + 10, int(self.fish_y) - 5))
        
        # 진행도 게이지
        progress_x = cylinder_x - 50
        progress_width = 25
        progress_height = cylinder_height
        
        pygame.draw.rect(screen, (30, 30, 50), (progress_x - 4, cylinder_y - 4, progress_width + 8, progress_height + 8))
        pygame.draw.rect(screen, (60, 60, 80), (progress_x - 4, cylinder_y - 4, progress_width + 8, progress_height + 8), 3)
        pygame.draw.rect(screen, DARK_GRAY, (progress_x, cylinder_y, progress_width, progress_height))
        
        fill_height = (self.catch_progress / 100) * progress_height
        fill_y = cylinder_y + progress_height - fill_height
        
        if self.catch_progress > 70:
            progress_color, light_color = GREEN, BRIGHT_GREEN
        elif self.catch_progress > 30:
            progress_color, light_color = YELLOW, BRIGHT_YELLOW
        else:
            progress_color, light_color = RED, BRIGHT_RED
        
        pygame.draw.rect(screen, progress_color, (progress_x, fill_y, progress_width, fill_height))
        pygame.draw.rect(screen, light_color, (progress_x, fill_y, 4, fill_height))
        
        # 낚싯찌
        bobber_x = 450 + (self.power / 100) * 300
        bobber_y = 370 + math.sin(pygame.time.get_ticks() / 80) * 4
        draw_pixel_fishing_line(screen, (380, 260), (bobber_x, bobber_y - 10), tension=35)
        draw_pixel_bobber(screen, int(bobber_x), int(bobber_y), submerged=True)
        
        if random.random() < 0.3:
            self.add_splash_particle(bobber_x, 370)
        draw_splash_particle(screen, self.splash_particles)
        
        # 물고기 정보
        info_box = pygame.Rect(30, 100, 200, 80)
        pygame.draw.rect(screen, (30, 30, 50, 200), info_box)
        pygame.draw.rect(screen, WHITE, info_box, 2)
        
        fish = self.current_fish
        fish_info = font_medium.render(f"{fish['name']}", True, WHITE)
        screen.blit(fish_info, (45, 110))
        
        rarity_colors = {"trash": GRAY, "common": WHITE, "uncommon": GREEN, "rare": (100, 149, 237), "epic": (186, 85, 211), "legendary": YELLOW}
        rarity_kr = {"trash": "잡동사니", "common": "일반", "uncommon": "고급", "rare": "희귀", "epic": "영웅", "legendary": "전설"}
        rarity_text = font_small.render(f"[{rarity_kr[fish['rarity']]}]", True, rarity_colors[fish['rarity']])
        screen.blit(rarity_text, (45, 145))
        
        help_text = font_tiny.render("SPACE/클릭: 올라가기", True, WHITE)
        screen.blit(help_text, (30, SCREEN_HEIGHT - 40))
    
    def is_fish_in_bar(self):
        if not self.current_fish:
            return False
        fish_center = self.fish_y + 20
        return self.bar_y <= fish_center <= self.bar_y + self.bar_height
    
    def draw_result(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        if self.caught_fish:
            fish_name = self.caught_fish["name"]
            rarity = self.caught_fish["rarity"]
            
            if rarity == "trash":
                text = font_large.render("뭔가를 건졌다...", True, GRAY)
            else:
                text = font_large.render("물고기를 잡았다!", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(text, text_rect)
            
            fish_name_text = font_large.render(fish_name, True, WHITE)
            name_rect = fish_name_text.get_rect(center=(SCREEN_WIDTH // 2, 210))
            screen.blit(fish_name_text, name_rect)
            
            rarity_colors = {"trash": GRAY, "common": WHITE, "uncommon": GREEN, "rare": (100, 149, 237), "epic": (186, 85, 211), "legendary": YELLOW}
            rarity_kr = {"trash": "잡동사니", "common": "일반", "uncommon": "고급", "rare": "희귀", "epic": "영웅", "legendary": "전설"}
            rarity_text = font_medium.render(f"[{rarity_kr[rarity]}] - {self.caught_fish['price']}G", True, rarity_colors[rarity])
            rarity_rect = rarity_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
            screen.blit(rarity_text, rarity_rect)
            
            # 가방이 가득 찼을 때
            if len(self.inventory) >= self.get_bag_size():
                full_text = font_small.render("가방이 가득 찼습니다!", True, RED)
                full_rect = full_text.get_rect(center=(SCREEN_WIDTH // 2, 420))
                screen.blit(full_text, full_rect)
            
            # 물고기 이미지 크게 표시
            fish_img = fish_images.get(fish_name)
            display_img = pygame.transform.scale(fish_img, (120, 120))
            screen.blit(display_img, (SCREEN_WIDTH // 2 - 60, 290))
        else:
            text = font_large.render("놓쳤다...", True, RED)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 220))
            screen.blit(text, text_rect)
        
        continue_text = font_tiny.render("잠시 후 자동으로 계속됩니다...", True, GRAY)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, 450))
        screen.blit(continue_text, continue_rect)
    
    def draw_inventory(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(220)
        screen.blit(overlay, (0, 0))
        
        title = font_large.render("가방", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 45))
        screen.blit(title, title_rect)
        
        if not self.inventory:
            empty_text = font_medium.render("가방이 비어있습니다", True, GRAY)
            empty_rect = empty_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
            screen.blit(empty_text, empty_rect)
        else:
            fish_counts = {}
            for fish in self.inventory:
                name = fish["name"]
                if name in fish_counts:
                    fish_counts[name]["count"] += 1
                else:
                    fish_counts[name] = {"fish": fish, "count": 1}
            
            y_offset = 90
            total_value = 0
            for name, data in fish_counts.items():
                fish = data["fish"]
                count = data["count"]
                value = fish["price"] * count
                total_value += value
                
                # 물고기 이미지
                fish_img = fish_images.get(name)
                icon_img = pygame.transform.scale(fish_img, (40, 40))
                screen.blit(icon_img, (70, y_offset - 8))
                
                rarity_colors = {"trash": GRAY, "common": WHITE, "uncommon": GREEN, "rare": (100, 149, 237), "epic": (186, 85, 211), "legendary": YELLOW}
                fish_text = font_small.render(f"{name} x{count}", True, rarity_colors[fish["rarity"]])
                screen.blit(fish_text, (125, y_offset))
                
                price_text = font_small.render(f"{value}G", True, YELLOW)
                screen.blit(price_text, (350, y_offset))
                
                y_offset += 40
            
            total_text = font_medium.render(f"총 가치: {total_value}G", True, YELLOW)
            screen.blit(total_text, (80, y_offset + 15))
            
            sell_rect = pygame.Rect(SCREEN_WIDTH // 2 - 90, y_offset + 60, 180, 40)
            pygame.draw.rect(screen, GREEN, sell_rect)
            pygame.draw.rect(screen, BRIGHT_GREEN, (sell_rect.x, sell_rect.y, sell_rect.width, 4))
            pygame.draw.rect(screen, DARK_GREEN, (sell_rect.x, sell_rect.y + sell_rect.height - 4, sell_rect.width, 4))
            pygame.draw.rect(screen, WHITE, sell_rect, 2)
            sell_text = font_small.render("전부 판매 [S]", True, WHITE)
            sell_text_rect = sell_text.get_rect(center=sell_rect.center)
            screen.blit(sell_text, sell_text_rect)
        
        close_text = font_tiny.render("[I/ESC] 닫기", True, GRAY)
        close_rect = close_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 35))
        screen.blit(close_text, close_rect)
    
    def draw_shop(self, screen):
        # 상점 배경
        screen.blit(shop_img, (0, 0))
        
        if self.state == STATE_SHOP_MAIN:
            self.draw_shop_main(screen)
        elif self.state == STATE_SHOP_CATEGORY:
            self.draw_shop_category(screen)
    
    def draw_shop_main(self, screen):
        # 소지금 표시
        money_box = pygame.Rect(SCREEN_WIDTH - 180, 15, 165, 35)
        pygame.draw.rect(screen, (30, 30, 50, 200), money_box)
        pygame.draw.rect(screen, YELLOW, money_box, 2)
        money_text = font_small.render(f"소지금: {self.total_money}G", True, YELLOW)
        screen.blit(money_text, (SCREEN_WIDTH - 170, 22))
        
        # 카테고리 버튼들
        categories = ["미끼", "릴", "낚싯바늘", "낚싯줄", "가방"]
        button_width = 140
        button_height = 45
        start_x = (SCREEN_WIDTH - button_width) // 2
        start_y = 350
        
        self.category_rects = []
        for i, cat in enumerate(categories):
            rect = pygame.Rect(start_x, start_y + i * 55, button_width, button_height)
            self.category_rects.append((rect, cat))
            
            # 버튼 배경
            pygame.draw.rect(screen, (50, 40, 30), rect)
            pygame.draw.rect(screen, (80, 60, 40), (rect.x, rect.y, rect.width, 4))
            pygame.draw.rect(screen, (30, 25, 20), (rect.x, rect.y + rect.height - 4, rect.width, 4))
            pygame.draw.rect(screen, (100, 80, 60), rect, 2)
            
            # 장비 레벨 표시
            if cat != "미끼":
                level = self.equipment[cat]
                if level > 0:
                    level_text = f" [{SHOP_DATA[cat]['items'][level-1]}]"
                    cat_text = font_small.render(f"{cat}{level_text}", True, WHITE)
                else:
                    cat_text = font_small.render(cat, True, WHITE)
            else:
                if self.bait:
                    cat_text = font_small.render(f"{cat} ({self.bait_count})", True, (255, 180, 100))
                else:
                    cat_text = font_small.render(cat, True, WHITE)
            
            text_rect = cat_text.get_rect(center=rect.center)
            screen.blit(cat_text, text_rect)
        
        # 안내 텍스트
        hint_text = font_tiny.render("[P/ESC] 나가기", True, LIGHT_GRAY)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        screen.blit(hint_text, hint_rect)
    
    def draw_shop_category(self, screen):
        cat = self.shop_category
        data = SHOP_DATA[cat]
        
        # 상단 정보
        money_box = pygame.Rect(SCREEN_WIDTH - 180, 15, 165, 35)
        pygame.draw.rect(screen, (30, 30, 50, 200), money_box)
        pygame.draw.rect(screen, YELLOW, money_box, 2)
        money_text = font_small.render(f"소지금: {self.total_money}G", True, YELLOW)
        screen.blit(money_text, (SCREEN_WIDTH - 170, 22))
        
        # 카테고리 제목
        title_box = pygame.Rect(15, 15, 200, 35)
        pygame.draw.rect(screen, (30, 30, 50, 200), title_box)
        pygame.draw.rect(screen, WHITE, title_box, 2)
        title_text = font_medium.render(cat, True, WHITE)
        screen.blit(title_text, (25, 18))
        
        # 설명
        desc_text = font_tiny.render(data["description"], True, LIGHT_GRAY)
        screen.blit(desc_text, (25, 55))
        
        # 아이템 목록
        self.item_rects = []
        start_y = 350
        
        for i, (item_name, price, effect) in enumerate(zip(data["items"], data["prices"], data["effects"])):
            rect = pygame.Rect(80, start_y + i * 50, SCREEN_WIDTH - 160, 42)
            self.item_rects.append((rect, i))
            
            # 구매 가능 여부 확인
            can_buy = self.total_money >= price
            already_owned = False
            
            if not data["consumable"]:
                current_level = self.equipment[cat]
                already_owned = current_level >= i + 1
                can_buy = can_buy and current_level == i  # 순서대로만 구매 가능
            
            # 배경색
            if already_owned:
                bg_color = (40, 60, 40)
                border_color = GREEN
            elif can_buy:
                bg_color = (50, 40, 30)
                border_color = (100, 80, 60)
            else:
                bg_color = (40, 35, 35)
                border_color = (80, 60, 60)
            
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, border_color, rect, 2)
            
            # 아이템 이름
            if already_owned:
                name_text = font_small.render(f"{item_name} [보유중]", True, GREEN)
            else:
                name_text = font_small.render(item_name, True, WHITE if can_buy else GRAY)
            screen.blit(name_text, (rect.x + 15, rect.y + 5))
            
            # 효과 설명
            if cat == "미끼":
                effect_str = f"희귀확률 x{effect}"
            elif cat == "릴":
                effect_str = f"속도 x{effect}"
            elif cat == "낚싯바늘":
                effect_str = f"증가속도 x{effect}"
            elif cat == "낚싯줄":
                effect_str = f"감소속도 x{effect}"
            elif cat == "가방":
                effect_str = f"크기 {effect}칸"
            
            effect_text = font_tiny.render(effect_str, True, CYAN if can_buy else GRAY)
            screen.blit(effect_text, (rect.x + 15, rect.y + 25))
            
            # 가격
            if not already_owned:
                price_color = YELLOW if can_buy else (100, 80, 60)
                price_text = font_small.render(f"{price}G", True, price_color)
                price_rect = price_text.get_rect(right=rect.right - 15, centery=rect.centery)
                screen.blit(price_text, price_rect)
        
        # 안내 텍스트
        hint_text = font_tiny.render("[ESC] 뒤로  |  숫자키(1~5)로 구매", True, LIGHT_GRAY)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        screen.blit(hint_text, hint_rect)
    
    def handle_shop_click(self, pos):
        if self.state == STATE_SHOP_MAIN:
            for rect, cat in self.category_rects:
                if rect.collidepoint(pos):
                    self.shop_category = cat
                    self.state = STATE_SHOP_CATEGORY
                    return
        elif self.state == STATE_SHOP_CATEGORY:
            for rect, idx in self.item_rects:
                if rect.collidepoint(pos):
                    if self.buy_item(self.shop_category, idx):
                        pass  # 구매 성공
                    return


def main():
    clock = pygame.time.Clock()
    game = FishingGame()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000.0
        
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        action_pressed = mouse_pressed or keys[pygame.K_SPACE]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.state not in [STATE_SHOP_MAIN, STATE_SHOP_CATEGORY]:
                        game.handle_action()
                elif event.key == pygame.K_i:
                    if game.state not in [STATE_SHOP_MAIN, STATE_SHOP_CATEGORY]:
                        game.toggle_inventory()
                elif event.key == pygame.K_p:
                    game.toggle_shop()
                elif event.key == pygame.K_ESCAPE:
                    if game.state == STATE_INVENTORY:
                        game.state = STATE_IDLE
                    elif game.state == STATE_SHOP_CATEGORY:
                        game.state = STATE_SHOP_MAIN
                    elif game.state == STATE_SHOP_MAIN:
                        game.state = STATE_IDLE
                elif event.key == pygame.K_s:
                    if game.state == STATE_INVENTORY:
                        game.sell_all_fish()
                # 숫자키로 상점 아이템 구매
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    if game.state == STATE_SHOP_CATEGORY:
                        idx = event.key - pygame.K_1
                        game.buy_item(game.shop_category, idx)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game.state in [STATE_SHOP_MAIN, STATE_SHOP_CATEGORY]:
                        game.handle_shop_click(event.pos)
                    else:
                        game.handle_action()
        
        game.update(dt, action_pressed)
        game.draw(screen)
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()
