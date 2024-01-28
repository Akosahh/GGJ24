import random
import pygame

from player import Player
from city import CityFactory
from port import PortFactory, VehicleFactory, Vehicle, Port

class Game:
    def __init__(self, font, font_size, background_asset):
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.font = pygame.font.SysFont(font, font_size)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(background_asset).convert()
        self.last_interaction = pygame.time.get_ticks()
        self.on_flight = None
        self.last_port = None

        self.player = Player(self.screen, "./assets/images/laughing.png", 30, 100)
        self.city_factory = CityFactory(
            surface=self.screen,
            locations=[
                (1800, 1200),
                (1771, 685),
                (2100, 1200),
                (2490, 2100),
                (4016, 1503),
                (4686, 1683),
                (4655, 2673),
                (7145, 2593),
                (4586, 932),
                (5485, 692),
                (5996, 1243),
                (6725, 662),
            ],
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
        self.handle_flight()
        self.plane_logic()
        self.check_player_interactions()

        for city in self.city_factory.city_list:
            city.npc_list.move_npcs(self.dt, self.background)
            city.npc_list.collision_with_npcs_check(self.player, [self.background_x_offset, self.background_y_offset])
            city.npc_list.timers(self.dt)

        self.screen.fill( (0,0,0) )

        self.background_x_offset %= 8192

        for i in range(3):
            self.screen.blit(
                self.background,
                ((-self.background_x_offset + 8192 * i, -self.background_y_offset)),
            )
        for i in range(3):
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
        if self.player.can_move:
            frame_speed = self.player.speed * self.dt

            self.check_up(frame_speed)
            self.check_down(frame_speed)
            self.check_horizontal(frame_speed)

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
                if self.on_flight == plane:
                    self.on_flight = None
                    plane.start_port.player_waiting = False
                    self.player.can_move = True
                    self.last_port.player_waiting = False
                    self.last_port = None
                    
                start_port = random.choice(self.plane_factory.ports)
                end_port = random.choice(self.plane_factory.ports)

                self.plane_factory.vehicles[i] = Vehicle(
                    self.plane_factory.background,
                    self.plane_factory.image_asset,
                    self.plane_factory.scale,
                    start_port,
                    end_port,
                )

                if start_port.player_waiting:
                    self.on_flight = self.plane_factory.vehicles[i]

    def check_player_interactions(self):
        if self.keys[pygame.K_e] and (pygame.time.get_ticks() - self.last_interaction) > 200:
            self.last_interaction = pygame.time.get_ticks()
            if self.player.can_move:
                port = self.port_factory.collision_checks(self.player, [self.background_x_offset, self.background_y_offset])

                if port:
                    self.background_x_offset = port.get_x() - self.player.get_x()
                    self.background_y_offset = port.get_y() - self.player.get_y()
                    self.player.can_move = False
                    port.player_waiting = True
                    self.last_port = port
            elif not self.on_flight:
                self.player.can_move = True
                self.last_port.player_waiting = False
                self.last_port = None
                
    
    def handle_flight(self):
        if self.on_flight:
            self.background_x_offset = self.on_flight.get_x() - self.player.get_x()
            self.background_y_offset = self.on_flight.get_y() - self.player.get_y()