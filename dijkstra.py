class Node():
    
    def __init__(self):
        
        self.parent: Node = None
        self.parentIndex: list = None
        self.cost: int = 0
        self.has_expanded: bool = False


class Dijkstra():
    
    def __init__(self, matrix) -> None:
        self.matrix = matrix
        self.fila = []
        
        self.lim_cima = 0
        self.lim_baixo = len(self.matrix[0]) - 1
        self.lim_esq = 0
        self.lim_dir = len(self.matrix[0]) - 1
    
    
    def expandir(self, matrix: list, nodeAtualPos: list, nodeExpandidoPos: list):
        nodeAtual: Node = matrix[nodeAtualPos[0]][nodeAtualPos[1]]
        nodeExpandido: Node = matrix[nodeExpandidoPos[0]][nodeExpandidoPos[1]]


        nodeExpandido.parent = nodeAtual
        nodeExpandido.parentIndex = nodeAtualPos
        nodeExpandido.cost = nodeExpandido.parent.cost + 1
        nodeExpandido.has_expanded = True

        self.fila.append(nodeExpandidoPos)


    def shortest_path(self, start: list, target: list):
        
        self.fila = []

        nodes = [[Node() for _ in range(len(self.matrix))] for _ in range(len(self.matrix))]
        nodes[start[0]][start[1]].has_expanded = True
        
        nodeAtual = start
        

        while nodeAtual != target:
            
            linhaAtual = nodeAtual[0]
            colunaAtual = nodeAtual[1]

            #cima
            cima = [linhaAtual - 1, colunaAtual]
            linhaCima = cima[0]
            colunaCima = cima[1]
            if (linhaCima >= self.lim_cima) and self.matrix[linhaCima][colunaCima] != 1 and nodes[linhaCima][colunaCima].has_expanded == False:
                self.expandir(nodes, nodeAtual, cima)

            #esquerda
            esquerda = [linhaAtual, colunaAtual - 1]
            linhaEsquerda = esquerda[0]
            colunaEsquerda = esquerda[1]
            if (colunaEsquerda >= self.lim_esq) and self.matrix[linhaEsquerda][colunaEsquerda] != 1 and nodes[linhaEsquerda][colunaEsquerda].has_expanded == False:
                self.expandir(nodes, nodeAtual, esquerda)

            #baixo
            baixo = [linhaAtual + 1, colunaAtual]
            linhaBaixo = baixo[0]
            colunaBaixo = baixo[1]
            if (linhaBaixo <= self.lim_baixo) and self.matrix[linhaBaixo][colunaBaixo] != 1 and nodes[linhaBaixo][colunaBaixo].has_expanded == False:
                self.expandir(nodes, nodeAtual, baixo)

            #direita
            direita = [linhaAtual, colunaAtual + 1]
            linhaDireita = direita[0]
            colunaDireita = direita[1]
            if (colunaDireita <= self.lim_dir) and self.matrix[linhaDireita][colunaDireita] != 1 and nodes[linhaDireita][colunaDireita].has_expanded == False:
                self.expandir(nodes, nodeAtual, direita)

            if len(self.fila) > 0:
                nodeAtual = self.fila.pop(0)

        shortest_path = []
        while nodeAtual != start:
            nodeAtualObj = nodes[nodeAtual[0]][nodeAtual[1]]
            parentIndex = nodeAtualObj.parentIndex
            shortest_path.append(parentIndex)
            nodeAtual = parentIndex
        
        shortest_path = shortest_path[::-1]
        shortest_path.append(target)
        
        return shortest_path