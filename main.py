from game import *
from settings import *
from statistics import *
from widgets import *
from colors import *
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


class MainMenu:
    def __init__(self, screen: pygame.Surface, sprites) -> None:
        self.screen = screen
        self.sprites = sprites
        self.game, self.settings, self.statistics = None, None, None
        self.db = Database()
        self.InitUI()

    def InitUI(self):
        self.screen.fill(VERY_DARK_BG)
        self.title = PygameText(self.screen, text="Zmeyqa Reborn",
                                coordinates=(width // 2, 15))

        self.buttons = list()
        self.buttons.append(PygameButton(
            self.screen, text="Начать", coordinates=(width // 2, height * 0.2, width * 0.5, height * 0.1),
            border_color=DARK_BG,
            background_color=DARK_BG,
            text_color=LIGHT,
            border_radius=5,
            border_size=2,
            font_size=18
        ))
        self.buttons[-1].on_clicked = self.start_game
        start_icon = PygameImage(self.screen,
                                 "start.png",
                                 coordinates=(
                                     self.buttons[-1].coordinates[0] - self.buttons[-1].coordinates[
                                         2] // 2 + width * 0.05,
                                     self.buttons[-1].coordinates[1]),
                                 image_size=height * 0.05
                                 )

        self.buttons.append(PygameButton(
            self.screen, text="Настройки", coordinates=(width // 2, height * 0.35, width * 0.5, height * 0.1),
            border_color=DARK_BG,
            background_color=DARK_BG,
            text_color=LIGHT,
            border_radius=5,
            border_size=2,
            font_size=18
        ))
        self.buttons[-1].on_clicked = self.show_settings
        settings_icon = PygameImage(self.screen,
                                    "settings.png",
                                    coordinates=(self.buttons[-1].coordinates[0] - self.buttons[-1].coordinates[
                                        2] // 2 + width * 0.05, self.buttons[-1].coordinates[1]),
                                    image_size=height * 0.05
                                    )

        self.buttons.append(PygameButton(
            self.screen, text="Статистика", coordinates=(width // 2, height * 0.8, width * 0.5, height * 0.1),
            border_color=DARK_BG,
            background_color=DARK_BG,
            text_color=LIGHT,
            border_radius=5,
            border_size=2,
            font_size=18
        ))
        self.buttons[-1].on_clicked = self.show_statistics
        stats_icon = PygameImage(self.screen,
                                 "statistic.png",
                                 coordinates=(
                                     self.buttons[-1].coordinates[0] - self.buttons[-1].coordinates[
                                         2] // 2 + width * 0.05,
                                     self.buttons[-1].coordinates[1]),
                                 image_size=height * 0.05
                                 )

    def play_button_sound(self, who_calls):
        for button in self.buttons:
            if button.on_clicked == who_calls:
                button.play_sound()

    def start_game(self):
        self.play_button_sound(self.start_game)
        self.game = Game(self.screen, cells_count=[15, 12, 10][self.db.get_settings()[1] - 1])
        self.buttons.clear()

    def show_settings(self):
        self.play_button_sound(self.start_game)
        self.settings = Settings(self.screen)
        self.buttons.clear()

    def show_statistics(self):
        self.play_button_sound(self.start_game)
        self.statistics = Statistics(self.screen)
        self.buttons.clear()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Zmeyqa reborn")
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)

    screen.fill(VERY_DARK_BG)
    sprites = pygame.sprite.Group()
    menu = MainMenu(screen, sprites)
    db = Database()

    pygame.mixer.init()
    background_sound = pygame.mixer.Sound('sounds/background.mp3')
    background_sound.play()
    background_sound.set_volume(0.1 * db.get_settings()[0] / 100)

    programIcon = pygame.image.load(f'{os.getcwd()}/assets/cobra.png')
    pygame.display.set_icon(programIcon)
    running = True

    while running:
        if menu.game:
            menu.game.InitUI()
            menu.game.snake.move(
                0.01 * menu.game.snake.speed * ((0.5 * menu.game.snake.direction) if menu.game.snake.direction in {menu.game.snake.LEFT, menu.game.snake.RIGHT} else 0),
                -0.01 * menu.game.snake.speed * (menu.game.snake.direction if menu.game.snake.direction in {menu.game.snake.UP, menu.game.snake.DOWN} else 0)
            )

        if pygame.mouse.get_pressed()[0]:
            if menu.settings:
                for clickable in menu.settings.clickable:
                    if type(clickable) == PygameSlider:
                        if clickable.point_in_area(pygame.mouse.get_pos()):
                            clickable.on_click(pygame.mouse.get_pos())
                            db.save_settings(clickable.progress, db.get_settings()[1])
                            volume = db.get_settings()[0] / 100
                            pygame.mixer.music.set_volume(volume)
                            background_sound.set_volume(0.1 * volume)

        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                if menu.game:
                    menu.game.db.set_stats((max(menu.game.db.get_attempts()) if menu.game.db.get_attempts() else 0) + 1, menu.game.score)
                running = False
                pygame.quit()
            if keys[pygame.K_ESCAPE]:
                if menu.game:
                    menu.game.db.set_stats((max(menu.game.db.get_attempts()) if menu.game.db.get_attempts() else 0) + 1, menu.game.score)
                if any([menu.game, menu.statistics, menu.settings]):
                    menu.game, menu.statistics, menu.settings = None, None, None
                    menu.InitUI()
            if menu.game:
                if not menu.game.can_move: break
                if menu.game.check_eated_or_killed(): break
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in menu.buttons:
                    button.pressed(pygame.mouse.get_pos())

                if menu.settings:
                    for clickable in menu.settings.clickable:
                        if type(clickable) is not PygameSlider:
                            clickable.pressed(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if menu.game and menu.game.can_move:
                    menu.game.InitUI()
                    if keys[pygame.K_LEFT]:
                        # menu.game.snake.move(-0.5 * menu.game.cell_size, 0)
                        menu.game.snake.set_direction(menu.game.snake.LEFT)
                    elif keys[pygame.K_RIGHT]:
                        # menu.game.snake.move(0.5 * menu.game.cell_size, 0)
                        menu.game.snake.set_direction(menu.game.snake.RIGHT)
                    elif keys[pygame.K_UP]:
                        # menu.game.snake.move(0, -0.5 * menu.game.cell_size)
                        menu.game.snake.set_direction(menu.game.snake.UP)
                    elif keys[pygame.K_DOWN]:
                        # menu.game.snake.move(0, 0.5 * menu.game.cell_size)
                        menu.game.snake.set_direction(menu.game.snake.DOWN)
                    else:
                        menu.game.snake.update()

        pygame.display.flip()

pygame.quit()
