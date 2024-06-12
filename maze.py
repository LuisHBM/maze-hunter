# Extenal libraries
import pygame
import random
import os
import copy

# Internal libraries
from world import World
from dijkstra import Dijkstra
from astar import AStar

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


def write_num_of_nodes(numero, nome_arquivo):
    """
    Escreve um número float em uma nova linha em um arquivo.

    Args:
    numero (float): O número float a ser escrito no arquivo.
    nome_arquivo (str): Nome do arquivo onde o float será escrito.
    """
    try:
        with open(nome_arquivo, 'a') as arquivo:  # Use 'a' para abrir o arquivo em modo de anexação
            arquivo.write(f"{numero}\n")
        print(f"O float {numero} foi escrito no arquivo {nome_arquivo} com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao escrever no arquivo: {e}")

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
    
    def __init__(self, maze_seed: int) -> None:
        
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
    
    
    def filtered_treasures(self) -> list:
        
        filtered_treasures = []
        
        for treasure_pos in self.world.treasures:
            x, y = treasure_pos
            is_stuck = self.world.map[x-1][y] == self.world.legend["WALL"] if x-1 >= 0 else True
            is_stuck = is_stuck and (self.world.map[x+1][y] == self.world.legend["WALL"] if x+1 < self.world.maze_size  else True)
            is_stuck = is_stuck and (self.world.map[x][y-1] == self.world.legend["WALL"] if y-1 >= 0 else True)
            is_stuck = is_stuck and (self.world.map[x][y+1] == self.world.legend["WALL"] if y+1 < 0 else True)
            
            if not is_stuck:
                filtered_treasures.append(treasure_pos)
        
        return filtered_treasures             
    
    def calculate_path(self, target:float):
         
        player_pos = self.world.player.position
        
        if self.mode == self.ASTAR:
            self.path = self.astar.shortest_path(player_pos, target)
        elif self.mode == self.DIJKSTRA:
            self.path = self.dijkstra.shortest_path(player_pos, [target])
    
    
    def game_loop(self):

        while(self.running):
            
            self.world.draw_world(self.path)
            pygame.display.flip()
            
            self.calculate_path(self.world.treasures[0])
            
            while (len(self.path) > 0):
            
                #print(f"Step: {self.steps}")
                #print(f"Score: {self.score}")
                
                target = self.path.pop(0)
                move = self.move_to(target)
                
                if move != 0:
                    #print(f"Movement: {move}")
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
                pygame.time.wait(100)  # Slow down the game a bit 
            
            if (self.mode == self.DIJKSTRA):
                write_num_of_nodes(self.dijkstra.nodes_count, "dijkstra_nodes.txt")
                self.dijkstra.nodes_count = 0
            elif (self.mode == self.ASTAR):
                write_num_of_nodes(self.astar.nodes_count, "astar_nodes.txt")
                self.astar.nodes_count = 0
        
        #print(f"Step: {self.steps}")
        #print(f"Score: {self.score}")
        #print("")
        
        found_treasures = self.world.num_treasures - len(self.world.treasures)
        print(f"Found {found_treasures} treasures")
        print(f"Final score: {self.score}")


if __name__ == "__main__":
    
    for _ in range(0, 50):
        seed = 500
        maze = Maze(seed)
        
        random.seed(None)
        random.shuffle(maze.world.treasures)
        
        treasures = copy.deepcopy(maze.world.treasures)
        maze.mode = Maze.DIJKSTRA
        maze.game_loop()
        
        maze = Maze(seed)
        maze.world.treasures = treasures
        maze.mode = Maze.ASTAR
        maze.game_loop()
        
    pygame.quit()