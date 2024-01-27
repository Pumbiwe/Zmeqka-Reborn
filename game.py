import os
import random

import pygame
from colors import *
from widgets import *


class Game:
    def __init__(self, screen: pygame.surface, cells_count: int = 10):
        self.screen = screen
        self.cells_count = cells_count
        self.width, self.height = screen.get_rect()[2:]

        self.initUI()

    def place_apple(self, x, y):
        cell_size = (self.width - 40) // self.cells_count
        self.apple = PygameImage(self.screen,
                                 "apple.png",
                                 (20 + x * cell_size - (cell_size * 0.5 if x else -cell_size * 0.5),
                                  20 + y * cell_size - (cell_size * 0.5 if y else -cell_size * 0.5)),
                                 image_size=cell_size)

    def initUI(self):
        self.screen.fill(VERY_DARK_BG)
        background_border = PygameRectangle(self.screen, YELLOW, 15, 15, self.width - 30, self.height - 30)

        cell_size = (self.width - 40) // self.cells_count
        for x in range(self.cells_count):
            for y in range(self.cells_count):
                cell = PygameRectangle(self.screen,
                                       GREEN if (x + y) % 2 else DARK_GREEN,
                                       20 + x * cell_size,
                                       20 + y * cell_size,
                                       cell_size,
                                       cell_size)
        self.place_apple(random.randint(0, self.cells_count), random.randint(0, self.cells_count))
        Snake = PygameSnake(self.screen, [(self.width / 2 + cell_size / 2, self.height / 2 + cell_size / 2), (self.width / 2 + cell_size / 2, self.height / 2 + cell_size), (self.width / 2 + cell_size / 2, self.height / 2 + cell_size *1.5)], cell_size / 2)


if __name__ == '__main__':

    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    screen.fill(VERY_DARK_BG)
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()
