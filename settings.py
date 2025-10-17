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
        self.InitUI()

    def InitUI(self):
        self.clickable.clear()
        self.screen.fill(VERY_DARK_BG)
        self.title = PygameText(self.screen, text="Settings",
                                coordinates=(self.width // 2, 15))

        self.difficulty_text = PygameText(
            self.screen,
            text="Difficulty",
            coordinates=(self.width // 2, self.height * 0.2)
        )
        self.difficulty_value = PygameText(
            self.screen,
            text=str(self.db.get_settings()[1]),
            coordinates=(self.width // 2, self.height * 0.3)
        )
        self.difficulty_left = PygameImageButton(
            self.screen,
            "left.png",
            image_size=32,
            coordinates=(self.width * 0.35, self.height * 0.3)
        )
        self.difficulty_right = PygameImageButton(
            self.screen,
            "right.png",
            image_size=32,
            coordinates=(self.width * 0.65, self.height * 0.3)
        )

        self.difficulty_right.args = 1
        self.difficulty_left.args = -1
        self.difficulty_left.on_clicked = self.change_difficulty
        self.difficulty_right.on_clicked = self.change_difficulty
        self.clickable.append(self.difficulty_left)
        self.clickable.append(self.difficulty_right)


        self.volume_text = PygameText(self.screen,
                                      text="Volume",
                                      coordinates=(self.width // 2, self.height // 2 - self.width * 0.05)
                                      )
        self.volume_slider = PygameSlider(self.screen, self.width // 2, self.height // 2, self.width * 0.4,
                                     self.height * 0.05)
        self.volume_slider.set_progress(self.db.get_settings()[0])
        self.clickable.append(self.volume_slider)

        self.snake = PygameImage(
            self.screen,
            coordinates=(self.width // 2, self.height * 0.8),
            image_size=256
        )

    def change_difficulty(self, value):
        new_value = self.db.get_settings()[1] + value
        if 1 <= new_value <= 5:
            self.db.save_settings(self.db.get_settings()[0], new_value)
            self.InitUI()
        del new_value



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
