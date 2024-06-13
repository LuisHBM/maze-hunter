# Extenal libraries
import pygame
import random
import sys
import os

# Internal libraries
from world import World
from dijkstra import Dijkstra
from astar import AStar

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Maze():
    
    # Movements
    UP = 1
    BACK  = 2
    LEFT  = 3
    RIGHT = 4
    
    # Modes
    NONE = 0
    DIJKSTRA = 1
    ASTAR = 2
    
    def __init__(self, maze_seed: int=None) -> None:
        
        self.world = World(maze_seed)
        self.running = True
        self.score = 0
        self.steps = 0
        
        # Path planning
        self.path = []
        self.dijkstra = Dijkstra(self.world)
        self.astar = AStar(self.world)
        
        self.world.draw_world()
        
        self.mode = 0
    
    
    def print_score(self):
        print(f"Step: {self.steps}")
        print(f"Score: {self.score}")
  
                    
    def update_score(self):
        
        px, py = self.world.player.position
        
        self.score -= 1

        if [px, py] in self.world.treasures:
            self.world.treasures.remove([px, py])
            print("Treasure found! Treasures left:", len(self.world.treasures))
            self.score += 50
            self.print_score()
            
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
    
    
    def get_best_treasure(self) -> list:
        
        treasures = self.world.get_treasures_out_of_water()
        
        if len(treasures) < 1:
            treasures = self.world.treasures
        
        closest_treasure = []
        lowest_distance = sys.maxsize
        player_pos = self.world.player.position
        
        for treasure in treasures:
            x_t, y_t = treasure
            x_p, y_p = player_pos
            
            d = ((x_t - x_p)**2 + (y_t - y_p)**2)**0.5
            if d < lowest_distance:
                closest_treasure = treasure
                lowest_distance = d
        
        return closest_treasure
            
            
    def calculate_path(self):
         
        player_pos = self.world.player.position
        
        if self.mode == self.ASTAR:
            self.path = self.astar.shortest_path(player_pos, self.get_best_treasure())
        elif self.mode == self.DIJKSTRA:
            self.path = self.dijkstra.shortest_path(player_pos, self.world.treasures)
    
    
    def game_loop(self):

        while(self.running):
            
            self.world.draw_world(self.path)
            pygame.display.flip()
            
            # Calls path finding functions
            self.calculate_path()
            
            while (len(self.path) > 0):
                
                target = self.path.pop(0)
                move = self.move_to(target)
                
                if move != 0:
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
                
                self.world.draw_world(self.path)
                pygame.display.flip()
                pygame.time.wait(100)
        
        found_treasures = self.world.num_treasures - len(self.world.treasures)
        print(f"Found {found_treasures} treasures")
        print(f"Final score: {self.score}")
        print(f"Steps: {self.steps}")
        
        pygame.quit()


if __name__ == "__main__":
    
    os.system("clear")
    
    mode = int(sys.argv[1])
    
    print("Chosen mode: ", end="")
    if(mode == Maze.ASTAR):
        print("Astar")
    elif(mode == Maze.DIJKSTRA):
        print("Dijkstra")
    else:
        print("None")
    print("")
    
    maze = Maze()
    maze.mode = mode
    maze.game_loop()