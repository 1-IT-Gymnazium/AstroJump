import pygame
from Settings import player_colour, player_speed


class Player:
    def __init__(self, x, y, width, height, screen, graphics=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.graphics = graphics
        self.speed = player_speed
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

    def draw(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, player_colour, rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.move_left = True
            if event.key == pygame.K_d:
                self.move_right = True
            if event.key == pygame.K_w:
                self.move_up = True
            if event.key == pygame.K_s:
                self.move_down = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.move_left = False
            if event.key == pygame.K_d:
                self.move_right = False
            if event.key == pygame.K_w:
                self.move_up = False
            if event.key == pygame.K_s:
                self.move_down = False

    def is_moving(self):
        return self.move_left or self.move_right or self.move_up or self.move_down

    def move(self):
        if self.move_left:
            self.x -= self.speed
        if self.move_right:
            self.x += self.speed
        if self.move_up:
            self.y -= self.speed
        if self.move_down:
            self.y += self.speed
