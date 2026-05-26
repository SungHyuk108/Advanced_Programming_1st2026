"""화면, 색상, 게임 상태 상수."""
# =========================================================
# 화면 설정
# ========================================================

SCALE = 2
BASE_WIDTH = 512
BASE_HEIGHT = 288
SCREEN_WIDTH = BASE_WIDTH * SCALE   # 1024
SCREEN_HEIGHT = BASE_HEIGHT * SCALE # 576

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
