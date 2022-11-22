from generate_field import get_field 
import heapq

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
        self.priority = self.get_priority(type)
        self.type = type
    
    def __lt__(self, other):
        return self.priority < other.priority
    
    def get_priority(self, type):
        priority_dict = {"D": 2, "PLL": 1, "LL": 3, "S": 0, "P": -1}
        return priority_dict[type]
    
    def get_type(self):
        return self.type
class Player(Target):
    def __init__(self, position, diamonds_to_catch):
        super().__init__(position, "P")
        self.diamonds_to_catch = diamonds_to_catch
        self.diamonds = 0
        self.key = False
    
    def catch_key(self):
        self.key = True
    
    def open_door(self):
        self.key = False
    
    def catch_diamond(self):
        self.diamonds += 1
    
    def has_all_diamonds(self):
        return self.diamonds == self.diamonds_to_catch
    
    def has_key(self):
        return self.key
    
    def set_total_diamonds(self, diamonds_amount):
        self.diamonds_to_catch = diamonds_amount

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
    width = len(maze[0])
    height = len(maze)

    if maze[node.position[0]][node.position[1]] == "P":
        maze[node.position[0]][node.position[1]] = "M"

    children = []

    for new_position in [(0,-1), (-1,0), (0,1), (1,0)]:
        node_row = node.position[0]
        node_col = node.position[1]
        node_row, node_col = node_row + new_position[0], node_col + new_position[1]

        if node_row > (height -1) or node_row < 0 or node_col > (width - 1) or node_col < 0:
            continue

        if maze[node_row][node_col] == "M":
            continue

        node_pos = node_row, node_col
        new_node = Node(node_pos, node.g, heuristic(node_pos, end_node.position), node)

        children.append(new_node)
    
    return children

def astar(maze, start, end):
    start_node = Node(start, 0, heuristic(start, end), None)
    end_node = Node(end, 0, 0, None)

    open_list = []
    closed_list = set()

    heapq.heappush(open_list, start_node)

    while len(open_list) > 0:
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node)
        
        if maze[current_node.position[0]][current_node.position[1]] == "D" and current_node.position != end_node.position:
            print("Nuevo objetivo encontrado!")
            return current_node

        if current_node.position == end_node.position:
            return get_path(current_node)
        
        children = get_children(current_node, end_node, maze)
        
        for child in children:
            is_closed = False
            for closed in closed_list:
                if child.position == closed.position:
                    is_closed = True
                    break
            if is_closed: continue

            spot = maze[child.position[0]][child.position[1]]
            child.g = current_node.g + 1
            child.h = heuristic(child.position, end_node.position)
            child.f = child.g + child.h
            child.parent = current_node

            #print("spot:", spot, "position:", child.position, "child.g:", child.g, "child.h:", child.h, "child.f:", child.f)

            condition = False
            for open_node in open_list:
                if child.position == open_node.position and child.g > open_node.g:
                    condition = True
                    break
            if condition: continue

            heapq.heappush(open_list, child)
        #print()
    return None

#------------------------------------------------------------------
def get_targets(field):
    target_list = []
    for i in range(len(field)-1, -1, -1):
        row = field[i]
        for j in range(len(row)):
            elem = row[j]
            if elem == "S" or elem == "D" or elem == "P" or elem == "PLL" or elem == "LL":
                if elem == "P":
                    target = Player((i,j), 0)
                else:
                    target = Target((i,j), elem)
                target_list.append(target)
                
    return target_list

def build_adj_matrix(nodes):
    total_nodes = len(nodes)

    matrix = [] #total_nodes^2
    for i in range(total_nodes):
        row = []
        for j in range(0, total_nodes):
            distance = heuristic(nodes[j].position, nodes[i].position)
            distance = distance if distance > 0 else 100
            row.append(distance)
        matrix.append(row)
    return matrix

def get_final_path(init_target, init_idx):
    iter = 0
    current_idx = init_idx
    current_target = init_target
    path = []
    while iter < len(nodes_list) -1:
        min_dst = min(adj_matrix[current_idx])
        next_target_idx = adj_matrix[current_idx].index(min_dst)

        next_target = nodes_list[next_target_idx]

        for i in range(len(adj_matrix)):
            adj_matrix[i][current_idx] = 100
        
        field[current_target.position[0]][current_target.position[1]] = 0
        #steps.append((current_target, next_target))

        path_or_node = astar(field, current_target.position, next_target.position)
        if path_or_node is None:
            print("A STAR IS NONE")
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
        path += partial_path

        current_target = next_target
        current_idx = next_target_idx
        iter += 1
    return path

#------------------------------------------------------------------
field = get_field()
#for row in field:
#    print(row)

nodes_list = get_targets(field)
adj_matrix = build_adj_matrix(nodes_list)

total_diamonds = 0
player = None
player_idx = -1
for node in nodes_list:
    if node.get_type() == "D":
        total_diamonds += 1
    elif node.get_type() == "P":
        player = node

if (player != None):
    player.set_total_diamonds(total_diamonds)
    player_idx = nodes_list.index(player)
    final_path = get_final_path(player, player_idx)
    print(final_path)
