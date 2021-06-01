import pygame

from agent import Agent

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Steering Behaviour")
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        
        self.group = [Agent(self.width, self.height) for i in range(100)]
    
    def update(self):
        
        while not self.exit:
            
            # Update delta
            dt = self.clock.get_time() / 1000
            
            # Check for event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # Render
            self.screen.fill((56,56,56))
            
            for agent in self.group:
                agent.out_of_bounds(self.width, self.height)
                agent.follow(self.group)
                agent.update(dt)
                
                pygame.draw.circle(self.screen, (255,255,255), agent.position, 7)
                
            pygame.display.flip()
            self.clock.tick(self.ticks)
        
        pygame.quit()
            

if __name__ == '__main__':
    game = Game()
    game.update()