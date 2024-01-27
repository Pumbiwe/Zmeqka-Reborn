import os

import pygame
from pygame import Rect

from colors import *
from sql_manager import Database
from widgets import *


class Settings:
    def __init__(self, screen, cells_count: int = 10):
        self.screen = screen
        self.db = Database()
        self.width, self.height = screen.get_rect()[2:]
        self.clickable = list()
        self.initUI()

    def initUI(self):
        self.screen.fill(VERY_DARK_BG)
        self.title = PygameText(self.screen, text="Settings",
                                coordinates=(self.width // 2, 15))

        self.volume_text = PygameText(self.screen,
                                      text="Volume",
                                      coordinates=(self.width // 2, self.height // 2 - self.width * 0.05)
                                      )
        self.volume_slider = PygameSlider(self.screen, self.width // 2, self.height // 2, self.width * 0.4,
                                     self.height * 0.05)
        self.volume_slider.set_progress(self.db.get_settings()[0])
        self.clickable.append(self.volume_slider)



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
