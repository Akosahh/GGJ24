import math
import random
import json
import pygame


class PortFactory:
    def __init__(self, background, image_asset, file):
        self.background = background
        self.image_asset = image_asset
        self.ports = []

        data = json.load(open(file))
        for port in data:
            self.ports.append(
                Port(background, image_asset, port["scale"], port["position"])
            )

    def render(self, x_offset, y_offset):
        for port in self.ports:
            port.render(x_offset, y_offset)


class Port:
    def __init__(self, background, image_asset, scale, position):
        self.background = background
        self.image = pygame.image.load(image_asset)
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.scale = scale
        self.position = position

    def render(self, x_offset, y_offset):
        self.background.blit(self.image, self.get_render_position(x_offset, y_offset))

    def get_render_position(self, x_offset, y_offset):
        x_pos = self.position[0] - x_offset
        y_pos = self.position[1] - y_offset
        return (x_pos, y_pos)

class VehicleFactory:
    def __init__(self, background, image_asset, scale, count, ports):
        self.background = background
        self.image_asset = image_asset
        self.scale = scale
        self.count = count
        self.ports = ports
        self.vehicles = []

        for i in range(count):
            self.vehicles.append(
                Vehicle(
                    self.background,
                    self.image_asset,
                    self.scale,
                    random.choice(self.ports).position,
                    random.choice(self.ports).position,
                )
            )

    def render(self, x_offset, y_offset):
        for vehicle in self.vehicles:
            vehicle.render(x_offset, y_offset)


class Vehicle:
    def __init__(self, background, image_asset, scale, start_position, end_position):
        self.background = background
        self.image = pygame.image.load(image_asset)
        self.scale = scale
        self.start_position = start_position
        self.end_position = end_position
        self.position = start_position
        self.complete = 0
        self.step = 0.01
        self.distance = math.sqrt(
            pow(self.end_position[0] - self.start_position[0], 2)
            + pow(self.end_position[1] - self.start_position[1], 2)
        )
        self.image = pygame.transform.scale(self.image, (1.5 * scale, scale))
        self.image = pygame.transform.flip(
            self.image,
            True if self.start_position[0] < self.end_position[0] else False,
            False,
        )

    def render(self, x_offset, y_offset):
        self.background.blit(self.image, self.get_render_position(x_offset, y_offset))

    def get_render_position(self, x_offset, y_offset):
        x_pos = self.position[0] - x_offset
        y_pos = self.position[1] - y_offset
        return (x_pos, y_pos)

    def calculate_position(self):
        self.position = (
            (1 - self.complete) * self.start_position[0]
            + self.complete * self.end_position[0],
            (1 - self.complete) * self.start_position[1]
            + self.complete * self.end_position[1],
        )
        self.complete += self.step
