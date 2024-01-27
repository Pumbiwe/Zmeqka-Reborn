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
        self.game = Game(self.screen)

    def show_settings(self):
        self.play_button_sound(self.start_game)
        self.settings = Settings(self.screen)

    def show_statistics(self):
        self.play_button_sound(self.start_game)
        self.statistics = Statistics(self.screen)


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
        if pygame.mouse.get_pressed()[0]:
            if menu.settings:
                for clickable in menu.settings.clickable:
                    clickable.on_clicked(pygame.mouse.get_pos())
                    if type(clickable) == PygameSlider:
                        if clickable.point_in_area(pygame.mouse.get_pos()):
                            db.save_settings(clickable.progress, db.get_settings()[1])
                            volume = db.get_settings()[0] / 100
                            pygame.mixer.music.set_volume(volume)
                            background_sound.set_volume(0.1 * volume)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in menu.buttons:
                    button.pressed(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    if any([menu.game, menu.statistics, menu.settings]):
                        menu.game, menu.statistics, menu.settings = None, None, None
                        menu.InitUI()

        pygame.display.flip()

pygame.quit()
