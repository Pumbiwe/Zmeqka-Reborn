import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from colors import *
from widgets import *


class MainMenu:
    def __init__(self, screen: pygame.Surface, sprites) -> None:
        self.screen = screen
        self.sprites = sprites
        self.InitUI()

    def InitUI(self):
        self.screen.fill(VERY_DARK_BG)
        self.greeting = PygameText(self.screen, text="Приветствуем тебя, странник!",
                                   coordinates=(width // 2, height - 100))
        self.description = PygameText(self.screen,
                                      text="Ты находишься на главном окне. Здесь можно начать игру или посмотреть справочную информацию",
                                      coordinates=(width // 2, height - 100 + 22), font_size=12, text_color=GREY)

        self.buttons = list()
        self.buttons.append(PygameButton(
            self.screen, text="Начать", coordinates=(width - 60, height - 35, 100, 50),
            border_color=DARK_BG,
            background_color=DARK_BG,
            text_color=LIGHT,
            border_radius=10,
            border_size=2,
            font_size=18
        ))

        self.buttons.append(PygameButton(
            self.screen, text="Таблица Менделеева", coordinates=(115, 45, 200, 50),
            text_color=LIGHT,
            border_color=DARK_BG,
            border_radius=12,
            border_size=5,
            font_size=16,
            background_color=BLUE
        ))

        self.buttons.append(PygameButton(
            self.screen, text="Таблица растворимости", coordinates=(width - 115, 45, 200, 50),
            text_color=LIGHT,
            border_color=DARK_BG,
            border_radius=12,
            border_size=5,
            font_size=16,
            background_color=BLUE
        ))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("The world of chemistry: Great Invention")

    programIcon = pygame.image.load(f'{os.getcwd()}/assets/chemistry.png')
    pygame.display.set_icon(programIcon)

    size = width, height = 720, 500
    screen = pygame.display.set_mode(size)

    sprites = pygame.sprite.Group()
    running = True

    screen.fill(VERY_DARK_BG)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

pygame.quit()