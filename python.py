import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 500))

pygame.mixer.init()
sound = pygame.mixer.Sound("./sounds/CantinaBand3.wav")


bg = pygame.image.load("./images/map.jpg")

clock = pygame.time.Clock()
running = True


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.mixer.Sound.play(sound)

    screen.blit(bg, (0, 0))

    pygame.display.flip()
    clock.tick(40)

pygame.quit()
