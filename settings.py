# Настройки отображения
DEFAULT_IMAGE_SIZE = (300, 300)
FPS = 120
HEIGHT = 1000
WIDTH = 1600
START_X, START_Y = 0, -300
X_OFFSET, Y_OFFSET = 20, 0

# Изображения
BG_IMAGE_PATH = 'graphics/1/Дизайн без названия.png'
GRID_IMAGE_PATH = 'graphics/1/gridline2.png'
GAME_INDICES = [1, 2, 3]
SYM_PATH = 'graphics/1/'

# Текст
TEXT_COLOR = 'White'
UI_FONT = 'graphics/font/kidspace.ttf'
UI_FONT_SIZE = 30
WIN_FONT_SIZE = 110

# Иконки
symbols = {
    'raccoon_1': f"{SYM_PATH}/Енот.png",
    'bear_2': f"{SYM_PATH}/медведь.png",
    'lion_3': f"{SYM_PATH}/лев.png",
    'bear_4': f"{SYM_PATH}/медведь.png",
    'lion_5': f"{SYM_PATH}/лев.png",
    # 'wolf_gold_a_6': f"{SYM_PATH}/Волк_золотой.png",
    # 'bear_b_7': f"{SYM_PATH}/медведь.png",
    # 'wolf_d_8': f"{SYM_PATH}/волк.png",
    # 'lion_c_9': f"{SYM_PATH}/лев.png",
    # 'wolf_d_10': f"{SYM_PATH}/волк.png",

}

payouts = {
    'five_row': 3.39,
    'three_row': 0.5,
    'ten_row': 7.5
}