import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
dt = 0

scroll = [screen.get_width()/2, screen.get_height()/2]

bg = pygame.image.load("./images/land_shallow_topo_8192.tif").convert()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill('black')

    # RENDER YOUR GAME HERE
    screen.blit(bg, scroll)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        scroll[1] += 600 * dt
    if keys[pygame.K_s]:
        scroll[1] -= 600 * dt
    if keys[pygame.K_a]:
        scroll[0] += 600 * dt
    if keys[pygame.K_d]:
        scroll[0] -= 600 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()