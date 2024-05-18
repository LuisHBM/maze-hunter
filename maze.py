import pygame
import random

from world import World

class Maze():
    
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # Movements
    FRONT = 1
    BACK  = 2
    LEFT  = 3
    RIGHT = 4
    
    def __init__(self) -> None:
        
        self.world = World()
        self.running = True
        self.score = 0
        self.steps = 0
        
        # Initializing pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.world.width, self.world.height))
        pygame.display.set_caption('Maze Treasure Hunt')
        
        self.draw_world()
        
        
    def draw_world(self):
        
        px, py = self.world.player.position
        
        # Drawing
        self.screen.fill(self.BLACK)
        for row in range(self.world.maze_size):
            for col in range(self.world.maze_size):
                
                rect = pygame.Rect(col*self.world.block_size, row*self.world.block_size, self.world.block_size, self.world.block_size)
                if [col, row] in self.world.walls:
                    pygame.draw.rect(self.screen, self.BLACK, rect)
                elif [col, row] in self.world.water:
                    pygame.draw.rect(self.screen, self.BLUE, rect)            
                else:
                    pygame.draw.rect(self.screen, self.WHITE, rect)
                if [col, row] == [px, py]:
                    pygame.draw.rect(self.screen, self.RED, rect)
                elif [col, row] in self.world.treasures:
                    pygame.draw.rect(self.screen, self.WHITE, rect)
                    self.screen.blit(self.world.treasure_image, (col*self.world.block_size, row*self.world.block_size))
               
                    
    def update_score(self):
        
        px, py = self.world.player.position
        
        self.score -= 1

        if [px, py] in self.world.treasures:
            self.world.treasures.remove([px, py])
            print("Treasure found! Treasures left:", len(self.world.treasures))
            self.score += 50
            
        if [px, py] in self.world.water:
            self.score -= 5
            print("In water! Paying heavier price:", [px, py])
        
        
    def move_player_front(self) -> bool:
        pass
    
    def move_player_back(self) -> bool:
        pass
    
    def move_player_left(self) -> bool:
        pass
    
    def move_player_right(self) -> bool:
        pass
    
    def move_randomly(self) -> int:     
        #      Front
        # Left   0   Right
        #      Back
        
        move = random.randint(1, 4)
        
        player_pos = self.world.player.position
        if move == self.FRONT:
            next_pos = (player_pos[0], player_pos[1] + 1) 
        elif move == self.BACK:
            next_pos = (player_pos[0], player_pos[1] - 1) 
        elif move == self.RIGHT:
            next_pos = (player_pos[0] + 1, player_pos[1]) 
        elif move == self.LEFT:
            next_pos = (player_pos[0] - 1, player_pos[1]) 
        else:
            print(f"Movement {move} doesn't exist.")
            self.running = False
            return 0
            
        if self.world.can_move_to(next_pos):
            self.world.player.position = next_pos
            return move
        
        return 0
            
            
    def game_loop(self):
        
        while self.running:
            
            print(f"Step: {self.steps}")
            print(f"Score: {self.score}")
            
            pygame.display.flip()
            pygame.time.wait(100)  # Slow down the game a bit
            
            move = self.move_randomly()
            
            self.draw_world()
            
            if move != 0:
                print(f"Moveu: {move}")
                self.update_score()
                self.steps += 1
            
            # Checks if the player already collected 8 treasures
            if len(self.world.treasures) <= 4:
                self.running = False
            
            if not self.world.treasures:
                self.running = False
            #if self.steps >= 800: 
            #    print(f"Maximum number of steps {steps}")
            #    self.running = False
            
            print(f" ")

        found_treasures = self.world.num_treasures - len(self.world.treasures)
        print(f"Found {found_treasures} treasures")
        final_score = (found_treasures * 50) + self.score
        print(f"Final score: {final_score}")
        pygame.quit()

if __name__ == "__main__":
    
    maze = Maze()
    
    maze.game_loop()