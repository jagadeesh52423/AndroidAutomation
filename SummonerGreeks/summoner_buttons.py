from enum import Enum, auto


class SummonerButtons(Enum):
    GAME = (0, 0),
    ACHIEVEMENTS = auto(),
    SELLER_BUY = auto(),
    SELLER_OKAY = auto(),
    MONITOR_REJECT = auto(),
    WATCHER = auto(),
    ACHIEVEMENTS_CLOSE = auto(),
    ORBS = auto(),
    ORBS_CLOSE = auto(),
    COMPLETE_CONTINUE = auto(),
    NEW_GAME_CONFIRM = auto(),
    UPGRADE_MONSTER = auto(),
    CLOSE_UPGRADING = auto(),
    SETTINGS = auto(),
    MAP_SELECT = auto(),
    JOINT_REVENGE_HARD_MAP = auto()
