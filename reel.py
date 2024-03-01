from settings import *
import pygame, random


class Reel:
    def __init__(self, pos):
        self.symbol_list = pygame.sprite.Group()
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5] # Имеет значение только в том случае, если имеется более 5 символов.

        self.reel_is_spinning = False

        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(symbols[item], pos, idx))
            pos = list(pos)
            pos[1] += 300
            pos = tuple(pos)

    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            # Анимация начала вращения барабана в шахматном порядке
            if self.delay_time <= 0:

                # Перебрать все 5 символов на барабане; обрезать; добавить новый случайный символ поверх стека
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 100

                    # Правильный интервал зависит от вышеуказанного дополнения, которое в конечном итоге достигнет 1200
                    if symbol.rect.top == 1200:
                        if reel_is_stopping:
                            self.reel_is_spinning = False


                        symbol_idx = symbol.idx
                        symbol.kill()
                        # Создать случайный символ вместо вышеуказанного.
                        self.symbol_list.add(Symbol(symbols[random.choice(self.shuffled_keys)], ((symbol.x_val), -300), symbol_idx))

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        # Получить и вернуть текстовое представление символов на данном барабане
        spin_symbols = []
        for i in GAME_INDICES:
            spin_symbols.append(self.symbol_list.sprites()[i].sym_type)
        return spin_symbols[::-1]


class Symbol(pygame.sprite.Sprite):
    def __init__(self, pathToFile, pos, idx):
        super().__init__()

        self.sym_type = pathToFile.split('/')[3].split('.')[0]

        self.pos = pos
        self.idx = idx
        self.image = pygame.image.load(pathToFile).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.x_val = self.rect.left

        # Используется для анимации выигрыша
        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False

    def update(self):
        # Немного увеличивает размер выигрышных символов
        if self.fade_in:
            if self.size_x < 320:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))

        # Исчезает невыигрышные символы
        elif not self.fade_in and self.fade_out:
            if self.alpha > 115:
                self.alpha -= 7
                self.image.set_alpha(self.alpha)