"""타이틀 화면 UI 상태."""
import pygame
from game.config import SCREEN_WIDTH, SCREEN_HEIGHT, STATE_IDLE, STATE_SHOP_MAIN, STATE_INVENTORY, STATE_COLLECTION, STATE_ACHIEVEMENT

title_text   = "FISHING GAME"
title_y      = -150
title_target_y = 100
title_speed  = 5
show_menu    = False

# 메뉴 버튼 설정
menu_buttons = [
    {"text": "GAME START", "scene": STATE_IDLE},
    {"text": "상점",        "scene": STATE_SHOP_MAIN},
    {"text": "가방",        "scene": STATE_INVENTORY},
    {"text": "도감",        "scene": STATE_COLLECTION},
    {"text": "업적",        "scene": STATE_ACHIEVEMENT},
]

# 버튼 크기
BTN_SIDE_W  = 220   # 좌우 버튼 너비
BTN_SIDE_H  = 100   # 좌우 버튼 높이
BTN_MID_W   = 280   # 가운데 버튼 너비
BTN_MID_H   = 70    # 가운데 버튼 높이
BTN_V_GAP   = 30    # 좌우 버튼 세로 간격
BTN_H_PAD   = 80    # 좌우 버튼 좌/우 여백

center_y    = SCREEN_HEIGHT // 2 + 60   # 버튼 그룹 세로 중심

# 좌측 버튼 x
left_x  = BTN_H_PAD
# 우측 버튼 x
right_x = SCREEN_WIDTH - BTN_H_PAD - BTN_SIDE_W
# 좌우 버튼 상단 y (두 버튼이 세로 중심에 오도록)
side_top_y = center_y - BTN_SIDE_H - BTN_V_GAP // 2

button_rects = [
    # 0: GAME START (가운데)
    pygame.Rect(SCREEN_WIDTH // 2 - BTN_MID_W // 2,
                center_y - BTN_MID_H // 2,
                BTN_MID_W, BTN_MID_H),
    # 1: 상점 (왼쪽 위)
    pygame.Rect(left_x, side_top_y, BTN_SIDE_W, BTN_SIDE_H),
    # 2: 가방 (왼쪽 아래)
    pygame.Rect(left_x, side_top_y + BTN_SIDE_H + BTN_V_GAP, BTN_SIDE_W, BTN_SIDE_H),
    # 3: 도감 (오른쪽 위)
    pygame.Rect(right_x, side_top_y, BTN_SIDE_W, BTN_SIDE_H),
    # 4: 업적 (오른쪽 아래)
    pygame.Rect(right_x, side_top_y + BTN_SIDE_H + BTN_V_GAP, BTN_SIDE_W, BTN_SIDE_H),
]
