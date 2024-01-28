import random
import pygame

from player import Player
from city import CityFactory
from port import PortFactory, VehicleFactory, Vehicle

class Game:
    def __init__(self, font, font_size, background_asset):
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.font = pygame.font.SysFont(font, font_size)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(background_asset).convert()

        self.player = Player(self.screen, "./assets/images/laughing.png", 30, 100)
        self.city_factory = CityFactory(
            surface=self.screen,
            locations=[(1800, 1200), (1771, 685)],
            scale=90,
            image="./assets/images/city_image_1.png"
        )

        self.port_factory = PortFactory(
            self.screen, "./assets/images/airport.svg", "./airports.json"
        )
        self.plane_factory = VehicleFactory(
            self.screen,
            "./assets/images/airplane.png",
            30,
            10,
            self.port_factory.ports,
        )

        self.background_x_offset = 0
        self.background_y_offset = 0

    def update(self):
        self.dt = self.clock.tick(60) / 1000

        self.get_key_presses()
        self.check_exit()
        self.check_player_movement()
        self.plane_logic()

        for city in self.city_factory.city_list:
            city.npc_list.move_npcs(self.dt, self.background)
            city.npc_list.collision_with_npcs_check(self.player, [self.background_x_offset, self.background_y_offset])

        self.screen.fill( (0,0,0) )

        for i in range(3):
            self.screen.blit(
                self.background,
                ((-self.background_x_offset + 8192 * i, -self.background_y_offset)),
            )
            self.city_factory.render(self.background_x_offset - 8192 * i, self.background_y_offset)
            self.port_factory.render(self.background_x_offset - 8192 * i, self.background_y_offset)
            self.plane_factory.render(self.background_x_offset - 8192 * i, self.background_y_offset)
        
        self.player.render()
        self.render_ui()

        pygame.display.flip()

    def render_ui(self):
        position_info = self.font.render(
            f"Scroll: [{self.background_x_offset}, {self.background_y_offset}]",
            True,
            (255, 0, 0),
        )
        self.screen.blit(position_info, (20, 20))

    def get_key_presses(self):
        self.keys = pygame.key.get_pressed()

    def check_player_movement(self):
        frame_speed = self.player.speed * self.dt

        self.check_up(frame_speed)
        self.check_down(frame_speed)
        self.check_horizontal(frame_speed)

        self.background_x_offset %= 8192

    def check_up(self, frame_speed):
        if self.keys[pygame.K_w]:
            if self.check_position_is_sea(
                self.player.get_x(), self.player.get_y() - frame_speed
            ):
                return
            if self.player.vertical_offset > 0:
                self.player.vertical_offset -= frame_speed
            elif self.background_y_offset > 0:
                self.background_y_offset -= frame_speed
            else:
                self.background_y_offset = 0
                if self.player.vertical_offset > -self.screen.get_height() / 2:
                    self.player.vertical_offset -= frame_speed
                else:
                    self.player.vertical_offset = -self.screen.get_height() / 2

    def check_down(self, frame_speed):
        if self.keys[pygame.K_s]:
            if self.check_position_is_sea(
                self.player.get_x(), self.player.get_y() + frame_speed + 30
            ):
                return
            if self.player.vertical_offset < 0:
                self.player.vertical_offset += frame_speed
            elif self.background_y_offset < (4096 - self.screen.get_height()):
                self.background_y_offset += frame_speed
            else:
                self.background_y_offset = 4096 - self.screen.get_height()
                if self.player.vertical_offset < self.screen.get_height() / 2:
                    self.player.vertical_offset += frame_speed
                else:
                    self.player.vertical_offset = self.screen.get_height() / 2

    def check_horizontal(self, frame_speed):
        if self.keys[pygame.K_a]:
            if self.check_position_is_sea(
                self.player.get_x() - frame_speed, self.player.get_y()
            ):
                return
            self.background_x_offset -= frame_speed
        if self.keys[pygame.K_d]:
            if self.check_position_is_sea(
                self.player.get_x() + frame_speed + 30, self.player.get_y()
            ):
                return
            self.background_x_offset += frame_speed

    def check_position_is_sea(self, x, y):
        return self.screen.get_at((int(x), int(y))) == (10, 10, 51, 255)

    def check_exit(self):
        if self.keys[pygame.K_ESCAPE]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def plane_logic(self):
        for i, plane in enumerate(self.plane_factory.vehicles):
            if plane.complete < 1:
                plane.calculate_position()
            else:
                self.plane_factory.vehicles[i] = Vehicle(
                    self.plane_factory.background,
                    self.plane_factory.image_asset,
                    self.plane_factory.scale,
                    random.choice(self.plane_factory.ports).position,
                    random.choice(self.plane_factory.ports).position,
                )
