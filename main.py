import pygame
from game import Game

game = Game("didot.ttc", 72, "./assets/images/land_shallow_topo_8192.tif")

running = True

while running:

    game.update()

    # -------- Logic --------
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()