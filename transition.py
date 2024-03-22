import pygame


def circular_fade(screen, mode='in', duration=500, max_radius=None, border_color=(255, 255, 255), border_thickness=15):
    if max_radius is None:
        max_radius = int((screen.get_width() ** 2 + screen.get_height() ** 2) ** 0.5)
    clock = pygame.time.Clock()

    if mode == 'out':
        for alpha in range(0, 255, 3):
            fade_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            current_radius = int(max_radius * (alpha / 255))
            pygame.draw.circle(fade_surface, (0, 0, 0, alpha), (screen.get_width() // 2, screen.get_height() // 2), current_radius)
            pygame.draw.circle(fade_surface, border_color + (alpha,), (screen.get_width() // 2, screen.get_height() // 2), current_radius + border_thickness, border_thickness)
            screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            clock.tick(60)

    if max_radius is None:
        max_radius = int((screen.get_width() ** 2 + screen.get_height() ** 2) ** 0.5 / 2)
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while True:
        elapsed = pygame.time.get_ticks() - start_time
        progress = elapsed / duration
        if progress >= 1: break

        if mode == 'out':
            radius = int(max_radius * progress)
        else:  # Fade in
            radius = int(max_radius * (1 - progress))

        fade_surface = screen.copy()
        alpha = 255 * (1 - progress) if mode == 'out' else 255 * progress
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(alpha)

        pygame.draw.circle(fade_surface, (0, 0, 0, 0), (screen.get_width() // 2, screen.get_height() // 2), radius)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)
