"""물고기, 상점, 희귀도 데이터."""
from game.config import GRAY, WHITE, GREEN, YELLOW

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
