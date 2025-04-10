import pygame, sys
from settings import *
from level import *
from player import *
import menu.principal_menu

class Game:
    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('D&D 2D')
        self.clock = pygame.time.Clock()
        self.level = Level() # Se llama a la función level, por lo que se ejecuta su constructor y por tanto se dibujan los elementos de la matriz WORLD_MAP.
        self.status = 'menu'

    
    def run(self):
        while True:
            if self.status == 'menu':
                self.status = menu.principal_menu.show_menu()
            elif self.status == 'game':
                self.level = Level()
                self.play_game()
            elif self.status == 'quit':
                pygame.quit()
                sys.exit()

    def play_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.status = 'quit'
                    return
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)



if __name__ == '__main__':
    game = Game()
    game.run()