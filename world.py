import pygame
import random

class Player():
    
    def __init__(self) -> None:
        self.position = [.0, .0]

class World():
    
    def __init__(self) -> None:
                
        # World measurements
        self.width = 800
        self.height = 800
        self.maze_size = 20
        self.block_size = self.width // self.maze_size
        
        # Game objects
        self.num_treasures = 12
        
        # Generating world
        self.generate_player()
        self.generate_treasures()
        self.generate_water()
        self.generate_walls()
    
    
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
    
    def generate_water(self):
        
        self.water = []
    
        water_size = min(self.maze_size, self.maze_size) // 2
        start_x = random.randint(0, self.maze_size - water_size)
        start_y = random.randint(0, self.maze_size - water_size)

        # Fill the square with water
        for i in range(start_x, start_x + water_size // 2):
            for j in range(start_y, start_y + water_size):
                self.water.append([i, j])
                
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