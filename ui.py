from player import Player
from settings import *
import pygame, random


class UI:
    def __init__(self, player):
        self.player = player
        self.plus_button_pressed = False
        self.minus_button_pressed = False
        # Добавьте кнопки "+/-"
        self.plus_button_image = pygame.image.load('graphics/1/icons8-плюс-48.png').convert_alpha()
        self.minus_button_image = pygame.image.load('graphics/1/icons8-minus-48.png').convert_alpha()
        self.plus_button_rect = self.plus_button_image.get_rect(bottomleft=(1290, 980))
        self.minus_button_rect = self.minus_button_image.get_rect(bottomright=(1270, 980))
        self.display_surface = pygame.display.get_surface()
        try:
            self.font, self.bet_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE), pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        except:
            pass
            # Вывод для настроек
            # print("Ошибка загрузки шрифта!")
            # print(f"В настоящее время переменная UI_FONT имеет значение {UI_FONT}")
            # print("Существует ли файл?")
            # quit()
        self.win_text_angle = random.randint(-4, 4)

    def display_info(self):
        player_data = self.player.get_data()

        # Баланс и размер ставки
        # balance_surf = self.font.render("Balance: $" + player_data['balance'], True, TEXT_COLOR, None)
        x, y = 20, self.display_surface.get_size()[1] - 30
        # balance_rect = balance_surf.get_rect(bottomleft = (x, y))

        bet_surf = self.bet_font.render("Wager: $" + player_data['bet_size'], True, TEXT_COLOR, None)
        x = self.display_surface.get_size()[0] - 20
        bet_rect = bet_surf.get_rect(bottomright = (x, y))

        # Рисования данных игрока
        # pygame.draw.rect(self.display_surface, False, balance_rect)
        pygame.draw.rect(self.display_surface, False, bet_rect)
        # self.display_surface.blit(balance_surf, balance_rect)
        self.display_surface.blit(bet_surf, bet_rect)

        # Распечатайте последний выигрыш, если есть.
        if self.player.last_payout:
            last_payout = player_data['last_payout']
            win_surf = self.win_font.render("WIN! $" + last_payout, True, TEXT_COLOR, None)
            x1 = 800
            y1 = self.display_surface.get_size()[1] - 60
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center=(x1, y1))
            self.display_surface.blit(win_surf, win_rect)

    def display_buttons(self):
        # Отображение кнопок "+/-"
        self.display_surface.blit(self.plus_button_image, self.plus_button_rect)
        self.display_surface.blit(self.minus_button_image, self.minus_button_rect)

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))
        self.display_info()
        self.display_buttons()

    def stop_spinning_with_loss(self):
        # Получаем текущее состояние барабанов после остановки
        spin_result = self.get_spin_result()
        # Определяем комбинации символов, которые означают проигрыш
        losing_combinations = [
            ['Енот', 'медведь', 'лев'],
            ['лев', 'Енот', 'медведь'],
            ['медведь', 'Енот', 'лев'],
            ['Енот', 'лев', 'медведь'],
            ['медведь', 'лев', 'Енот'],
        ]

        # Останавливаем барабаны на первой найденной проигрышной комбинации
        for i in range(len(spin_result)):
            if spin_result[i] in losing_combinations:
                self.stop_reel_at_index(i)
                break

    def get_spin_result(self):
        # Получить и вернуть результаты спина для каждого барабана
        spin_results = {}
        for reel_index, reel in enumerate(self.reels):
            spin_results[reel_index] = reel.reel_spin_result()
        return spin_results

    def stop_reel_at_index(self, reel_index):
        # Остановить барабан на указанном индексе
        self.reels[reel_index].reel_is_spinning = False