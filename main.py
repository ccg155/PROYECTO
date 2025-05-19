import pygame, sys
from settings import *
from level import *
from player import *

class Game:
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('FlowerPower Hardcore')
        self.clock = pygame.time.Clock()
        self.level = Level() # Se llama a la función level, por lo que se ejecuta su constructor y por tanto se dibujan los elementos de la matriz WORLD_MAP.

        # Sonido
        main_sound = pygame.mixer.Sound('audio/main.ogg')
        main_sound.play(loops = -1)
        main_sound.set_volume(0.4)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.level.toggle_menu()
            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()