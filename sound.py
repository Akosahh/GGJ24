import pygame

class SoundEngine:

    def __init__(self):
        pygame.mixer.init()
        self.laugh = pygame.mixer.Sound("./assets/sounds/main_laugh_1.wav")

    def play_laugh(self):
        self.laugh.play()