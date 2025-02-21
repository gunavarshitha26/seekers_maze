import tkinter as tk
import numpy as np
from tkinter import ttk
from collections import deque
import random

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("SEEKERS MAZE")
        
        self.size = 15
        self.cell_size = 35
        self.animation_speed = 50  
        self.is_animating = False
        
        self.animation_buffer = deque(maxlen=5)
        self.frame_count = 0
        
        self.agent_pos = [1, 1]
        self.agent_parts = []
        self.paths = []
        self.current_path_index = 0
        self.step_index = 0
        self.move_count = 0
        self.optimal_path_length = float('inf')
        
        
        self.colors = {
            0: "#FFFFFF",  # Path
            1: "#2C3E50",  # Wall
            2: "#27AE60",  # Start
            3: "#E74C3C",  # End
            4: "#F1C40F",  # Current path
            5: "#3498DB",  # Visited
            6: "#9B59B6"   # Optimal path
        }
        
        self.create_widgets()
        self.create_maze()
        self.draw_agent()
        
    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10, expand=True, fill='both')
        
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.size * self.cell_size,
            height=self.size * self.cell_size,
            bg='white',
            highlightthickness=1
        )
        self.canvas.grid(row=0, column=0, rowspan=10, padx=10, sticky='nsew')
        
        control_frame = ttk.LabelFrame(self.main_frame, text="Controls", padding=5)
        control_frame.grid(row=0, column=1, sticky='n', padx=10)
        
        ttk.Label(control_frame, text="Animation Speed:").pack(pady=5)
        self.speed_scale = ttk.Scale(
            control_frame,
            from_=10,
            to=200,
            orient='horizontal',
            value=self.animation_speed
        )
        self.speed_scale.pack(pady=5, padx=5, fill='x')
        
        self.info_frame = ttk.LabelFrame(control_frame, text="Path Information", padding=5)
        self.info_frame.pack(pady=5, padx=5, fill='x')
        
        self.moves_var = tk.StringVar(value="Moves: 0")
        self.optimal_var = tk.StringVar(value="Optimal: -")
        
        ttk.Label(self.info_frame, textvariable=self.moves_var).pack(pady=2)
        ttk.Label(self.info_frame, textvariable=self.optimal_var).pack(pady=2)
        
        buttons = [
            ("New Maze", self.reset_maze),
            ("Find All Paths", self.start_pathfinding),
            ("Stop Animation", self.stop_animation),
            ("Show Optimal Path", self.find_optimal_path)
        ]
        
        for text, command in buttons:
            ttk.Button(control_frame, text=text, command=command, width=20).pack(pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(control_frame, textvariable=self.status_var, wraplength=150)
        self.status_label.pack(pady=10)
    
    def create_maze(self):
        self.maze = np.ones((self.size, self.size))
        
        def generate_maze_prim():
            walls = set()
            start = (1, 1)
            self.maze[start] = 0
            
            def add_walls(x, y):
                for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 < nx < self.size-1 and 0 < ny < self.size-1:
                        walls.add((nx, ny, x + dx//2, y + dy//2))
            
            add_walls(*start)
            
            while walls:
                wall = random.choice(list(walls))
                walls.remove(wall)
                x, y, px, py = wall
                
                if self.maze[x, y] == 1:
                    if sum(self.maze[x+dx, y+dy] == 0 for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]) <= 1:
                        self.maze[x, y] = self.maze[px, py] = 0
                        add_walls(x, y)
        
        generate_maze_prim()
        
        self.maze[1, 1] = 2  # Start
        self.maze[self.size-2, self.size-2] = 3  # End
        
        for _ in range(2):
            x, y = random.randint(1, self.size-2), random.randint(1, self.size-2)
            if self.maze[x, y] == 1:
                self.maze[x, y] = 0
        
        self.draw_maze()
    
    def draw_maze(self):
        self.canvas.delete("maze")
        
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i, j] != 0: 
                    x1 = j * self.cell_size
                    y1 = i * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=self.colors[int(self.maze[i, j])],
                        outline="#BDC3C7",
                        tags="maze"
                    )
    
    def draw_agent(self):
        for part in self.agent_parts:
            self.canvas.delete(part)
        self.agent_parts.clear()
        
        x = self.agent_pos[1] * self.cell_size + self.cell_size/2
        y = self.agent_pos[0] * self.cell_size + self.cell_size/2
        radius = self.cell_size/3
        
        body = self.canvas.create_line(
            x, y-radius,
            x, y+radius,
            fill="#000000",
            width=3,
            tags="agent"
        )
        
        head = self.canvas.create_oval(
            x-radius/2, y-radius*1.5,
            x+radius/2, y-radius,
            fill="#FFB6C1",
            outline="#000000",
            tags="agent"
        )
        
        arm_angle = (self.frame_count % 60) / 30 * 3.14159
        arm_x1 = x - radius/2 * np.cos(arm_angle)
        arm_y1 = y - radius/2 + radius/4 * np.sin(arm_angle)
        arm_x2 = x + radius/2 * np.cos(arm_angle)
        arm_y2 = y - radius/2 - radius/4 * np.sin(arm_angle)
        
        arms = self.canvas.create_line(
            arm_x1, arm_y1,
            arm_x2, arm_y2,
            fill="#000000",
            width=2,
            tags="agent"
        )
        
        leg_angle = (self.frame_count % 60) / 30 * 3.14159
        leg_x1 = x - radius/2 * np.cos(leg_angle)
        leg_y1 = y + radius/2 + radius/4 * np.sin(leg_angle)
        leg_x2 = x + radius/2 * np.cos(leg_angle)
        leg_y2 = y + radius/2 - radius/4 * np.sin(leg_angle)
        
        legs = self.canvas.create_line(
            leg_x1, leg_y1,
            leg_x2, leg_y2,
            fill="#000000",
            width=2,
            tags="agent"
        )
        
        self.agent_parts.extend([body, head, arms, legs])
        self.frame_count += 1
        
        if self.is_animating:
            self.root.after(50, self.update_agent_animation)
    
    def update_agent_animation(self):
        if self.is_animating:
            self.draw_agent()
    
    def find_paths(self):
        def iterative_dfs():
            stack = [(1, 1, [], {(1, 1)})]
            paths = []
            optimal_length = float('inf')
            optimal_path = []
            
            while stack:
                x, y, path, visited = stack.pop()
                current_path = path + [(x, y)]
                
                if self.maze[x, y] == 3:
                    paths.append(current_path)
                    if len(current_path) < optimal_length:
                        optimal_length = len(current_path)
                        optimal_path = current_path[:]
                    continue
                
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    next_x, next_y = x + dx, y + dy
                    if (0 <= next_x < self.size and 
                        0 <= next_y < self.size and 
                        self.maze[next_x, next_y] != 1 and 
                        (next_x, next_y) not in visited):
                        stack.append((next_x, next_y, current_path, visited | {(next_x, next_y)}))
            
            return paths, optimal_path, optimal_length
        
        self.paths, self.optimal_path, self.optimal_path_length = iterative_dfs()
        return bool(self.paths)
    
    def animate_path(self):
        if not self.is_animating:
            return
        
        if self.current_path_index >= len(self.paths):
            self.status_var.set(f"Found {len(self.paths)} paths!")
            self.optimal_var.set(f"Optimal: {self.optimal_path_length-1} moves")
            return
        
        current_path = self.paths[self.current_path_index]
        
        if self.step_index < len(current_path):
            x, y = current_path[self.step_index]
            if self.maze[x, y] not in [2, 3]:
                self.maze[x, y] = 4
            self.agent_pos = [x, y]
        
        self.move_count = self.step_index
        self.moves_var.set(f"Moves: {self.move_count}")
        
        self.draw_maze()
        self.draw_agent()
        
        self.step_index += 1
        if self.step_index >= len(current_path):
            self.step_index = 0
            self.current_path_index += 1
        
        speed = int(self.speed_scale.get())
        self.root.after(speed, self.animate_path)
    
    def start_pathfinding(self):
        self.is_animating = True
        self.current_path_index = 0
        self.step_index = 0
        self.move_count = 0
        self.status_var.set("Finding paths...")
        
        if self.find_paths():
            self.animate_path()
        else:
            self.status_var.set("No valid paths found!")
    
    def stop_animation(self):
        self.is_animating = False
        self.status_var.set("Animation stopped")
    
    def reset_maze(self):
        self.stop_animation()
        self.paths = []
        self.agent_pos = [1, 1]
        self.move_count = 0
        self.optimal_path_length = float('inf')
        self.moves_var.set("Moves: 0")
        self.optimal_var.set("Optimal: -")
        self.create_maze()
        self.draw_agent()
        self.status_var.set("New maze created")
    
    def find_optimal_path(self):
        if not self.paths:
            self.status_var.set("Find paths first!")
            return
        
        self.draw_maze()
        for x, y in self.optimal_path:
            if self.maze[x, y] not in [2, 3]:
                self.maze[x, y] = 6
        
        self.draw_maze()
        self.optimal_var.set(f"Optimal: {self.optimal_path_length-1} moves")
        
        self.is_animating = True
        self.animate_optimal_path(self.optimal_path, 0)
    
    def animate_optimal_path(self, path, index):
        if not self.is_animating or index >= len(path):
            return
        
        self.agent_pos = list(path[index])
        self.draw_agent()
        self.moves_var.set(f"Moves: {index}")
        
        speed = int(self.speed_scale.get())
        self.root.after(speed, self.animate_optimal_path, path, index + 1)

def main():
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    
    game = MazeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
