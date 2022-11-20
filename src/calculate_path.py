from generate_field import get_field 

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


field = get_field()

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

def astar(field, player, goal):
    start_node = Node(None, player)
    end_node = Node(None, goal)

    open_list = []
    closed_list = []

    open_list.append(start_node)
    while open_list:
        current_node = open_list[0]

        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        
        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node

            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        
        children = []
        for new_position in [(0,-1), (-1,0), (0,1), (1,0)]:
            node_row = current_node.position[0]
            node_col = current_node.position[1]
            node_row, node_col = node_row + new_position[0], node_col + new_position[1]

            if node_row > (len(field) -1) or node_row < 0 or node_col > (len(field[0]) - 1) or node_col < 0:
                continue

            if field[node_row][node_col] == "M":
                continue

            node_pos = node_row, node_col
            new_node = Node(current_node, node_pos)

            children.append(new_node)
        
        for child in children:

            is_closed = False
            for closed_child in closed_list:
                if child == closed_child:
                    is_closed = True
                    break
            if is_closed: continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            condition = False
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    condition = True
                    break
            if condition: continue

            open_list.append(child)

player, goal = get_player_and_goal(field)

for row in field:
    print(row)

path = astar(field, player, goal)
print(path)

init_y, init_x = path[0]
new_path = []
for pos_y, pos_x in path:
    if pos_x == init_x + 1:
        new_path.append("derecha")
    elif pos_x == init_x - 1:
        new_path.append("izquierda")
    elif pos_y == init_y + 1:
        new_path.append("abajo")
    elif pos_y == init_y -1:
        new_path.append("arriba")
    init_x, init_y = pos_x, pos_y

print(new_path)