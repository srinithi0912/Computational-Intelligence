import random
import math

class WumpusWorld:
    def __init__(self, size, mode="random"):
        self.size = size
        self.actions_taken = 0
        self.agent_alive = True
        self.has_gold = False
        self.bump = False
        self.scream = False
        self.grid = [["" for _ in range(size)] for _ in range(size)]
        self.visited = [[False for _ in range(size)] for _ in range(size)]
        self.path = []
        if mode == "random":
            self.random_setup()
        else:
            self.manual_setup()
        self.add_breeze_stench()

    def random_setup(self):
        self.agent_pos = (self.size-1, 0)
        self.path.append(self.agent_pos)
        safe_zone = [self.agent_pos]
        pit_count = int(input("Enter number of pits: "))
        available = [(i,j) for i in range(self.size)
                     for j in range(self.size)
                     if (i,j) not in safe_zone]
        pits = random.sample(available, pit_count)
        for (x,y) in pits:
            self.grid[x][y] = "P"

        # Wumpus
        while True:
            x = random.randint(0,self.size-1)
            y = random.randint(0,self.size-1)
            if self.grid[x][y] == "" and (x,y) not in safe_zone:
                self.grid[x][y] = "W"
                break

        # Gold
        while True:
            x = random.randint(0,self.size-1)
            y = random.randint(0,self.size-1)
            if self.grid[x][y] == "" and (x,y) != self.agent_pos:
                self.grid[x][y] = "G"
                break

    def manual_setup(self):
        self.agent_pos = (self.size-1, 0)
        self.path.append(self.agent_pos)
        pit_count = int(input("Enter number of pits: "))
        print(f"Enter {pit_count} Pit positions:")
        for i in range(pit_count):
            px = int(input("Pit X: "))
            py = int(input("Pit Y: "))
            self.grid[px][py] = "P"
        wx = int(input("Enter Wumpus X position: "))
        wy = int(input("Enter Wumpus Y position: "))
        self.grid[wx][wy] = "W"
        gx = int(input("Enter Gold X position: "))
        gy = int(input("Enter Gold Y position: "))
        self.grid[gx][gy] = "G"

    def add_breeze_stench(self):
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == "P":
                    for dx,dy in directions:
                        nx, ny = i+dx, j+dy
                        if 0<=nx<self.size and 0<=ny<self.size:
                            if "B" not in self.grid[nx][ny]:
                                self.grid[nx][ny] += "B"
                if self.grid[i][j] == "W":
                    for dx,dy in directions:
                        nx, ny = i+dx, j+dy
                        if 0<=nx<self.size and 0<=ny<self.size:
                            if "S" not in self.grid[nx][ny]:
                                self.grid[nx][ny] += "S"

    def get_sensors(self):
        x, y = self.agent_pos
        smell = "Stench" if "S" in self.grid[x][y] else "None"
        breeze = "Breeze" if "B" in self.grid[x][y] else "None"
        glitter = "Glitter" if "G" in self.grid[x][y] else "None"
        bump = "Bump" if self.bump else "None"
        scream = "Scream" if self.scream else "None"
        return [smell, breeze, glitter, bump, scream]

    def move(self, direction):
        self.bump = False
        x, y = self.agent_pos

        # ---- GRAB ----
        if direction == "grab":
            if "G" in self.grid[x][y]:
                print("Gold Grabbed Successfully!")
                self.has_gold = True
            else:
                print("No Gold Here to Grab!")
            self.actions_taken += 1
            return

        if direction == "up":
            nx, ny = x-1, y
        elif direction == "down":
            nx, ny = x+1, y
        elif direction == "left":
            nx, ny = x, y-1
        elif direction == "right":
            nx, ny = x, y+1
        else:
            print("Invalid Action!")
            return

        if 0 <= nx < self.size and 0 <= ny < self.size:
            self.agent_pos = (nx, ny)
            self.path.append(self.agent_pos)
            self.visited[nx][ny] = True
        else:
            self.bump = True

        self.actions_taken += 1
        self.check_status()

    def possible_path(self):
        x, y = self.agent_pos
        moves = []
        directions = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        for nx, ny in directions:
            if 0 <= nx < self.size and 0 <= ny < self.size:
                moves.append((nx, ny))
        return moves

    def check_status(self):
        x, y = self.agent_pos
        if "P" in self.grid[x][y]:
            print("Fell into Pit!")
            self.agent_alive = False
        if "W" in self.grid[x][y]:
            print("Killed by Wumpus!")
            self.agent_alive = False

    def display_full_world(self):
        print("\n****** INITIAL FULL WORLD ******")
        for i in range(self.size):
            for j in range(self.size):
                if (i,j) == self.agent_pos:
                    print("A", end="\t")
                else:
                    print(self.grid[i][j] if self.grid[i][j] != "" else ".", end="\t")
            print()

    def display(self):
        print("\n****** AGENT VIEW ******")
        for i in range(self.size):
            for j in range(self.size):
                if (i,j) == self.agent_pos:
                    print("A", end="\t")
                elif self.visited[i][j]:
                    print("V", end="\t")
                else:
                    print(".", end="\t")
            print()

        print("\nCurrent Position:", self.agent_pos)
        print("Possible Path:", self.possible_path())
        print("Percept:", self.get_sensors())

    def play(self):
        self.visited[self.agent_pos[0]][self.agent_pos[1]] = True
        self.display_full_world()
        while self.agent_alive and not self.has_gold:
            self.display()
            action = input("Enter action (up/down/left/right/grab): ")
            self.move(action)
        print("\n****** GAME OVER ******")
        print("Total Actions:", self.actions_taken)
        print("Final Path:", self.path)

while True:
    print("\n****** WUMPUS WORLD MENU ******")
    print("1. Random World")
    print("2. Manual Input World")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        size = int(input("Enter grid size: "))
        game = WumpusWorld(size, "random")
        game.play()
    elif choice == "2":
        size = int(input("Enter grid size: "))
        game = WumpusWorld(size, "manual")
        game.play()
    elif choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid Choice!")
