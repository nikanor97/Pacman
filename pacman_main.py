import sys
import pygame
import pygame_menu
from pygame.color import THECOLORS

from config import *
from pacman import Pacman
from ghost import Ghost
from field import Field
from field_config_relations import teleport
from field_config_points import *


last_pressed_key = ''


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.ticker = 0

        self.score = 0
        self.difficulty = ''

        self.background = pygame.image.load(f"{PATH_IMAGE}\\{BACKGROUND_IMAGE}.png")

        self.field = Field(LOOT_IMAGE)

        self.pacman = Pacman(self.screen, self.field, p73)

        self.ghost_0 = Ghost(GHOST_RED_IMAGE, self.screen, self.field, self.pacman, p30)
        self.ghost_1 = Ghost(GHOST_BLUE_IMAGE, self.screen, self.field, self.pacman, p31)
        self.ghost_2 = Ghost(GHOST_ORANGE_IMAGE, self.screen, self.field, self.pacman, p32)
        self.ghost_3 = Ghost(GHOST_PINK_IMAGE, self.screen, self.field, self.pacman, p25)

    def game_over(self):
        """
        Shows "game over" text
        """
        # font = pygame.font.SysFont('couriernew', 50, bold=True)
        font = pygame.font.Font(FONT_BOLD, 50)
        text = font.render(str('GAME OVER'), True, THECOLORS['red'])
        self.screen.blit(text, (210, 300))

    def you_won(self):
        """
        Shows "you won!" text
        """
        # font = pygame.font.SysFont('couriernew', 50, bold=True)
        font = pygame.font.Font(FONT_BOLD, 50)
        text = font.render(str('YOU WON!'), True, THECOLORS['red'])
        self.screen.blit(text, (210, 300))

    @staticmethod
    def update_last_pressed_key(event: pygame.event):
        """
        Updates last pressed key
        :param event:
        """
        global last_pressed_key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                last_pressed_key = 'left'
            elif event.key == pygame.K_RIGHT:
                last_pressed_key = 'right'
            elif event.key == pygame.K_UP:
                last_pressed_key = 'up'
            elif event.key == pygame.K_DOWN:
                last_pressed_key = 'down'

    @staticmethod
    def handle_quit(event: pygame.event):
        """
        Handles quit operation
        :param event:
        :return:
        """
        # if event.type == pygame.QUIT:
        #     pygame.quit()
        #     sys.exit()
        pass

    def draw_teleport_shadows(self):
        """
        Draws white rectangles on the teleport ends (to make teleportation smoother)
        """
        for teleport_point in teleport:
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (teleport_point[0] - self.pacman.mob_size[0] // 2,
                              teleport_point[1] - self.pacman.mob_size[1] // 2,
                              self.pacman.mob_size[0], self.pacman.mob_size[1]))

    def show_score(self):
        """
        Shows the score on the screen
        """
        # font = pygame.font.SysFont('couriernew', 30, bold=True)
        font = pygame.font.Font(FONT_BOLD, 30)
        text = font.render(f'SCORE: {str(self.score)}', True, THECOLORS['blue'])
        self.screen.blit(text, (110, 610))

    def show_mode(self):
        """
        Shows game difficulty on the screen
        """
        # font = pygame.font.SysFont('couriernew', 30, bold=True)
        font = pygame.font.Font(FONT_BOLD, 30)
        text = font.render(f'Mode: {str(self.difficulty)}', True, THECOLORS['blue'])
        self.screen.blit(text, (110, 640))

    def draw_loot(self):
        """
        Draws loot onjects on the field
        """
        for coord in self.field.loot_objects:
            loot = self.field.loot_objects[coord]
            if loot.is_enabled:
                self.screen.blit(loot.sprite, coord)

    def eat_loot_by_pacman(self):
        """
        Marks loot objects as is_enabled=False if pacman crosses them
        """
        pacman_center = self.pacman.center
        pacman_size = self.pacman.mob_size[0] // 2
        pacman_top = (pacman_center[0], pacman_center[1] - pacman_size)
        pacman_bottom = (pacman_center[0], pacman_center[1] + pacman_size)
        pacman_left = (pacman_center[0] - pacman_size, pacman_center[1])
        pacman_right = (pacman_center[0] + pacman_size, pacman_center[1])
        for pacman_coords in [pacman_top, pacman_bottom, pacman_left, pacman_right]:
            if pacman_coords in self.field.loot_objects and self.field.loot_objects[pacman_coords].is_enabled:
                self.field.loot_objects[pacman_coords].is_enabled = False
                self.score += 50
                self.field.loot_counter -= 1

    def run(self):
        """
        The main game loop
        """

        self.ghost_0.set_difficulty(self.difficulty)
        self.ghost_1.set_difficulty(self.difficulty)
        self.ghost_2.set_difficulty(self.difficulty)
        self.ghost_3.set_difficulty(self.difficulty)

        pacman_eaten = False
        pacman_dead_show = False
        pacman_dead = False
        you_won = False

        while True:

            for event in pygame.event.get():
                self.handle_quit(event)
                self.update_last_pressed_key(event)

            self.screen.blit(self.background, (0, 0))

            if not pacman_eaten and not you_won:

                ghost_0_success = self.ghost_0.move_function(self.ticker)
                ghost_1_success = self.ghost_1.move_function(self.ticker)
                ghost_2_success = self.ghost_2.move_function(self.ticker)
                ghost_3_success = self.ghost_3.move_function(self.ticker)

                if ghost_0_success or ghost_1_success or ghost_2_success or ghost_3_success:
                    pacman_eaten = True

                self.pacman.move(last_pressed_key, self.ticker)

            self.eat_loot_by_pacman()

            self.draw_teleport_shadows()
            self.draw_loot()
            self.show_score()
            self.show_mode()

            if self.field.loot_counter == 0:
                you_won = True
                self.ghost_0.show_not_moving(self.ticker)
                self.ghost_1.show_not_moving(self.ticker)
                self.ghost_2.show_not_moving(self.ticker)
                self.ghost_3.show_not_moving(self.ticker)
                self.pacman.show_not_moving(self.ticker)
                self.you_won()

            if pacman_eaten:
                self.ghost_0.show_not_moving(self.ticker)
                self.ghost_1.show_not_moving(self.ticker)
                self.ghost_2.show_not_moving(self.ticker)
                self.ghost_3.show_not_moving(self.ticker)
                if not pacman_dead and pacman_dead_show:
                    self.pacman.die(self.ticker)
                elif not pacman_dead and not pacman_dead_show:
                    self.pacman.show_not_moving(self.ticker)
                elif pacman_dead:
                    self.game_over()

            self.ticker += 1
            if self.ticker == 60:
                self.ticker = 0
                if pacman_dead_show:
                    pacman_dead = True
                elif pacman_eaten:
                    pacman_dead_show = True

            pygame.display.flip()
            self.clock.tick(600)


class Menu:
    def __init__(self, game: Game):
        self.game = game
        self.screen = game.screen
        theme = pygame_menu.themes.THEME_BLUE
        theme.widget_font = 'cambria'
        self.menu = pygame_menu.Menu(SCREEN_SIZE[1], SCREEN_SIZE[0], 'Pacman', theme=theme)
        self.difficulty = self.menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
        self.menu.add_button('Play', self.start_the_game)
        self.menu.add_button('Quit', pygame_menu.events.EXIT)

    def mainloop(self):
        self.menu.mainloop(self.screen)

    def start_the_game(self):
        self.game.difficulty = self.difficulty.get_value()[0]
        self.game.run()


def runner():
    """
    The game runner function
    """
    game = Game()
    menu = Menu(game)
    menu.mainloop()


runner()
