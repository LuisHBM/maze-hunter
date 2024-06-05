from pathplanning import AbsNode, PathPlanning

class Node(AbsNode):
    
    def __init__(self):
        super().__init__()
        self.g_cost = 0

class Dijkstra(PathPlanning):
    
    def __init__(self, matrix: list[list], legend: dict) -> None:
        super().__init__(matrix, legend)
    
    
    def update_cost(self, node: Node, node_index: list, target_position=None):
        x, y = node_index
        node.g_cost = node.parent.g_cost + (1 if self.matrix[x][y] == self.legend["EMPTY"] else 5) 


    def sort_queue(self):
        size = len(self.queue)
        
        for i in range(0, size):
            for j in range(i+1, size):
                
                x1, y1 = self.queue[j]
                x2, y2 = self.queue[i]
                node_j: Node = self.nodes[x1][y1]
                node_i: Node = self.nodes[x2][y2]
                
                if node_j.g_cost < node_i.g_cost:
                    self.queue[j], self.queue[i] =  self.queue[i], self.queue[j]


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
            
            current_row = current_node[0]
            current_column = current_node[1]
            
            """
        
            Expanding nodes
            
            """
            
            # Expands to up ====================================    
            
            up = [current_row - 1, current_column]
            row_up, column_up = up
            
            if (row_up >= self.up_limit) and self.matrix[row_up][column_up] != self.legend["WALL"] and self.nodes[row_up][column_up].has_expanded == False:
                self.expand(current_node, up)
            
            # Expands to left ====================================  
            
            left = [current_row, current_column - 1]
            row_left, column_left = left
            
            if (column_left >= self.left_limit) and self.matrix[row_left][column_left] != self.legend["WALL"] and self.nodes[row_left][column_left].has_expanded == False:
                self.expand(current_node, left)
            
            # Expands to down ====================================  
            
            down = [current_row + 1, current_column]
            row_down, column_down = down
            
            if (row_down <= self.down_limit) and self.matrix[row_down][column_down] != self.legend["WALL"] and self.nodes[row_down][column_down].has_expanded == False:
                self.expand(current_node, down)

            # Expands to right ====================================  
            
            right = [current_row, current_column + 1]
            row_right, column_right = right
            
            if (column_right <= self.right_limit) and self.matrix[row_right][column_right] != self.legend["WALL"] and self.nodes[row_right][column_right].has_expanded == False:
                self.expand(current_node, right)
            
            # Gets next node position to expand

            if len(self.queue) > 0:
                current_node = self.queue.pop(0)
        
        return self.reconstruct_path(start, target_reached, current_node)