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
        self.title = PygameText(self.screen, text="Zmeyqa Reborn",
                                   coordinates=(width // 2, 15))

        self.buttons = list()
        self.buttons.append(PygameButton(
            self.screen, text="Начать", coordinates=(width // 2, width // 6, 200, 50),
            border_color=DARK_BG,
            background_color=DARK_BG,
            text_color=LIGHT,
            border_radius=5,
            border_size=2,
            font_size=18
        ))
        self.buttons.append(PygameButton(
            self.screen, text="Настройки", coordinates=(width // 2, width // 4, 200, 50),
            border_color=DARK_BG,
            background_color=DARK_BG,
            text_color=LIGHT,
            border_radius=5,
            border_size=2,
            font_size=18
        ))
        self.buttons.append(PygameButton(
            self.screen, text="Статистика", coordinates=(width // 2, width // 3, 200, 50),
            border_color=DARK_BG,
            background_color=DARK_BG,
            text_color=LIGHT,
            border_radius=5,
            border_size=2,
            font_size=18
        ))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Zmeyqa reborn")

    programIcon = pygame.image.load(f'{os.getcwd()}/assets/cobra.png')
    pygame.display.set_icon(programIcon)

    size = width, height = 720, 500
    screen = pygame.display.set_mode(size)

    sprites = pygame.sprite.Group()
    running = True

    screen.fill(VERY_DARK_BG)

    menu = MainMenu(screen, sprites)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in menu.buttons:
                    button.pressed(pygame.mouse.get_pos())

        pygame.display.flip()

pygame.quit()