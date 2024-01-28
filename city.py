import pygame
from random import randint
import math
from npc import NpcFactory

class CityFactory:
    def __init__(self, surface, locations, scale, image):
        self.surface = surface
        self.scale = scale
        self.locations = locations
        self.city_image = image
        self.city_list = []

        for location in self.locations:
            self.city_list.append(City(
                surface=self.surface,
                location=location,
                scale=self.scale,
                image=self.city_image
            ))

    def render(self):
        for city in self.city_list:
            city.render()


class City:
    def __init__(self, surface, location, scale, image):
        self.surface = surface
        self.scale = scale
        self.location = location
        self.centre = (self.location[0] + self.scale / 2, self.location[1] + self.scale / 2)
        self.city_image = pygame.image.load(image)
        self.city_image = pygame.transform.scale(self.city_image, (self.scale, self.scale))
        self.npc_list = self.create_npc()

    def render(self):
        self.surface.blit(self.city_image, self.location)
        self.npc_list.render()


    def create_npc(self):
        npc_factory = NpcFactory(
            surface=self.surface,
            scale=25,
            image="./assets/images/bored_emoji.png",
        )

        npc_factory.add_npcs(position=[self.set_x_y_npc(100) for i in range(20)])
        npc_factory.add_npcs(position=[self.set_x_y_npc(150) for i in range(30)])

        return npc_factory


    def set_x_y_npc(self, radius_range):

        angle = randint(0, 360)
        random_x_mod = randint(self.scale - 20, radius_range)
        random_y_mod = randint(self.scale - 20, radius_range)

        if 0 <= angle < 90:
            x, y = self.centre[0] + random_x_mod * math.cos(angle), self.centre[1] + random_y_mod * math.sin(angle)
            return (x, y)

        elif 90 <= angle < 180:
            x, y = self.centre[0] - random_x_mod * math.cos(angle), self.centre[1] + random_y_mod * math.sin(angle)
            return (x, y)

        elif 180 <= angle < 270:
            x, y = self.centre[0] - random_x_mod * math.cos(angle), self.centre[1] - random_y_mod * math.sin(angle)
            return (x, y)

        elif 270 <= angle <= 360:
            x, y = self.centre[0] + random_x_mod * math.cos(angle), self.centre[1] - random_y_mod * math.sin(angle)
            return (x, y)

