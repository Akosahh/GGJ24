import pygame
import math

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1920, 1080))
font = pygame.font.SysFont("didot.ttc", 72)
clock = pygame.time.Clock()
pygame.mixer.init()

bg = pygame.image.load("./assets/images/land_shallow_topo_8192.tif").convert()
player = pygame.image.load("./assets/images/laughing.png")
player = pygame.transform.scale(player, (30, 30))

sound = pygame.mixer.Sound("./assets/sounds/main_laugh_1.wav")

running = True
dt = 0
speed = 600
scroll = [0, 0]

while running:
    # -------- DRAW --------
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    for i in range(3):
        for j in range(3):
            screen.blit(bg, ((-scroll[0] + 8192 * i, -scroll[1] + 4096 * j)))

    screen.blit(player, (screen.get_width() / 2, screen.get_height() / 2))
    
    img = font.render(f"Scroll: [{scroll[0]}, {scroll[1]}]", True, (255, 0, 0))
    screen.blit(img, (20, 20))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # -------- Logic --------
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        scroll[1] -= speed * dt
    if keys[pygame.K_s]:
        scroll[1] += speed * dt
    if keys[pygame.K_a]:
        scroll[0] -= speed * dt
    if keys[pygame.K_d]:
        scroll[0] += speed * dt
    if keys[pygame.K_ESCAPE]:
        pygame.mixer.Sound.play(sound)

    scroll = [scroll[0] % 8192, scroll[1] % 4096]

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
