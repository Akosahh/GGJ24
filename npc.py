import math
import random
import pygame

class NpcFactory:
    def __init__(self, surface, scale, image):
        self.surface = surface
        self.scale = scale
        self.citizen_image = image
        self.npc_list = []
        self.population = len(self.npc_list)

    def render(self, x_offset, y_offset):
        for npc in self.npc_list:
            npc.render(x_offset, y_offset)

    def add_npcs(self, position):
        for i in range(len(position)):
            self.npc_list.append(Npc(self.surface, self.scale, self.citizen_image, position[i], 50))
        self.population = len(self.npc_list)

    def get_positions(self):
        return [n.position for n in self.npc_list]
    
    def move_npcs(self, dt):
        for npc in self.npc_list:
            npc.move(dt)

    def collision_with_npcs_check(self, player, bg_offset):
        for npc in self.npc_list:
            if not npc.infected:
                if npc.collision_with_npc_check(player, bg_offset):
                    npc.citizen_image = pygame.image.load("./assets/images/laughing.png")
                    npc.citizen_image = pygame.transform.scale(npc.citizen_image, (npc.scale, npc.scale))

class Npc:
    def __init__(self, surface, scale, image, position, speed):
        self.surface = surface
        self.scale = scale
        self.citizen_image = pygame.image.load(image)
        self.citizen_image = pygame.transform.scale(self.citizen_image, (self.scale, self.scale))
        self.position = position
        self.infected = False

        self.speed = speed
        self.new_direction()

    def new_direction(self):

        # Direction of 0 = moving right
        self.direction = math.radians(random.randrange(0, 360, 30))

        self.x_vel = math.cos(self.direction) * self.speed
        self.y_vel = math.sin(self.direction) * self.speed    

    def render(self, x_offset, y_offset):
        self.surface.blit(self.citizen_image, self.get_render_position(x_offset, y_offset))

    def get_render_position(self, x_offset, y_offset):
        x_pos = self.position[0] - x_offset
        y_pos = self.position[1] - y_offset
        return (x_pos, y_pos)

    def move(self, dt):
        x_pos = self.position[0] + self.x_vel * dt
        y_pos = self.position[1] + self.y_vel * dt
        self.position = (x_pos, y_pos)

    def collision_with_npc_check(self, player, bg_offset):
        x_min = self.position[0] - self.scale
        x_max = self.position[0] + self.scale
        y_min = self.position[1] - self.scale
        y_max = self.position[1] + self.scale

        return (x_min < (bg_offset[0] + player.get_x()) < x_max) and (y_min < (bg_offset[1] + player.get_y()) < y_max)



