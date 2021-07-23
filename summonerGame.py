from ppadb.client import Client
import numpy
import time
from mss import mss
from enum import Enum, auto


class SummonerGame:
    def __init__(self, device, sct):
        self.device = device
        self.sct = sct
        self.colors = {
            SummonerColors.ENABLED: (245, 208, 20),
            SummonerColors.ACHIEVEMENTS_CONFIRMATION: (28, 34, 99),
            SummonerColors.DISABLED: (0, 0, 0),
            SummonerColors.SUMMONER_SCROLL: (92, 108, 153),
            SummonerColors.COMPLETED: (114, 99, 38),
            SummonerColors.COMPLETED_2: (253, 214, 68),
            SummonerColors.MONITOR_SELLER_SCROLL: (87, 195, 107),
            SummonerColors.CONFIRM_SELLER: (114, 178, 70),
            SummonerColors.CONFIRM_MONITOR: (173, 105, 63)
        }
        self.buttons = {
            SummonerButtons.ACHIEVEMENTS: (939, 190),
            SummonerButtons.SELLER_BUY: (925, 1264),
            SummonerButtons.SELLER_OKAY: (670, 1278),
            SummonerButtons.MONITOR_REJECT: (308, 1328),
            SummonerButtons.ACHIEVEMENTS_CLOSE: (994, 140),
            SummonerButtons.ORBS: (90, 320),
            SummonerButtons.ORBS_CLOSE: (999, 78),
            SummonerButtons.COMPLETE_CONTINUE: (550, 1680),
            SummonerButtons.NEW_GAME: (541, 1526),
            SummonerButtons.NEW_GAME_CONFIRM: (545, 2253)
        }

    def start(self):
        self.gamePage()

    def gamePage(self):
        while True:
            achievements_location = {'left': 419, 'top': 147, 'width': 1, 'height': 1}
            if self.get_color(achievements_location, reason='achievements check') == SummonerColors.ENABLED:
                self.achievementsPage()

            orbs_location = {'left': 72, 'top': 189, 'width': 1, 'height': 1}
            if self.get_color(orbs_location, reason='orbs collection') == SummonerColors.ENABLED:
                self.orbsPage()

            game_complete_check_location = {'left': 8, 'top': 67, 'width': 1, 'height': 1}
            if self.get_color(game_complete_check_location, reason='game complete check') in [SummonerColors.COMPLETED, SummonerColors.COMPLETED_2]:
                self.completePage()

            monitor_seller_banner_location = {'left': 140, 'top': 303, 'width': 1, 'height': 1}
            if self.get_color(monitor_seller_banner_location, reason='seller-monitor check') == SummonerColors.MONITOR_SELLER_SCROLL:
                monitor_seller_character_location = {'left': 415, 'top': 878, 'width': 1, 'height': 1}
                time.sleep(1)
                if self.get_color(monitor_seller_character_location, reason='confirm seller') == SummonerColors.CONFIRM_SELLER:
                    self.sellerPage()
                elif self.get_color(monitor_seller_character_location, reason='confirm monitor') == SummonerColors.CONFIRM_MONITOR:
                    self.monitorPage()

            time.sleep(1)

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

    def achievementsPage(self):
        self.click_button(SummonerButtons.ACHIEVEMENTS)
        print("On Page: Achievements")
        time.sleep(1)
        confirmation_location = {'left': 34, 'top': 159, 'width': 1, 'height': 1}
        if self.get_color(confirmation_location, reason='achievements page confirmation') != SummonerColors.ACHIEVEMENTS_CONFIRMATION:
            print("Achievements page mismatch! Going back!")
            return

        buttons = [(904, 342), (904, 572), (904, 798), (904, 1058), (904, 1298), (904, 1519), (904, 1759), (904, 1996)]
        for button in buttons:
            self.device.shell('input tap {} {}'.format(button[0], button[1]))

        self.click_button(SummonerButtons.ACHIEVEMENTS_CLOSE)
        print("Closing Achievements page!")

    def sellerPage(self):
        time.sleep(1)
        self.click_button(SummonerButtons.SELLER_BUY)
        print("On Page: Seller!")
        self.click_button(SummonerButtons.SELLER_OKAY)
        print("Returned from seller page!")
        time.sleep(0.2)

    def monitorPage(self):
        time.sleep(1)
        self.click_button(SummonerButtons.MONITOR_REJECT)
        print("Rejecting monitor ad!")
        # time.sleep(0.5)
        # self.click_button(SummonerButtons.SELLER_OKAY)
        # print("Returned from seller page!")

    def completePage(self):
        self.click_button(SummonerButtons.COMPLETE_CONTINUE)
        print("Congratulations on completing game!")
        time.sleep(0.5)
        print("Starting new game!")
        self.click_button(SummonerButtons.NEW_GAME)
        time.sleep(1.5)
        print("Confirm new game!")
        self.click_button(SummonerButtons.NEW_GAME_CONFIRM)

    def confirm_page(self, location, color, reason=None):
        for _ in range(5):
            if self.get_color(location, reason) == color:
                return True
        return False

    def click_button(self, button):
        pointer = self.buttons.get(button)
        self.device.shell('input tap {} {}'.format(pointer[0], pointer[1]))

    def orbsPage(self):
        self.click_button(SummonerButtons.ORBS)
        print("On Page: Orbs")

        time.sleep(1)
        scroll_location = {'left': 62, 'top': 137, 'width': 1, 'height': 1}
        if not self.confirm_page(scroll_location, SummonerColors.SUMMONER_SCROLL, reason='orbs page confirmation'):
            print("Orbs page mismatch!")
            return

        buttons = {'orb_buy_10': (195, 2265), 'skip_button' : (548, 2265), 'continue_button': (548, 1176)}
        for button in buttons.values():
            self.device.shell('input tap {} {}'.format(button[0], button[1]))
            time.sleep(0.5)

        self.click_button(SummonerButtons.ORBS_CLOSE)
        print("Closing Orbs page!")
        pass


class SummonerColors(Enum):
    ENABLED = auto(),
    ACHIEVEMENTS_CONFIRMATION = auto(),
    SUMMONER_SCROLL = auto(),
    DISABLED = auto(),
    COMPLETED = auto(),
    COMPLETED_2 = auto(),
    MONITOR_SELLER_SCROLL = auto(),
    CONFIRM_SELLER = auto(),
    CONFIRM_MONITOR = auto()


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
    NEW_GAME = auto(),
    NEW_GAME_CONFIRM = auto()


if __name__ == '__main__':
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()

    # set screen end at 479,30
    if len(devices) == 0:
        print("No devices available!")
        quit()

    device = devices[0]
    sct = mss()
    game = SummonerGame(device, sct)
    game.start()
    # location = {'left': 416, 'top': 883, 'width': 1, 'height': 1}
    # 416, 88
    # print(game.get_color(location))

