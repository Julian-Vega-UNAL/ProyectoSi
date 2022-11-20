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
            dir_path.append("➡️")
        elif pos_x == init_x - 1:
            dir_path.append("⬅️")
        elif pos_y == init_y + 1:
            dir_path.append("⬇️")
        elif pos_y == init_y -1:
            dir_path.append("⬆️")
        init_x, init_y = pos_x, pos_y
    return dir_path

def get_children(node, end_node, maze):
    width = len(maze[0])
    height = len(maze)
    
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
        
        if current_node.position == end_node.position:
            return get_path(current_node)
        
        children = get_children(current_node, end_node, maze)
        
        for child in children:
            if child in closed_list:
                continue

            child.g = current_node.g + 1
            child.h = heuristic(child.position, end_node.position)
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
def get_player_and_goal(field):
    player = (-1, -1)
    goal = (-1, -1)
    for i in range(len(field)):
        row = field[i]
        for j in range(len(row)):
            elem = row[j]
            if elem == "P":
                player = (i,j)
            if elem == "S":
                goal = (i,j)
            if player != (-1, -1) and goal != (-1, -1):
                return player, goal
    return player, goal

#------------------------------------------------------------------
field = get_field()
player, goal = get_player_and_goal(field)

for row in field:
    print(row)

path = astar(field, player, goal)
print(path)