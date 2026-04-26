from collections import deque
class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self,node):
        if node not in self.graph:
            self.graph[node] = []
            return True
        else:
            return False
    def add_edge(self,u,v):
        if u in self.graph and v in self.graph:
            if u not in self.graph[v] and v not in self.graph[u]:
                self.graph[u].append(v)
                self.graph[v].append(u)
                return True
            else:
                print(f"Edge {u}-{v} is already created.")
                return False
        else:
            print("One or both nodes are not in the graph.")
            return False

    def delete_node(self,node):
        if node in self.graph:
            del self.graph[node]
            for key in self.graph:
                self.graph[key] = [n for n in self.graph[key] if n!=node]
            print(f"{node} is deleted.")
        else:
            print(f"Given {node} is not present in the graph.")

    def delete_edge(self,u,v):
        if u in self.graph and v in self.graph:
            if u in self.graph[v]:
                self.graph[v].remove(u)
            if v in self.graph[u]:
                self.graph[u].remove(v)
            print(f"{u}-{v} edge is deleted.")
        else:
            print("One or Both nodes are not in Graph")

    def bfs(self,start,goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or goal is not found in the graph!")
            return None
        visited = set()
        queue = deque([[start]])

        fringe = [start]
        cpath = list()

        print("Initial Fringe:",fringe[0])
        while queue:
            path = queue.popleft()
            node = path[-1]
            
            if node in fringe:
                fringe.remove(node)
            
            if node not in visited:
                visited.add(node)
                cpath.append(node)
            
            if node == goal:
                print(f"Visited: {visited}\n\n")
                print("Goal Reached!!")
                print("BFS Traversal:"," -> ".join(cpath))
                print("BFS Path:"," -> ".join(path))
                return path

            for neighbour in self.graph[node]:
                if neighbour not in visited and neighbour not in fringe:
                    new_path = path + [neighbour]
                    queue.append(new_path)
                    fringe.append(neighbour)

            print(f"Visited: {visited}\n")
            print("BFS Traversal:"," -> ".join(cpath))
            print(f"Fringe:"," ".join(fringe))

        print("Path not Found!")
        return None
    
    def dfs(self,start,goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or goal is not found in the given graph!")
            return None
        visited = set()
        stack = [[start]]

        fringe = [start]
        cpath = list()
        print("\nInitial Fringe:",fringe[0])

        while stack:
            path =  stack.pop()
            node = path[-1]

            if node in fringe:
                fringe.remove(node)
            
            if node not in visited:
                visited.add(node)
                cpath.append(node)
            
            if node == goal:
                print(f"Visited: {visited}\n\n")
                print("Goal Reached!")
                print("DFS Traversal:"," -> ".join(cpath))
                print(f"Final Path(DFS):"," -> ".join(path))
                return path
            
            for neighbour in reversed(self.graph[node]):
                if neighbour not in visited and neighbour not in fringe:
                    stack.append(path+[neighbour])
                    fringe.append(neighbour)
            print(f"Visited: {visited}\n")
            print(f"DFS Traversal:"," -> ".join(cpath))
            print(f"Fringe:"," ".join(fringe))

        print("Path not Found!")
        return None
    
    def display(self):
        print("Adjacency List")
        for node,neighbor in self.graph.items():
            print(f"{node} -> {' '.join(map(str,neighbor))}")

g = Graph() 
n = int(input("Enter the Number of Nodes:"))
if n>50:
    print("Maximum 50 nodes are allowed")
    exit()
print("Enter Nodes in the graph:")
for _ in range(n):
    node = input()
    g.add_node(node)
e = int(input("Enter the Number of edges:"))
for _ in range(e):
    u,v = input().split()
    g.add_edge(u,v)
g.display()
print("\n*** (Informed Search) ***\n")
print("1.Add Node\n2.Add Edge\n3.Delete Node\n4.Delete Edge\n5.BFS Traversal\n6.DFS Traversal\n7.Display Adjacency List\n8.Exit\n")
exit = True
while(exit):
    n = int(input("Enter the Option:"))
    if n==1:
        a = input("Enter the New Node:")
        if g.add_node(a):
            print(f"node {a} is added.")
        else:
            print(f"node {a} is already in the graph. ")
        g.display()
    elif n==2:
        print("Enter the Edges:")
        x,y = input().split()
        if g.add_edge(x,y):
            print(f"Edge {x}-{y} is added.")  
        g.display()
    elif n==3:
        d = input("Enter the Node to Delete:")
        g.delete_node(d)
        g.display()
    elif n==4:
        print("Enter the Edges to delete:")
        o,m = input().split()
        g.delete_edge(o,m)
        g.display()
    elif n==5:
        start = input("Enter the Start Node:")
        goal =input("Enter the Goal Node:")
        g.bfs(start,goal)
        print()
    elif n==6:
        st = input("Enter the Start Node:")
        go = input("Enter the Goal Node:")
        g.dfs(st,go)
        print()
    elif n==7:
        g.display()
        print()
    elif n==8:
        exit=False
        print("Exiting from BFS Traversal!!")
    else:
        print("Invalid option!!")
