import pygame
from random import randint
import math


class City:
    def __init__(self, surface):
        self.surface = surface
        self.size = 90
        self.people_size = 25
        self.location = (1800, 1200)
        self.centre = (self.location[0] + self.size / 2, self.location[1] + self.size / 2)
        self.city_image = pygame.image.load("./assets/images/city_image_1.png")
        self.city_image = pygame.transform.scale(self.city_image, (self.size, self.size))
        self.citizen_image = pygame.image.load("./assets/images/bored_emoji.png")
        self.citizen_image = pygame.transform.scale(self.citizen_image, (self.people_size, self.people_size))
        self.colour = "white"
        # self.population = 35
        self.x_y_list = []

    def render(self):

        self.surface.blit(self.city_image, self.location)
        for coord in self.x_y_list:
            self.surface.blit(self.citizen_image, coord)

    def set_x_y_npc(self, radius_range):

        angle = randint(0, 360)
        random_x_mod = randint(self.size - 20, radius_range)
        random_y_mod = randint(self.size - 20, radius_range)

        if 0 <= angle < 90:
            x, y = self.centre[0] + random_x_mod * math.cos(angle), self.centre[1] + random_y_mod * math.sin(angle)
            return x, y

        elif 90 <= angle < 180:
            x, y = self.centre[0] - random_x_mod * math.cos(angle), self.centre[1] + random_y_mod * math.sin(angle)
            return x, y

        elif 180 <= angle < 270:
            x, y = self.centre[0] - random_x_mod * math.cos(angle), self.centre[1] - random_y_mod * math.sin(angle)
            return x, y

        elif 270 <= angle <= 360:
            x, y = self.centre[0] + random_x_mod * math.cos(angle), self.centre[1] - random_y_mod * math.sin(angle)
            return x, y

    def create_population(self, radius_range, population):
        for n in range(population):
            x, y = self.set_x_y_npc(radius_range)
            self.x_y_list.append((x, y))

