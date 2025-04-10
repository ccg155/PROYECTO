import pygame, sys
from settings import *
from level import *
from player import *

class Game:
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('D&D 2D')
        self.clock = pygame.time.Clock()
        self.level = Level() # Se llama a la función level, por lo que se ejecuta su constructor y por tanto se dibujan los elementos de la matriz WORLD_MAP.
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()