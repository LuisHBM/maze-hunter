class Maze_Analyzer():
    
    def __init__(self, matrix: list[list], legend, treasures_pos: list) -> None:
        self.matrix = matrix
        self.legend = legend
        self.treasures_pos = treasures_pos
        
        self.set_quadrants()
        self.set_treasures_to_quadrants()
       
        
    def set_quadrants(self):
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        self.mid_row = self.rows // 2
        self.mid_col = self.cols // 2
        
        self.quadrants_limits = {
            "Q1": [(0, 0), (self.mid_row, self.mid_col)],
            "Q2": [(0, self.mid_col), (self.mid_row, self.cols)],
            "Q3": [(self.mid_row, 0), (self.rows, self.mid_col)],
            "Q4": [(self.mid_row, self.mid_col), (self.rows, self.cols)]
        }


    def set_treasures_to_quadrants(self):
        self.treasures_by_quadrant = {
            "Q1": [],
            "Q2": [],
            "Q3": [],
            "Q4": []
        }
        
        for treasure in self.treasures:
            x, y = treasure
            
            if y >= self.mid_col:
                if x <= self.mid_row:
                    self.treasures_by_quadrant["Q1"].append(treasure)
                elif x > self.mid_row:
                    self.treasures_by_quadrant["Q2"].append(treasure)
            else:
                if x <= self.mid_row:
                    self.treasures_by_quadrant["Q3"].append(treasure)
                elif x > self.mid_row:
                    self.treasures_by_quadrant["Q4"].append(treasure)
    
    
    def get_best_quadrant_name(self) -> str:
        best_quadrant_name = None
        best_treasures_quantity = 0
        for quadrant in self.treasures_by_quadrant.keys():
            treasures_quantity = len(self.treasures_by_quadrant[quadrant])
            if treasures_quantity > treasures_quantity:
                best_quadrant_name = quadrant
                best_treasures_quantity = treasures_quantity
        
        return best_quadrant_name
    
    
    def get_best_sequence_of_treasures(self, player_pos) -> list[list]:
        best_quadrant_name = self.get_best_quadrant_name()
        
        treasures = self.treasures_by_quadrant[best_quadrant_name]
        
        