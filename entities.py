import pygame

class Player:

    def __init__(self, screen, image_asset, scale, speed):
        self.screen = screen
        self.image = pygame.image.load(image_asset)
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.speed = speed
        self.scale = scale
        self.vertical_offset = 0

    def render(self):
        self.screen.blit(self.image, (self.get_x(), self.get_y()))

    def get_x(self):
        return self.screen.get_width() / 2
    
    def get_y(self):
        return (self.screen.get_height() / 2) + self.vertical_offset