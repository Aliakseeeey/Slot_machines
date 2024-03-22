# Слот-машина на Python с использованием Pygame

Данный проект представляет собой простую слот-машину, реализованную на Python с использованием библиотеки Pygame.

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Aliakseeeey/Slot_machines.git
cd slot-machine

2. Создайте и активируйте виртуальную среду Python:

python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate      # Для Windows

3. Установите зависимости:

pip install -r requirements.txt

4. Запуск

python main.py

Для создания исполняемого файла расхирения .exe используйте команду:
pyinstaller --onefile --name AfricaSlot --icon=icon.ico main.py

Также в папку dist нужно скопировать папки с аудио, фото и иконки.