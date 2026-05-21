import pygame
import sys

# =========================================================
# 초기 설정
# =========================================================

pygame.init()

# =========================================================
# 화면 설정
# 나중에 수정하기 쉽게 변수화
# =========================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fishing Game")

# =========================================================
# FPS 설정
# =========================================================

clock = pygame.time.Clock()
FPS = 60

# =========================================================
# 색상 설정
# 원하는 색으로 자유롭게 수정 가능
# =========================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BACKGROUND_COLOR = (120, 190, 255)

BUTTON_COLOR = (240, 240, 240)
BUTTON_HOVER_COLOR = (180, 220, 255)

TITLE_COLOR = (255, 255, 255)

# =========================================================
# 폰트 설정
# 시스템 폰트 사용
# 폰트 이름/크기 수정 가능
# =========================================================

TITLE_FONT = pygame.font.SysFont("malgungothic", 80)
MENU_FONT = pygame.font.SysFont("malgungothic", 35)

# =========================================================
# 게임 상태 설정
# =========================================================

current_scene = "title"

# =========================================================
# 타이틀 애니메이션 설정
# =========================================================

title_text = "FISHING GAME"

title_y = -150
title_target_y = 120

title_speed = 5

show_menu = False

# =========================================================
# 버튼 설정
# 버튼 위치 및 크기 수정 가능
# =========================================================

button_width = 250
button_height = 70

button_gap = 20

menu_buttons = [
    {
        "text": "낚시",
        "scene": "fishing",
    },
    {
        "text": "상점",
        "scene": "shop",
    },
    {
        "text": "가방",
        "scene": "inventory",
    },
    {
        "text": "도감",
        "scene": "collection",
    },
    {
        "text": "업적",
        "scene": "achievement",
    }
]

# =========================================================
# 버튼 Rect 생성
# =========================================================

button_rects = []

start_y = 260

for i, button in enumerate(menu_buttons):

    rect = pygame.Rect(
        SCREEN_WIDTH // 2 - button_width // 2,
        start_y + i * (button_height + button_gap),
        button_width,
        button_height
    )

    button_rects.append(rect)

# =========================================================
# 장면별 배경 색상
# 임시용
# =========================================================

scene_colors = {
    "fishing": (100, 180, 255),
    "shop": (255, 220, 120),
    "inventory": (180, 180, 180),
    "collection": (140, 255, 180),
    "achievement": (255, 180, 120),
}

# =========================================================
# 메인 루프
# =========================================================

running = True

while running:

    # =====================================================
    # 이벤트 처리
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # =================================================
        # 마우스 클릭 처리
        # =================================================

        if event.type == pygame.MOUSEBUTTONDOWN:

            # 메뉴 화면에서만 버튼 클릭 가능
            if show_menu and current_scene == "title":

                for i, rect in enumerate(button_rects):

                    if rect.collidepoint(event.pos):

                        current_scene = menu_buttons[i]["scene"]

            # 다른 장면에서 ESC 누르면 타이틀 복귀
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                current_scene = "title"

    # =====================================================
    # 타이틀 화면
    # =====================================================

    if current_scene == "title":

        screen.fill(BACKGROUND_COLOR)

        # =================================================
        # 타이틀 내려오는 애니메이션
        # =================================================

        if title_y < title_target_y:

            title_y += title_speed

        else:
            show_menu = True

        # =================================================
        # 타이틀 출력
        # =================================================

        title_surface = TITLE_FONT.render(title_text, True, TITLE_COLOR)

        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, title_y))

        screen.blit(title_surface, title_rect)

        # =================================================
        # 메뉴 버튼 출력
        # =================================================

        if show_menu:

            mouse_pos = pygame.mouse.get_pos()

            for i, rect in enumerate(button_rects):

                # 마우스 올리면 색 변경
                if rect.collidepoint(mouse_pos):
                    color = BUTTON_HOVER_COLOR
                else:
                    color = BUTTON_COLOR

                pygame.draw.rect(
                    screen,
                    color,
                    rect,
                    border_radius=15
                )

                # 버튼 텍스트 출력
                text_surface = MENU_FONT.render(
                    menu_buttons[i]["text"],
                    True,
                    BLACK
                )

                text_rect = text_surface.get_rect(center=rect.center)

                screen.blit(text_surface, text_rect)

    # =====================================================
    # 낚시 화면
    # =====================================================

    elif current_scene == "fishing":

        screen.fill(scene_colors["fishing"])

        text = TITLE_FONT.render("낚시 화면", True, WHITE)

        screen.blit(text, (80, 80))

    # =====================================================
    # 상점 화면
    # =====================================================

    elif current_scene == "shop":

        screen.fill(scene_colors["shop"])

        text = TITLE_FONT.render("상점 화면", True, BLACK)

        screen.blit(text, (80, 80))

    # =====================================================
    # 가방 화면
    # =====================================================

    elif current_scene == "inventory":

        screen.fill(scene_colors["inventory"])

        text = TITLE_FONT.render("가방 화면", True, WHITE)

        screen.blit(text, (80, 80))

    # =====================================================
    # 도감 화면
    # =====================================================

    elif current_scene == "collection":

        screen.fill(scene_colors["collection"])

        text = TITLE_FONT.render("도감 화면", True, BLACK)

        screen.blit(text, (80, 80))

    # =====================================================
    # 업적 화면
    # =====================================================

    elif current_scene == "achievement":

        screen.fill(scene_colors["achievement"])

        text = TITLE_FONT.render("업적 화면", True, BLACK)

        screen.blit(text, (80, 80))

    # =====================================================
    # 화면 업데이트
    # =====================================================

    pygame.display.update()

    # =====================================================
    # FPS 적용
    # =====================================================

    clock.tick(FPS)

# =========================================================
# 게임 종료
# =========================================================

pygame.quit()
sys.exit()