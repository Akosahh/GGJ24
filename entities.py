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

    def collision_with_npc_check(self, npc, bg_offset):
        x_min = npc.position[0] - npc.scale
        x_max = npc.position[0] + npc.scale
        y_min = npc.position[1] - npc.scale
        y_max = npc.position[1] + npc.scale

        return (x_min < (bg_offset[0] + self.get_x()) < x_max) and (y_min < (bg_offset[1] + self.get_y()) < y_max)
