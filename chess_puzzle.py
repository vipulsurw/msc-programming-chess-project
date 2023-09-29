def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
	return int(ord(loc[0])-96), int(loc[1])
    
	
def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
	return str(str(chr(ord('`')+x))+str(y))

class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
	self.x = pos_X
	self.y = pos_Y
	self.side = side_
	


Board = tuple[int, list[Piece]]


def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B''' 
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return True
    return False
	
def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
	for x in B[1]:
      if (pos_X, pos_Y) == (x.pos_x, x.pos_y):
          return x

class Bishop(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
	self.unicode = '\u2657' if side_ else '\u265D'
	super().__init__(pos_X, pos_Y, side_)

	
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        '''
	dx = abs(pos_X - self.pos_x)
        dy = abs(pos_Y - self.pos_y)
        if dx != dy:
            return False
        if is_piece_at(pos_X, pos_Y, B) and piece_at(pos_X, pos_Y, B).side == self.side:
            return False
        if pos_X > self.pos_x:
            x_dir = 1
        else:
            x_dir = -1
        if pos_Y > self.pos_y:
            y_dir = 1
        else:
            y_dir = -1
        for i in range(1, dx):
            if is_piece_at(self.pos_x + i*x_dir, self.pos_y + i*y_dir, B):
                return False
        return True

   
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        '''
	
	if not self.can_reach(pos_X, pos_Y, B):
        return False

    	captured_piece = None
    	if is_piece_at(pos_X, pos_Y, B):
		captured_piece = piece_at(pos_X, pos_Y, B)
        	B[1].remove(captured_piece)
    
    	orig_pos_x, orig_pos_y = self.pos_x, self.pos_y
    	self.pos_x, self.pos_y = pos_X, pos_Y
    	is_valid = not is_check(self.side, B)

    	self.pos_x, self.pos_y = orig_pos_x, orig_pos_y
    	if captured_piece:
        	B[1].append(captured_piece)

    	return is_valid


    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
	if is_piece_at(pos_X, pos_Y, B):
            captured_piece = piece_at(pos_X, pos_Y, B)
            B[1].remove(captured_piece)
        self.pos_x = pos_X
        self.pos_y = pos_Y
        return B


class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
	self.unicode = '\u2654' if side_ else '\u265A'
	super().__init__(pos_X, pos_Y, side_)

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''
	
	
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
	if not self.can_reach(pos_X, pos_Y, B):
        return False

        captured_piece = None
        if is_piece_at(pos_X, pos_Y, B):
        captured_piece = piece_at(pos_X, pos_Y, B)
        B[1].remove(captured_piece)
    
        orig_pos_x, orig_pos_y = self.pos_x, self.pos_y
        self.pos_x, self.pos_y = pos_X, pos_Y
        is_valid = not is_check(self.side, B)

        self.pos_x, self.pos_y = orig_pos_x, orig_pos_y
        if captured_piece:
          B[1].append(captured_piece)

        return is_valid

	
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
	if is_piece_at(pos_X, pos_Y, B):
            captured_piece = piece_at(pos_X, pos_Y, B)
            B[1].remove(captured_piece)
        self.pos_x = pos_X
        self.pos_y = pos_Y
        return B

def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    king = None
    for piece in B[1]:
        if isinstance(piece, King) and piece.side == side:
            king = piece
            break
    if king is None:
        return False
    
    for piece in B[1]:
        if piece.side == side:
            continue
        if piece.can_reach(king.pos_x, king.pos_y, B):
            return True
        
    return False

def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side
    Hints: 
    - use is_check
    - use can_move_to
    '''
    if not is_check(side, B):
        return False

    #Check if the king can move to a safe square
    king = None
    for piece in B[1]:
        if isinstance(piece, King) and piece.side == side:
            king = piece
            break
    if king is None:
        return False

    for x in range(king.pos_x - 1, king.pos_x + 2):
        for y in range(king.pos_y - 1, king.pos_y + 2):
            if king.can_reach(x, y, B) and not is_check(side, (B[0], B[1] + [King(x, y, side)])):
                return False

    #Check if any piece can block the check or capture the attacker
    for piece in B[1]:
        if piece.side != side:
            for x in range(8):
                for y in range(8):
                    if piece.can_reach(x, y, B) and not is_check(side, (B[0], B[1] + [type(piece)(x, y, piece.side)])):
                        return False

    #Check if the king can be captured
    for piece in B[1]:
        if piece.side != side:
            if piece.can_reach(king.pos_x, king.pos_y, B):
                return True

    # If none of the above cases is true, it's a stalemate
    return True

def is_stalemate(side: bool, B: Board) -> bool:
	'''
    	checks if configuration of B is stalemate for side

    	Hints: 
    	- use is_check
    	- use can_move_to 
    	'''
	if is_check(side, B):
        return False

    	# Check if the side has any valid moves
    	for piece in B[1]:
        	if piece.side == side:
            		for x in range(8):
                		for y in range(8):
                    			if piece.can_move_to(x, y, B):
                        			return False
    
    	return True
    


 
def read_board(filename: str) -> Board:
    with open(filename, 'r') as f:
        # Read board size
        board_size = int(f.readline().strip())

        # Read white pieces
        white_pieces = []
        white_piece_locations = [piece.strip() for piece in f.readline().split(',')]
        for location in white_piece_locations:
            piece_type = location[0]
            x, y = location2index(location[1:])
            piece = None
            if piece_type == 'B':
                piece = Bishop(x, y, True)
            elif piece_type == 'K':
                piece = King(x, y, True)
            if piece is not None:
                white_pieces.append(piece)

        # Read black pieces
        black_pieces = []
        black_piece_locations = [piece.strip() for piece in f.readline().split(',')]
        for location in black_piece_locations:
            piece_type = location[0]
            x, y = location2index(location[1:])
            piece = None
            if piece_type == 'B':
                piece = Bishop(x, y, False)
            elif piece_type == 'K':
                piece = King(x, y, False)
            if piece is not None:
                black_pieces.append(piece)

        # Create board tuple
        board = (board_size, white_pieces + black_pieces)

    return board



     


def save_board(filename: str, B: Board) -> None:
	'''saves board configuration into file in current directory in plain format'''
	size, pieces = B
    	white_pieces = [f"{piece.__class__.__name__[0]}{index2location(piece.pos_x, piece.pos_y)}" for piece in pieces if piece.side]
    	black_pieces = [f"{piece.__class__.__name__[0]}{index2location(piece.pos_x, piece.pos_y)}" for piece in pieces if not piece.side]
    	lines = [f"{size}\n", f"{', '.join(white_pieces)}\n", f"{', '.join(black_pieces)}\n"]
    	with open(filename, 'x') as f:
        f.writelines(lines)


def find_black_move(B: Board) -> tuple[Piece, int, int]:
	'''
    	returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    	assumes there is at least one black piece that can move somewhere

    	Hints: 
    	- use methods of random library
    	- use can_move_to
    	'''
	for piece in B[1]:
        if piece.side == False: 
            for x in range(8):
                for y in range(8):
                    if piece.can_move_to(x, y, B):
                        return (piece, x, y)
    return None
    



def conf2unicode(board: Board) -> str:
    '''converts board configuration to unicode format string (see section Unicode board configurations)'''
    space_char = '\u2001'
    board_size, pieces_list = board
    board_array = [[space_char] * board_size for _ in range(board_size)]
    for piece in pieces_list:
        # y starts from bottom upwards
        i = board_size - piece.pos_y
        j = piece.pos_x - 1
        board_array[i][j] = piece.unicode
    return '\n'.join(''.join(s) for s in board_array)


def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''  
    while True:
      filename = input("File name for initial configuration: ")  
      board = read_board(filename)
      print('\nThe initial configuration is:')
      print(conf2unicode(board) + '\n')
    # White's move
      white_move = input("Next move of White: ")
      if white_move == "QUIT":
        # Save the current configuration to a file
        filename = input("File name to store the configuration: ")
        save_board(filename, board)
        print("The game configuration saved.")
        break
      if not is_check(True, board):
        print("This is not a valid move.")
      else:
        board = save_board(filename, board)
        print(conf2unicode(board) + '\n')
        if is_checkmate(False, board):
            print("Game over. White wins.")
            break
        elif is_stalemate(False, board):
            print("Game over. Stalemate.")
            break
        else:
            # Black's move
            black_move = find_black_move(board)
            board = make_move(board, black_move)
            print("Next move of Black is", black_move)
            print(conf2unicode(board) + '\n')
            if is_checkmate(True, board):
                print("Game over. Black wins.")
                break
            elif is_stalemate(True, board):
                print("Game over. Stalemate.")
                break
	

if __name__ == '__main__': #keep this in
   main()
