import os

import pygame
from colors import *
from widgets import *


class Settings:
    def __init__(self, screen, cells_count: int = 10):
        self.screen = screen
        self.width, self.height = screen.get_rect()[2:]
        self.initUI()

    def initUI(self):
        self.screen.fill(VERY_DARK_BG)
        self.title = PygameText(self.screen, text="Settings",
                                coordinates=(self.width // 2, 15))



if __name__ == '__main__':
    pygame.init()

    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    screen.fill(VERY_DARK_BG)
    settings = Settings(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()