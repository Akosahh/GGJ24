import pygame
from entities import Player
from npccity import City

class Game:

    def __init__(self, font, font_size, background_asset):

        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.font = pygame.font.SysFont(font, font_size)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(background_asset).convert()

        self.player = Player(self.screen, "./assets/images/laughing.png", 30, 100)
        self.city = City(self.background)
        self.city.create_population(50)
        self.city.create_population(100)

        self.background_x_offset = 0
        self.background_y_offset = 0

    def update(self):
        
        self.dt = self.clock.tick(60) / 1000

        self.get_key_presses()
        self.check_player_movement()

        self.screen.fill("black")

        for i in range(3):
            self.screen.blit(self.background, ((-self.background_x_offset + 8192 * i, -self.background_y_offset)))

        self.render_entities()
        self.render_ui()
        
        pygame.display.flip()

    def render_entities(self):
        self.player.render()
        self.city.render()



    def render_ui(self):
        position_info = self.font.render(f"Scroll: [{self.background_x_offset}, {self.background_y_offset}]", True, (255, 0, 0))
        self.screen.blit(position_info, (20, 20))

    def get_key_presses(self):
        self.keys = pygame.key.get_pressed()

    def check_player_movement(self):
        frame_speed = self.player.speed * self.dt

        self.check_up(frame_speed)
        self.check_down(frame_speed)
        self.check_horizontal(frame_speed)

        self.background_x_offset %= 8192
        
        self.background_x_offset = int(self.background_x_offset)
        self.background_y_offset = int(self.background_y_offset)

    def check_up(self, frame_speed):
        if self.keys[pygame.K_w]:
            if self.check_position_is_sea(self.player.get_x(), self.player.get_y() - frame_speed):
                return
            if self.player.vertical_offset > 0:
                self.player.vertical_offset -= frame_speed
            elif self.background_y_offset > 0:
                self.background_y_offset -= frame_speed
            else:
                self.background_y_offset = 0
                if self.player.vertical_offset > -int(self.screen.get_height() / 2):
                    self.player.vertical_offset -= frame_speed
                else:
                    self.player.vertical_offset = -int(self.screen.get_height() / 2)

    def check_down(self, frame_speed):
        if self.keys[pygame.K_s]:
            if self.check_position_is_sea(self.player.get_x(), self.player.get_y() + frame_speed + 30):
                return
            if self.player.vertical_offset < 0:
                self.player.vertical_offset += self.player.speed * self.dt
            elif self.background_y_offset < (4096 - self.screen.get_height()):
                self.background_y_offset += frame_speed
            else:
                self.background_y_offset = (4096 - self.screen.get_height())
                if self.player.vertical_offset < int(self.screen.get_height() / 2):
                    self.player.vertical_offset += frame_speed
                else:
                    self.player.vertical_offset = int(self.screen.get_height() / 2)

    def check_horizontal(self, frame_speed):
        if self.keys[pygame.K_a]:
            if self.check_position_is_sea(self.player.get_x() - frame_speed, self.player.get_y()):
                return
            self.background_x_offset -= frame_speed
        if self.keys[pygame.K_d]:
            if self.check_position_is_sea(self.player.get_x() + frame_speed + 30, self.player.get_y()):
                return
            self.background_x_offset += frame_speed

    def check_position_is_sea(self, x, y):
        return self.screen.get_at((int(x), int(y))) == (10, 10, 51, 255)