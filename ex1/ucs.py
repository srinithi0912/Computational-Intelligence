import heapq
class Graph:
    def __init__(self):
        self.graph = {}
    
    def add_node(self,node):
        if node not in self.graph:
            self.graph[node]=[]
            return True
        else:
            return False
        
    def add_edge(self,u,v,cost):
        if u in self.graph and v in self.graph:
            if not any(n == v for n,_ in self.graph[u]):
                self.graph[u].append((v,cost))
                self.graph[v].append((u,cost))
                return True
            else:
                print(f"Edge {u}-{v} is already in the graph.")
                return False
        else:
            print("one or both nodes are not found.")
            return False
        
    def delete_node(self,node):
        if node in self.graph:
            del self.graph[node]
            for key in self.graph:
                self.graph[key] = [(i,j) for i,j in self.graph[key] if i!=node]
            print(f"{node} is deleted.")
        else:
            print(f"{node} is not found.")

    def delete_edge(self,u,v):
        if u in self.graph and v in self.graph:
            self.graph[u] = [(i,j) for i,j in self.graph[u] if i!=v]
            self.graph[v] = [(i,j) for i,j in self.graph[v] if i!=u]
            print(f"Edge {u}-{v} is deleted.")
        else:
            print("One or both nodes are not found in the graph.")

    def ucs(self,start,goal):
        if start not in self.graph or goal not in self.graph:
            print("Start or goal is not found in the given graph!")
            return None
        frontier = []
        heapq.heappush(frontier,(0,start,[start]))
        best_cost = {start:0}
        visited = set()
        print(f"Initial Fringe: {[(start, 0)]}")

        while frontier:
            cost,node,path = heapq.heappop(frontier)

            if node in visited:
                continue
            visited.add(node)
            
            print("Current Path:"," -> ".join(path))

            if node == goal:
                print("Goal Reached.\n")
                return path,cost
            
            for neighbour,edge_cost in self.graph[node]:
                 total_cost = cost + edge_cost
                 if neighbour not in best_cost or total_cost < best_cost[neighbour]:
                    best_cost[neighbour] = total_cost
                    heapq.heappush(frontier,(total_cost,neighbour,path+[neighbour]))
            
            print(f"Visited: {visited}\n")
            print("Fringe: ",[(n,c) for c,n,_ in frontier])
        print("Path not found.")
        return None
    
    def display(self):
        print("Adjacency List:")
        for node,neighbour in self.graph.items():
            print(f"{node} -> ",end="")
            for neigh,cost in neighbour:
                print(f"{neigh}({cost})",end="")
            print()

g = Graph()
n = int(input("Enter the Number of Nodes:"))
if n>50:
    print("Maximum 50 Nodes are allowed.")
    exit()
print("Enter Nodes in Graph:")
for _ in range(n):
    node = input()
    g.add_node(node)
e = int(input("Enter the Number of Edges:"))
for _ in range(e):
    u,v,c = input().split()
    g.add_edge(u,v,int(c))
g.display()
print("\n*** (Informed Search) ***\n")
print("1.Add Node\n2.Add Edge\n3.Delete Node\n4.Delete Edge\n5.UCS Traversal\n6.Display Adjacency List\n8.Exit\n")
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
        print("Enter the Cost:")
        c = int(input())
        if g.add_edge(x,y,c):
            print(f"Edge {x}-{y} is added with {c}.")  
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
        p,c = g.ucs(start,goal)
        print("Path: "," -> ".join(p))
        print("Total Cost: ",c)
        print()
    elif n==6:
        g.display()
        print()
    elif n==7:
        exit=False
        print("Exiting from BFS Traversal!!")
    else:
        print("Invalid option!!")

