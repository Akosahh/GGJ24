import pygame
import random


class NpcFactory:
    def __init__(self, surface, scale, image):
        self.surface = surface
        self.scale = scale
        self.citizen_image = image
        self.npc_list = []
        self.population = len(self.npc_list)


    def render(self):
        for npc in self.npc_list:
            npc.render()

    def add_npcs(self, position):
        for i in range(len(position)):
            self.npc_list.append(Npc(self.surface, self.scale, self.citizen_image, position[i]))
        self.population = len(self.npc_list)

    def get_positions(self):
        return [n.position for n in self.npc_list]

    def collision_with_npcs_check(self, player, bg_offset):
        for npc in self.npc_list:
            if not npc.infected:
                if npc.collision_with_npc_check(player, bg_offset):
                    npc.citizen_image = pygame.image.load("./assets/images/laughing.png")
                    npc.citizen_image = pygame.transform.scale(npc.citizen_image, (npc.scale, npc.scale))


class Npc:
    def __init__(self, surface, scale, image, position):
        self.surface = surface
        self.scale = scale
        self.citizen_image = pygame.image.load(image)
        self.citizen_image = pygame.transform.scale(self.citizen_image, (self.scale, self.scale))
        self.position = position
        self.infected = False

    def render(self):
        self.surface.blit(self.citizen_image, self.position)

    def collision_with_npc_check(self, player, bg_offset):
        x_min = self.position[0] - self.scale
        x_max = self.position[0] + self.scale
        y_min = self.position[1] - self.scale
        y_max = self.position[1] + self.scale

        return (x_min < (bg_offset[0] + player.get_x()) < x_max) and (y_min < (bg_offset[1] + player.get_y()) < y_max)



