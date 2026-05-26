"""FishingGame — 모든 믹스인을 합친 메인 클래스."""
from game.fishing_game.achievement.mixin import AchievementMixin
from game.fishing_game.bag.mixin import BagMixin
from game.fishing_game.core import CoreMixin
from game.fishing_game.fishing.mixin import FishingMixin
from game.fishing_game.shop.mixin import ShopMixin


class FishingGame(
    CoreMixin,
    FishingMixin,
    ShopMixin,
    BagMixin,
    AchievementMixin,
):
    pass
