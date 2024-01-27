import pygame
from entities import Player

class Game:

    def __init__(self, size, font, font_size, background_asset):

        pygame.init()

        self.screen = pygame.display.set_mode(size)
        self.font = pygame.font.SysFont(font, font_size)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(background_asset).convert()

        self.player = Player("./assets/images/laughing.png", 30, 100)

        self.background_x_offset = 0
        self.background_y_offset = 0

    def update(self):
        self.get_key_presses()
        self.check_player_movement()

        self.screen.fill("black")

        for i in range(3):
            for j in range(3):
                self.screen.blit(self.background, ((-self.background_x_offset + 8192 * i, -self.background_y_offset + 4096 * j)))

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
            self.background_y_offset -= self.player.speed * self.dt
        if self.keys[pygame.K_s]:
            self.background_y_offset += self.player.speed * self.dt
        if self.keys[pygame.K_a]:
            self.background_x_offset -= self.player.speed * self.dt
        if self.keys[pygame.K_d]:
            self.background_x_offset += self.player.speed * self.dt

        self.background_x_offset %= 8192
        self.background_y_offset %= 4096
        
        self.background_x_offset = int(self.background_x_offset)
        self.background_y_offset = int(self.background_y_offset)