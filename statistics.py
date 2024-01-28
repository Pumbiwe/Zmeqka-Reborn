import os

import pygame
from colors import *
from widgets import *
from sql_manager import Database


class Statistics:
    def __init__(self, screen, cells_count: int = 10):
        self.screen = screen
        self.width, self.height = screen.get_rect()[2:]
        self.db = Database()
        self.initUI()

    def initUI(self):
        self.screen.fill(VERY_DARK_BG)
        self.title = PygameText(self.screen, text="Статистика",
                                coordinates=(self.width // 2, self.height * 0.025))

        self.img_left = PygameImage(self.screen, coordinates=(self.width * 0.15, self.height * 0.5), image_size=128)
        self.img_right = PygameImage(self.screen, coordinates=(self.width * 0.85, self.height * 0.5), image_size=128)
        self.img_right.flipper(True)

        if not self.db.get_attempts():
            self.information = PygameText(
                self.screen,
                text="Последние 10 игр еще не сформированы",
                coordinates=(self.width // 2, self.height * 0.1)
            )
        else:
            stats = list()
            for i, el in enumerate(self.db.get_stats()[::-1]):
                if i >= 10: break
                stats.append(el)
            stats.sort()
            for i, y in enumerate(stats):
                text = PygameText(
                    self.screen,
                    text=f"{i + 1}. Результат: {y[1]}.",
                    coordinates=(self.width / 2, (self.height * 0.1 + i * self.height * 0.09))
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
