import math
import random
import pygame

class NpcFactory:
    def __init__(self, surface, scale):
        self.surface = surface
        self.scale = scale
        self.npc_list = []
        self.population = len(self.npc_list)

    def render(self, x_offset, y_offset):
        for npc in self.npc_list:
            npc.render(x_offset, y_offset)

    def add_npcs(self, position):
        for i in range(len(position)):
            self.npc_list.append(Npc(self.surface, self.scale, position[i], 50))
        self.population = len(self.npc_list)

    def get_positions(self):
        return [n.position for n in self.npc_list]
    
    def move_npcs(self, dt, background_image):
        for npc in self.npc_list:
            npc.move(dt, background_image)

    def collision_with_npcs_check(self, player, bg_offset):
        for i in range(len(self.npc_list)):
            npc = self.npc_list[i]
            if not npc.infected:
                for i in range(3):
                    if npc.collision_check(player, (bg_offset[0] - 8192 * i, bg_offset[1])):
                        npc.infected = True
            else:
                for j in range(len(self.npc_list)):
                    if i == j:
                        continue
                    second_npc = self.npc_list[j]
                    if not second_npc.infected:
                        if npc.collision_check(second_npc, (0,0)):
                            second_npc.infected = True

    def timers(self, time):
        for npc in self.npc_list:
            npc.timer(time)


class Npc:
    def __init__(self, surface, scale, position, speed):
        self.surface = surface
        self.scale = scale

        self.bored_image = pygame.image.load("./assets/images/bored_emoji.png")
        self.bored_image = pygame.transform.scale(self.bored_image, (self.scale, self.scale))
        self.laughing_image = pygame.image.load("./assets/images/laughing.png")
        self.laughing_image = pygame.transform.scale(self.laughing_image, (self.scale, self.scale))
        self.angry_image = pygame.image.load("./assets/images/angry_emoji.png")
        self.angry_image = pygame.transform.scale(self.angry_image, (self.scale, self.scale))

        self.position = position
        self.infected = 0
        self.time = 0

        self.speed = speed
        self.new_direction()

    def new_direction(self):

        # Direction of 0 = moving right
        self.direction = math.radians(random.randrange(0, 360, 30))

        self.x_vel = math.cos(self.direction) * self.speed
        self.y_vel = math.sin(self.direction) * self.speed    

    def render(self, x_offset, y_offset):
        if self.infected == 0:
            self.surface.blit(self.bored_image, self.get_render_position(x_offset, y_offset))
        elif self.infected == 1:
            self.surface.blit(self.laughing_image, self.get_render_position(x_offset, y_offset))
        elif self.infected == 2:
            self.surface.blit(self.angry_image, self.get_render_position(x_offset, y_offset))

    def get_render_position(self, x_offset, y_offset):
        x_pos = self.position[0] - x_offset
        y_pos = self.position[1] - y_offset
        return (x_pos, y_pos)
    
    def get_x(self):
        return self.position[0]
    
    def get_y(self):
        return self.position[1]

    def move(self, dt, background_image):
        x_pos = self.position[0] + self.x_vel * dt
        y_pos = self.position[1] + self.y_vel * dt
        if self.check_position_is_sea(x_pos, y_pos, background_image):
            self.new_direction()
            return
        self.position = (x_pos, y_pos)

    def check_position_is_sea(self, x, y, background_image):
        return background_image.get_at((int(x), int(y))) == (10, 10, 51, 255)

    def collision_check(self, entity, bg_offset):
        x_diff = abs(self.get_x() - entity.get_x() - bg_offset[0])
        y_diff = abs(self.get_y() - entity.get_y() - bg_offset[1])
        distance = math.sqrt(math.pow(x_diff, 2) + math.pow(y_diff, 2))
        return distance < (self.scale / 2) + (entity.scale / 2)

    def timer(self, time):
        if self.infected == 1:
            self.time += time

            if self.time >= 10:
                self.infected = 2
                self.time = 0

        elif self.infected == 2:
            self.time += time

            if self.time >= 5:
                self.infected = 0
                self.time = 0
