import settings
from player import Player
from reel import *
from settings import *
from ui import UI
from wins import *
import pygame


class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False

        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}

        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

        # Импорт звуков
        self.spin_sound = pygame.mixer.Sound('audio/mechanical_analog.mp3')
        self.spin_sound.set_volume(0.08)
        self.win_three = pygame.mixer.Sound('audio/win_jackpot_03 (mp3cut.net).wav')
        self.win_three.set_volume(0.5)
        self.win_four = pygame.mixer.Sound('audio/win_jackpot_04 (mp3cut.net).wav')
        self.win_four.set_volume(0.6)
        self.win_five = pygame.mixer.Sound('audio/money_jackpot (mp3cut.net).wav')
        self.win_five.set_volume(0.7)

    def cooldowns(self):
        # Позволяет игроку вращаться, только если все барабаны НЕ вращаются.
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()

            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)

                # Воспроизвести звук победы
                self.play_win_sound(self.win_data)

                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                self.ui.win_text_angle = random.randint(-4, 4)

    def input(self):
        keys = pygame.key.get_pressed()

        # Проверяет наличие клавиши пробела, возможности переключения вращения и баланса для покрытия размера ставки.
        if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size
            self.currPlayer.last_payout = None

    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    def spawn_reels(self):
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (300 + X_OFFSET), y_topleft

            self.reel_list[self.reel_index] = Reel((x_topleft, y_topleft))
            self.reel_index += 1

    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False

            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                self.spin_sound.play()
                self.win_animation_ongoing = False

    def get_result(self):
        for reel in self.reel_list:
            self.spin_result[reel] = self.reel_list[reel].reel_spin_result()

        return self.spin_result

    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        result_v = [None, None, None, None, None]
        result_v[0], result_v[1], result_v[2], result_v[3], result_v[4] = horizontal[0][0], horizontal[1][1], \
                                                                          horizontal[2][2], horizontal[1][3], \
                                                                          horizontal[0][4]

        result_inverted_v = [None, None, None, None, None]
        result_inverted_v[0], result_inverted_v[1], result_inverted_v[2], result_inverted_v[3], result_inverted_v[4] = \
                                                                                horizontal[2][0], horizontal[1][1], \
                                                                                horizontal[0][2], horizontal[1][3], \
                                                                                horizontal[2][4]
        if all(x == result_v[0] for x in result_v):
            hits = {4: [result_v[0], [0, 1, 2, 3, 4]]}
            self.can_animate = True
            return hits
        elif all(x == result_inverted_v[0] for x in result_inverted_v):
            hits = {5: [result_inverted_v[0], [0, 1, 2, 3, 4]]}
            self.can_animate = True
            return hits
        else:
            for row in horizontal:
                for sym in row:
                    if row.count(sym) > 4 and sym != 'Енот':  # Потенциальная победа
                        possible_win = [idx for idx, val in enumerate(row) if sym == val]
                        # Проверяем possible_win на наличие подпоследовательности длиной более 2 и добавляем к попаданиям
                        if len(longest_seq(possible_win)) > 2:
                            hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
            if hits:
                self.can_animate = True
                return hits

    def pay_player(self, win_data, curr_player):
        multiplier = sum(len(v[1]) for v in win_data.values())
        payout_mapping = {
            5: 'five_row',
        }

        spin_payout = settings.payouts.get(payout_mapping.get(multiplier, None), 0) * curr_player.bet_size

        curr_player.balance += spin_payout
        self.machine_balance -= spin_payout
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout

    def play_win_sound(self, win_data):
        sum = 0
        for item in win_data.values():
            sum += len(item[1])
        if sum == 3:
            self.win_three.play()
        elif sum == 4:
            self.win_four.play()
        elif sum > 4:
            self.win_five.play()

    def win_animation(self):
        if self.win_animation_ongoing and self.win_data:
            for k, v in list(self.win_data.items()):
                if k == 1:
                    animationRow = 3
                elif k == 3:
                    animationRow = 1
                elif k == 2:
                    animationRow = 2
                elif k == 4:
                    animationRow = 4
                else:
                    animationRow = 5
                animationCols = v[1]
                if animationRow <= 3:
                    for reel in self.reel_list:
                        if reel in animationCols and self.can_animate:
                            self.reel_list[reel].symbol_list.sprites()[animationRow].fade_in = True
                        for symbol in self.reel_list[reel].symbol_list:
                            if not symbol.fade_in:
                                symbol.fade_out = True
                elif animationRow == 4:
                    for reel_index, symbol_index in [(0, 3), (1, 2), (2, 1), (3, 2), (4, 3)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_in = True
                    for reel_index, symbol_index in [(1, 3), (2, 3), (3, 3), (0, 2), (2, 2), (4, 2), (0, 1),
                                                     (1, 1), (3, 1), (4, 1)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_out = True
                else:
                    for reel_index, symbol_index in [(0, 1), (1, 2), (2, 3), (3, 2), (4, 1)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_in = True
                    for reel_index, symbol_index in [(0, 3), (1, 3), (3, 3), (4, 3), (0, 2), (2, 2), (4, 2),
                                                     (1, 1), (2, 1), (3, 1)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_out = True

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update()
        self.ui.update()
        self.win_animation()
