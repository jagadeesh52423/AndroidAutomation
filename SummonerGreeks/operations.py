import numpy
from mss import mss
from SummonerGreeks.summoner_colors import SummonerColors
from SummonerGreeks.summoner_buttons import SummonerButtons


class SummonerOperations:
    def __init__(self, device):
        self.device = device
        self.sct = mss()
        self.colors = {
            SummonerColors.ENABLED: (245, 208, 20),
            SummonerColors.ACHIEVEMENTS_CONFIRMATION: (28, 34, 99),
            SummonerColors.DISABLED: (0, 0, 0),
            SummonerColors.SUMMONER_SCROLL: (92, 108, 153),
            SummonerColors.COMPLETED: (114, 99, 38),
            SummonerColors.COMPLETED_2: (253, 214, 68),
            SummonerColors.MONITOR_SELLER_SCROLL: (87, 195, 107),
            SummonerColors.CONFIRM_SELLER: (114, 178, 70),
            SummonerColors.CONFIRM_MONITOR: (173, 105, 63),
            SummonerColors.INSUFFICIENT_ORBS: (186, 182, 180),
            SummonerColors.MONSTER_BUY_AVAILABLE: (66, 238, 166)
        }
        self.buttons = {
            SummonerButtons.ACHIEVEMENTS: (939, 190),
            SummonerButtons.SELLER_BUY: (934, 1275),
            SummonerButtons.SELLER_OKAY: (670, 1278),
            SummonerButtons.MONITOR_REJECT: (308, 1328),
            SummonerButtons.ACHIEVEMENTS_CLOSE: (994, 140),
            SummonerButtons.ORBS: (90, 320),
            SummonerButtons.ORBS_CLOSE: (999, 78),
            SummonerButtons.COMPLETE_CONTINUE: (550, 1680),
            SummonerButtons.NEW_GAME: (541, 1526),
            SummonerButtons.NEW_GAME_CONFIRM: (545, 2253),
            SummonerButtons.UPGRADE_MONSTER: (975, 2200),
            SummonerButtons.CLOSE_UPGRADING: (1000, 2300)
        }

    def get_color(self, location, reason=None):
        color = numpy.array(self.sct.grab(location))
        baseColors = color[0][0]
        try:
            current = tuple(baseColors[0:3])
            for summoner_color in SummonerColors:
                if self.compare_color(self.colors.get(summoner_color), current):
                    print("Matched {} with {} ({}) ".format(current, summoner_color, self.colors.get(summoner_color)))
                    return summoner_color
            print(color, " is not matching with", reason + "!" if reason else " any given!")
            return None
        except KeyError as e:
            print("Key missed: ", e.args)
            return None

    @staticmethod
    def compare_color(button, current):
        for i in range(3):
            if abs(button[i] - current[i]) > 10:
                return False
        return True

    def confirm_page(self, location, color, reason=None):
        for _ in range(5):
            if self.get_color(location, reason) == color:
                return True
        return False

    def click_button(self, button=None, pointer=None):
        if button:
            pointer = self.buttons.get(button)
        self.device.shell('input tap {} {}'.format(pointer[0], pointer[1]))
