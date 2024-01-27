import pygame
from entities import Player

class Game:

    def __init__(self, font, font_size, background_asset):

        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.font = pygame.font.SysFont(font, font_size)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(background_asset).convert()

        self.player = Player("./assets/images/laughing.png", 30, 1000)

        self.background_x_offset = 0
        self.background_y_offset = 0

    def update(self):
        self.get_key_presses()
        self.check_player_movement()

        self.screen.fill("black")

        for i in range(3):
            self.screen.blit(self.background, ((-self.background_x_offset + 8192 * i, -self.background_y_offset)))

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        self.dt = self.clock.tick(60) / 1000

        self.render_entities()
        self.render_ui()
        
        pygame.display.flip()

    def render_entities(self):
        self.player.render(self.screen)

    def render_ui(self):
        position_info = self.font.render(f"Scroll: [{self.background_x_offset}, {self.background_y_offset}]", True, (255, 0, 0))
        self.screen.blit(position_info, (20, 20))

    def get_key_presses(self):
        self.keys = pygame.key.get_pressed()

    def check_player_movement(self):
        if self.keys[pygame.K_w]:
            if self.player.vertical_offset > 0:
                self.player.vertical_offset -= self.player.speed * self.dt
            elif self.background_y_offset > 0:
                self.background_y_offset -= self.player.speed * self.dt
            else:
                self.background_y_offset = 0
                if self.player.vertical_offset > -int(self.screen.get_height() / 2):
                    self.player.vertical_offset -= self.player.speed * self.dt
                else:
                    self.player.vertical_offset = -int(self.screen.get_height() / 2)
        if self.keys[pygame.K_s]:
            if self.player.vertical_offset < 0:
                self.player.vertical_offset += self.player.speed * self.dt
            elif self.background_y_offset < (4096 - self.screen.get_height()):
                self.background_y_offset += self.player.speed * self.dt
            else:
                self.background_y_offset = (4096 - self.screen.get_height())
                if self.player.vertical_offset < int(self.screen.get_height() / 2):
                    self.player.vertical_offset += self.player.speed * self.dt
                else:
                    self.player.vertical_offset = int(self.screen.get_height() / 2)
        if self.keys[pygame.K_a]:
            self.background_x_offset -= self.player.speed * self.dt
        if self.keys[pygame.K_d]:
            self.background_x_offset += self.player.speed * self.dt

        self.background_x_offset %= 8192
        
        self.background_x_offset = int(self.background_x_offset)
        self.background_y_offset = int(self.background_y_offset)