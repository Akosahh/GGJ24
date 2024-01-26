import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 500))

bg = Background("./images/map.jpg")

clock = pygame.time.Clock()
running = True


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg.image, (0,0))

    pygame.display.flip()
    clock.tick(40)

pygame.quit()
