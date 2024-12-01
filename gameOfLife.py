import tkinter as tk
import random

def randomState(height, width):
    #Generate a random game state
    board = []
    for y in range(height):
        boardRow = [0] * width
        for x in range(width):
            if random.random() >= 0.5:
                boardRow[x] = 1
        board.append(boardRow)
    return board

def nextState(board):
    #Calculate the next game state
    width = len(board[0])
    height = len(board)
    newBoard = [[0] * width for x in range(height)]
    for y in range(height):
        for x in range(width):
            total = 0
            if x != 0:
                total += board[y][x - 1]
            if y != 0:
                total += board[y - 1][x]
            if x != width - 1:
                total += board[y][x + 1]
            if y != height - 1:
                total += board[y + 1][x]
            if x != 0 and y != 0:
                total += board[y - 1][x - 1]
            if x != width - 1 and y != height - 1:
                total += board[y + 1][x + 1]
            if x != 0 and y != height - 1:
                total += board[y + 1][x - 1]
            if x != width - 1 and y != 0:
                total += board[y - 1][x + 1]

            if total <= 1:
                newBoard[y][x] = 0
            elif total <= 3 and board[y][x] == 1:
                newBoard[y][x] = 1
            elif total == 3:
                newBoard[y][x] = 1
            elif total >= 4:
                newBoard[y][x] = 0
    return newBoard

# UI Class
class GameOfLifeUI:
    def __init__(self, master, height, width):
        self.master = master
        self.height = height
        self.width = width
        self.running = False
        self.cell_size = int(500 / width)
        self.board = randomState(height, width)

        # Create Canvas for grid display
        self.canvas = tk.Canvas(master, width=width * self.cell_size, height=height * self.cell_size, bg="white")
        self.canvas.pack()

        # Control Buttons
        self.next_button = tk.Button(master, text="Next Generation", command=self.next_generation)
        self.next_button.pack(side=tk.LEFT)

        self.randomize_button = tk.Button(master, text="Randomize", command=self.randomize_board)
        self.randomize_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(master, text="Clear", command=self.clear_board)
        self.clear_button.pack(side=tk.LEFT)

        self.start_stop_button = tk.Button(master, text="Start", command=self.toggle_running)
        self.start_stop_button.pack(side=tk.LEFT)

        # Draw initial grid
        self.draw_grid()

        # Enable cell toggling with clicks
        self.canvas.bind("<Button-1>", self.toggle_cell)

    def draw_grid(self):
        #Draw in the grid
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "black" if self.board[y][x] == 1 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

    def toggle_cell(self, event):
        #Toggle the state of a cell when clicked
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if 0 <= x < self.width and 0 <= y < self.height:
            self.board[y][x] = 1 if self.board[y][x] == 0 else 0
            self.draw_grid()

    def next_generation(self):
        #Change board to next state
        self.board = nextState(self.board)
        self.draw_grid()

    def randomize_board(self):
        #Randomize the board state
        self.board = randomState(self.height, self.width)
        self.draw_grid()

    def clear_board(self):
        #Clear the board
        self.board = [[0] * self.width for x in range(self.height)]
        self.draw_grid()
    
    def toggle_running(self):
        #Start or stop the continuous game
        self.running = not self.running
        if self.running:
            self.start_stop_button.config(text="Stop")
            self.run_continuously()
        else:
            self.start_stop_button.config(text="Start")

    def run_continuously(self):
        #Run the game continuously
        if self.running:
            self.next_generation()
            self.master.after(10, self.run_continuously)

# Run the UI
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game of Life")

    # Example dimensions for the grid
    height, width = 30, 30
    app = GameOfLifeUI(root, height, width)

    root.mainloop()