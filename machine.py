import settings
from player import Player
from reel import *
from settings import *
from ui import UI
from wins import *
import pygame
import time


class Machine:
    def __init__(self, ui):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 1000.00
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False
        self.ui = ui
        # Добавление кнопок "+" и "-" внизу экрана
        self.plus_button_image = pygame.image.load('graphics/1/icons8-плюс-48.png').convert_alpha()
        self.minus_button_image = pygame.image.load('graphics/1/icons8-minus-48.png').convert_alpha()
        self.plus_button_rect = self.plus_button_image.get_rect(bottomleft=(1290, 980))
        self.minus_button_rect = self.minus_button_image.get_rect(bottomright=(1270, 980))
        self.last_button_press_time = 0.0
        self.increase_bet_flag = False
        self.decrease_bet_flag = False

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

        # if keys[pygame.K_EQUALS]:
        #     self.currPlayer.increase_bet()
        # elif keys[pygame.K_MINUS]:
        #     self.currPlayer.decrease_bet()

        # Проверьте нажатия на кнопки "+/-" на экране
        self.after_spin()
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.plus_button_rect.collidepoint(mouse_pos):
                self.increase_bet()
            elif self.minus_button_rect.collidepoint(mouse_pos):
                self.decrease_bet()
        max_win = self.checking_maximum_win()
        self.maximum_bet_scroll()
        # Проверяет наличие клавиши пробела, возможности переключения вращения и баланса для покрытия размера ставки.
        # if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
        if keys[pygame.K_SPACE] and self.can_toggle and self.machine_balance >= max_win:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.place_bet()
            self.balance_machine()

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
        result_one = [None, None, None, None, None]
        result_two = [None, None, None, None, None]
        result_three = [None, None, None, None, None]
        result_one[0], result_one[1], result_one[2], result_one[3], result_one[4] = horizontal[0][0], horizontal[0][1], \
                                                                          horizontal[0][2], horizontal[0][3], \
                                                                          horizontal[0][4]
        result_two[0], result_two[1], result_two[2], result_two[3], result_two[4] = horizontal[1][0], horizontal[1][1], \
                                                                          horizontal[1][2], horizontal[1][3], \
                                                                          horizontal[1][4]
        result_three[0], result_three[1], result_three[2], result_three[3], result_three[4] = horizontal[2][0], horizontal[2][1], \
                                                                          horizontal[2][2], horizontal[2][3], \
                                                                          horizontal[2][4]
        result_v = [None, None, None, None, None]
        result_v[0], result_v[1], result_v[2], result_v[3], result_v[4] = horizontal[0][0], horizontal[1][1], \
                                                                          horizontal[2][2], horizontal[1][3], \
                                                                          horizontal[0][4]

        result_inverted_v = [None, None, None, None, None]
        result_inverted_v[0], result_inverted_v[1], result_inverted_v[2], result_inverted_v[3], result_inverted_v[4] = \
                                                                                horizontal[2][0], horizontal[1][1], \
                                                                                horizontal[0][2], horizontal[1][3], \
                                                                               horizontal[2][4]
        if all(symbol == result_one[0] != 'Енот' for symbol in result_one) and all(
                result_one[i] == result_two[i] for i in range(len(result_one))):
            hits = {6: [result_v[0], [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]]}
            self.can_animate = True
            return hits

        elif all(symbol == result_two[0] != 'Енот' for symbol in result_two) and all(
                result_two[i] == result_three[i] for i in range(len(result_two))):
            hits = {7: [result_v[0], [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]]}
            self.can_animate = True
            return hits

        elif all(symbol == result_three[0] != 'Енот' for symbol in result_three) and all(
                result_one[i] == result_three[i] for i in range(len(result_one))):
            hits = {8: [result_v[0], [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]]}
            self.can_animate = True
            return hits
        elif all(x == result_v[0] != 'Енот' for x in result_v):
            hits = {4: [result_v[0], [0, 1, 2, 3, 4]]}
            self.can_animate = True
            return hits
        elif all(x == result_inverted_v[0] != 'Енот' for x in result_inverted_v):
            hits = {5: [result_inverted_v[0], [0, 1, 2, 3, 4]]}
            self.can_animate = True
            return hits

        elif all(x == result_one[0] != 'Енот' for x in result_one):
            hits = {9: [result_one[0], [0, 1, 2, 3, 4]]}
            self.can_animate = True
            return hits
        elif all(x == result_two[0] != 'Енот' for x in result_two):
            hits = {10: [result_two[0], [0, 1, 2, 3, 4]]}
            self.can_animate = True
            return hits
        elif all(x == result_three[0] != 'Енот' for x in result_three):
            hits = {11: [result_three[0], [0, 1, 2, 3, 4]]}
            self.can_animate = True
            return hits
        else:
            for row in horizontal:
                for sym in row:
                    if row.count(sym) > 2  and sym != 'Енот':  # Потенциальная победа
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
            7: 'three_row',
            6: 'three_row',
            # 8: 'three_row',
            3: 'three_row',
            10: 'ten_row'
        }

        spin_payout = settings.payouts.get(payout_mapping.get(multiplier, None), 0) * curr_player.bet_size
        curr_player.balance += spin_payout
        # Уменьшение баланса машины на выигрыш
        self.machine_balance -= spin_payout
        ###########################
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout

    def play_win_sound(self, win_data):
        sum = 0
        for item in win_data.values():
            sum += len(item[1])
        # if sum == 3:
        #     self.win_three.play()
        # elif sum > 4:
        #     self.win_four.play()
        if sum == 5:
            self.win_five.play()

    def win_animation(self):
        if self.win_animation_ongoing and self.win_data:
            flag = True
            for k, v in list(self.win_data.items()):
                data = self.win_data.items()
                win_numbers = list(data)[0][1][1]
                if len(win_numbers) == 3 and flag is False:
                    continue
                if len(win_numbers) == 3:
                    flag = False
                if len(v[1]) == 4:
                    continue
                mapping = {
                    1: 3,
                    3: 1,
                    2: 2,
                    4: 4,
                    5: 5,
                    6: 6,
                    7: 7,
                    8: 8,
                    9: 9,
                    10: 10
                }

                animationRow = mapping.get(k, 11)
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
                elif animationRow == 5:
                    for reel_index, symbol_index in [(0, 1), (1, 2), (2, 3), (3, 2), (4, 1)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_in = True
                    for reel_index, symbol_index in [(0, 3), (1, 3), (3, 3), (4, 3), (0, 2), (2, 2), (4, 2),
                                                     (1, 1), (2, 1), (3, 1)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_out = True
                elif animationRow == 6:
                    for reel_index, symbol_index in [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
                                                     (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_in = True
                    for reel_index, symbol_index in [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_out = True
                elif animationRow == 7:
                    for reel_index, symbol_index in [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
                                                     (0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_in = True
                    for reel_index, symbol_index in [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_out = True
                elif animationRow == 8:
                    for reel_index, symbol_index in [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                                                     (0, 3), (1, 3), (2, 3), (3, 3), (4, 3)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_in = True
                    for reel_index, symbol_index in [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_out = True


                elif animationRow == 9:
                    for reel_index, symbol_index in [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_in = True
                    for reel_index, symbol_index in [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                                                     (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_out = True

                elif animationRow == 10:
                    for reel_index, symbol_index in [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_in = True
                    for reel_index, symbol_index in [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                                                     (0, 3), (1, 3), (2, 3), (3, 3), (4, 3)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_out = True

                elif animationRow == 11:
                    for reel_index, symbol_index in [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_in = True
                    for reel_index, symbol_index in [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
                                                     (0, 2), (1, 2), (2, 2), (3, 2), (4, 2)]:
                        self.reel_list[reel_index].symbol_list.sprites()[symbol_index].fade_out = True

    def balance_machine(self):
        """Увеличение баланса машины на ставку игрока"""
        self.machine_balance += self.currPlayer.bet_size
        return self.machine_balance

    def checking_maximum_win(self):
        """Проверка макимального выигрыша за данный прокрут"""
        maximum_win_scroll = self.currPlayer.bet_size * settings.payouts.get("ten_row")
        return maximum_win_scroll

    def maximum_bet_scroll(self):
        """Максимальная ставка для данного прокрута"""
        maximum_bet = self.machine_balance / settings.payouts.get("ten_row")
        print(f"Баланс машины - {self.machine_balance}")
        print(int(maximum_bet))
        return int(maximum_bet)

    def increase_bet(self):
        """Увеличение ставки на 10, но не превышая максимальное значение. Кнопка реагирует только каждые 0.3сек"""
        current_time = time.time()
        if current_time - self.last_button_press_time >= 0.3:
            maximum_bet = int(self.maximum_bet_scroll())
            self.currPlayer.bet_size = min(self.currPlayer.bet_size + 10.00, maximum_bet)

            self.last_button_press_time = current_time

    def decrease_bet(self):
        """Уменьшение ставки на 10, но не менее 10. Кнопка реагирует только каждые 0.3сек"""
        current_time = time.time()
        if current_time - self.last_button_press_time >= 0.3:
            self.currPlayer.bet_size = max(10.00, self.currPlayer.bet_size - 10.00)
            self.last_button_press_time = current_time

    def after_spin(self):
        """Исправление ставки на макимально возможную"""
        if self.currPlayer.bet_size > self.maximum_bet_scroll():
            self.currPlayer.bet_size = self.maximum_bet_scroll()

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update()
        self.ui.update()
        self.win_animation()
