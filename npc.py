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


class Npc:
    def __init__(self, surface, scale, image, position):
        self.surface = surface
        self.scale = scale
        self.citizen_image = pygame.image.load(image)
        self.citizen_image = pygame.transform.scale(self.citizen_image, (self.scale, self.scale))
        self.position = position

    def render(self):
        self.surface.blit(self.citizen_image, self.position)


