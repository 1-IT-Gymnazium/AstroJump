import pygame
import sys
from settings import *
import csv
from player import Player
from camera import Camera
from slider import Slider
from transition import circular_fade
from enemy import ProjectileManager


# TODOS:

# todo: split up code into multiple smaller functions and refactor some functions into classes
# todo: resize portal block, figure out how to import it as a 64X128 tile instead of 64X64, make it work as the level end transition to the next level
# todo: create final layouts of all 3 levels
# todo: create documentation with external program
# todo: import sounds for sound effects like jumping, getting hit, dying etc... (jumping sound already added)
# todo: work on optimization
# todo: fix player transparent glasses drawing issue

# todo: (Optional) create double jump
# todo: (Optional) make more stuff for menu like more settings options etc...
# todo: (Optional) add visual effects like particles etc. ..


class Game:
    """
    A class to manage the main game environment including initialization,
    game loops, and transitions between different states of the game such as menus and levels.

    :param none: This class constructor takes no parameters.
    """

    def __init__(self):

        """
        Initializes the game environment, setting up the screen, loading resources, and initializing game components.
        """

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AstroJump")

        num_tiles = 17
        self.tile_images = [pygame.image.load(f'Graphics/tiles/{i}.png') for i in range(num_tiles)]

        # colors
        self.white = (255, 255, 255)
        self.button_color = (0, 7, 78)
        self.quit_button_color = (125, 50, 50)
        self.quit_button_hover_color = (200, 50, 50)
        self.hover_color = (0, 50, 125)

        # player
        self.player = Player(100, 100, 50, 50, self.screen)
        self.initial_player_position = (self.player.x, self.player.y)

        # camera
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)

        # sliders
        self.sfx_slider = Slider(810, 400, 300, 40, 0, 1, 0.5)
        self.music_slider = Slider(810, 700, 300, 40, 0, 1, 0.5)

        # fonts
        self.font_custom = pygame.font.Font("Graphics/fonts/pixel_font.ttf", 50)

        # sounds
        self.button_sound = pygame.mixer.Sound("Sounds/button_sound3.mp3")
        self.bg_music = "Sounds/BG_music.mp3"
        self.bg_level_music = "Sounds/level_bg_music1.mp3"
        self.hit_sound = pygame.mixer.Sound("Sounds/hit_sound.mp3")
        pygame.mixer.music.load(self.bg_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        self.current_level = None

        # enemies
        self.spikes = []
        self.projectiles = []  # List to hold projectiles
        self.last_shot_time = 0
        self.projectile_manager = ProjectileManager(self)

        self.game_paused = False

    def draw_text(self, text, font, color, x, y):

        """
        Draws text on the game screen at a specified position.

        :param str text: The text to be displayed.
        :param Font font: A pygame Font object used to render the text.
        :param tuple color: A tuple representing the RGB color of the text.
        :param int x: The x-coordinate of the text position.
        :param int y: The y-coordinate of the text position.
        """

        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        self.screen.blit(text_obj, text_rect)

    def draw_button(self, text, rect, color):

        """
        Draws a button with text centered on the screen.

        :param str text: The text to be displayed on the button.
        :param Rect rect: A pygame Rect object representing the button's position and dimensions.
        :param tuple color: A tuple representing the RGB color of the button.
        """

        pygame.draw.rect(self.screen, color, rect, border_radius=30)
        text_surface = self.font_custom.render(text, True, self.white)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def main_menu(self):
        """
        Handles the main menu loop, processing events and updating the display.
        """

        while True:
            bg = pygame.image.load("Graphics/backgrounds/BG.png")
            self.screen.blit(bg, (0, 0))

            self.draw_text("Astro Jump", self.font_custom, self.white, WINDOW_WIDTH // 2, 300)

            mx, my = pygame.mouse.get_pos()

            play_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
            tutorial_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
            settings_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 600, BUTTON_WIDTH, BUTTON_HEIGHT)
            quit_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 700, BUTTON_WIDTH, BUTTON_HEIGHT)

            play_hovered = play_button.collidepoint((mx, my))
            tutorial_hovered = tutorial_button.collidepoint((mx, my))
            settings_hovered = settings_button.collidepoint((mx, my))
            quit_hovered = quit_button.collidepoint((mx, my))

            self.draw_button("Play", play_button, self.hover_color if play_hovered else self.button_color)
            self.draw_button("Tutorial", tutorial_button, self.hover_color if tutorial_hovered else self.button_color)
            self.draw_button("Settings", settings_button, self.hover_color if settings_hovered else self.button_color)
            self.draw_button("Quit Game", quit_button, self.quit_button_hover_color if quit_hovered else self.quit_button_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if play_button.collidepoint((mx, my)):
                    if pygame.mouse.get_pressed()[0]:
                        self.button_sound.play()
                        self.level_select()

                if tutorial_button.collidepoint((mx, my)):
                    if pygame.mouse.get_pressed()[0]:
                        self.button_sound.play()
                        self.tutorial()

                if settings_button.collidepoint((mx, my)):
                    if pygame.mouse.get_pressed()[0]:
                        self.button_sound.play()
                        self.settings()

                if quit_button.collidepoint((mx, my)):
                    if pygame.mouse.get_pressed()[0]:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def level_select(self):

        """
        Displays the level selection menu and handles level loading based on user interaction.
        """

        while True:
            level_bg = pygame.image.load("Graphics/backgrounds/Level_BG.png")
            self.screen.blit(level_bg, (0, 0))

            self.draw_text("Select a Level", self.font_custom, self.white, WINDOW_WIDTH // 2, 175)

            mx, my = pygame.mouse.get_pos()

            return_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 800, BUTTON_WIDTH, BUTTON_HEIGHT)
            level1 = pygame.Rect((WINDOW_WIDTH - 3 * BUTTON_WIDTH - 2 * BUTTON_GAP) // 2, 250, BUTTON_WIDTH, BUTTON_HEIGHT)
            level2 = pygame.Rect(level1.right + BUTTON_GAP, 250, BUTTON_WIDTH, BUTTON_HEIGHT)
            level3 = pygame.Rect(level2.right + BUTTON_GAP, 250, BUTTON_WIDTH, BUTTON_HEIGHT)

            return_hovered = return_button.collidepoint((mx, my))
            level1_hovered = level1.collidepoint((mx, my))
            level2_hovered = level2.collidepoint((mx, my))
            level3_hovered = level3.collidepoint((mx, my))

            self.draw_button("Return", return_button, self.hover_color if return_hovered else self.button_color)
            self.draw_button("Level 1", level1, self.hover_color if level1_hovered else self.button_color)
            self.draw_button("Level 2", level2, self.hover_color if level2_hovered else self.button_color)
            self.draw_button("Level 3", level3, self.hover_color if level3_hovered else self.button_color)

            if level1.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    circular_fade(self.screen, 'out')
                    pygame.mixer.music.load(self.bg_level_music)
                    pygame.mixer.music.play(-1)
                    self.show_map("levels/level1.csv")

            if level2.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    circular_fade(self.screen, 'out')
                    pygame.mixer.music.load(self.bg_level_music)
                    pygame.mixer.music.play(-1)
                    self.show_map("levels/level2.csv")

            if level3.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    circular_fade(self.screen, 'out')
                    pygame.mixer.music.load(self.bg_level_music)
                    pygame.mixer.music.play(-1)
                    self.show_map("levels/level3.csv")

            if return_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            pygame.display.update()

    def tutorial(self):

        """
        Displays the tutorial screen and handles interactions within the tutorial.
        """

        while True:
            tutorial_bg = pygame.image.load("Graphics/backgrounds/Level_BG.png")
            self.screen.blit(tutorial_bg, (0, 0))

            mx, my = pygame.mouse.get_pos()

            return_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 900, BUTTON_WIDTH, BUTTON_HEIGHT)
            page1 = pygame.Rect((WINDOW_WIDTH // 2) - 250, 300, 500, 400)

            return_hovered = return_button.collidepoint((mx, my))

            self.draw_button("Return", return_button, self.hover_color if return_hovered else self.button_color)
            pygame.draw.rect(self.screen, self.button_color, page1, border_radius=30)

            self.draw_text("Tutorial", self.font_custom, self.white, WINDOW_WIDTH // 2, 175)
            self.draw_text("Return", self.font_custom, self.white, return_button.centerx, return_button.centery)
            self.draw_text("A - move left", self.font_custom, self.white, page1.centerx, 350)
            self.draw_text("D - move right", self.font_custom, self.white, page1.centerx, 450)
            self.draw_text("Space - jump", self.font_custom, self.white, page1.centerx, 550)

            if return_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            pygame.display.update()

    def settings(self):

        """
        Displays the settings menu where users can adjust preferences like sound volume.
        """

        while True:
            tutorial_bg = pygame.image.load("Graphics/backgrounds/Level_BG.png")
            self.screen.blit(tutorial_bg, (0, 0))

            mx, my = pygame.mouse.get_pos()

            return_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 900, BUTTON_WIDTH, BUTTON_HEIGHT)

            return_hovered = return_button.collidepoint((mx, my))

            self.draw_button("Return", return_button, self.hover_color if return_hovered else self.button_color)
            self.draw_text("Settings", self.font_custom, self.white, WINDOW_WIDTH // 2, 175)
            self.draw_text("SFX volume", self.font_custom, self.white, WINDOW_WIDTH // 2, 350)
            self.draw_text("Music volume", self.font_custom, self.white, WINDOW_WIDTH // 2, 650)

            self.sfx_slider.draw(self.screen)
            self.music_slider.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.sfx_slider.handle_event(event, mx, my)
                self.music_slider.handle_event(event, mx, my)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.button_sound.set_volume(self.sfx_slider.value)
                    pygame.mixer.music.set_volume(self.music_slider.value)

                if return_button.collidepoint((mx, my)):
                    if pygame.mouse.get_pressed()[0]:
                        self.button_sound.play()
                        return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            pygame.display.update()

    def show_respawn_menu(self):

        """
        Displays the respawn menu when the player dies and handles the actions based on user interaction.
        """

        main_menu_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2 - 20, 500, 300, BUTTON_HEIGHT)
        respawn_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
        quit_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 600, BUTTON_WIDTH, BUTTON_HEIGHT)

        mx, my = pygame.mouse.get_pos()
        main_menu_hovered = main_menu_button.collidepoint((mx, my))
        respawn_hovered = respawn_button.collidepoint((mx, my))
        quit_hovered = quit_button.collidepoint((mx, my))

        if self.player.y > 1800:
            self.game_paused = True
            self.screen.fill((0, 0, 0))
            self.draw_text("You fell into the abyss", self.font_custom, self.quit_button_color, WINDOW_WIDTH // 2, 175)
            self.draw_button("Main menu", main_menu_button, self.hover_color if main_menu_hovered else self.button_color)
            self.draw_button("Respawn", respawn_button, self.hover_color if respawn_hovered else self.button_color)
            self.draw_button("Quit", quit_button, self.quit_button_hover_color if quit_hovered else self.quit_button_color)

            if respawn_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.player.reset_position()
                    self.button_sound.play()
                    self.game_paused = False

            if main_menu_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.player.reset_position()
                    self.button_sound.play()
                    pygame.mixer.music.load(self.bg_music)
                    pygame.mixer.music.play(-1)
                    circular_fade(self.screen, "out")
                    self.main_menu()
                    self.game_paused = False
                    return

            if quit_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def show_game_menu(self):

        """
        Displays the in-game menu and handles navigation based on user interaction.
        """

        while True:
            mx, my = pygame.mouse.get_pos()

            resume_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
            settings_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
            main_menu_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 600, BUTTON_WIDTH, BUTTON_HEIGHT)
            quit_button = pygame.Rect(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 700, BUTTON_WIDTH, BUTTON_HEIGHT)

            resume_hovered = resume_button.collidepoint((mx, my))
            quit_hovered = quit_button.collidepoint((mx, my))
            settings_hovered = settings_button.collidepoint((mx, my))
            main_menu_hovered = main_menu_button.collidepoint((mx, my))

            tutorial_bg = pygame.image.load("Graphics/backgrounds/Level_BG.png")
            self.screen.blit(tutorial_bg, (0, 0))
            self.draw_button("Resume", resume_button, self.hover_color if resume_hovered else self.button_color)
            self.draw_button("Quit", quit_button, self.quit_button_hover_color if quit_hovered else self.quit_button_color)
            self.draw_button("Settings", settings_button, self.hover_color if settings_hovered else self.button_color)
            self.draw_button("Menu", main_menu_button, self.hover_color if main_menu_hovered else self.button_color)

            if resume_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    return

            if main_menu_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.player.reset_position()
                    self.button_sound.play()
                    pygame.mixer.music.load(self.bg_music)
                    pygame.mixer.music.play(-1)
                    circular_fade(self.screen, "out")
                    self.main_menu()

            if settings_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    self.button_sound.play()
                    self.settings()

            if quit_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            pygame.display.update()

    def transition_next_level(self, next_level_filename):

        """
        Manages the transition to the next level, including loading the new level map.

        :param str next_level_filename: The filename of the next level to load.
        """
        self.player.reset_position()
        self.current_level = next_level_filename
        circular_fade(self.screen, "out")
        self.show_map(next_level_filename)

    def find_cannons_position(self, tile_id_to_find):

        """
        Searches the current level's map file for specific tiles, returning their positions.

        :param int tile_id_to_find: The tile ID to search for in the map.
        :return: A list of tuples indicating the positions (column, row) of found tiles.
        :rtype: list
        """

        file_path = self.current_level

        cannons = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row_index, row in enumerate(reader):
                for col_index, tile_id in enumerate(row):
                    if int(tile_id) == tile_id_to_find:
                        cannons.append((col_index, row_index))
        return cannons

    def show_map(self, map_filename=None):

        """
        Displays the game map and handles all interactions within the game level.

        :param str map_filename: Optional filename of the map to load, defaults to None.
        """

        self.player.position_was_reset = False
        non_coll_tiles = [0]
        if map_filename is not None:
            self.current_level = map_filename

            # Load the map from the CSV file
        game_map = []
        with open(map_filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                game_map.append([int(tile_id) for tile_id in row])

        clock = pygame.time.Clock()
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)

        while True:

            map_bg = pygame.image.load("Graphics/backgrounds/Level_BG.png").convert_alpha()
            self.screen.blit(map_bg, (0, 0))
            self.player.update_animation()

            # Handle events
            for event in pygame.event.get():
                self.handle_event(event)

            if self.player.x > 4864 and self.current_level == "levels/level1.csv":
                next_level_filename = "levels/level2.csv"
                self.transition_next_level(next_level_filename)
                return

            if self.player.x > 4864 and self.current_level == "levels/level2.csv":
                next_level_filename = "levels/level3.csv"
                self.transition_next_level(next_level_filename)
                return

            # Apply gravity
            new_x, new_y = self.apply_gravity()

            # Horizontal Collision Check
            new_x = self.check_horizontal_collision(game_map, new_x, non_coll_tiles)

            # Vertical Collision Check
            new_y = self.check_vertical_collision(game_map, new_y, non_coll_tiles)

            self.player.update_position(new_x, new_y)
            self.draw_map(game_map, non_coll_tiles)
            self.player.draw(self.camera)
            self.camera.update(self.player)
            if self.game_paused is False:
                self.projectile_manager.draw_projectiles(self.screen, self.camera)
            self.show_respawn_menu()
            current_time = pygame.time.get_ticks() / 1000
            self.projectile_manager.update_projectiles(current_time)
            self.check_projectile_collisions()
            pygame.display.update()
            clock.tick(60)
            self.player.position_was_reset = False

    def draw_map(self, game_map, non_coll_tiles):
        """
        Draws the game map on the screen based on tile IDs that are not specified as non-collidable.

        :param list game_map: A 2D list representing the map where each value corresponds to a tile ID.
        :param list non_coll_tiles: A list of tile IDs that should not be drawn because they are non-collidable.
        """

        for row_index, row in enumerate(game_map):
            for col_index, tile_id in enumerate(row):
                if tile_id not in non_coll_tiles:
                    tile_image = self.tile_images[tile_id]
                    if tile_id == 15:
                        y_offset = TILE_HEIGHT - SPIKE_HEIGHT
                        tile_rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT + y_offset, SPIKE_WIDTH, SPIKE_HEIGHT)
                    # todo:change this according to portal size logic
                    elif tile_id == 16:
                        y_offset = TILE_HEIGHT - CANNON_HEIGHT
                        tile_rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT + y_offset, CANNON_WIDTH, CANNON_HEIGHT)
                    else:
                        tile_rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)

                    self.screen.blit(tile_image, self.camera.apply(tile_rect))

    def check_horizontal_collision(self, game_map, new_x, non_coll_tiles):
        """
        Checks for horizontal collisions between the player and collidable tiles in the game map.

        :param list game_map: A 2D list representing the map where each value corresponds to a tile ID.
        :param int new_x: The proposed new x-coordinate for the player, based on movement.
        :param list non_coll_tiles: A list of tile IDs that the player can pass through without collision.
        :return: The new x-coordinate for the player after collision checks.
        :rtype: int
        """

        for row_index, row in enumerate(game_map):
            for col_index, tile_id in enumerate(row):
                if tile_id not in non_coll_tiles:
                    if tile_id == 15:
                        tile_rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT + (TILE_HEIGHT - SPIKE_HEIGHT), SPIKE_WIDTH, SPIKE_HEIGHT)
                    elif tile_id == 16:
                        tile_rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT + (TILE_HEIGHT - CANNON_HEIGHT), CANNON_WIDTH, CANNON_HEIGHT)
                    else:
                        tile_rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)

                    player_rect = pygame.Rect(new_x, self.player.y, self.player.width, self.player.height)

                    if player_rect.colliderect(tile_rect):
                        if tile_id == 15:
                            self.player.position_was_reset = True
                            self.player.reset_position()
                            self.camera.update(self.player)
                            self.hit_sound.play()
                        if new_x > self.player.x:  # Moving right
                            new_x = tile_rect.left - self.player.width
                        elif new_x < self.player.x:  # Moving left
                            new_x = tile_rect.right

        return new_x

    def check_vertical_collision(self, game_map, new_y, non_coll_tiles):
        """
        Checks for vertical collisions between the player and collidable tiles in the game map.

        :param list game_map: A 2D list representing the map where each value corresponds to a tile ID.
        :param int new_y: The proposed new y-coordinate for the player, based on gravity or jumping.
        :param list non_coll_tiles: A list of tile IDs that the player can pass through without collision.
        :return: The new y-coordinate for the player after collision checks.
        :rtype: int
        """

        for row_index, row in enumerate(game_map):
            for col_index, tile_id in enumerate(row):
                if tile_id not in non_coll_tiles:
                    if tile_id == 15:
                        tile_rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT + (TILE_HEIGHT - SPIKE_HEIGHT), SPIKE_WIDTH, SPIKE_HEIGHT)
                    elif tile_id == 16:
                        tile_rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT + (TILE_HEIGHT - CANNON_HEIGHT), CANNON_WIDTH, CANNON_HEIGHT)
                    else:
                        tile_rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)

                    player_rect = pygame.Rect(self.player.x, new_y, self.player.width, self.player.height)

                    if player_rect.colliderect(tile_rect):
                        if tile_id == 15:
                            self.player.position_was_reset = True
                            self.player.reset_position()
                            self.camera.update(self.player)
                            self.hit_sound.play()
                        if new_y > self.player.y:  # Falling down
                            new_y = tile_rect.top - self.player.height
                            self.player.vertical_velocity = 0
                            self.player.is_jumping = False
                            self.player.can_jump = True
                        elif new_y < self.player.y:  # Jumping up
                            new_y = tile_rect.bottom

        return new_y

    def check_projectile_collisions(self):
        """
        Checks for collisions between any projectile and the player, resetting the player's position if a collision occurs.
        """
        for projectile in self.projectile_manager.projectiles:
            if self.player.rect.colliderect(projectile.rect):
                self.hit_sound.play()
                self.player.reset_position()
                print("kulka trefila")

    def apply_gravity(self):
        """
        Applies gravity to the player, updating their vertical velocity and position.

        :return: A tuple containing the new x and y coordinates of the player.
        :rtype: tuple
        """

        if not self.player.is_jumping or self.player.vertical_velocity > 0:
            self.player.vertical_velocity += self.player.gravity
            self.player.is_jumping = True
        new_x, new_y = self.player.calculate_new_position()
        return new_x, new_y

    def handle_event(self, event):
        """
        Handles a single event from the pygame event queue, affecting the game state or player based on the event type.

        :param Event event: A pygame event object to be processed.
        """

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        self.player.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.show_game_menu()
