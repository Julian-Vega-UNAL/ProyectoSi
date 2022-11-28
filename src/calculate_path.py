import os
from generate_field import get_field
import heapq

player = None
#------------------------------------------------------------------
class Node():
    def __init__(self, position, g, h, parent):
        self.parent = parent
        self.position = position

        self.g = g
        self.h = h
        self.f = g + h
    
    def __lt__(self, other):
        return self.f < other.f

class Target():
    def __init__(self, position, type):
        self.position = position
        self.type = type
    
    def get_type(self):
        return self.type

class Player(Target):
    def __init__(self, position, diamonds_to_catch, keys_to_catch):
        super().__init__(position, "P")
        self.diamonds_to_catch = diamonds_to_catch
        self.keys_to_catch = keys_to_catch
        self.key = False
    
    def catch_key(self):
        self.key = True
        self.keys_to_catch -= 1
    
    def open_door(self):
        self.key = False
    
    def catch_diamond(self):
        self.diamonds_to_catch -= 1
    
    def has_all_diamonds(self):
        return self.diamonds_to_catch == 0
    
    def has_key(self):
        return self.key
    
    def set_total_diamonds(self, diamonds_amount):
        self.diamonds_to_catch = diamonds_amount

    def set_total_keys(self, keys_amount):
        self.keys_to_catch = keys_amount

#------------------------------------------------------------------
def heuristic(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def get_path(node):
    path = []
    while node is not None:  
        path.append(node.position)
        node = node.parent
    path = path[::-1]

    init_y, init_x = path[0]
    dir_path = []
    for pos_y, pos_x in path:
        if pos_x == init_x + 1:
            dir_path.append("right")
        elif pos_x == init_x - 1:
            dir_path.append("left")
        elif pos_y == init_y + 1:
            dir_path.append("down")
        elif pos_y == init_y -1:
            dir_path.append("up")
        init_x, init_y = pos_x, pos_y
    return dir_path

def get_children(node, end_node, maze):
    global player
    width = len(maze[0])
    height = len(maze)

    children = []
    node_row = node.position[0]
    node_col = node.position[1]
    for new_position in [(0,-1), (-1,0), (0,1), (1,0)]: 
        child_row, child_col = node_row + new_position[0], node_col + new_position[1]

        if child_row > (height -1) or child_row < 0 or child_col > (width - 1) or child_col < 0:
            continue

        #------------------------------------------------------------------
        #CURRENT NODE'S CHILDREN LOGIC
        child = maze[child_row][child_col]

        if child == "M":
            continue

        if child == "S" and player != None and not player.has_all_diamonds():
            continue

        if child == "PLL" and player != None and not player.has_key():
            continue

        #------------------------------------------------------------------

        child_pos = child_row, child_col 
        child = Node(child_pos, node.g, heuristic(child_pos, end_node.position), node)

        children.append(child)
    
    return children

def astar(maze, start, end):
    global player
    start_node = Node(start, 0, heuristic(start, end), None)
    end_node = Node(end, 0, 0, None)

    open_list = []
    closed_list = set()

    heapq.heappush(open_list, start_node)

    while len(open_list) > 0:
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node)

        current_row = current_node.position[0]
        current_col = current_node.position[1]

        current_type = maze[current_row][current_col]

        #------------------------------------------------------------------
        #CURRENT NODE IN PATH LOGIC

        if current_node.position == end_node.position:
            return get_path(current_node)
        
        if current_type == "PI":
            maze[current_row][current_col] = "M"
        
        if (current_type == "D" or current_type == "PLL" or (current_type == "LL" and player != None and not player.has_key())) and current_node.position != end_node.position:
            #print("Nuevo objetivo encontrado!", current_node.position)
            return current_node
        
        #------------------------------------------------------------------

        children = get_children(current_node, end_node, maze)
        
        for child in children:
            is_closed = False
            for closed in closed_list:
                if child.position == closed.position:
                    is_closed = True 
                    break
            if is_closed: continue

            child.g = current_node.g + 1
            child.h = heuristic(child.position, end_node.position)
            child.f = child.g + child.h
            child.parent = current_node

            condition = False
            for open_node in open_list:
                if child.position == open_node.position and child.g > open_node.g:
                    condition = True
                    break
            if condition: continue

            heapq.heappush(open_list, child)
    return None

#------------------------------------------------------------------
def get_targets(field, types):
    target_list = []
    for i in range(len(field)-1, -1, -1):
        row = field[i]
        for j in range(len(row)):
            elem = row[j]
            if elem in types:
                if elem == "P":
                    target = Player((i,j), 0, 0)
                else:
                    target = Target((i,j), elem)
                target_list.append(target)
    return target_list

def build_adj_matrix(nodes): #### Matriz adyacente
    total_nodes = len(nodes)
    matrix = [] #total_nodes^2 #### Toma la distancia de los nodos y se pone en la matriz

    for i in range(total_nodes):
        row = []
        for j in range(0, total_nodes):
            distance = heuristic(nodes[j].position, nodes[i].position)
            distance = distance if distance > 0 else 100
            row.append(distance)
        matrix.append(row)
    
    return matrix

def get_final_path(maze, init_target, init_idx):
    global player
    global nodes_list
    global adj_matrix

    iter = 0
    current_idx = init_idx
    current_target = init_target 
    path = []
    while iter < len(nodes_list) -1: 
        #Get next target as the closest target to the current
        current_target_adj_array = adj_matrix[current_idx].copy()
        min_dst = min(current_target_adj_array)
        next_target_idx = current_target_adj_array.index(min_dst)
        next_target = nodes_list[next_target_idx]

        while next_target.type == "LL" and player != None and player.has_key():
            current_target_adj_array[next_target_idx] = 100

            min_dst = min(current_target_adj_array)
            next_target_idx = current_target_adj_array.index(min_dst)
            next_target = nodes_list[next_target_idx]
 
        #The current target was reached, no need to be aimed from anywhere else
        for i in range(len(adj_matrix)):
            adj_matrix[i][current_idx] = 100
        
        current_target_type = maze[current_target.position[0]][current_target.position[1]]

        #------------------------------------------------------------------
        # CURRENT TARGET LOGIC

        if current_target_type == "D" and player != None:
            player.catch_diamond()

        if current_target_type == "LL" and player != None and not player.has_key():
            player.catch_key()
        
        if current_target_type == "PLL" and player != None and player.has_key():
            player.open_door()

        #------------------------------------------------------------------

        #Find the closest key
        while next_target.type != "LL" and player != None and player.keys_to_catch > 0 and player.has_key() == False:
            current_target_adj_array[next_target_idx] = 100

            min_dst = min(current_target_adj_array)
            next_target_idx = current_target_adj_array.index(min_dst)
            next_target = nodes_list[next_target_idx]

        maze[current_target.position[0]][current_target.position[1]] = 0
        
        current_maze = [row[:] for row in maze] #Copy matrix
        #A* would find another target in the way. Then, returns the node
        path_or_node = astar(current_maze, current_target.position, next_target.position)
        
        #Would reach another new target from another path
        while isinstance(path_or_node, Node): 
            next_target = path_or_node

            #Gets the index of the returned node
            for idx in range(len(nodes_list)):
                aux_node = nodes_list[idx]
                if aux_node.position == next_target.position:
                    next_target_idx = idx
                    break
            current_maze = [row[:] for row in maze] #Copy matrix
            path_or_node = astar(current_maze, current_target.position, next_target.position)

        if path_or_node is None:
            print("PATH NOT FOUND")
            exit()
        
        partial_path = path_or_node
        #print(partial_path)
        path += partial_path

        #Takes the next target as the new initial point.
        current_target = next_target
        current_idx = next_target_idx
        maze = current_maze
        iter += 1
    return path

#------------------------------------------------------------------

### Estrategia para rocas:
### guardar en una lista / diccionario adicional los Huecos u rocas, junto a posiciones (Linea 170)
### Calcular distancias y ordenar tal que se Asigne a un hueco la roca mas cercana #Funcion assign_rock 
### Inicializar lista nodos de solo roca y hueco 
### Usar Find path or A* para encontrar camino desde roca a hueco (creando un path parcial que resuelve la roca)
### Dependiendo de la primera direccion del path parcial adjuntar un step extra al inicio para saber donde colocar el monito (Guardar esta posicion como objetivo) 
### Crear sub funcion swing: si la direccion siguiente NO es igual a la anterior, mover el monito alrededor de la roca hasta que sea la direccion que se quiera (Left Up) 
### Crear objetivos en el field Liean 247
### agregar al partial path el camino de la roca Linea 242
### De esa manera el monito recoje todo, va a la posicion inicial para resolver la roca, ejecuta los pasos de la roca, y luego vuelve a hacer el algoritmo ya hecho
### Esto deberia hacer el Nivel 4 y 5

field = get_field()
#os.system("clear")
######
### Funcion obtener roca
###
types = ["S", "D", "P", "PLL", "LL"]
nodes_list = get_targets(field, types)
adj_matrix = build_adj_matrix(nodes_list)

total_diamonds = 0
total_keys = 0
player_idx = -1
for node in nodes_list:
    if node.get_type() == "D":
        total_diamonds += 1
    elif node.get_type() == "LL":
        total_keys += 1
    elif node.get_type() == "P":
        player = node

if player != None:
    player.set_total_diamonds(total_diamonds)
    player.set_total_keys(total_keys)
    player_idx = nodes_list.index(player)
    final_path = get_final_path(field, player, player_idx)
    #print(final_path)