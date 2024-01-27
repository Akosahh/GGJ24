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

    def collision_with_npc_check(self, npc_position_list, npc_size, player_pos):
        collision = False

        for position in npc_position_list:
            x_min = position[0] - npc_size
            x_max = position[0] + npc_size
            y_min = position[1] - npc_size
            y_max = position[1] + npc_size

            if (x_min < (player_pos[0] + self.get_x()) < x_max) and (y_min < (player_pos[1] + self.get_y()) < y_max):
                collision = True

