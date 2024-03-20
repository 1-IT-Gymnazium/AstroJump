import pygame


def fade_to_black(screen, fade_speed=5):
    fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 300, fade_speed):  # Adjust fade speed and range as needed
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(50)  # Delay to make the fade noticeable


def fade_from_black(screen, fade_speed=5):
    fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_surface.fill((0, 0, 0))
    for alpha in range(300, 0, fade_speed):  # Adjust fade speed and range as needed
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(50)  # Delay to make the fade noticeable
