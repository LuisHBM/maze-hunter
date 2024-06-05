from abc import ABC, abstractmethod

class AbsNode(ABC):
    
    def __init__(self):
        
        self.parent: AbsNode = None
        self.index: list = None
        self.has_expanded: bool = False


class PathPlanning(ABC):
    
    def __init__(self, matrix: list[list], legend: dict) -> None:
        self.matrix = matrix
        self.legend: dict = legend
        self.nodes = []
        self.queue = []
        
        self.up_limit = 0
        self.down_limit = len(self.matrix) - 1
        self.left_limit = 0
        self.right_limit = len(self.matrix[0]) - 1
        
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
    
    def expand(self, current_node_pos: list, expanded_node_pos: list):
        x1, y1 = current_node_pos
        x2, y2 = expanded_node_pos

        current_node: AbsNode = self.nodes[x1][y1]
        expanded_node: AbsNode = self.nodes[x2][y2]

        expanded_node.parent = current_node
        expanded_node.parent.index = current_node_pos
        expanded_node.has_expanded = True
        self.update_cost(expanded_node, expanded_node_pos)

        self.queue.append(expanded_node_pos)
        self.sort_queue()
    
    
    @abstractmethod
    def sort_queue(self):
        pass
    
    @abstractmethod
    def update_cost(self, node, node_index, target_position=None):
        pass
    
    @abstractmethod
    def shortest_path(self, start, target):
        pass
    
    def reconstruct_path(self, start_pos: list, final_pos: list, current_node: AbsNode) -> list:
        """
        
        Retrace the path taken by the path planning algorithm
        
        """
        
        path = []
        
        while current_node != start_pos:
            x, y = current_node
            current_node_object = self.nodes[x][y]
            
            parent_index = current_node_object.parent.index
            path.append(parent_index)
            current_node = parent_index
        
        path = path[::-1]
        path.append(final_pos)
        
        return path