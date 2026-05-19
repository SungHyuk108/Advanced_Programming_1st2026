import pygame
import random
import math
import os

# 초기화
pygame.init()

# 화면 설정 - 배경 이미지 크기에 맞춤 (512x288을 2배로 스케일)
SCALE = 2
BASE_WIDTH = 512
BASE_HEIGHT = 288
SCREEN_WIDTH = BASE_WIDTH * SCALE
SCREEN_HEIGHT = BASE_HEIGHT * SCALE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Fishing Game")

# 색상 팔레트 (고퀄리티 픽셀 아트 스타일)
WATER_BLUE = (64, 164, 223)
DEEP_WATER = (35, 100, 170)
DARKER_WATER = (25, 70, 140)
SKY_BLUE = (135, 206, 235)
SAND = (238, 214, 175)
WHITE = (255, 255, 255)
OFF_WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
BRIGHT_RED = (255, 80, 80)
DARK_RED = (160, 40, 40)
GREEN = (60, 179, 113)
BRIGHT_GREEN = (100, 220, 140)
DARK_GREEN = (40, 130, 80)
YELLOW = (255, 215, 0)
BRIGHT_YELLOW = (255, 240, 100)
ORANGE = (255, 140, 0)
BROWN = (139, 90, 43)
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (180, 130, 70)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (200, 200, 200)
CYAN = (100, 200, 255)
LIGHT_CYAN = (180, 230, 255)

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

# 폰트 초기화
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

# 물고기 종류
FISH_DATA = [
    {"name": "멸치", "rarity": "common", "speed": 2, "size": 50, "color": (192, 192, 192), "price": 10},
    {"name": "고등어", "rarity": "common", "speed": 2.5, "size": 45, "color": (70, 130, 180), "price": 25},
    {"name": "광어", "rarity": "uncommon", "speed": 3, "size": 40, "color": (160, 82, 45), "price": 50},
    {"name": "참돔", "rarity": "uncommon", "speed": 3.5, "size": 38, "color": (255, 105, 180), "price": 80},
    {"name": "참치", "rarity": "rare", "speed": 4.5, "size": 35, "color": (0, 0, 139), "price": 150},
    {"name": "황금잉어", "rarity": "legendary", "speed": 6, "size": 32, "color": (255, 215, 0), "price": 500},
]

# 이미지 로드
def load_image(path, scale=None):
    try:
        img = pygame.image.load(path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except:
        return None

# 경로 설정
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
background_img = load_image(os.path.join(ASSETS_PATH, "background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
fisherman_img = load_image(os.path.join(ASSETS_PATH, "fisherman.png"), (128, 128))


def draw_pixel_rect(surface, color, rect, pixel_size=2):
    """픽셀 스타일 사각형 그리기"""
    x, y, w, h = rect
    for py in range(0, h, pixel_size):
        for px in range(0, w, pixel_size):
            pygame.draw.rect(surface, color, (x + px, y + py, pixel_size, pixel_size))


def draw_pixel_bobber(surface, x, y, submerged=False):
    """고퀄리티 픽셀 낚싯찌"""
    p = 2  # 픽셀 크기
    
    if not submerged:
        # 흰색 상단부 (원통형 효과)
        pygame.draw.rect(surface, OFF_WHITE, (x - 3*p, y - 10*p, 6*p, 3*p))
        pygame.draw.rect(surface, WHITE, (x - 2*p, y - 11*p, 4*p, p))
        pygame.draw.rect(surface, LIGHT_GRAY, (x - 3*p, y - 7*p, 6*p, p))
        
        # 빨간 하단부 (그라데이션 효과)
        pygame.draw.rect(surface, BRIGHT_RED, (x - 4*p, y - 6*p, 8*p, 2*p))
        pygame.draw.rect(surface, RED, (x - 5*p, y - 4*p, 10*p, 6*p))
        pygame.draw.rect(surface, DARK_RED, (x - 4*p, y + 2*p, 8*p, 3*p))
        pygame.draw.rect(surface, DARK_RED, (x - 3*p, y + 5*p, 6*p, 2*p))
        
        # 하이라이트
        pygame.draw.rect(surface, BRIGHT_RED, (x - 3*p, y - 4*p, 2*p, 4*p))
    else:
        # 물속에 들어간 찌 (살짝만 보임)
        pygame.draw.rect(surface, (180, 80, 80), (x - 3*p, y - 2*p, 6*p, 4*p))


def draw_pixel_fishing_line(surface, start, end, tension=0):
    """고퀄리티 픽셀 낚싯줄 (곡선)"""
    x1, y1 = start
    x2, y2 = end
    
    # 베지어 곡선으로 자연스러운 낚싯줄
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2 + tension
    
    points = []
    for t in range(21):
        t = t / 20
        # 2차 베지어 곡선
        px = (1-t)**2 * x1 + 2*(1-t)*t * mid_x + t**2 * x2
        py = (1-t)**2 * y1 + 2*(1-t)*t * mid_y + t**2 * y2
        points.append((int(px), int(py)))
    
    # 줄 그리기 (두께 있는 픽셀 라인)
    for i in range(len(points) - 1):
        pygame.draw.line(surface, LIGHT_GRAY, points[i], points[i+1], 2)
        pygame.draw.line(surface, WHITE, (points[i][0], points[i][1]-1), (points[i+1][0], points[i+1][1]-1), 1)


def draw_pixel_cylinder(surface, x, y, width, height):
    """고퀄리티 픽셀 실린더 (물탱크 스타일)"""
    p = 2
    
    # 외곽 테두리 (진한 파랑)
    pygame.draw.rect(surface, (20, 50, 100), (x - p*2, y - p*2, width + p*4, height + p*4))
    
    # 메인 배경 (그라데이션 효과)
    for i in range(0, height, p*4):
        ratio = i / height
        r = int(35 + ratio * 15)
        g = int(100 - ratio * 30)
        b = int(170 - ratio * 30)
        pygame.draw.rect(surface, (r, g, b), (x, y + i, width, p*4))
    
    # 물결 효과 (픽셀 패턴)
    wave_time = pygame.time.get_ticks() / 500
    for wy in range(0, height, p*8):
        wave_offset = int(math.sin(wave_time + wy / 20) * p)
        pygame.draw.rect(surface, (50, 120, 190), (x + wave_offset, y + wy, p*2, p*4))
        pygame.draw.rect(surface, (50, 120, 190), (x + width - p*4 + wave_offset, y + wy + p*4, p*2, p*4))
    
    # 하이라이트 (왼쪽)
    pygame.draw.rect(surface, (80, 150, 210), (x, y, p*2, height))
    
    # 그림자 (오른쪽)
    pygame.draw.rect(surface, (20, 60, 120), (x + width - p*2, y, p*2, height))
    
    # 상단/하단 테두리 디테일
    pygame.draw.rect(surface, (60, 90, 140), (x - p, y - p, width + p*2, p*2))
    pygame.draw.rect(surface, (60, 90, 140), (x - p, y + height - p, width + p*2, p*2))


def draw_pixel_bar(surface, x, y, width, height, active=False):
    """고퀄리티 픽셀 플레이어 바"""
    p = 2
    
    # 메인 색상
    if active:
        main_color = BRIGHT_GREEN
        light_color = (150, 255, 180)
        dark_color = DARK_GREEN
    else:
        main_color = (80, 160, 100)
        light_color = (120, 200, 140)
        dark_color = (50, 120, 70)
    
    # 배경
    pygame.draw.rect(surface, main_color, (x, y, width, height))
    
    # 상단 하이라이트
    pygame.draw.rect(surface, light_color, (x, y, width, p*2))
    pygame.draw.rect(surface, light_color, (x, y, p*2, height))
    
    # 하단 그림자
    pygame.draw.rect(surface, dark_color, (x, y + height - p*2, width, p*2))
    pygame.draw.rect(surface, dark_color, (x + width - p*2, y, p*2, height))
    
    # 중앙 패턴
    for py in range(p*4, height - p*4, p*6):
        pygame.draw.rect(surface, light_color, (x + p*4, y + py, width - p*8, p))


def draw_pixel_fish(surface, x, y, fish_data, direction=1):
    """고퀄리티 픽셀 물고기"""
    p = 2
    size = fish_data["size"]
    color = fish_data["color"]
    
    # 색상 변형
    r, g, b = color
    light_color = (min(255, r + 40), min(255, g + 40), min(255, b + 40))
    dark_color = (max(0, r - 40), max(0, g - 40), max(0, b - 40))
    
    # 방향에 따라 그리기
    if direction > 0:
        # 몸통 (타원형)
        pygame.draw.ellipse(surface, color, (x, y, size, size // 2))
        pygame.draw.ellipse(surface, light_color, (x + p, y + p, size // 2, size // 4))
        
        # 꼬리
        tail_points = [
            (x + size - p*2, y + size // 4),
            (x + size + p*6, y - p*2),
            (x + size + p*6, y + size // 2 + p*2)
        ]
        pygame.draw.polygon(surface, color, tail_points)
        pygame.draw.polygon(surface, dark_color, tail_points, 2)
        
        # 지느러미
        fin_points = [
            (x + size // 3, y),
            (x + size // 2, y - p*4),
            (x + size * 2 // 3, y)
        ]
        pygame.draw.polygon(surface, dark_color, fin_points)
        
        # 눈
        pygame.draw.rect(surface, WHITE, (x + p*3, y + p*2, p*4, p*4))
        pygame.draw.rect(surface, BLACK, (x + p*4, y + p*3, p*2, p*2))
    else:
        # 반대 방향
        pygame.draw.ellipse(surface, color, (x, y, size, size // 2))
        pygame.draw.ellipse(surface, light_color, (x + size // 2 - p, y + p, size // 2, size // 4))
        
        tail_points = [
            (x + p*2, y + size // 4),
            (x - p*6, y - p*2),
            (x - p*6, y + size // 2 + p*2)
        ]
        pygame.draw.polygon(surface, color, tail_points)
        pygame.draw.polygon(surface, dark_color, tail_points, 2)
        
        fin_points = [
            (x + size // 3, y),
            (x + size // 2, y - p*4),
            (x + size * 2 // 3, y)
        ]
        pygame.draw.polygon(surface, dark_color, fin_points)
        
        pygame.draw.rect(surface, WHITE, (x + size - p*7, y + p*2, p*4, p*4))
        pygame.draw.rect(surface, BLACK, (x + size - p*6, y + p*3, p*2, p*2))


def draw_splash_particle(surface, particles):
    """물방울 파티클 그리기"""
    for p in particles:
        alpha = int(255 * p['life'])
        size = int(p['size'] * p['life'])
        if size > 0:
            # 물방울 (그라데이션 효과)
            pygame.draw.circle(surface, LIGHT_CYAN, (int(p['x']), int(p['y'])), size + 1)
            pygame.draw.circle(surface, CYAN, (int(p['x']), int(p['y'])), size)
            if size > 2:
                pygame.draw.circle(surface, WHITE, (int(p['x']) - 1, int(p['y']) - 1), size // 2)


class FishingGame:
    def __init__(self):
        self.state = STATE_IDLE
        self.inventory = []
        self.total_money = 0
        self.reset_game()
        
    def reset_game(self):
        # 캐스팅 관련
        self.power = 0
        self.power_direction = 1
        self.perfect_zone_start = random.randint(60, 80)
        self.perfect_zone_end = self.perfect_zone_start + 15
        self.is_perfect_cast = False
        
        # 대기 관련
        self.wait_time = 0
        self.max_wait_time = random.uniform(3, 6)
        self.bobber_y = 0
        self.bobber_bob = 0
        self.splash_particles = []
        
        # 물기 관련
        self.bite_timer = 0
        self.bite_time_limit = 2.0
        
        # 미니게임 관련 (물리엔진)
        self.bar_y = 200
        self.bar_height = 70
        self.bar_velocity = 0
        self.bar_acceleration = 0
        self.bar_max_speed = 6
        self.bar_accel_time = 0.5
        self.bar_accel_rate = self.bar_max_speed / self.bar_accel_time
        
        self.fish_y = 150
        self.fish_direction = 1
        self.fish_speed = 3
        self.catch_progress = 50
        self.current_fish = None
        
        # 결과
        self.caught_fish = None
        self.result_timer = 0
        
    def select_fish(self):
        weights = [40, 30, 15, 10, 4, 1]
        if self.is_perfect_cast:
            weights = [20, 25, 25, 15, 10, 5]
        
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
            # 물리엔진 적용
            if action_pressed:
                self.bar_acceleration = -self.bar_accel_rate
            else:
                self.bar_acceleration = self.bar_accel_rate / 1.5
            
            self.bar_velocity += self.bar_acceleration * dt
            self.bar_velocity = max(-self.bar_max_speed, min(self.bar_max_speed, self.bar_velocity))
            self.bar_y += self.bar_velocity
            
            # 실린더 범위
            cylinder_top = 80
            cylinder_bottom = 420
            if self.bar_y <= cylinder_top:
                self.bar_y = cylinder_top
                self.bar_velocity = 0
            elif self.bar_y >= cylinder_bottom - self.bar_height:
                self.bar_y = cylinder_bottom - self.bar_height
                self.bar_velocity = 0
            
            # 물고기 AI
            self.fish_y += self.fish_direction * self.fish_speed
            
            if random.random() < 0.02:
                self.fish_direction *= -1
            
            fish_size = self.current_fish["size"]
            if self.fish_y <= cylinder_top:
                self.fish_y = cylinder_top
                self.fish_direction = 1
            elif self.fish_y >= cylinder_bottom - fish_size:
                self.fish_y = cylinder_bottom - fish_size
                self.fish_direction = -1
            
            # 게이지 계산
            bar_top = self.bar_y
            bar_bottom = self.bar_y + self.bar_height
            fish_center = self.fish_y + fish_size / 2
            
            if fish_center >= bar_top and fish_center <= bar_bottom:
                self.catch_progress += 35 * dt
            else:
                self.catch_progress -= 18 * dt
            
            self.catch_progress = max(0, min(100, self.catch_progress))
            
            if self.catch_progress >= 100:
                self.caught_fish = self.current_fish
                self.inventory.append(self.caught_fish)
                self.state = STATE_RESULT
                self.result_timer = 0
            elif self.catch_progress <= 0:
                self.caught_fish = None
                self.state = STATE_RESULT
                self.result_timer = 0
            
            # 첨벙 효과 업데이트
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
            self.bar_acceleration = 0
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
    
    def sell_all_fish(self):
        for fish in self.inventory:
            self.total_money += fish["price"]
        self.inventory = []
    
    def draw(self, screen):
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
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            screen.fill(SKY_BLUE)
            pygame.draw.rect(screen, WATER_BLUE, (0, 350, SCREEN_WIDTH, 250))
        
        # 낚시꾼 (부두 끝에 위치)
        if fisherman_img:
            # 부두 끝 위치에 맞게 배치 (배경 이미지 기준)
            fisherman_x = 295
            fisherman_y = 205
            
            # 부두 연장 픽셀 그리기 (이미지와 자연스럽게 연결)
            # 수평 나무 판자
            pygame.draw.rect(screen, (120, 80, 45), (290, 340, 100, 14))
            pygame.draw.rect(screen, (140, 95, 55), (290, 340, 100, 4))
            pygame.draw.rect(screen, (90, 60, 35), (290, 350, 100, 4))
            
            # 수직 기둥들
            for px in [300, 340, 375]:
                pygame.draw.rect(screen, (100, 70, 40), (px, 354, 14, 50))
                pygame.draw.rect(screen, (120, 85, 50), (px, 354, 4, 50))
                pygame.draw.rect(screen, (80, 55, 30), (px + 10, 354, 4, 50))
            
            screen.blit(fisherman_img, (fisherman_x, fisherman_y))
        else:
            self.draw_fisherman_pixel(screen, 320, 240)
    
    def draw_fisherman_pixel(self, screen, x, y):
        """폴백용 픽셀 낚시꾼"""
        p = 3
        # 머리
        pygame.draw.rect(screen, (255, 220, 177), (x, y, p*7, p*7))
        # 모자
        pygame.draw.rect(screen, RED, (x - p, y - p*3, p*9, p*4))
        # 몸
        pygame.draw.rect(screen, (70, 130, 180), (x - p, y + p*7, p*9, p*10))
        # 다리
        pygame.draw.rect(screen, DARK_BROWN, (x, y + p*17, p*3, p*5))
        pygame.draw.rect(screen, DARK_BROWN, (x + p*4, y + p*17, p*3, p*5))
    
    def draw_ui(self, screen):
        # 돈 표시 (픽셀 스타일 박스)
        ui_box = pygame.Rect(15, 15, 160, 35)
        pygame.draw.rect(screen, (30, 30, 50), ui_box)
        pygame.draw.rect(screen, (60, 60, 80), ui_box, 3)
        pygame.draw.rect(screen, (80, 80, 100), (17, 17, 156, 2))
        
        money_text = font_small.render(f"소지금: {self.total_money}G", True, YELLOW)
        screen.blit(money_text, (25, 22))
        
        # 가방 아이콘 (픽셀 스타일)
        bag_rect = pygame.Rect(SCREEN_WIDTH - 70, 15, 55, 50)
        pygame.draw.rect(screen, BROWN, bag_rect)
        pygame.draw.rect(screen, LIGHT_BROWN, (SCREEN_WIDTH - 68, 17, 51, 3))
        pygame.draw.rect(screen, DARK_BROWN, bag_rect, 3)
        pygame.draw.rect(screen, DARK_BROWN, (SCREEN_WIDTH - 55, 10, 25, 8))
        
        bag_text = font_small.render(f"{len(self.inventory)}", True, WHITE)
        screen.blit(bag_text, (SCREEN_WIDTH - 52, 35))
        
        if self.state == STATE_IDLE:
            hint = font_tiny.render("[I] 가방", True, LIGHT_GRAY)
            screen.blit(hint, (SCREEN_WIDTH - 65, 70))
    
    def draw_idle(self, screen):
        # 안내 텍스트 (픽셀 스타일 박스)
        text = font_medium.render("SPACE/클릭으로 낚시 시작!", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        
        box_rect = pygame.Rect(text_rect.x - 15, text_rect.y - 10, text_rect.width + 30, text_rect.height + 20)
        pygame.draw.rect(screen, (30, 30, 50, 200), box_rect)
        pygame.draw.rect(screen, WHITE, box_rect, 2)
        
        screen.blit(text, text_rect)
    
    def draw_casting(self, screen):
        # 파워 게이지 (픽셀 스타일)
        gauge_x = SCREEN_WIDTH // 2 - 150
        gauge_y = 80
        gauge_width = 300
        gauge_height = 28
        
        # 게이지 외곽
        pygame.draw.rect(screen, (30, 30, 50), (gauge_x - 6, gauge_y - 6, gauge_width + 12, gauge_height + 12))
        pygame.draw.rect(screen, (60, 60, 80), (gauge_x - 6, gauge_y - 6, gauge_width + 12, gauge_height + 12), 3)
        pygame.draw.rect(screen, DARK_GRAY, (gauge_x, gauge_y, gauge_width, gauge_height))
        
        # 퍼펙트 존
        perfect_x = gauge_x + (self.perfect_zone_start / 100) * gauge_width
        perfect_width = ((self.perfect_zone_end - self.perfect_zone_start) / 100) * gauge_width
        pygame.draw.rect(screen, BRIGHT_YELLOW, (perfect_x, gauge_y, perfect_width, gauge_height))
        pygame.draw.rect(screen, YELLOW, (perfect_x, gauge_y + gauge_height - 4, perfect_width, 4))
        
        # 현재 파워
        power_width = (self.power / 100) * gauge_width
        pygame.draw.rect(screen, GREEN, (gauge_x, gauge_y, power_width, gauge_height))
        pygame.draw.rect(screen, BRIGHT_GREEN, (gauge_x, gauge_y, power_width, 4))
        pygame.draw.rect(screen, DARK_GREEN, (gauge_x, gauge_y + gauge_height - 4, power_width, 4))
        
        # 표시선
        line_x = gauge_x + power_width
        pygame.draw.rect(screen, WHITE, (line_x - 2, gauge_y - 6, 4, gauge_height + 12))
        
        # 텍스트
        text = font_small.render(f"파워: {int(self.power)}%", True, WHITE)
        screen.blit(text, (gauge_x, gauge_y + gauge_height + 10))
    
    def draw_waiting(self, screen):
        # 낚싯찌 위치
        bobber_x = 450 + (self.power / 100) * 300
        bobber_y = 355 + self.bobber_bob
        
        # 낚싯줄 (곡선)
        line_start = (380, 280)
        line_end = (bobber_x, bobber_y - 15)
        draw_pixel_fishing_line(screen, line_start, line_end, tension=30)
        
        # 낚싯찌
        draw_pixel_bobber(screen, int(bobber_x), int(bobber_y))
        
        # 물방울 파티클
        draw_splash_particle(screen, self.splash_particles)
        
        # 퍼펙트 표시
        if self.is_perfect_cast:
            text = font_large.render("PERFECT!", True, YELLOW)
            shadow = font_large.render("PERFECT!", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text, text_rect)
        
        # 대기 텍스트
        dots = "." * (int(self.wait_time * 2) % 4)
        text = font_small.render(f"기다리는 중{dots}", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(text, text_rect)
    
    def draw_bite(self, screen):
        # 물속으로 들어가는 찌
        bobber_x = 450 + (self.power / 100) * 300
        bobber_y = 380 + math.sin(self.bite_timer * 25) * 3
        
        # 낚싯줄
        line_start = (380, 280)
        line_end = (bobber_x, bobber_y)
        draw_pixel_fishing_line(screen, line_start, line_end, tension=40)
        
        # 물속에 들어간 찌
        draw_pixel_bobber(screen, int(bobber_x), int(bobber_y), submerged=True)
        
        # 물방울
        draw_splash_particle(screen, self.splash_particles)
        
        # 경고
        remaining = self.bite_time_limit - self.bite_timer
        color = RED if remaining < 1 else YELLOW
        
        if int(self.bite_timer * 10) % 2 == 0:
            text = font_large.render("!! SPACE/클릭 !!", True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            
            # 박스
            box_rect = pygame.Rect(text_rect.x - 15, text_rect.y - 8, text_rect.width + 30, text_rect.height + 16)
            pygame.draw.rect(screen, (50, 20, 20), box_rect)
            pygame.draw.rect(screen, color, box_rect, 3)
            
            screen.blit(text, text_rect)
        
        time_text = font_medium.render(f"{remaining:.1f}초", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(time_text, time_rect)
    
    def draw_catching(self, screen):
        # 실린더 (오른쪽 배치)
        cylinder_x = SCREEN_WIDTH - 130
        cylinder_y = 80
        cylinder_width = 70
        cylinder_height = 340
        
        draw_pixel_cylinder(screen, cylinder_x, cylinder_y, cylinder_width, cylinder_height)
        
        # 플레이어 바
        bar_active = self.is_fish_in_bar()
        draw_pixel_bar(screen, cylinder_x + 6, int(self.bar_y), cylinder_width - 12, self.bar_height, bar_active)
        
        # 물고기 (바 위에 그리기)
        fish = self.current_fish
        draw_pixel_fish(screen, cylinder_x + 10, int(self.fish_y), fish, self.fish_direction)
        
        # 진행도 게이지
        progress_x = cylinder_x - 50
        progress_width = 25
        progress_height = cylinder_height
        
        # 게이지 배경
        pygame.draw.rect(screen, (30, 30, 50), (progress_x - 4, cylinder_y - 4, progress_width + 8, progress_height + 8))
        pygame.draw.rect(screen, (60, 60, 80), (progress_x - 4, cylinder_y - 4, progress_width + 8, progress_height + 8), 3)
        pygame.draw.rect(screen, DARK_GRAY, (progress_x, cylinder_y, progress_width, progress_height))
        
        # 진행도 바
        fill_height = (self.catch_progress / 100) * progress_height
        fill_y = cylinder_y + progress_height - fill_height
        
        if self.catch_progress > 70:
            progress_color = GREEN
            light_color = BRIGHT_GREEN
        elif self.catch_progress > 30:
            progress_color = YELLOW
            light_color = BRIGHT_YELLOW
        else:
            progress_color = RED
            light_color = BRIGHT_RED
        
        pygame.draw.rect(screen, progress_color, (progress_x, fill_y, progress_width, fill_height))
        pygame.draw.rect(screen, light_color, (progress_x, fill_y, 4, fill_height))
        
        # 낚싯찌 첨벙 (미니게임 중)
        bobber_x = 450 + (self.power / 100) * 300
        bobber_y = 370 + math.sin(pygame.time.get_ticks() / 80) * 4
        
        draw_pixel_fishing_line(screen, (380, 280), (bobber_x, bobber_y - 10), tension=35)
        draw_pixel_bobber(screen, int(bobber_x), int(bobber_y), submerged=True)
        
        # 첨벙 효과
        if random.random() < 0.3:
            self.add_splash_particle(bobber_x, 370)
        draw_splash_particle(screen, self.splash_particles)
        
        # 물고기 정보
        info_box = pygame.Rect(30, 100, 200, 80)
        pygame.draw.rect(screen, (30, 30, 50, 200), info_box)
        pygame.draw.rect(screen, WHITE, info_box, 2)
        
        fish_info = font_medium.render(f"{fish['name']}", True, WHITE)
        screen.blit(fish_info, (45, 110))
        
        rarity_colors = {"common": WHITE, "uncommon": GREEN, "rare": (100, 149, 237), "legendary": YELLOW}
        rarity_kr = {"common": "일반", "uncommon": "고급", "rare": "희귀", "legendary": "전설"}
        rarity_text = font_small.render(f"[{rarity_kr[fish['rarity']]}]", True, rarity_colors[fish['rarity']])
        screen.blit(rarity_text, (45, 145))
        
        # 조작 안내
        help_text = font_tiny.render("SPACE/클릭: 올라가기", True, WHITE)
        screen.blit(help_text, (30, SCREEN_HEIGHT - 40))
    
    def is_fish_in_bar(self):
        if not self.current_fish:
            return False
        fish_size = self.current_fish["size"]
        fish_center = self.fish_y + fish_size / 2
        return self.bar_y <= fish_center <= self.bar_y + self.bar_height
    
    def draw_result(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        if self.caught_fish:
            text = font_large.render("물고기를 잡았다!", True, GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(text, text_rect)
            
            fish_name = font_large.render(self.caught_fish["name"], True, WHITE)
            name_rect = fish_name.get_rect(center=(SCREEN_WIDTH // 2, 210))
            screen.blit(fish_name, name_rect)
            
            rarity_colors = {"common": WHITE, "uncommon": GREEN, "rare": (100, 149, 237), "legendary": YELLOW}
            rarity_kr = {"common": "일반", "uncommon": "고급", "rare": "희귀", "legendary": "전설"}
            rarity = self.caught_fish["rarity"]
            rarity_text = font_medium.render(f"[{rarity_kr[rarity]}] - {self.caught_fish['price']}G", True, rarity_colors[rarity])
            rarity_rect = rarity_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
            screen.blit(rarity_text, rarity_rect)
            
            # 큰 물고기 그리기
            fish_display = self.caught_fish.copy()
            fish_display["size"] = 100
            draw_pixel_fish(screen, SCREEN_WIDTH // 2 - 50, 300, fish_display, 1)
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
        
        # 제목
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
                
                # 물고기 아이콘
                fish_icon = fish.copy()
                fish_icon["size"] = 35
                draw_pixel_fish(screen, 80, y_offset - 5, fish_icon, 1)
                
                rarity_colors = {"common": WHITE, "uncommon": GREEN, "rare": (100, 149, 237), "legendary": YELLOW}
                fish_text = font_small.render(f"{name} x{count}", True, rarity_colors[fish["rarity"]])
                screen.blit(fish_text, (140, y_offset))
                
                price_text = font_small.render(f"{value}G", True, YELLOW)
                screen.blit(price_text, (350, y_offset))
                
                y_offset += 35
            
            total_text = font_medium.render(f"총 가치: {total_value}G", True, YELLOW)
            screen.blit(total_text, (80, y_offset + 15))
            
            # 판매 버튼
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
                    game.handle_action()
                elif event.key == pygame.K_i:
                    game.toggle_inventory()
                elif event.key == pygame.K_ESCAPE:
                    if game.state == STATE_INVENTORY:
                        game.state = STATE_IDLE
                elif event.key == pygame.K_s:
                    if game.state == STATE_INVENTORY:
                        game.sell_all_fish()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.handle_action()
        
        game.update(dt, action_pressed)
        game.draw(screen)
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()
