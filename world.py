import pygame
import random

class Player():
    
    def __init__(self) -> None:
        self.position = [.0, .0]

class World():
    
        
    # Colors
    WALL_COLOR = (0, 0, 0)
    GROUND_COLOR = (255, 255, 255)
    PLAYER_COLOR = (255, 0, 0)
    WATER_COLOR = (0, 0, 255)
    PATH_COLOR = (0, 255, 0)
    PATH_WATER_COLOR = (0, 200, 100)
    
    def __init__(self, seed=0) -> None:
                
        # World measurements
        self.width = 800
        self.height = 800
        self.maze_size = 20
        self.block_size = self.width // self.maze_size
        random.seed(seed)
        
        # Game objects
        self.num_treasures = 12
        
        # Matrix for path planning
        self.legend = {
            "EMPTY": 0,
            "WALL": 1,
            "WATER": 2
        }
        self.map = [[self.legend["EMPTY"] for _ in range(self.maze_size)] for _ in range(self.maze_size)]
        
        # Generating world
        self.generate_player()
        self.generate_treasures()
        self.generate_water()
        self.generate_walls()
        
        # Pygame 
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Maze Treasure Hunt')
    
    
    def generate_treasures(self):
        
        # Load treasure image
        treasure_image = pygame.image.load('treasure.png')
        self.treasure_image = pygame.transform.scale(treasure_image, (self.block_size, self.block_size))

        # Generating treasures
        self.treasures = []
        for _ in range(self.num_treasures):  # Number of treasures
            while True:
                treasure = [random.randint(0, self.maze_size-1), random.randint(0, self.maze_size-1)]
                if treasure not in self.treasures and treasure != self.player.position:
                    self.treasures.append(treasure)
                    break
    
    def generate_player(self):
        
        self.player = Player()
        self.player.position = [random.randint(0, self.maze_size-1), random.randint(0, self.maze_size-1)]
        
    def generate_walls(self):
        
        # Generating walls and obstacles dynamically
        self.walls = []
        
        for i in range(1, self.maze_size-1):  # Avoid placing walls on the border
            for j in range(1, self.maze_size-1):
                if [i,j] != self.player.position \
                and [i,j] not in self.treasures \
                and random.choice([True, False, False]):  
                    self.walls.append([i, j])
                    self.map[i][j] = self.legend["WALL"]
        
    def generate_water(self):
        
        self.water = []
    
        water_size = min(self.maze_size, self.maze_size) // 2
        start_x = random.randint(0, self.maze_size - water_size)
        start_y = random.randint(0, self.maze_size - water_size)

        # Fill the square with water
        for i in range(start_x, start_x + water_size // 2):
            for j in range(start_y, start_y + water_size):
                self.water.append([i, j])
                self.map[i][j] = self.legend["WATER"]
    
    
    def draw_world(self, path=None):
        px, py = self.player.position
        
        # Drawing
        self.screen.fill(self.WALL_COLOR)
        for row in range(self.maze_size):
            for col in range(self.maze_size):
                
                rect = pygame.Rect(col*self.block_size, row*self.block_size, self.block_size, self.block_size)
                if path is not None and [col, row] in path:
                    if [col, row] not in self.water:
                        pygame.draw.rect(self.screen, self.PATH_COLOR, rect)
                    else:
                        pygame.draw.rect(self.screen, self.PATH_WATER_COLOR, rect)
                elif [col, row] in self.walls:
                    pygame.draw.rect(self.screen, self.WALL_COLOR, rect)
                elif [col, row] in self.water:
                    pygame.draw.rect(self.screen, self.WATER_COLOR, rect)            
                else:
                    pygame.draw.rect(self.screen, self.GROUND_COLOR, rect)
                if [col, row] == [px, py]:
                    pygame.draw.rect(self.screen, self.PLAYER_COLOR, rect)
                if [col, row] in self.treasures:
                    self.screen.blit(self.treasure_image, (col*self.block_size, row*self.block_size))
                
    def can_move_to(self, position) -> bool:
        
        # Checks if the movement is more than 1 block
        if abs(position[0] - self.player.position[0]) > 1 or abs(position[1] - self.player.position[1]) > 1:
            return False
        
        # Checks if there is a wall or is out of the world
        if [position[0], position[1]] not in self.walls \
        and 0 <= position[0] < self.maze_size \
        and 0 <= position[1] < self.maze_size:
            return True
        else:
            return False