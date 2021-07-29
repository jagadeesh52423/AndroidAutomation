from ppadb.client import Client
import time
from SummonerGreeks.summoner_buttons import SummonerButtons
from SummonerGreeks.summoner_colors import SummonerColors
from SummonerGreeks.operations import SummonerOperations


class SummonerGame:
    def __init__(self, device, monster_no=0):
        self.operations = SummonerOperations(device)
        self.monster_no = monster_no

    def start(self):
        self.gamePage()

    def gamePage(self):
        while True:
            achievements_location = {'left': 419, 'top': 147, 'width': 1, 'height': 1}
            if self.operations.get_color(achievements_location, reason='achievements check') == SummonerColors.ENABLED:
                self.achievementsPage()

            game_complete_check_location = {'left': 8, 'top': 67, 'width': 1, 'height': 1}
            if self.operations.get_color(game_complete_check_location, reason='game complete check') in [SummonerColors.COMPLETED, SummonerColors.COMPLETED_2]:
                self.completePage()

            orbs_location = {'left': 72, 'top': 189, 'width': 1, 'height': 1}
            if self.operations.get_color(orbs_location, reason='orbs collection') == SummonerColors.ENABLED:
                self.orbsPage()
                time.sleep(1)
                self.upgradeMonsterPage()

            monitor_seller_banner_location = {'left': 140, 'top': 303, 'width': 1, 'height': 1}
            if self.operations.get_color(monitor_seller_banner_location, reason='seller-monitor check') == SummonerColors.MONITOR_SELLER_SCROLL:
                monitor_seller_character_location = {'left': 415, 'top': 878, 'width': 1, 'height': 1}
                time.sleep(1)
                monitor_or_seller_confirmation = self.operations.get_color(monitor_seller_character_location, reason='confirm seller')
                if monitor_or_seller_confirmation == SummonerColors.CONFIRM_SELLER:
                    self.sellerPage()
                elif monitor_or_seller_confirmation == SummonerColors.CONFIRM_MONITOR:
                    self.monitorPage()

            time.sleep(1)

    def achievementsPage(self):
        self.operations.click_button(SummonerButtons.ACHIEVEMENTS)
        print("On Page: Achievements")
        time.sleep(1)
        confirmation_location = {'left': 34, 'top': 159, 'width': 1, 'height': 1}
        if self.operations.get_color(confirmation_location, reason='achievements page confirmation') != SummonerColors.ACHIEVEMENTS_CONFIRMATION:
            print("Achievements page mismatch! Going back!")
            return

        buttons = [(904, 342), (904, 572), (904, 798), (904, 1058), (904, 1298), (904, 1519), (904, 1759), (904, 1996)]
        for button in buttons:
            self.operations.click_button(pointer=button)

        self.operations.click_button(SummonerButtons.ACHIEVEMENTS_CLOSE)
        print("Closing Achievements page!")

    def sellerPage(self):
        time.sleep(0.5)
        self.operations.click_button(SummonerButtons.SELLER_BUY)
        print("On Page: Seller!")
        time.sleep(1)
        self.operations.click_button(SummonerButtons.SELLER_OKAY)
        print("Returned from seller page!")
        time.sleep(0.2)

    def monitorPage(self):
        time.sleep(0.2)
        self.operations.click_button(SummonerButtons.MONITOR_REJECT)
        print("Rejecting monitor ad!")
        # time.sleep(0.5)
        # self.click_button(SummonerButtons.SELLER_OKAY)
        # print("Returned from seller page!")

    def completePage(self):
        self.operations.click_button(SummonerButtons.COMPLETE_CONTINUE)
        print("Congratulations on completing game!")
        time.sleep(0.5)
        print("Starting new game!")
        self.operations.click_button(SummonerButtons.NEW_GAME)
        time.sleep(1.5)
        print("Confirm new game!")
        self.operations.click_button(SummonerButtons.NEW_GAME_CONFIRM)

    def upgradeMonsterPage(self):
        if self.monster_no == 0:
            return
        if self.monster_no > 9:
            raise AttributeError('We\'ve only 9 monsters!')
        self.operations.click_button(SummonerButtons.UPGRADE_MONSTER)
        click_rows = (368, 650, 925)
        click_cols = (750, 1150, 1575)
        color_rows = (164, 286, 407)
        color_cols = (387, 565, 744)
        row_index = (self.monster_no - 1) % 3
        col_index = (self.monster_no - 1) // 3
        while True:
            self.operations.click_button(pointer=(click_rows[row_index], click_cols[col_index]))
            monster_color_location = {'left': color_rows[row_index], 'top': color_cols[col_index], 'width': 1, 'height': 1}
            print("Clicking", click_rows[row_index], click_cols[col_index])
            if self.operations.get_color(monster_color_location) != SummonerColors.MONSTER_BUY_AVAILABLE:
                break
        self.operations.click_button(SummonerButtons.CLOSE_UPGRADING)

    def orbsPage(self):
        self.operations.click_button(SummonerButtons.ORBS)
        print("On Page: Orbs")

        time.sleep(1)
        scroll_location = {'left': 62, 'top': 137, 'width': 1, 'height': 1}
        if not self.operations.confirm_page(scroll_location, SummonerColors.SUMMONER_SCROLL, reason='orbs page confirmation'):
            print("Orbs page mismatch!")
            return

        while True:
            buttons = {'orb_buy_10': (195, 2265), 'skip_button' : (548, 2265), 'continue_button': (548, 1176)}
            for button in buttons.values():
                self.operations.click_button(pointer=button)
                time.sleep(0.5)

            location = {'left': 124, 'top': 1044, 'width': 1, 'height': 1}
            if self.operations.get_color(location) == SummonerColors.INSUFFICIENT_ORBS:
                break
            time.sleep(0.5)

        time.sleep(0.5)
        self.operations.click_button(SummonerButtons.ORBS_CLOSE)
        print("Closing Orbs page!")
        pass


if __name__ == '__main__':
    adb = Client(host='127.0.0.1', port=5037)
    devices = adb.devices()

    # set screen end at 479,30
    if len(devices) == 0:
        print("No devices available!")
        quit()

    device = devices[0]
    game = SummonerGame(device, 0)
    game.start()
    # location = {'left': 405, 'top': 743, 'width': 1, 'height': 1}
    # print(game.operations.get_color(location))

