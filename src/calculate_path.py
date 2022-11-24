from generate_field import get_field 
import heapq

######## Clases a usar en el algoritmo
class Node(): #Define Nodos, los cales tienen padre e hijo
    def __init__(self, position, g, h, parent):
        self.parent = parent
        self.position = position

        self.g = g
        self.h = h
        self.f = g + h
    
    def __lt__(self, other):
        return self.f < other.f
class Target(): #Define objetivos, tiene posicion, priridad de acuerdo a tipo de tile
    def __init__(self, position, type):
        self.position = position
        self.priority = self.get_priority(type)
        self.type = type
    
    def __lt__(self, other):
        return self.priority < other.priority
    
    def get_priority(self, type):
        priority_dict = {"D": 2, "PLL": 1, "LL": 3, "S": 0, "P": -1}
        return priority_dict[type]
    
    def get_type(self):
        return self.type
class Player(Target): #Clase jugador, el cual tiene posicion y diamantes a caputrar
    def __init__(self, position, diamonds_to_catch):
        super().__init__(position, "P")
        self.diamonds_to_catch = diamonds_to_catch
        self.diamonds = 0
        self.key = False ###### Jugador inicia sin llave
    
    def catch_key(self): # Cuando agarra se vuelve verdadero
        self.key = True
    
    def open_door(self): # cuando abre puerta hace key falso para identificar que se usó la llave
        self.key = False
    
    def catch_diamond(self): #Cuantos diamantes ha agarrado
        self.diamonds += 1
    
    def has_all_diamonds(self): ## Verifica si ha agarrado los diamantes
        return self.diamonds == self.diamonds_to_catch
    
    def has_key(self): # Retorna estado de tener llave
        return self.key
    
    def set_total_diamonds(self, diamonds_amount): ## cuantos diamaantes tiene que agarrar
        self.diamonds_to_catch = diamonds_amount

#------------------------------------------------------------------#### Funciones que componen el algoritmo principal
def heuristic(start, end): ### Heuristica (distancia entre 2 puntos
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def get_path(node): #### Algoritmo de busqueda 
    path = []      #### Lista que contiene posiciones 
    while node is not None:  
        path.append(node.position) #### agrega posicion a nodo
        node = node.parent  ##### Nuevo nodo es el padre 
    path = path[::-1]  ###### Organiza lista al reves

    init_y, init_x = path[0] ###posicion del path
    dir_path = [] ##### Direcciones actuales
    for pos_y, pos_x in path: ##### Compara posicion anterior y current
        if pos_x == init_x + 1: #### Si se movió a la derecha
            dir_path.append("right")
        elif pos_x == init_x - 1: ### Si se movio a la izquierda
            dir_path.append("left")
        elif pos_y == init_y + 1:## Si se movio abajo abaho
            dir_path.append("down")
        elif pos_y == init_y -1:### Si se movio arriba
            dir_path.append("up")
        init_x, init_y = pos_x, pos_y#### Actualiza la posicion actual
    return dir_path ##### Retorna Lista 

def get_children(node, end_node, maze): ###obtener hijo (Nodo que sigue(?)
    width = len(maze[0]) #Ancho del maze (field)
    height = len(maze) #### largod el mazo (field)

    if maze[node.position[0]][node.position[1]] == "P": ## Si la posicion es donde esta el jugador, actualizar a Muro (para que no vuelva por dodne inicio(?)
        maze[node.position[0]][node.position[1]] = "M"

    children = []  ### Lista de niños

    for new_position in [(0,-1), (-1,0), (0,1), (1,0)]: ########## Nueva posicion? 
        node_row = node.position[0] ###Fila del nodo actual
        node_col = node.position[1] ##Columna del nodo actual
        node_row, node_col = node_row + new_position[0], node_col + new_position[1] ##### Actualiza la posicion del nodo con suma

        if node_row > (height -1) or node_row < 0 or node_col > (width - 1) or node_col < 0: ###### ignora si es el borde
            continue

        if maze[node_row][node_col] == "M": ###### Ignora si es un muro
            continue

        node_pos = node_row, node_col #### la posicion columna y fila de los nodos se guarda 
        new_node = Node(node_pos, node.g, heuristic(node_pos, end_node.position), node) #Se crea nuevo nodo, se le mete la posicion actual, g, la distancia desde la posicion actual a la meta

        children.append(new_node)### Se mete el nuevo nodo a la lista de hijos
    
    return children ###retorna la lista de hijos

def astar(maze, start, end): #### Algoritmo A*
    start_node = Node(start, 0, heuristic(start, end), None) ##### Nodo de inicio,con distancia desde el inicio al fin
    end_node = Node(end, 0, 0, None) ####### Nodo de fin, obviamente la distancia del fin al fin es 0

    open_list = [] ### lista
    closed_list = set() #### set?

    heapq.heappush(open_list, start_node) ### pushea el nodo al heap sin joder con la estructura

    while len(open_list) > 0: #### Mientra el len de la lista sea mayor de 0 
        current_node = heapq.heappop(open_list)  #####quita elemento de la lista abierta y la pone en lista cerrada
        closed_list.add(current_node)
        
        if maze[current_node.position[0]][current_node.position[1]] == "D" and current_node.position != end_node.position:  ##### Si la posicion actual es un diamante
            print("Nuevo objetivo encontrado!") #### Registra el objetivo encontrado
            return current_node

        if current_node.position == end_node.position: ###### Su la posicion es el fin
            return get_path(current_node) #### Ejectuar buscar camino desde el nodo current
        
        children = get_children(current_node, end_node, maze) ### los hijos se encuentran desde el nodo actual y el ultimo nodo, con Field
        
        for child in children: ### recorrje los hijos
            is_closed = False #### Abre la lista
            for closed in closed_list: #### Recorre la lista cerrada
                if child.position == closed.position: ##### Si esta cerrada
                    is_closed = True ### Registra que lo esta
                    break ##y hace break
            if is_closed: continue ### se cerro continua

            spot = maze[child.position[0]][child.position[1]]    ##### Spot gaurda posicion del hijo
            child.g = current_node.g + 1 #####  se le suma 1 al G
            child.h = heuristic(child.position, end_node.position) #### heurisitca desde el hijo al nodo final
            child.f = child.g + child.h #### F es la suma de g y h?
            child.parent = current_node #### El padre es el nodo actual

            #print("spot:", spot, "position:", child.position, "child.g:", child.g, "child.h:", child.h, "child.f:", child.f)

            condition = False  ### condicional
            for open_node in open_list: ### recorre nodo abiertos 
                if child.position == open_node.position and child.g > open_node.g: #### Si la posicon del niño es la del nodo abierto y el g del hijo es mayor que la del nodo abierto   
                    condition = True ### Condicional a veradero y rompa
                    break
            if condition: continue ### sino continue iterando

            heapq.heappush(open_list, child) ##### pushea el hijo a la lista abierta
        #print()
    return None

#------------------------------------------------------------------
def get_targets(field): ##### Recorre el campo y busca targets, por el momento Diamantes, Puerta y Llave
    target_list = []
    for i in range(len(field)-1, -1, -1):
        row = field[i]
        for j in range(len(row)):
            elem = row[j]
            if elem == "S" or elem == "D" or elem == "P" or elem == "PLL" or elem == "LL":
                if elem == "P":
                    target = Player((i,j), 0)### Si es jugador, asignar 
                else:
                    target = Target((i,j), elem)
                target_list.append(target)
                ##################### Agregar aqui la parte de reconocer roca y agregar a lista/diccionario
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

def get_final_path(init_target, init_idx): ##### Funcion final
    iter = 0 ### iteraciones
    current_idx = init_idx ### 
    current_target = init_target  ##### Asigna el target inicial como primero
    path = [] ##### Array de path
    while iter < len(nodes_list) -1: #### mientras el largo de la lista de nodos 
        min_dst = min(adj_matrix[current_idx]) ##### la distancia minima = valor minimo de la matriz adyacente
        next_target_idx = adj_matrix[current_idx].index(min_dst) ###### El siguiente id de target va a ser el que tenga el indice cuyo tenga la minima distancia 

        next_target = nodes_list[next_target_idx] #### i el siguiente targe va a ser el nodo con el susodicho idx
 
        for i in range(len(adj_matrix)): ### recorre matriz adyacente y asigna el valor 100
            adj_matrix[i][current_idx] = 100
        
        field[current_target.position[0]][current_target.position[1]] = 0
        #steps.append((current_target, next_target)) 

        path_or_node = astar(field, current_target.position, next_target.position)
        if path_or_node is None:
            print("A STAR IS NONE") ### Si no encuentra path pues yaper
            exit()
        
        while isinstance(path_or_node, Node): 
            next_target = path_or_node 

            for idx in range(len(nodes_list)):
                aux_node = nodes_list[idx]
                if aux_node.position == next_target.position:
                    next_target_idx = idx
                    break
            
            path_or_node = astar(field, current_target.position, next_target.position)
            if path_or_node is None:
                print("A STAR IS NONE")
                exit()
        
        partial_path = path_or_node
        #print(partial_path)
        path += partial_path ### se adjunta el path parcial 
        ###### Aqui Iria el que si esta en objetivo para roca, ejecutar el partial path de roca 
        current_target = next_target #### se cambia de target
        current_idx = next_target_idx #### se cambia idx
        iter += 1 ### se itera y repite
    return path

#------------------------------------------------------------------ Proceso Final

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


#Obtiene el campo
field = get_field()
######
### Funcion obtener roca
###

#for row in field:
#    print(row)

## Obtiene las lista de Nodos por objetivos (por el momento diamantes, llaves y puertas)
nodes_list = get_targets(field)
## Matriz de adjuntas a partir de lista de nodo
adj_matrix = build_adj_matrix(nodes_list)

total_diamonds = 0
player = None
player_idx = -1
for node in nodes_list: # Contador diamantes y crea nodo jugador
    if node.get_type() == "D":
        total_diamonds += 1
    elif node.get_type() == "P":
        player = node

if (player != None):
    player.set_total_diamonds(total_diamonds) #Fedea cantidad de diamantes a algoritmo
    player_idx = nodes_list.index(player) #
    final_path = get_final_path(player, player_idx) #Ejecuta algoritmo 
    print(final_path)
