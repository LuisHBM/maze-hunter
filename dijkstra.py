from pathplanning import AbsNode, PathPlanning
from world import World

class Node(AbsNode):
    
    def __init__(self):
        super().__init__()
        self.g_cost = 0

class Dijkstra(PathPlanning):
    
    def __init__(self, world: World) -> None:
        super().__init__(world)
    
    
    def update_cost(self, node: Node, node_index: list, target_position: list):
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
        self.nodes = [[None for _ in range(len(self.matrix))] for _ in range(len(self.matrix))]
        self.nodes[start[0]][start[1]] = Node()

        current_node = start
        target_reached = start

        while True:
            
            current_row = current_node[0]
            current_column = current_node[1]
            
            """
        
            Expanding nodes
            
            """
            
            # Expands to up ====================================    
            
            up = [current_row - 1, current_column]
            row_up, column_up = up
            
            if (row_up >= self.up_limit) and self.matrix[row_up][column_up] != self.legend["WALL"] and self.nodes[row_up][column_up] == None:
                self.nodes[row_up][column_up] = Node()
                target_reached = [row_up, column_up] if [row_up, column_up] in targets else None
                self.expand(current_node, up, None)
                
                if target_reached:
                    break         
            
            # Expands to left ====================================  
            
            left = [current_row, current_column - 1]
            row_left, column_left = left
            
            if (column_left >= self.left_limit) and self.matrix[row_left][column_left] != self.legend["WALL"] and self.nodes[row_left][column_left] == None:
                self.nodes[row_left][column_left] = Node()
                target_reached = [row_left, column_left] if [row_left, column_left] in targets else None
                self.expand(current_node, left, None)
                
                if target_reached:
                    break
            
            # Expands to down ====================================  
            
            down = [current_row + 1, current_column]
            row_down, column_down = down
            
            if (row_down <= self.down_limit) and self.matrix[row_down][column_down] != self.legend["WALL"] and self.nodes[row_down][column_down] == None:
                self.nodes[row_down][column_down] = Node()
                target_reached = [row_down, column_down] if [row_down, column_down] in targets else None
                self.expand(current_node, down, None)
                
                if target_reached:
                    break

            # Expands to right ====================================  
            
            right = [current_row, current_column + 1]
            row_right, column_right = right
            
            if (column_right <= self.right_limit) and self.matrix[row_right][column_right] != self.legend["WALL"] and self.nodes[row_right][column_right] == None:
                self.nodes[row_right][column_right] = Node()
                target_reached = [row_right, column_right] if [row_right, column_right] in targets else None
                self.expand(current_node, right, None)
                
                if target_reached:
                    break
            
            # Gets next node position to expand

            if len(self.queue) > 0:
                current_node = self.queue.pop(0)
        
        x, y = target_reached
        return self.reconstruct_path(start, target_reached, self.nodes[x][y])