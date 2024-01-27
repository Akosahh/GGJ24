import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 500))

pygame.mixer.init()
sound = pygame.mixer.Sound("./sounds/main_laugh_1.wav")
test_sound = pygame.mixer.Sound("./sounds/CantinaBand3.wav")

bg = pygame.image.load("./images/map.jpg")

player = pygame.image.load("./images/laughing.png")
player = pygame.transform.scale(player, (30, 30))

clock = pygame.time.Clock()
running = True
dt = 0

player_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg, (0, 0))
    # pygame.draw.circle(screen, player, player_position, 10)
    screen.blit(player, player_position)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_position.y -= 300 * dt
    if keys[pygame.K_s]:
        player_position.y += 300 * dt
    if keys[pygame.K_a]:
        player_position.x -= 300 * dt
    if keys[pygame.K_d]:
        player_position.x += 300 * dt
    if keys[pygame.K_ESCAPE]:
        pygame.mixer.Sound.play(sound)

    pygame.display.update()
    dt = clock.tick(40) / 10000

pygame.quit()
