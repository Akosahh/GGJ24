import pygame
from PIL import Image


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 500))

bg = Background("./images/map.jpg")
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

    screen.blit(bg.image, (0, 0))
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

    pygame.display.update()
    dt = clock.tick(40) / 10000

pygame.quit()
