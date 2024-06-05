class Node():
    
    def __init__(self):
        
        self.parent: Node = None
        self.parent_index: list = None
        self.cost: int = 0
        self.has_expanded: bool = False


class Dijkstra():
    
    def __init__(self, matrix: list[list], legend: dict) -> None:
        self.matrix = matrix
        self.legend: dict = legend
        self.nodes = []
        self.queue = []
        
        self.up_limit = 0
        self.down_limit = len(self.matrix[0]) - 1
        self.left_limit = 0
        self.right_limit = len(self.matrix[0]) - 1
    
    
    def sort_queue(self):
        size = len(self.queue)
        
        for i in range(0, size):
            for j in range(i+1, size):
                x1, y1 = self.queue[j]
                x2, y2 = self.queue[i]
                if self.nodes[x1][y1].cost < self.nodes[x2][y2].cost:
                    self.queue[j], self.queue[i] =  self.queue[i], self.queue[j]
    
    
    def expand(self, current_node_pos: list, expanded_node_pos: list):
        x1, y1 = current_node_pos
        x2, y2 = expanded_node_pos

        current_node: Node = self.nodes[x1][y1]
        expanded_node: Node = self.nodes[x2][y2]

        expanded_node.parent = current_node
        expanded_node.parent_index = current_node_pos
        expanded_node.cost = expanded_node.parent.cost + (1 if self.matrix[x2][y2] == self.legend["EMPTY"] else 5) 
        expanded_node.has_expanded = True

        self.queue.append(expanded_node_pos)
        self.sort_queue()


    def shortest_path(self, start: list, targets: list):
        
        self.queue = []

        # Initializing nodes
        self.nodes = [[Node() for _ in range(len(self.matrix))] for _ in range(len(self.matrix))]
        self.nodes[start[0]][start[1]].has_expanded = True
        
        current_node = start
        target_reached = start

        while True:
            
            if current_node in targets:
                target_reached = current_node
                break
            
            current_line = current_node[0]
            current_column = current_node[1]
            
            """
        
            Expanding nodes
            
            """

            # Expands to up
            up = [current_line - 1, current_column]
            line_up = up[0]
            column_up = up[1]
            if (line_up >= self.up_limit) and self.matrix[line_up][column_up] != 1 and self.nodes[line_up][column_up].has_expanded == False:
                self.expand(current_node, up)

            # Expands to left
            left = [current_line, current_column - 1]
            line_left = left[0]
            column_left = left[1]
            if (column_left >= self.left_limit) and self.matrix[line_left][column_left] != 1 and self.nodes[line_left][column_left].has_expanded == False:
                self.expand(current_node, left)

            # Expands to down
            down = [current_line + 1, current_column]
            line_down = down[0]
            column_down = down[1]
            if (line_down <= self.down_limit) and self.matrix[line_down][column_down] != 1 and self.nodes[line_down][column_down].has_expanded == False:
                self.expand(current_node, down)

            # Expands to right
            right = [current_line, current_column + 1]
            line_right = right[0]
            column_right = right[1]
            if (column_right <= self.right_limit) and self.matrix[line_right][column_right] != 1 and self.nodes[line_right][column_right].has_expanded == False:
                self.expand(current_node, right)

            if len(self.queue) > 0:
                current_node = self.queue.pop(0)

        """
        
        Retrace the path taken by Dijkstra
        
        """
        
        shortest_path = []
        while current_node != start:
            current_node_object = self.nodes[current_node[0]][current_node[1]]
            parent_index = current_node_object.parent_index
            shortest_path.append(parent_index)
            current_node = parent_index
        
        shortest_path = shortest_path[::-1]
        shortest_path.append(target_reached)
        
        return shortest_path