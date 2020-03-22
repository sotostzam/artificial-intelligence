import json
from queue import PriorityQueue

class Node:
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.discovered = False

    # Rich comparison method called by x < y 
    def __lt__(self, other):
        # Returns priority based on alphabetical order
        return self.value < other.value

    def get_cost(self, target):
        for edge in self.edges:
            if edge['node'] == target:
                return edge['cost']

class Graph:
    def __init__(self):
        self.nodes = []
        self.start = None
        self.target = None

    def getNode(self, value):
        for i in self.nodes:
            if i.value == value:
                return i

    def ucs_search(self, start_Node, target_Node):
        frontier = PriorityQueue()
        frontier.put((0, (start_Node, [])))    ## Prepei na allaxei se (priority, (diadromh, current_node))
        while frontier:
            current_cost, state =  frontier.get()
            current = state[0]
            current_path = state[1]
            if current.discovered != True:
                current.discovered = True
                if current == target_Node:
                    current_path.append(current.value)
                    print("Path: " + str(' -> '.join(current_path)))
                    print("Accumulated cost: " + str(current_cost))
                    return True
                for edge in current.edges:
                    if edge['node'].discovered != True:
                        edge['node'].parent = current
                        new_cost = current_cost + current.get_cost(edge['node'])
                        new_path = current_path.copy()
                        new_path.append(current.value)
                        frontier.put((new_cost, (edge['node'], new_path)))
        return False

graph = Graph()

with open('tour_romania.json') as json_file:
    data = json.load(json_file)
    for i in data:
        node = Node(i)
        for j in data[i]:
            for k in j:
                item = {"node": k, "cost": j[k]}
                node.edges.append(item)
        graph.nodes.append(node)

    # Replace any edge with the respective node object
    for node in graph.nodes:
        for edge in range(0, len(node.edges)):
            for i in graph.nodes:
                if node.edges[edge]['node'] == i.value:
                     node.edges[edge]['node'] = i

start_Node  = graph.getNode("Arad")
target_Node = graph.getNode("Bucharest")
graph.ucs_search(start_Node, target_Node)