from tkinter import Tk, Canvas, messagebox, Label

class Connect4:
    # number of columns on the board
    column_count = 7
    # number of rows on the board
    row_count = 6
    # left and top offset of the canvas
    left_top_offset = 30    
    # width of each column
    column_width = 50
    # diameter of each piece
    piece_diameter = 40
    # spacing between pieces
    piece_spacing = column_width - piece_diameter
    # width of canvas
    canvas_width = 400
    # height of canvas
    canvas_height = 350
    # background color of canvas
    canvas_background = "blue"

    # create Player class to hold name and color
    class Player:
        def __init__(self, name, color):
            self.name = name
            self.color = color

    # initialize variables
    def __init__(self):
        # create root tkinter object
        self.root = Tk()
        # add title
        self.root.title("Connect4")
        # disable resizing of the window
        self.root.resizable(False, False) 

        # create canvas graphical object that will be used as board
        self.canvas = Canvas(self.root, width = self.canvas_width, height = self.canvas_height, bg = self.canvas_background)
        # create canvas click event that captures the mouse click
        self.canvas.bind('<Button-1>', self.canvas_on_click)
        # create canvas motion event that captures the mouse movement
        self.canvas.bind('<Motion>', self.canvas_on_hover)
        self.canvas.pack()       
        
        # draw game board on canvas
        self.draw_board()

        # create player1 object
        self.player1 = self.Player("Red Player", "red")
        # create player2 object
        self.player2 = self.Player("Yellow Player", "yellow")
        # set first player as player1
        self.player_current = self.player1
        # create player's turn label
        self.player_current_label = Label(self.root, text=f"Current Player: {self.player_current.name}", font = ('Arial', 14), fg = 'black')
        self.player_current_label.pack(side='bottom')    

        # initialize selected column
        self.column_selected = 0    
        
        self.root.mainloop()

    # mouse motion event handler
    def canvas_on_hover(self, event):      
        # capture mouse X coordinate and get the column that coresponds to this X
        new_column_selected = self.get_column_selected(event.x)

        # check if mouse is over new column
        if new_column_selected != self.column_selected:
            #print("column: " + str(self.get_current_column(event.x)))
            # check if column_selected_effect exists
            if hasattr(self, "column_selected_effect"):
                # delete previous column_selected_effect rectangle
                self.canvas.delete(self.column_selected_effect)
            # updated selected column
            self.column_selected = new_column_selected
            # generate selection effect rectangle x1, x2, y1, y2
            x1 = self.column_selected * self.column_width + self.left_top_offset - self.piece_spacing/2
            y1 = self.left_top_offset - self.piece_spacing/2
            x2 = x1 + self.piece_diameter + self.piece_spacing
            y2 = self.left_top_offset + self.row_count * self.piece_diameter + (self.row_count - 1) * self.piece_spacing + self.piece_spacing/2
            # create new column_selected_effect rectangle
            self.column_selected_effect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="grey")
        

    # create a connect4 for board, 6 row by 7 columns
    def draw_board(self):
        # create a nested list of 2 dimensions to hold the board of the game
        # this is where the data of each piece will be saved
        self.board = [[' ' for j in range(self.column_count)] for i in range(self.row_count)]
        # generate 6x7 white circles on the canvas background to create a connect4 game board
        for i in range(6):
            for j in range(7):
                x1 = j * self.column_width + self.left_top_offset
                y1 = i * self.column_width + self.left_top_offset
                x2 = x1 + self.piece_diameter
                y2 = y1 + self.piece_diameter
                self.canvas.create_oval(x1, y1, x2, y2, fill='white')

    # mouse click event handler
    def canvas_on_click(self, event):
        # capture mouse X coordinate and get the column that coresponds to this X
        column_clicked = self.get_column_selected(event.x)

        # check if column is full by checking if the top piece is free
        if self.board[0][column_clicked] != ' ':
            return      
          
        # get the first available row to place a piece on the selected column
        row = self.get_row_available(column_clicked)      
        # place a piece to the selected column and row
        self.place_piece(row, column_clicked)

        # check if there is a winner
        winner = self.get_winner()
        
        # if there is a winner show it's name on a messagebox and exit
        if winner is not None:
            messagebox.showinfo("Game Over", f"{winner.name} wins!")
            self.root.destroy()
        # if there is a no winner and the board is full it is a tie
        elif all(self.board[i][j] != ' ' for i in range(6) for j in range(7)):
            messagebox.showinfo("Game Over", "It's a tie!")
            self.root.destroy()
        # if there is a no winner and the board is not full we continue to play
        else:
            # switch playr's turn
            if self.player_current == self.player1:
                self.player_current = self.player2
            else:
                self.player_current = self.player1
            # update current player's label
            self.player_current_label.config(text = f"Current Player: {self.player_current.name}")

    # place piece to [row, column] position and update turn
    def place_piece(self, row, column):      
        # generate a circle using the current player's color
        x1 = column * self.column_width + self.left_top_offset
        y1 = row * self.column_width + self.left_top_offset
        x2 = x1 + self.piece_diameter
        y2 = y1 + self.piece_diameter
        color = self.player_current.color
        self.canvas.create_oval(x1, y1, x2, y2, fill = color, tags = 'disk')
        # by placing a piece we insert a player object in the board's nested list
        self.board[row][column] = self.player_current

    # get column from user's click position
    def get_column_selected(self, x):
        # calculate selected column by dividing the X coordinate with the column's width
        column = (x - self.left_top_offset + int(self.piece_spacing/2)) // self.column_width
        # check if the selection is outside of the board
        if column > (self.column_count - 1):
            column = self.column_count -1
        if column < 0:
            column = 0
        return column
    
    # get available row for the piece 
    def get_row_available(self, column):
        # from index 5 (wich corresponds to the bottom row) until index 0, 
        # check to see if there is an empty row and return it's index
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
