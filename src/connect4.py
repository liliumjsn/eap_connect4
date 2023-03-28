from tkinter import Tk, Canvas, messagebox, Label

class Connect4:
    column_count = 7
    row_count = 6
    left_top_offset = 30
    spacing = 10
    column_width = 50
    piece_diameter = 40
    canvas_width = 400
    canvas_height = 350
    background = "blue"

    # create Player class to hold name and color
    class Player:
        def __init__(self, name, color):
            self.name = name
            self.color = color

    # initialize variables
    def __init__(self):
        self.root = Tk()
        self.root.title("Connect4")
        self.root.resizable(False, False) 

        self.canvas = Canvas(self.root, width = self.canvas_width, height = self.canvas_height, bg = self.background)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.pack()       
        
        self.draw_board()

        self.player1 = self.Player("Red Player", "red")
        self.player2 = self.Player("Yellow Player", "yellow")

        self.current_player = self.player1
        self.turn_label = Label(self.root, text=f"Current Player: {self.current_player.name}", font = ('Arial', 14), fg = 'black')
        self.turn_label.pack(side='bottom')        
        
        self.root.mainloop()

    # create a connect4 for board, 6 row by 7 columns
    def draw_board(self):
        self.board = [[' ' for j in range(self.column_count)] for i in range(self.row_count)]
        for i in range(6):
            for j in range(7):
                x1 = j * self.column_width + self.left_top_offset
                y1 = i * self.column_width + self.left_top_offset
                x2 = x1 + self.piece_diameter
                y2 = y1 + self.piece_diameter
                self.canvas.create_oval(x1, y1, x2, y2, fill='white')

    # click event handler
    def on_click(self, event):
        column = self.get_current_column(event.x)

        # check if column is full
        if self.board[0][column] != ' ':
            return
        
        row = self.get_current_row(column)      
        self.place_piece(row, column)
        winner = self.get_winner()
        
        if winner is not None:
            messagebox.showinfo("Game Over", f"{winner.name} wins!")
            self.root.destroy()
        elif all(self.board[i][j] != ' ' for i in range(6) for j in range(7)):
            messagebox.showinfo("Game Over", "It's a tie!")
            self.root.destroy()
        else:
            if self.current_player == self.player1:
                self.current_player = self.player2
            else:
                self.current_player = self.player1
            self.turn_label.config(text = f"Current Player: {self.current_player.name}")

    # place piece to [row, column] position and update turn
    def place_piece(self, row, column):        
        x1 = column * self.column_width + self.left_top_offset
        y1 = row * self.column_width + self.left_top_offset
        x2 = x1 + self.piece_diameter
        y2 = y1 + self.piece_diameter
        color = self.current_player.color
        self.canvas.create_oval(x1, y1, x2, y2, fill = color, tags = 'disk')
        self.board[row][column] = self.current_player

    # get column from user's click position
    def get_current_column(self, x):
        column = (x - self.left_top_offset) // self.column_width
        if column > (self.column_count - 1):
            column = self.column_count -1
        if column < 0:
            column = 0
        return column
    
    # get available row for the piece 
    def get_current_row(self, column):
        for i in range(5, -1, -1):
            if self.board[i][column] == ' ':
                return i
       
    # check for winner and return it     
    def get_winner(self):
        # check rows for winner
        for i in range(6):
            for j in range(4):
                if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3] != ' ':
                    return self.board[i][j]
                
        # check columns for winner
        for i in range(3):
            for j in range(7):
                if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j] != ' ':
                    return self.board[i][j]
                
        # check diagonals (top-left to bottom-right) for winner
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] != ' ':
                    return self.board[i][j]
        
        # check diagonals (top-right to bottom-left) for winner
        for i in range(3):
            for j in range(3, 7):
                if self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == self.board[i+3][j-3] != ' ':
                    return self.board[i][j]
                
        return None

Connect4()
