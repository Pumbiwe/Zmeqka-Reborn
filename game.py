import os
import random

import pygame
from colors import *
from sql_manager import Database
from widgets import *


class Game:
    def __init__(self, screen: pygame.surface, cells_count: int = 10, colors=[GREEN, DARK_GREEN]):
        self.screen = screen
        self.cells_count = cells_count
        self.width, self.height = screen.get_rect()[2:]
        self.border_size = 10
        self.can_move = False
        self.game_over = False
        self.score = 3
        self.apple_coordinates = (random.randint(1, self.cells_count), random.randint(1, self.cells_count))
        self.db = Database()
        self.colors = colors

        self.moving = False
        self.clock = pygame.time.Clock()
        self.InitUI()
        self.place_snake()

    def place_apple(self, x, y):
        if self.game_over: return
        cell_size = (self.width - self.border_size * 2) // self.cells_count
        self.apple = PygameImage(self.screen,
                                 "apple.png",
                                 (self.get_coordinate_on_matrix(x, y)[0] - (cell_size * 0.5),
                                  self.get_coordinate_on_matrix(x, y)[1] - (
                                          cell_size * 0.5)),
                                 image_size=cell_size)

    def InitUI(self):
        if self.game_over: return
        self.screen.fill(VERY_DARK_BG)
        self.background_border = PygameRectangle(self.screen, YELLOW, int(self.border_size * 0.75),
                                                 int(self.border_size * 0.75),
                                                 self.width - int(self.border_size * 0.75) * 2,
                                                 self.height - int(self.border_size * 0.75) * 2)

        self.cell_size = (self.width - self.border_size * 2) // self.cells_count
        for x in range(self.cells_count):
            for y in range(self.cells_count):
                cell = PygameRectangle(self.screen,
                                       self.colors[0] if (x + y) % 2 else self.colors[1],
                                       *self.get_coordinate_on_matrix(x, y),
                                       self.cell_size,
                                       self.cell_size)
        self.place_apple(*self.apple_coordinates)


    def place_snake(self):
        if self.game_over: return
        self.snake = PygameSnake(self.screen,
                                 [
                                     self.get_coordinate_on_matrix(self.cells_count // 2 + 0.5, self.cells_count / 2),
                                     self.get_coordinate_on_matrix(self.cells_count // 2 + 0.5,
                                                                   self.cells_count / 2 + 0.5),
                                     self.get_coordinate_on_matrix(self.cells_count // 2 + 0.5,
                                                                   self.cells_count / 2 + 1)
                                 ],
                                 radius=self.cell_size / 3
                                 )

    def check_eated_or_killed(self):
        if self.game_over: return
        apple_coordinates = self.get_coordinate_on_matrix(self.apple_coordinates[0] - 0.5,
                                                          self.apple_coordinates[1] - 0.5)

        for point in self.snake.circles:
            if self.apple.rect.colliderect(point):
                self.eated_apple()
                return
            if any([
                point.x <= self.border_size,
                point.x >= self.width - self.border_size - self.cell_size * 0.5,
                point.y <= self.border_size,
                point.y >= self.height - self.border_size - self.cell_size * 0.5,
                len(set(self.snake.points)) != len(self.snake.points)
            ]):
                self.can_move = False
                self.game_over = True
                self.snake = None
                self.lose = PygameImage(self.screen, "lose.jpg", (self.width // 2, self.height // 2),
                                        image_size=self.height, opacity=230)
                self.score_text = PygameText(
                    self.screen,
                    text=f"Ваш результат: {self.score}{' очко.' if str(self.score)[-1] == '1' else ' очка.' if str(self.score)[-1] in {'2', '3', '4'} else ' очков.' if str(self.score)[-1] in {'5', '6', '7', '8', '9', '0'} else '.'}",
                    coordinates=(self.width / 2, self.height * 0.6)
                )
                return True

    def eated_apple(self):
        if self.game_over: return
        self.score += 1
        self.apple_coordinates = (random.randint(1, self.cells_count), random.randint(1, self.cells_count))
        self.InitUI()
        self.snake.grow()
        self.snake.update()
        self.place_apple(*self.apple_coordinates)
        pygame.mixer.music.load(f"sounds/eating.mp3")
        pygame.mixer.music.play()

    def get_coordinate_on_matrix(self, x, y):
        return self.border_size + x * self.cell_size, self.border_size + y * self.cell_size

    def snake_mover(self):
        while True:
            if self.game_over: return
            if self.can_move and not self.game_over:
                # self.InitUI()
                if self.snake.get_direction() == self.snake.DOWN:
                    self.snake.move(0, 0.5 * self.cell_size) # down
                if self.snake.get_direction() == self.snake.LEFT:
                    self.snake.move(-0.5 * self.cell_size, 0) # left
                if self.snake.get_direction() == self.snake.RIGHT:
                    self.snake.move(0.5 * self.cell_size, 0) # right
                if self.snake.get_direction() == self.snake.UP:
                    self.snake.move(0, -0.5 * self.cell_size) # up
                #self.snake.set_direction(self.snake.DOWN)
                time.sleep(0.1)


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
