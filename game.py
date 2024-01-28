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
        self.border_size = 10
        self.apple_coordinates = (random.randint(1, self.cells_count), random.randint(1, self.cells_count))

        self.moving = False
        self.clock = pygame.time.Clock()
        self.InitUI()
        self.place_snake()

    def place_apple(self, x, y):
        cell_size = (self.width - self.border_size * 2) // self.cells_count
        self.apple = PygameImage(self.screen,
                                 "apple.png",
                                 (self.get_coordinate_on_matrix(x, y)[0] - (cell_size * 0.5),
                                  self.get_coordinate_on_matrix(x, y)[1] - (
                                      cell_size * 0.5)),
                                 image_size=cell_size)

    def InitUI(self):
        self.screen.fill(VERY_DARK_BG)
        background_border = PygameRectangle(self.screen, YELLOW, int(self.border_size * 0.75),
                                            int(self.border_size * 0.75), self.width - int(self.border_size * 0.75) * 2,
                                            self.height - int(self.border_size * 0.75) * 2)

        self.cell_size = (self.width - self.border_size * 2) // self.cells_count
        for x in range(self.cells_count):
            for y in range(self.cells_count):
                cell = PygameRectangle(self.screen,
                                       GREEN if (x + y) % 2 else DARK_GREEN,
                                       *self.get_coordinate_on_matrix(x, y),
                                       self.cell_size,
                                       self.cell_size)
        self.place_apple(*self.apple_coordinates)

    async def mover(self):
        if self.moving:
            # self.clock.tick(self.speed)
            # time.sleep(5 / self.speed)
            self.snake.move(0, -0.5 * self.cell_size)

    def place_snake(self):
        self.snake = PygameSnake(self.screen,
                                 [
                                     self.get_coordinate_on_matrix(self.cells_count // 2 + 0.5, self.cells_count / 2),
                                     self.get_coordinate_on_matrix(self.cells_count // 2 + 0.5,
                                                                   self.cells_count / 2 + 0.5),
                                     self.get_coordinate_on_matrix(self.cells_count // 2 + 0.5,
                                                                   self.cells_count / 2 + 1)
                                 ],
                                 self.cell_size / 3
                                 )

    def check_if_eated(self):
        apple_coordinates = self.get_coordinate_on_matrix(self.apple_coordinates[0] - 0.5,
                                                          self.apple_coordinates[1] - 0.5)

        for point in self.snake.circles:
            if self.apple.rect.colliderect(point):
                self.eated_apple()
                break

    def eated_apple(self):
        self.apple_coordinates = (random.randint(1, self.cells_count), random.randint(1, self.cells_count))
        self.place_apple(*self.apple_coordinates)
        pygame.mixer.music.load(f"sounds/eating.mp3")
        pygame.mixer.music.play()

    def get_coordinate_on_matrix(self, x, y):
        return self.border_size + x * self.cell_size, self.border_size + y * self.cell_size

    def test(self):
        rect = PygameRectangle(screen=self.screen, color=RED, width=10, height=10, x=self.get_coordinate_on_matrix(*self.apple_coordinates)[0], y=self.get_coordinate_on_matrix(*self.apple_coordinates)[1])


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
