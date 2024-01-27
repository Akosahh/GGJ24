import pygame

class Player:

    def __init__(self, image_asset, scale, speed):
        self.image = pygame.image.load(image_asset)
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.speed = speed

    def render(self, screen):
        screen.blit(self.image, (screen.get_width() / 2, screen.get_height() / 2))