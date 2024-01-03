"""Code to run game"""
import pygame, random, sys, time
from pygame.locals import *

# pygame setup
width, height, top = 800, 600, 0
dead_white = [[],[]]
dead_black = [[],[]]
pygame.init()
display = pygame.display.set_mode((width, height+top))

# fonts
font = pygame.font.SysFont("timesnewroman", 60)
font_small = pygame.font.SysFont("timesnewroman", 25)

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (222, 205, 50)
green = (0, 255, 0)
red2 = (204, 0, 0)

def display_text(text, font, surface, x, y):
    """Display text for the game in pygame"""
    textobj = font.render(text, 1, red2)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

def dead(piece):
    """Keep track of the dead pieces"""
    data = []
    data.append(piece.get_name())
    data.append(piece.get_color())
    if data[1] == "White":
        if data[0] == "Pawn":
            dead_white[0].append(piece)
        else:
            dead_white[1].append(piece)
    else:
        if data[0] == "Pawn":
            dead_black[0].append(piece)
        else:
            dead_black[1].append(piece)

def draw_dead_pieces():
    """Draw dead pieces on the side of the chess board"""
    for itr in dead_white:
        k=0
        data = []
        for piece in itr:
            data.append(piece.get_name())
            data.append(piece.get_color())
            if data[0] == "Pawn":
                piece.draw_piece_by_coordinates(width-(width-height)/2,k*height/8+top,data[1])
            else:
                piece.draw_piece_by_coordinates(width-(width-height)/2+40,k*height/8+top,data[1])
            k+=1

    #For drawing dead black pieces
    for itr in dead_black:
        k=0
        data = []
        for piece in itr:
            data.append(piece.get_name())
            data.append(piece.get_color())
            if data[0] == "Pawn":
                piece.draw_piece_by_coordinates(0,k*height/8+top,data[1])
            else:
                piece.draw_piece_by_coordinates(40,k*height/8+top,data[1])
            k+=1

def load_img(image_name):
    """Load image function"""
    try:
        return pygame.image.load("sprites/"+image_name)
    except Exception as error:
        print(error)
        exit(1)


class ChessPiece:
    """Each object is a piece on the board"""

    # init
    def __init__(self, r, c, name, player):
        """Init function"""
        self.name = name
        self.color = player
        self.r = r
        self.c = c

        if self.name == "Pawn":
            self.adjustx,self.adjusty=15,10
        elif self.name == "Rook" or self.name == "Knight":
            self.adjustx,self.adjusty=11,10
        elif self.name == "Bishop":
            self.adjustx,self.adjusty=5,10
        elif self.name == "Queen" or self.name == "King":
            self.adjustx,self.adjusty=9,10

    def get_name(self):
        """Return name of piece e.g. "Pawn" """
        return self.name

    def get_color(self):
        """Return color of piece e.g. "White" """
        return self.color

    def get_pos(self):
        """Return position of piece e.g. (2,2)"""
        return (self.r, self.c)

    def set_pos(self, r, c):
        """Change position of piece"""
        self.r = r
        self.c = c

    def draw_piece(self):
        """Display a piece on the board"""
        if self.color == "White":
            player="1"
        else:
            player="2"
        if (self.r+self.c)%2 !=0:
            color="1"
        else:
            color="2"
        self.image = load_img(self.name+player+color+".png")
        self.imagerect = self.image.get_rect()
        self.imagerect.left = (width-height)/2+self.r*height/8+self.adjustx
        self.imagerect.top = self.c*height/8+self.adjusty+top
        display.blit(self.image,self.imagerect)

    def draw_piece_by_coordinates(self,r,c,player):
        """Draw a piece based on its coordinates"""
        if player == "White":
            player="1"
        else:
            player="2"
        color="2"
        self.image = load_img(self.name+player+color+".png")
        self.imagerect = self.image.get_rect()
        self.imagerect.left = r
        self.imagerect.top = c+top
        display.blit(self.image,self.imagerect)


class ChessBoard:
    """Handles the chess board"""

    # initialize 8x8 board filled with nothing
    board = []

    # init
    def __init__(self):
        """Init function"""
        # fill in pieces of board
        self.board = [[None for _ in range(8)] for _ in range(8)]
        # white pawns on 0-7, 6 and black pawns on 0-7, 1
        self.board[0][6] = ChessPiece(0,6,"Pawn","White")
        self.board[1][6] = ChessPiece(1,6,"Pawn","White")
        self.board[2][6] = ChessPiece(2,6,"Pawn","White")
        self.board[3][6] = ChessPiece(3,6,"Pawn","White")
        self.board[4][6] = ChessPiece(4,6,"Pawn","White")
        self.board[5][6] = ChessPiece(5,6,"Pawn","White")
        self.board[6][6] = ChessPiece(6,6,"Pawn","White")
        self.board[7][6] = ChessPiece(7,6,"Pawn","White")

        self.board[0][1] = ChessPiece(0,1,"Pawn","Black")
        self.board[1][1] = ChessPiece(1,1,"Pawn","Black")
        self.board[2][1] = ChessPiece(2,1,"Pawn","Black")
        self.board[3][1] = ChessPiece(3,1,"Pawn","Black")
        self.board[4][1] = ChessPiece(4,1,"Pawn","Black")
        self.board[5][1] = ChessPiece(5,1,"Pawn","Black")
        self.board[6][1] = ChessPiece(6,1,"Pawn","Black")
        self.board[7][1] = ChessPiece(7,1,"Pawn","Black")


        # other white pieces on 0-7, 7 and other black pieces on 0-7, 0
        self.board[0][7] = ChessPiece(0,7,"Rook","White")
        self.board[1][7] = ChessPiece(1,7,"Knight","White")
        self.board[2][7] = ChessPiece(2,7,"Bishop","White")
        self.board[3][7] = ChessPiece(3,7,"Queen","White")
        self.board[4][7] = ChessPiece(4,7,"King","White")
        self.board[5][7] = ChessPiece(5,7,"Bishop","White")
        self.board[6][7] = ChessPiece(6,7,"Knight","White")
        self.board[7][7] = ChessPiece(7,7,"Rook","White")

        self.board[0][0] = ChessPiece(0,0,"Rook","Black")
        self.board[1][0] = ChessPiece(1,0,"Knight","Black")
        self.board[2][0] = ChessPiece(2,0,"Bishop","Black")
        self.board[3][0] = ChessPiece(3,0,"Queen","Black")
        self.board[4][0] = ChessPiece(4,0,"King","Black")
        self.board[5][0] = ChessPiece(5,0,"Bishop","Black")
        self.board[6][0] = ChessPiece(6,0,"Knight","Black")
        self.board[7][0] = ChessPiece(7,0,"Rook","Black")


    def get_board(self):
        """Return chess board"""
        return self.board

    def display_board(self):
        """Displays the chess board"""
        for i in range(8):
            for j in range(8):
                if (i+j)%2 != 0:
                    pygame.draw.rect(display,(50,50,50),(i*(height)/8+(width-height)/2,j*(height)/8+top,(height)/8,(height)/8))
                else:
                    pygame.draw.rect(display,(200,200,200),(i*(height)/8+(width-height)/2,j*(height)/8+top,(height)/8,(height)/8))
                pygame.draw.rect(display,black,(i*(height)/8+(width-height)/2,j*(height)/8+top,(height)/8,(height)/8),1)
        self.draw_all_pieces()

    def draw_all_pieces(self):
        """Calls draw_piece for every square on the board"""
        for r in range(8):
            for c in range(8):
                if self.board[r][c] is not None:
                    self.board[r][c].draw_piece()


class Game:
    """Handles the game turns and functions"""

    board = None

    def __init__(self):
        """Init function"""
        self.board = ChessBoard()
        self.turn = "White"
        self.white_check = False
        self.black_check = False
        self.white_king_move = False
        self.black_king_move = False
        self.white_left_rook_move = False
        self.black_left_rook_move = False
        self.white_right_rook_move = False
        self.black_right_rook_move = False

    def change_turn(self):
        """Change whose turn it is"""
        if self.turn == "White":
            self.turn = "Black"
        else:
            self.turn = "White"

    def get_turn(self):
        """Return who's turn it is (Black/White)"""
        return self.turn


    def right_piece(self, r, c):
        """Check if a given piece is a given player's piece"""
        if self.board.board[r][c] is not None and self.board.board[r][c].color == self.turn:
            return True
        return False

    def move(self, old, new):
        """Moves a given piece"""
        if self.board.board[old[0]][old[1]].name == "King" and abs(new[0] - old[0]) == 2:
            if new == [2,7]:
                # update the values in the chess piece
                self.board.board[0][7].set_pos(3, 7)

                # move the chess piece on board class
                self.board.board[3][7] = self.board.board[0][7]

                # remove old location on board class
                self.board.board[0][7] = None

            # white castle to the right
            elif new == [6,7]:
                # update the values in the chess piece
                self.board.board[7][7].set_pos(5, 7)

                # move the chess piece on board class
                self.board.board[5][7] = self.board.board[7][7]

                # remove old location on board class
                self.board.board[7][7] = None

            # black castle to the left
            elif new == [2,0]:
                # update the values in the chess piece
                self.board.board[0][0].set_pos(3, 0)

                # move the chess piece on board class
                self.board.board[3][0] = self.board.board[0][0]

                # remove old location on board class
                self.board.board[0][0] = None

            # black castle to the right
            elif new == [6,0]:
                # update the values in the chess piece
                self.board.board[7][0].set_pos(5, 0)

                # move the chess piece on board class
                self.board.board[5][0] = self.board.board[7][0]

                # remove old location on board class
                self.board.board[7][0] = None

        
        # update the values in the chess piece
        self.board.board[old[0]][old[1]].set_pos(new[0], new[1])

        # move the chess piece on board class
        self.board.board[new[0]][new[1]] = self.board.board[old[0]][old[1]]

        # remove old location on board class
        self.board.board[old[0]][old[1]] = None


    # remove pieces
    def remove(self, r, c):
        """Remove piece at r,c"""
        # TODO: must implement dead function for this to work
        if self.board.board[r][c] != None:
            dead(self.board.board[r][c])

    def hint(self, r, c):
        """Show the possible places a piece could go"""
        loc = []
        piece = self.board.get_board()[r][c]
        if piece.get_name() == "Pawn":
            # pawn can only move forward (white - black +)
            if piece.get_color() == "White":
                # hasn't moved yet, nothing in squares two in front
                if c == 6 and self.board.board[r][c-1] is None and self.board.board[r][c-2] is None and self.valid_move([r,c],[r,c-2]):
                    self.highlight(r, c-2)
                    loc.append([r, c-2])
                    

                # moving up one spot normally
                if c > 0 and self.board.get_board()[r][c-1] is None and self.valid_move([r,c], [r,c-1]):
                    self.highlight(r, c-1)
                    loc.append([r, c-1])

                # attacking diagonal up right
                if r < 7 and c > 0 and self.board.get_board()[r+1][c-1] is not None and self.board.get_board()[r+1][c-1].get_color() == "Black" and self.valid_move([r,c],[r+1,c-1]):
                    self.highlight(r+1, c-1)
                    loc.append([r+1, c-1])

                # attacking diagonal up left
                if r > 0 and c > 0 and self.board.get_board()[r-1][c-1] is not None and self.board.get_board()[r-1][c-1].get_color() == "Black" and self.valid_move([r,c],[r-1,c-1]):
                    self.highlight(r-1, c-1)
                    loc.append([r-1, c-1])

            else:
                # mirror everything from white
                if c == 1 and self.board.get_board()[r][c+1] is None and self.board.get_board()[r][c+2] is None and self.valid_move([r,c],[r,c+2]):
                    self.highlight(r, c+2)
                    loc.append([r, c+2])

                if c < 7 and self.board.get_board()[r][c+1] is None and self.valid_move([r,c], [r,c+1]):
                    self.highlight(r, c+1)
                    loc.append([r, c+1])

                # attacking diagonal down right
                if r < 7 and c < 7 and self.board.get_board()[r+1][c+1] is not None and self.board.get_board()[r+1][c+1].get_color() == "White" and self.valid_move([r,c],[r+1,c+1]):
                    self.highlight(r+1, c+1)
                    loc.append([r+1, c+1])

                # attacking diagonal down left
                if r > 0 and c > 0 and self.board.get_board()[r-1][c+1] is not None and self.board.get_board()[r-1][c+1].get_color() == "White" and self.valid_move([r,c],[r-1,c+1]):
                    self.highlight(r-1, c+1)
                    loc.append([r-1, c+1])

        elif piece.get_name() == "Bishop":
            loc = self.hint_helper(r, c, "diag")

        elif piece.get_name() == "Knight":
            # if you can move two left
            if r-2 >= 0:
                # if you can move one up
                if c-1 >= 0:
                    if (self.board.get_board()[r-2][c-1] is None or (self.board.get_board()[r-2][c-1] is not None and (self.board.get_board()[r-2][c-1].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r-2,c-1]):
                        self.highlight(r-2, c-1)
                        loc.append([r-2, c-1])
                # if you can move one down
                if c+1 <= 7:
                    if (self.board.get_board()[r-2][c+1] is None or (self.board.get_board()[r-2][c+1] is not None and (self.board.get_board()[r-2][c+1].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r-2,c+1]):
                        self.highlight(r-2, c+1)
                        loc.append([r-2, c+1])
            # if you can move two up
            if c-2 >= 0:
                # if you can move one left
                if r-1 >= 0:
                    if (self.board.get_board()[r-1][c-2] is None or (self.board.get_board()[r-1][c-2] is not None and (self.board.get_board()[r-1][c-2].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r-1,c-2]):
                        self.highlight(r-1, c-2)
                        loc.append([r-1, c-2])

                # if you can move one right
                if r+1 <= 7:
                    if (self.board.get_board()[r+1][c-2] is None or (self.board.get_board()[r+1][c-2] is not None and (self.board.get_board()[r+1][c-2].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r+1,c-2]):
                        self.highlight(r+1, c-2)
                        loc.append([r+1, c-2])

            # if you can move two right
            if r+2 <= 7:
                # if you can move one up
                if c-1 >= 0:
                    if (self.board.get_board()[r+2][c-1] is None or (self.board.get_board()[r+2][c-1] is not None and (self.board.get_board()[r+2][c-1].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r+2,c-1]):
                        self.highlight(r+2, c-1)
                        loc.append([r+2, c-1])

                # if you can move one down
                if c+1 <= 7:
                    if (self.board.get_board()[r+2][c+1] is None or (self.board.get_board()[r+2][c+1] is not None and (self.board.get_board()[r+2][c+1].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r+2,c+1]):
                        self.highlight(r+2, c+1)
                        loc.append([r+2, c+1])

            # if you can move two down
            if c+2 <= 7:
                # if you can move one left
                if r-1 >= 0:
                    if (self.board.get_board()[r-1][c+2] is None or (self.board.get_board()[r-1][c+2] is not None and (self.board.get_board()[r-1][c+2].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r-1,c+2]):
                        self.highlight(r-1, c+2)
                        loc.append([r-1, c+2])
                # if you can move one right
                if r+1 <= 7:
                    if (self.board.get_board()[r+1][c+2] is None or (self.board.get_board()[r+1][c+2] is not None and (self.board.get_board()[r+1][c+2].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r+1,c+2]):
                        self.highlight(r+1, c+2)
                        loc.append([r+1, c+2])

        elif piece.get_name() == "Rook":
            loc = self.hint_helper(r ,c, "straight")

        #TODO: this
        elif piece.get_name() == "King":
            # check all 8 positions around
            # left
            if r > 0:
                if (self.board.get_board()[r-1][c] is None or (self.board.get_board()[r-1][c] is not None and (self.board.get_board()[r-1][c].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r-1,c]):
                    self.highlight(r-1,c)
                    loc.append([r-1,c])
                    # left up
            if c > 0 and r > 0:
                if (self.board.get_board()[r-1][c-1] is None or (self.board.get_board()[r-1][c-1] is not None and (self.board.get_board()[r-1][c-1].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r-1,c-1]):
                    self.highlight(r-1,c-1)
                    loc.append([r-1,c-1])
            # left down
            if r > 0 and c < 7:
                if (self.board.get_board()[r-1][c+1] is None or (self.board.get_board()[r-1][c+1] is not None and (self.board.get_board()[r-1][c+1].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r-1,c+1]):
                    self.highlight(r-1,c+1)
                    loc.append([r-1,c+1])

            # right
            if r < 7:
                if (self.board.get_board()[r+1][c] is None or (self.board.get_board()[r+1][c] is not None and (self.board.get_board()[r+1][c].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r+1,c]):
                    self.highlight(r+1,c)
                    loc.append([r+1,c])

                    # right up
            if r < 7 and c > 0:
                if (self.board.get_board()[r+1][c-1] is None or (self.board.get_board()[r+1][c-1] is not None and (self.board.get_board()[r+1][c-1].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r+1,c-1]):
                    self.highlight(r+1,c-1)
                    loc.append([r+1,c-1])
            # right down
            if r < 7 and c < 7:
                if (self.board.get_board()[r+1][c+1] is None or (self.board.get_board()[r+1][c+1] is not None and (self.board.get_board()[r+1][c+1].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r+1,c+1]):
                    self.highlight(r+1,c+1)
                    loc.append([r+1,c+1])
            # up
            if c > 0:
                if (self.board.get_board()[r][c-1] is None or (self.board.get_board()[r][c-1] is not None and (self.board.get_board()[r][c-1].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r,c-1]):
                    self.highlight(r,c-1)
                    loc.append([r,c-1])
            # down
            if c < 7:
                if (self.board.get_board()[r][c+1] is None or (self.board.get_board()[r][c+1] is not None and (self.board.get_board()[r][c+1].get_color() != self.board.get_board()[r][c].get_color()))) and self.valid_move([r,c],[r,c+1]):
                    self.highlight(r,c+1)
                    loc.append([r,c+1])

            # check castling positions
            # white left rook
            if not (self.white_check or self.white_king_move or self.white_left_rook_move) and self.board.board[r][c].color == "White" and self.board.board[1][7] is None and self.board.board[2][7] is None and self.board.board[3][7] is None and self.valid_move([4,7], [2,7]):
                self.highlight(2,7)
                loc.append([2,7])

            # white right rook
            if not (self.white_check or self.white_king_move or self.white_right_rook_move) and self.board.board[r][c].color == "White" and self.board.board[5][7] is None and self.board.board[6][7] is None and self.valid_move([4,7], [6,7]):
                self.highlight(6,7)
                loc.append([6,7])

            # black left rook
            if not (self.black_check or self.black_king_move or self.black_left_rook_move) and self.board.board[r][c].color == "Black" and self.board.board[1][0] is None and self.board.board[2][0] is None and self.board.board[3][0] is None and self.valid_move([4,0], [2,0]):
                self.highlight(2,0)
                loc.append([2,0])

            # black right rook
            if not (self.black_check or self.black_king_move or self.black_right_rook_move) and self.board.board[r][c].color == "Black" and self.board.board[5][0] is None and self.board.board[6][0] is None and self.valid_move([4,0], [6,0]):
                self.highlight(6,0)
                loc.append([6,0])


        elif piece.get_name() == "Queen":
            loc = self.hint_helper(r, c, "diag") + self.hint_helper(r, c, "straight")

        else:
            print(f"Error: Piece with name {piece.get_name()}")
            exit(1)
        return loc

    # check function
    def hint_helper(self, r, c, kind):
        """Helper function to check diagonals and straights for hint()"""
        loc = []
        moves = None
        if kind ==  "straight":
            moves = [[1, -1, 0, 0],[0, 0, 1, -1]]

        else:
            moves = [[1, 1, -1, -1],[1, -1, 1, -1]]

        counter = 0
        # for each direction
        while counter < 4:
            i, j = r + moves[0][counter], c + moves[1][counter]
            # expand outward for all spaes that are not occupied
            while i >= 0 and i < 8 and j >= 0 and j < 8 and self.board.get_board()[i][j] is None:
                if self.valid_move([r,c], [i,j]):
                    self.highlight(i,j)
                    loc.append([i,j])
                i += moves[0][counter]
                j += moves[1][counter]

            # once a piece is hit or the edge is hit
            if i >= 0 and i < 8 and j >= 0 and j < 8 and self.board.get_board()[i][j] is not None and (self.board.get_board()[i][j].get_color() is not self.board.get_board()[r][c].get_color()) and self.valid_move([r,c],[i,j]):
                self.highlight(i,j)
                loc.append([i,j])

            counter = counter + 1
        return loc


    # check for check function
    def is_checked(self, player):
        """Return true if player is checked"""
        r = -1
        c = -1
        # find location of player king
        for i in range(8):
            for j in range(8):
                if self.board.get_board()[i][j] and self.board.get_board()[i][j].get_color() == player and self.board.get_board()[i][j].get_name() == "King":
                    r = i
                    c = j

        # error checking to make sure king is on board
        if r == -1:
            print(f"Error: Could not find King of color {player} on board")
            exit(1)

        # check each type of piece to see if it is checking the king
        # pawn: check diagonals (color dependent for direction)
        if player == "White": # r-1 c-1 and r+1 c-1
            # if on the board
            if r-1 >= 0 and c-1 >= 0 and r-1 < 8 and c-1 < 8:
                if self.board.get_board()[r-1][c-1] and self.board.get_board()[r-1][c-1].get_name() == "Pawn" and self.board.get_board()[r-1][c-1].get_color() == "Black":
                    return True
            if r+1 >= 0 and c-1 >= 0 and r+1 < 8 and c-1 < 8:
                if self.board.get_board()[r+1][c-1] and self.board.get_board()[r+1][c-1].get_name() == "Pawn" and self.board.get_board()[r+1][c-1].get_color() == "Black":
                    return True
        else: # r-1 c+1 and r+1 c+1
             # if on the board
            if r-1 >= 0 and c+1 >= 0 and r-1 < 8 and c+1 < 8:
                if self.board.get_board()[r-1][c+1] and self.board.get_board()[r-1][c+1].get_name() == "Pawn" and self.board.get_board()[r-1][c+1].get_color() == "White":
                    return True

            if r+1 >= 0 and c+1 >= 0 and r+1 < 8 and c+1 < 8:
                if self.board.get_board()[r+1][c+1] and self.board.get_board()[r+1][c+1].get_name() == "Pawn" and self.board.get_board()[r+1][c+1].get_color() == "White":
                    return True
        # knight: check all 8 options make sure theyre on board first
        knights = [[-1, -2, 1, 2, -1, -2, 1, 2],[-2, -1, -2, -1, 2, 1, 2, 1]]
        for i in range(8):
            if r+knights[0][i] >= 0 and r+knights[0][i] < 8 and c+knights[1][i] >= 0 and c+knights[1][i] < 8:
                x = r+knights[0][i]
                y = c+knights[1][i]
                if self.board.board[x][y] is not None and self.board.board[x][y].get_color() is not player and self.board.board[x][y].get_name() == "Knight":
                    return True
        # bishop and queen check all four directions
        # check (-1, -1), (-1, 1), (1, -1), (-1, -1) until hitting a piece or going off of board
        i = -1
        j = -1
        dirs = [[-1, -1, 1, 1],[-1, 1, -1, 1]]
        for count in range(4):
            # until htting a piece of going off the board
            i = dirs[0][count]
            j = dirs[1][count]
            while r+i >= 0 and r+i < 8 and c+j >= 0 and c+j < 8:
                # if found piece same team
                if self.board.board[r+i][c+j] is not None and self.board.board[r+i][c+j].get_color() == player:
                    break
                # if found opponent piece but not bishop or queen
                elif self.board.board[r+i][c+j] is not None and self.board.board[r+i][c+j].get_color() != player and not (self.board.board[r+i][c+j].get_name() == "Bishop" or self.board.board[r+i][c+j].get_name() == "Queen"):
                    break
                # if found opponent piece that is bishop or queen
                elif self.board.board[r+i][c+j] is not None and self.board.board[r+i][c+j].get_color() != player and (self.board.board[r+i][c+j].get_name() == "Bishop" or self.board.board[r+i][c+j].get_name() == "Queen"):
                    return True

                # move one iteration out
                i = i + dirs[0][count]
                j = j + dirs[1][count]

        # rook and queen check all four directions
        # check (1, 0), (0, 1), (-1, 0), (0, -1) until hitting a piece or going off of board
        i = -1
        j = -1
        dirs = [[1, 0, -1, 0],[0, 1, 0, -1]]
        for count in range(4):
            # until htting a piece of going off the board
            i = dirs[0][count]
            j = dirs[1][count]
            while r+i >= 0 and r+i < 8 and c+j >= 0 and c+j < 8:
                # if found piece same team
                if self.board.board[r+i][c+j] is not None and self.board.board[r+i][c+j].get_color() == player:
                    break
                # if found opponent piece but not rook or queen
                elif self.board.board[r+i][c+j] is not None and self.board.board[r+i][c+j].get_color() != player and not (self.board.board[r+i][c+j].get_name() == "Rook" or self.board.board[r+i][c+j].get_name() == "Queen"):
                    break
                # if found opponent piece that is rook or queen
                elif self.board.board[r+i][c+j] is not None and self.board.board[r+i][c+j].get_color() != player and (self.board.board[r+i][c+j].get_name() == "Rook" or self.board.board[r+i][c+j].get_name() == "Queen"):
                    return True

                # move one iteration out
                i = i + dirs[0][count]
                j = j + dirs[1][count]

        # king check all surrounding pieces (8 options) (combined rook and bishop arrays)
        dirs = [[1, 0, -1, 0, -1, -1, 1, 1],[0, 1, 0, -1, -1, 1, -1, 1]]
        for count in range(8):
            i = dirs[0][count]
            j = dirs[1][count]
            # if the location is on the board
            if r+i >= 0 and r+i < 8 and c+j >= 0 and c+j < 8:
                # if there is a king on surrounding square
                if self.board.board[r+i][c+j] is not None and self.board.board[r+i][c+j].get_color() != player and self.board.board[r+i][c+j].get_name() == "King":
                    return True
        # if get through all options
        return False


    # valid move function
    def valid_move(self, old, new):
        """Check if a given move is a valid move"""
        # check if you can castle with the king
        if self.board.board[old[0]][old[1]].name == "King" and abs(new[0] - old[0]) == 2:
            old_loc = self.board.board[old[0]][old[1]]
            new_loc = self.board.board[new[0]][new[1]]
            # white castle to the left
            if new == [2,7] and self.board.board[old[0]][old[1]].color == "White":
                old_castle = self.board.board[0][7]
                new_castle = self.board.board[3][7]
                self.board.board[0][7] = None
                self.board.board[3][7] = old_castle
                not_valid = self.is_checked(self.get_turn())
                self.board.board[0][7] = old_castle
                self.board.board[3][7] = new_castle

            # white castle to the right
            elif new == [6,7] and self.board.board[old[0]][old[1]].color == "White":
                old_castle = self.board.board[7][7]
                new_castle = self.board.board[5][7]
                self.board.board[7][7] = None
                self.board.board[5][7] = old_castle
                not_valid = self.is_checked(self.get_turn())
                self.board.board[7][7] = old_castle
                self.board.board[5][7] = new_castle

            # black castle to the left
            elif new == [2,0] and self.board.board[old[0]][old[1]].color == "Black":
                old_castle = self.board.board[0][0]
                new_castle = self.board.board[3][0]
                self.board.board[0][0] = None
                self.board.board[3][0] = old_castle
                not_valid = self.is_checked(self.get_turn())
                self.board.board[0][0] = old_castle
                self.board.board[3][0] = new_castle

            # black castle to the right
            elif new == [6,0] and self.board.board[old[0]][old[1]].color == "Black":
                old_castle = self.board.board[7][0]
                new_castle = self.board.board[5][0]
                self.board.board[7][0] = None
                self.board.board[5][0] = old_castle
                not_valid = self.is_checked(self.get_turn())
                self.board.board[7][0] = old_castle
                self.board.board[5][0] = new_castle

        else:
            # for every other move
            old_loc = self.board.board[old[0]][old[1]]
            new_loc = self.board.board[new[0]][new[1]]
            self.board.board[old[0]][old[1]] = None
            self.board.board[new[0]][new[1]] = old_loc
            not_valid = self.is_checked(self.get_turn())
            self.board.board[old[0]][old[1]] = old_loc
            self.board.board[new[0]][new[1]] = new_loc
        return not not_valid

    # new piece function
    def new_piece(self, player, r, c, chess, display):
        """Function for checking and adding a new piece when the pawn reaches the end of the board"""
        # check if its the case
        if ((player == "White" and c == 0) or (player == "Black" and c == 7)) and self.board.board[r][c].get_name() == "Pawn":
            if player == "White":
                t="1"
            else:
                t="2"

            display.fill((200,200,200))
            draw_dead_pieces()
            chess.display_board()
            pygame.display.update()
            time.sleep(0.5)
            start=300
            pygame.draw.rect(display,(200,200,200),(start,250,230,70))
            image = load_img("Rook"+t+"2"+".png")
            imagerect = image.get_rect()
            imagerect.left = start+5
            imagerect.top = 255
            display.blit(image,imagerect)
            image = load_img("Knight"+t+"2"+".png")
            imagerect = image.get_rect()
            imagerect.left = start+55
            imagerect.top = 255
            display.blit(image,imagerect)
            image = load_img("Bishop"+t+"2"+".png")
            imagerect = image.get_rect()
            imagerect.left = start+105
            imagerect.top = 255
            display.blit(image,imagerect)
            image = load_img("Queen"+t+"2"+".png")
            imagerect = image.get_rect()
            imagerect.left = start+165
            imagerect.top = 255
            display.blit(image,imagerect)
            pygame.draw.rect(display,black,(start,250,230,70),1)
            pygame.draw.rect(display,black,(start,250,57,70),1)
            pygame.draw.rect(display,black,(start+57,250,52,70),1)
            pygame.draw.rect(display,black,(start+109,250,57,70),1)
            pygame.draw.rect(display,black,(start+166,250,64,70),1)
            flag=0
            while True:
                for event in pygame.event.get():
                    position=pygame.mouse.get_pos()
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        if position[1]>=250 and position[1]<=320:
                            if position[0]>=start and position[0]<=start+57:
                                p="Rook"
                                flag=1
                                break
                            elif position[0]>=start+57 and position[0]<=start+109:
                                p="Knight"
                                flag=1
                                break
                            elif position[0]>=start+109 and position[0]<=start+166:
                                p="Bishop"
                                flag=1
                                break
                            elif position[0]>=start+166 and position[0]<=start+230:
                                p="Queen"
                                flag=1
                                break
                    if position[1]>=250 and position[1]<=320:
                        if not(position[0]>=start and position[0]<=start+57):
                            pygame.draw.rect(display,black,(start,250,57,70),1)
                        if not(position[0]>=start+57 and position[0]<=start+109):
                            pygame.draw.rect(display,black,(start+57,250,52,70),1)
                        if not(position[0]>=start+109 and position[0]<=start+166):
                            pygame.draw.rect(display,black,(start+109,250,57,70),1)
                        if not(position[0]>=start+166 and position[0]<=start+230):
                            pygame.draw.rect(display,black,(start+166,250,64,70),1)

                    if position[1]>=250 and position[1]<=320:
                        if position[0]>=start and position[0]<=start+57:
                            pygame.draw.rect(display,red,(start,250,57,70),1)
                        if position[0]>=start+57 and position[0]<=start+109:
                            pygame.draw.rect(display,red,(start+57,250,52,70),1)
                        if position[0]>=start+109 and position[0]<=start+166:
                            pygame.draw.rect(display,red,(start+109,250,57,70),1)
                        if position[0]>=start+166 and position[0]<=start+230:
                            pygame.draw.rect(display,red,(start+166,250,64,70),1)

                pygame.display.update()
                if flag==1:
                    break

            piece=ChessPiece(r,c,p,player)
            self.board.board[r][c]=piece

    # no moves function
    def no_moves(self, player):
        """Returns true if the player cannot make any moves"""
        # if after looping through all pieces none of them can move return true
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] is not None and self.board.board[i][j].color == player and self.hint(i,j):
                    return False
        return True

    # stalemate function
    def stalemate(self):
        """Returns true if there is a stalemate condition"""
        # TODO this function needs to be better and account for other stalemate possibilities

        # only pieces on board are kings
        count = 0
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] is not None:
                    count = count + 1

        return count == 2


    # monitor functions
    def monitor_castelling_conditions(self,r,c):
        """Monitor rooks movement"""
        if r==0:
            if c==0:
                self.black_left_rook_move=True
            if c==7:
                self.white_left_rook_move=True
        if r==7:
            if c==0:
                self.black_right_rook_move=True
            if c==7:
                self.white_right_rook_move=True

    def monitor_castelling_conditions1(self,player):
        """Monitor check"""
        if player == "White":
            self.white_check=True
        else:
            self.black_check=True

    def monitor_castelling_conditions2(self,player):
        """Monitor king move"""
        if player == "White":
            self.white_king_move=True
        else:
            self.black_king_move=True


    # display grid function
    def highlight(self,x,y):
        """Highlights the location on the display"""
        pygame.draw.rect(display,yellow,(x*(height)/8+(width-height)/2,y*(height)/8+top,(height)/8,(height)/8),3)

    def dehighlight(self,places):
        """Removes highlight from the location on the display"""
        if places is not None:
            for place in places:
                pygame.draw.rect(display,white,(place[0]*(height)/8+(width-height)/2,place[1]*(height)/8+top,(height)/8,(height)/8),3)

    # display grid function
    def display_board(self):
        """Calls display_board on the board class level"""
        self.board.display_board()


class Run:
    """Class to run the program, run function should do everything"""

    def __init__(self):
        print("Startig Game")

    def run(self):
        """function to run the game"""
        try:
            while True:
                chess = Game()
                moveState = "None"
                display.fill((200,200,200))
                chess.display_board()
                places=[]
                d={"White":"Black","Black":"White"}
                while True:
                    gameOver=False
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            gameExit=True
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            position=pygame.mouse.get_pos()
                            x=int((position[0]-(width-height)/2)//(height/8))
                            y=int(position[1]//(height/8)+top)
                            if x >= 0 and x < 8 and y >= 0 and y < 8:
                                if moveState == "None" and chess.right_piece(x,y):
                                    oldPosition=[x,y]
                                    places=chess.hint(x,y)
                                    moveState="Hint"
                                elif moveState == "Hint":
                                    if [x,y] in places:
                                        chess.monitor_castelling_conditions(oldPosition[0],oldPosition[1])
                                        if chess.board.board[oldPosition[0]][oldPosition[1]].name == "King":
                                            chess.monitor_castelling_conditions2(chess.get_turn())
                                        chess.remove(x,y)
                                        chess.move(oldPosition,[x,y])           
                                        chess.new_piece(chess.get_turn(),x,y,chess,display)
                                        chess.change_turn()
                                        if chess.is_checked(chess.get_turn()):
                                            chess.monitor_castelling_conditions1(chess.get_turn())
                                            if not chess.no_moves(chess.get_turn()):
                                                display_text('Check!!!', font, display, 240, 200)
                                                pygame.display.update()
                                                time.sleep(0.5)
                                                display.fill((200,200,200))
                                                draw_dead_pieces()
                                                chess.display_board()
                                                pygame.display.update()
                                        if chess.no_moves(chess.get_turn()):
                                            display.fill((200,200,200))
                                            draw_dead_pieces()
                                            chess.display_board()
                                            if chess.is_checked(chess.get_turn()):
                                                display_text('CheckMate!!!', font, display, 240, 200)
                                                display_text('%s Wins'%(d[chess.get_turn()]), font, display, 240, 260)
                                            else:
                                                display_text('Stalemate!!!', font,display, 240, 200)
                                                display_text('Match Draw', font, display, 240, 260)
                                            pygame.display.update()
                                            gameOver=True
                                            break
                                        if chess.stalemate():
                                            display.fill((200,200,200))
                                            draw_dead_pieces()
                                            chess.display_board()
                                            display_text('Stalemate!!!', font, display, 240, 200)
                                            display_text('Match Draw', font, display, 240, 260)
                                            pygame.display.update()
                                            gameOver=True
                                            break
                                    display.fill((200,200,200))
                                    draw_dead_pieces()
                                    chess.display_board()
                                    moveState="None"
                                    if [x,y] not in places and x >= 0 and x < 8 and y >= 0 and y < 8 and chess.right_piece(x,y):
                                        oldPosition=[x,y]
                                        places=chess.hint(x,y)
                                        moveState="Hint"

                    pygame.display.update()
                    if gameOver:
                        break
            
                time.sleep(2)
                flag=0
                start=300
                pygame.draw.rect(display,(200,200,200),(start,250,230,70))
                pygame.draw.rect(display,black,(start,250,230,70),1)
                display_text('Play Again?', font_small, display, start+50, 250)
                pygame.draw.rect(display,black,(start+10,280,65,30),1)
                display_text('Yes', font_small, display, start+20, 275)
                pygame.draw.rect(display,black,(start+175,280,45,30),1)
                display_text('No', font_small, display, start+185, 275)
                pygame.display.update()
                while True:
                    b=0
                    for event in pygame.event.get():
                        position=pygame.mouse.get_pos()
                        if position[1]>=280 and position[1]<=310:
                            if not(position[0]>=start+10 and position[0]<=start+65):
                                pygame.draw.rect(display,black,(start+10,280,65,30),1)
                            if not(position[0]>=start+175 and position[0]<=start+220):
                                pygame.draw.rect(display,black,(start+175,280,45,30),1)
                        if position[1]>=280 and position[1]<=310:
                            if position[0]>=start+10 and position[0]<=start+65:
                                pygame.draw.rect(display,red,(start+10,280,65,30),1)
                            if position[0]>=start+175 and position[0]<=start+220:
                                pygame.draw.rect(display,red,(start+175,280,45,30),1)
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            if position[1]>=280 and position[1]<=310:
                                if position[0]>=start+10 and position[0]<=start+65:
                                    flag=1
                                    b=1
                                    break
                                if position[0]>=start+175 and position[0]<=start+220:
                                    flag=0
                                    b=1
                                    break
                        pygame.display.update()
                    if b==1:
                        break
                if flag==0:
                    break



        except Exception as error:
            print("There was an issue with the Game!")
            print(error)

        pygame.quit()
        sys.exit()


run = Run()
run.run()