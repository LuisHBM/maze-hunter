from pathplanning import AbsNode, PathPlanning

class Node(AbsNode):
    
    def __init__(self):
        super().__init__()
        self.g_cost = 0
        self.h_cost = 0
        
    def get_f_cost(self):
        return (self.g_cost + self.h_cost)

class Astar(PathPlanning):
    
    def __init__(self, matrix: list[list], legend: dict) -> None:
        super().__init__(matrix, legend)

        
    def update_cost(self, node: Node, node_index: list, target_pos: list):
        x, y = node_index
        node.g_cost = node.parent.g_cost + (1 if self.matrix[x][y] == self.legend["EMPTY"] else 5)
        
        """
        Manhattan geometry 
        https://en.wikipedia.org/wiki/Taxicab_geometry
        
        [x1,y1] -> goal
        [x0,y0] -> current position
        
        h(n) = |x1 - x0| + |y1 - y0|
        
        """
        
        x1, y1 = target_pos
        node.h_cost = abs(x1 - x) + abs(y1 - y)
    
    
    def sort_queue(self):
        size = len(self.queue)
        
        for i in range(0, size):
            for j in range(i+1, size):
                
                x1, y1 = self.queue[j]
                x2, y2 = self.queue[i]
                node_j: Node = self.nodes[x1][y1]
                node_i: Node = self.nodes[x2][y2]
                
                swap_nodes = False
                
                
                """
                    A* f cost:
                        f(n) = g(n) + h(n)
                
                    Checks if:
                    1° - Order by f cost.
                    2° - Order by h cost.
                    3° - Order by g cost.
                
                """
                if node_j.get_f_cost() < node_i.get_f_cost():
                    swap_nodes = True
                elif node_j.get_f_cost() == node_i.get_f_cost():
                    if node_j.h_cost < node_i.h_cost:
                        swap_nodes = True
                    elif node_j.h_cost == node_i.h_cost:
                        if node_j.g_cost < node_j.g_cost:
                            swap_nodes = True
                
                if(swap_nodes):
                    self.queue[j], self.queue[i] =  self.queue[i], self.queue[j]
                        

    def shortest_path(self, start: list, targets: list):
        pass