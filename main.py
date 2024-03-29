from machine import Machine
from settings import *
import ctypes, pygame, sys
from ui import UI
from player import Player

ctypes.windll.user32.SetProcessDPIAware()


class Game:
    def __init__(self):

        # Общая настройка
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        icon = pygame.image.load('icon2.ico')  # Замените 'путь_к_вашей_иконке.ico' на актуальный путь к вашей иконке
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Slot Machine')
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()
        # Создание экземпляра класса Player
        self.currPlayer = Player()

        # Создание экземпляра класса UI с передачей экземпляра класса Player
        self.ui = UI(self.currPlayer)

        # Создание экземпляра класса Machine с передачей экземпляра класса UI
        self.machine = Machine(self.ui)

        self.delta_time = 0

        # Звук
        main_sound = pygame.mixer.Sound('audio/track.mp3')
        main_sound.set_volume(0.7)
        main_sound.play(loops = -1)

    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:
            # Обработка операции выхода
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Временные переменные
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()

            pygame.display.update()
            self.screen.blit(self.bg_image, (0, 0))
            self.machine.update(self.delta_time)
            self.screen.blit(self.grid_image, (0, 0))
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()