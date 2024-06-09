from abc import ABC, abstractmethod
import pygame

from world import World

class AbsNode(ABC):
    
    def __init__(self):
        
        self.parent: AbsNode = None
        self.index: list = None


class PathPlanning(ABC):
    
    EXPANDED_NODE_COLOR = (255, 192, 203)
    
    def __init__(self, world: World) -> None:
        self.world = world
        self.matrix = self.world.map
        self.legend: dict = self.world.legend
        self.nodes = []
        self.queue = []
        
        self.up_limit = 0
        self.down_limit = len(self.matrix) - 1
        self.left_limit = 0
        self.right_limit = len(self.matrix[0]) - 1
        self.nodes_count = 0
        
        """
        Limits:
            Up -> index 0
            Left -> index 0
            Down -> index (size - 1)
            Right -> index (size[0] - 1)
        
                      Up  
                --------------
                |            |
                |            |
          Left  |   Matrix   | Right
                |            |
                |            |
                --------------
                     Down
        """
    def draw_expansion(self):
        self.world.draw_world()
        player_x, player_y = self.world.player.position
        
        for row in range(self.world.maze_size):
            for col in range(self.world.maze_size):
                rect = pygame.Rect(col*self.world.block_size, row*self.world.block_size, self.world.block_size, self.world.block_size)
                if self.nodes[col][row] is not None and (col != player_x or row != player_y):
                    pygame.draw.rect(self.world.screen, self.EXPANDED_NODE_COLOR, rect)
        
    
    def expand(self, current_node_pos: list, expanded_node_pos: list, target_position: list):
        x1, y1 = current_node_pos
        x2, y2 = expanded_node_pos

        current_node: AbsNode = self.nodes[x1][y1]
        expanded_node: AbsNode = self.nodes[x2][y2]

        expanded_node.parent = current_node
        expanded_node.parent.index = current_node_pos
        self.update_cost(expanded_node, expanded_node_pos, target_position)

        self.queue.append(expanded_node_pos)
        self.sort_queue()
        
        # Pygame
        self.draw_expansion()
        pygame.display.flip()
        pygame.time.wait(20)  # Slow down the game a bit 
    
    
    @abstractmethod
    def sort_queue(self):
        pass
    
    @abstractmethod
    def update_cost(self, node, node_index, target_position):
        pass
    
    @abstractmethod
    def shortest_path(self, start, target):
        pass
    
    def reconstruct_path(self, start_pos: list, final_pos: list, final_node: AbsNode) -> list:
        """
        
        Retrace the path taken by the path planning algorithm
        
        """
        
        path = []
        
        current_node = final_node.parent
        while current_node.index != start_pos:  
            parent_index = current_node.index
            path.append(parent_index)
            current_node = current_node.parent
        
        path = path[::-1]
        path.append(final_pos)
        
        return path