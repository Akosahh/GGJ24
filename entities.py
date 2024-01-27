import pygame

class Player:

    def __init__(self, image_asset, scale, speed):
        self.image = pygame.image.load(image_asset)
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.speed = speed
        self.vertical_offset = 0

    def render(self, screen):
        screen.blit(self.image, (int(screen.get_width() / 2), int(screen.get_height() / 2) + self.vertical_offset))