import os

import pygame
from colors import *
from widgets import *


class Statistics:
    def __init__(self, screen, cells_count: int = 10):
        self.screen = screen
        self.width, self.height = screen.get_rect()[2:]
        self.initUI()

    def initUI(self):
        self.screen.fill(VERY_DARK_BG)
        self.title = PygameText(self.screen, text="Statistics",
                                coordinates=(self.width // 2, self.height * 0.025))
        self.information = PygameText(
            self.screen,
            text="Последние 10 игр еще не сформированы",
            coordinates=(self.width // 2, self.height * 0.1)
        )


if __name__ == '__main__':
    pygame.init()

    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    screen.fill(VERY_DARK_BG)
    statistics = Statistics(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
