import pygame
import random

from world import World
from dijkstra import Dijkstra


class Maze():
    
    # Colors
    WALL_COLOR = (0, 0, 0)
    GROUND_COLOR = (255, 255, 255)
    PLAYER_COLOR = (255, 0, 0)
    WATER_COLOR = (0, 0, 255)
    PATH_COLOR = (0, 255, 0)
    PATH_WATER_COLOR = (0, 200, 100)

    # Movements
    UP = 1
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
        
        # Path planning
        self.path = []
        self.dijkstra = Dijkstra(self.world.map, self.world.legend)
        
        self.draw_world()
        
        
    def draw_world(self):
        
        px, py = self.world.player.position
        
        # Drawing
        self.screen.fill(self.WALL_COLOR)
        for row in range(self.world.maze_size):
            for col in range(self.world.maze_size):
                
                rect = pygame.Rect(col*self.world.block_size, row*self.world.block_size, self.world.block_size, self.world.block_size)
                if [col, row] in self.path:
                    if [col, row] not in self.world.water:
                        pygame.draw.rect(self.screen, self.PATH_COLOR, rect)
                    else:
                        pygame.draw.rect(self.screen, self.PATH_WATER_COLOR, rect)
                elif [col, row] in self.world.walls:
                    pygame.draw.rect(self.screen, self.WALL_COLOR, rect)
                elif [col, row] in self.world.water:
                    pygame.draw.rect(self.screen, self.WATER_COLOR, rect)            
                else:
                    pygame.draw.rect(self.screen, self.GROUND_COLOR, rect)
                if [col, row] == [px, py]:
                    pygame.draw.rect(self.screen, self.PLAYER_COLOR, rect)
                elif [col, row] in self.world.treasures:
                    if [col, row] not in self.path:
                        pygame.draw.rect(self.screen, self.GROUND_COLOR, rect)
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
        
    
    def move_randomly(self) -> int:     
        #      Front
        # Left   0   Right
        #      Back
        
        move = random.randint(1, 4)
        
        player_pos = self.world.player.position
        if move == self.UP:
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
    
    
    def move_to(self, pos) -> int:
        
        movement = 0
        
        if self.world.can_move_to(pos):
            
            x, y = self.world.player.position
            if pos[1] == y + 1:
                movement = self.UP
            elif pos[1] == y - 1:
                movement = self.BACK
            elif pos[0] == x + 1:
                movement = self.RIGHT
            elif pos[0] == x - 1:
                movement = self.LEFT
            
            self.world.player.position = pos
            
        return movement
    
    
    def get_closest_treasure(self) -> list:
        
        x_player, y_player = self.world.player.position
        x_closest, y_closest = self.world.treasures[0]
        d1 = ((x_closest - x_player)**2 + (y_closest - y_player)**2)**0.5
        
        for n in range(1, len(self.world.treasures)):
            x, y = self.world.treasures[n]
            d2 = ((x - x_player)**2 + (y - y_player)**2)**0.5
            if d2 < d1:
                x_closest, y_closest = self.world.treasures[n]
                d1 = d2
            
        return [x_closest, y_closest]
        
    
    def calculate_path(self):
         
        player_pos = self.world.player.position
        
        self.path = self.dijkstra.shortest_path(player_pos, self.world.treasures)
    
    
    def game_loop(self):
        
        while(self.running):
            
            self.calculate_path()
            
            while (len(self.path) > 0):
            
                print(f"Step: {self.steps}")
                print(f"Score: {self.score}")
                
                target = self.path.pop(0)
                move = self.move_to(target)
                
                if move != 0:
                    print(f"Movement: {move}")
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
                
                self.draw_world()
                pygame.display.flip()
                pygame.time.wait(100)  # Slow down the game a bit 
        
        print(f" ")
        print(f"Step: {self.steps}")
        print(f"Score: {self.score}")
        print(f" ")
        
        found_treasures = self.world.num_treasures - len(self.world.treasures)
        print(f"Found {found_treasures} treasures")
        print(f"Final score: {self.score}")
        pygame.quit()


if __name__ == "__main__":
    
    maze = Maze()
    
    maze.game_loop()