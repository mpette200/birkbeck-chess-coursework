import readline
from typing import TextIO, Optional

# if not blank need to include trailing slash in FILEPATH
FILEPATH = ''
MSG_IOERROR = 'file input/output is not valid'
CMD_QUIT = 'QUIT'


def location2index(loc: str) -> tuple[int, int]:
    '''Converts chess location to corresponding x and y coordinates.
    Raises an IOError if the input is not a valid chess location.
    Assumed the input string will always be of length at least 2.
    Bounds checking is not done so the return value needs to be
    checked by the caller. Example:
    >>> location2index('b5')
    (2, 5)
    '''
    letter = loc[0]
    digits = loc[1:]
    x = 1 + ord(letter) - ord('a')
    if x < 1 or x > 26 or not digits.isdigit():
        raise IOError(f"'{loc}' {MSG_IOERROR}")
    y = int(digits)
    if y < 1:
        raise IOError(f"'{loc}' {MSG_IOERROR}")
    return x, y


def index2location(x: int, y: int) -> str:
    '''Converts pair of coordinates to corresponding location.
    Assumes that x and y will always be within bounds and does
    not check. Example:
    >>> index2location(3, 16)
    'c16'
    '''
    letter = chr(x - 1 + ord('a'))
    return f'{letter}{y}'


class Piece:
    pos_x: int
    pos_y: int
    side: bool  # True for White and False for Black
    unicode: str

    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values'''
        if not (side_ is True or side_ is False):
            raise ValueError('side_ must be True or False')
            # can get hard to find bugs if side_ is for example NoneType
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_

    # type hint 'Board' is in quotes because it cannot be defined until
    # Piece has been defined (forward reference)
    @staticmethod
    def create_pieces(csv: str, side_: bool, B: 'Board') -> None:
        '''Populates board from text data given as a comma separated list.
        Creates each new piece of the specified type at the given location
        and pushes onto board array. Raises IOError if location out of bounds,
        or invalid piece type, or space already occupied, or not exactly
        one King is added, or if input string is empty.
        Example:
        >>> board = (5, [])
        >>> Piece.create_pieces('Kd2, Ra1', True, board)
        >>> board
        (5, [King(4, 2, white), Rook(1, 1, white)])
        '''
        piece_defs = {'K': King, 'B': Bishop, 'R': Rook}
        count_kings = 0
        size, pieces = B

        for piece_info in csv.split(','):
            piece_info = piece_info.strip()
            if len(piece_info) < 3:
                raise IOError(f'\'{csv}\' {MSG_IOERROR}')

            # get type
            piece_type = piece_info[0]
            if piece_type == 'K':
                count_kings += 1

            # get location
            loc = piece_info[1:]
            x, y = location2index(loc)
            if x > size or y > size or is_piece_at(x, y, B):
                raise IOError(f'\'{csv}\' {MSG_IOERROR}')

            # create piece
            if piece_type in piece_defs:
                constructor = piece_defs[piece_type]
            else:
                raise IOError(f'\'{csv}\' {MSG_IOERROR}')
            piece = constructor(x, y, side_)
            pieces.append(piece)

        if count_kings != 1:
            raise IOError(f'\'{csv}\' {MSG_IOERROR}')

    @staticmethod
    def is_inbounds(pos_X: int, pos_Y: int, B: 'Board') -> bool:
        '''Returns true if the destination is within the boundary of the board
        Example:
        >>> b = (4, [])
        >>> Piece.is_inbounds(1, 1, b)
        True
        >>> Piece.is_inbounds(1, 5, b)
        False
        '''
        size = B[0]
        x_inbounds = 0 < pos_X <= size
        y_inbounds = 0 < pos_Y <= size
        return x_inbounds and y_inbounds

    def is_destination_blocked(
            self, pos_X: int, pos_Y: int, B: 'Board') -> bool:
        '''Checks whether destination square is empty or occupied by
        a piece of the same or a different colour. If different colour the
        piece can be captured; if same colour the piece blocks the destination.
        Example:
        >>> b = read_board('board_small_valid.txt')
        >>> Kd2 = piece_at(4, 2, b)
        >>> fmt = 'Kd2.is_destination_blocked({}, {}, b) -> {}'
        >>> for i in range(1, 3):
        ...     for j in range(1, 4):
        ...         ans = Kd2.is_destination_blocked(i, j, b)
        ...         print(fmt.format(i, j, ans))
        ...
        Kd2.is_destination_blocked(1, 1, b) -> True
        Kd2.is_destination_blocked(1, 2, b) -> True
        Kd2.is_destination_blocked(1, 3, b) -> False
        Kd2.is_destination_blocked(2, 1, b) -> False
        Kd2.is_destination_blocked(2, 2, b) -> True
        Kd2.is_destination_blocked(2, 3, b) -> False
        '''
        if is_piece_at(pos_X, pos_Y, B):
            piece = piece_at(pos_X, pos_Y, B)
            # is also True if the piece coincides with itself
            return piece.side == self.side
        return False

    def can_reach(self, pos_X: int, pos_Y: int, B: 'Board') -> bool:
        '''Abstract method needs listing here to avoid Mypy warnings.
        '''

    def __eq__(self, P: object) -> bool:
        if not isinstance(P, Piece):
            raise NotImplementedError()
        return self.pos_x == P.pos_x \
            and self.pos_y == P.pos_y \
            and self.side == P.side \
            and type(self) == type(P)

    def __ne__(self, P: object) -> bool:
        return not self.__eq__(P)

    def __str__(self) -> str:
        '''For example:  King(4, 2, white)'''
        name = self.__class__.__name__
        side = 'white' if self.side else 'black'
        return f'{name}({self.pos_x}, {self.pos_y}, {side})'

    def __repr__(self) -> str:
        return self.__str__()


Board = tuple[int, list[Piece]]


def is_piece_at(pos_X: int, pos_Y: int, B: Board) -> bool:
    '''Checks if there is piece at coordinates pox_X, pos_Y of board B.
    Assumes that x and y will always be within bounds and does not check.
    Example:
    >>> b = (5, [])
    >>> Piece.create_pieces('Kd2, Ra1', True, b)
    >>> is_piece_at(1, 1, b)
    True
    '''
    size, pieces = B
    return any(p.pos_x == pos_X and p.pos_y == pos_Y for p in pieces)


def piece_at(pos_X: int, pos_Y: int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    Example:
    >>> b = (5, [])
    >>> Piece.create_pieces('Kd2, Ra1', True, b)
    >>> piece_at(1, 1, b)
    Rook(1, 1, white)
    '''
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            break
    # return needs to be outside loop for MyPy type checking
    return piece


class Rook(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
        self.unicode = '\u2656' if side_ else '\u265C'

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule2] and [Rule4](see section Intro)
        Hint: use is_piece_at
        '''
        inbounds = Piece.is_inbounds(pos_X, pos_Y, B)
        in_defined_moves = self.in_defined_moves(pos_X, pos_Y)
        if inbounds and in_defined_moves:
            is_blocked = self.is_destination_blocked(pos_X, pos_Y, B)
            is_leap_over = self.is_leap_over(pos_X, pos_Y, B)
            return not is_leap_over and not is_blocked
        else:
            return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules

        Hints:
        - firstly, check [Rule2] and [Rule4] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule5], use is_check on new board

        Example:
        >>> from io import StringIO
        >>> b = read_board_txt(StringIO("""4
        ... Kd2, Ra1, Bb2
        ... Rb4, Kd4"""))
        >>> Rb4 = piece_at(2, 4, b)
        >>> for i in range(1, 5):
        ...     for j in range(1, 5):
        ...         if Rb4.can_move_to(i, j, b):
        ...             print(f'Rb4 can move -> ({i}, {j})')
        ...
        Rb4 can move -> (2, 2)
        '''
        captured_piece = None
        if self.can_reach(pos_X, pos_Y, B):
            if is_piece_at(pos_X, pos_Y, B):
                captured_piece = piece_at(pos_X, pos_Y, B)
                B[1].remove(captured_piece)

            # temporarily move the piece to see if in check
            orig_X = self.pos_x
            orig_Y = self.pos_y
            self.pos_x = pos_X
            self.pos_y = pos_Y
            is_valid = not is_check(self.side, B)

            # reverse move and replace captured piece
            self.pos_x = orig_X
            self.pos_y = orig_Y
            if captured_piece is not None:
                B[1].append(captured_piece)
            return is_valid
        else:
            return False

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates
        pos_X, pos_Y on board B assumes this move is valid according to
        chess rules
        WARNING: this mutates the original board and then
        returns a reference to the mutated board.
        '''
        # WARNING: this mutates the original board
        if is_piece_at(pos_X, pos_Y, B):
            captured_piece = piece_at(pos_X, pos_Y, B)
            B[1].remove(captured_piece)
        self.pos_x = pos_X
        self.pos_y = pos_Y
        return B

    def in_defined_moves(self, pos_X: int, pos_Y: int) -> bool:
        '''Rooks can only move along a row or a column.
        Returns true if the move is along a row or column.
        Checking for zero move is done elsewhere.
        Example:
        >>> Rc3 = Rook(3, 3, True)
        >>> b = (5, [Rc3])
        >>> for x in range(1, 6):
        ...     for y in range(1, 6):
        ...         if Rc3.in_defined_moves(x, y):
        ...             print(f'{x}, {y} is in defined moves')
        ...
        1, 3 is in defined moves
        2, 3 is in defined moves
        3, 1 is in defined moves
        3, 2 is in defined moves
        3, 3 is in defined moves
        3, 4 is in defined moves
        3, 5 is in defined moves
        4, 3 is in defined moves
        5, 3 is in defined moves
        '''
        is_same_row = self.pos_y == pos_Y
        is_same_column = self.pos_x == pos_X
        return is_same_row or is_same_column

    def is_leap_over(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        Checks whether piece needs to leap over another piece
        to reach destination. Assumes destination is a valid move for
        the piece. Does not include the start square or finish square.
        Example:
        >>> b = read_board('board_small_valid.txt')
        >>> Ra4 = piece_at(1, 4, b)
        >>> Ra4.is_leap_over(1, 2, b)
        False
        >>> Ra4.is_leap_over(1, 1, b)
        True
        '''
        is_same_row = self.pos_y == pos_Y
        is_same_column = self.pos_x == pos_X
        if is_same_row:
            # important 1 + ...
            start = 1 + min(self.pos_x, pos_X)
            stop = max(self.pos_x, pos_X)
            path = ((x, pos_Y) for x in range(start, stop))
        elif is_same_column:
            # important 1 + ...
            start = 1 + min(self.pos_y, pos_Y)
            stop = max(self.pos_y, pos_Y)
            path = ((pos_X, y) for y in range(start, stop))
        # path does not include final destination or starting square
        # path may also be in reverse order
        return any(is_piece_at(x, y, B) for x, y in path)


class Bishop(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
        self.unicode = '\u2657' if side_ else '\u265D'

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this bishop can move to coordinates pos_X, pos_Y on
        board B according to rule [Rule1] and [Rule4]'''
        inbounds = Piece.is_inbounds(pos_X, pos_Y, B)
        in_defined_moves = self.in_defined_moves(pos_X, pos_Y)
        if inbounds and in_defined_moves:
            is_blocked = self.is_destination_blocked(pos_X, pos_Y, B)
            is_leap_over = self.is_leap_over(pos_X, pos_Y, B)
            return not is_leap_over and not is_blocked
        else:
            return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this bishop can move to coordinates pos_X, pos_Y on
        board B according to all chess rules
        Example:
        >>> from io import StringIO
        >>> b = read_board_txt(StringIO("""4
        ... Kd2, Ra4
        ... Bc2, Kd4, Rd1"""))
        >>> Bc2 = piece_at(3, 2, b)
        >>> for i in range(1, 5):
        ...     for j in range(1, 5):
        ...         if Bc2.can_move_to(i, j, b):
        ...             print(f'Bc2 can move -> ({i}, {j})')
        ...
        Bc2 can move -> (1, 4)
        '''
        captured_piece = None
        if self.can_reach(pos_X, pos_Y, B):
            if is_piece_at(pos_X, pos_Y, B):
                captured_piece = piece_at(pos_X, pos_Y, B)
                B[1].remove(captured_piece)

            # temporarily move the piece to see if in check
            orig_X = self.pos_x
            orig_Y = self.pos_y
            self.pos_x = pos_X
            self.pos_y = pos_Y
            is_valid = not is_check(self.side, B)

            # reverse move and replace captured piece
            self.pos_x = orig_X
            self.pos_y = orig_Y
            if captured_piece is not None:
                B[1].append(captured_piece)
            return is_valid
        else:
            return False

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns new board resulting from move of this bishop to coordinates
        pos_X, pos_Y on board B assumes this move is valid according to
        chess rules
        WARNING: this mutates the original board and then
        returns a reference to the mutated board.
        '''
        # WARNING: this mutates the original board
        if is_piece_at(pos_X, pos_Y, B):
            captured_piece = piece_at(pos_X, pos_Y, B)
            B[1].remove(captured_piece)
        self.pos_x = pos_X
        self.pos_y = pos_Y
        return B

    def in_defined_moves(self, pos_X: int, pos_Y: int) -> bool:
        '''Bishops can only move along diagonals.
        Returns true if move is along a diagonal.
        Checking for zero move is done elsewhere.
        '''
        is_diagonal = abs(pos_X - self.pos_x) == abs(pos_Y - self.pos_y)
        return is_diagonal

    def is_leap_over(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        Checks whether piece needs to leap over another piece
        to reach destination. Assumes destination is a valid move for
        the piece. Does not include the start square or finish square.
        '''
        # important 1 + ...
        start_x = 1 + min(self.pos_x, pos_X)
        stop_x = max(self.pos_x, pos_X)
        x_range = range(start_x, stop_x)

        # important 1 + ...
        start_y = 1 + min(self.pos_y, pos_Y)
        stop_y = max(self.pos_y, pos_Y)
        y_range = range(start_y, stop_y)

        path = ((x, y) for x, y in zip(x_range, y_range))
        # path does not include final destination or starting square
        # path may also be in reverse order
        return any(is_piece_at(x, y, B) for x, y in path)


class King(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)
        self.unicode = '\u2654' if side_ else '\u265A'

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on
        board B according to rule [Rule3] and [Rule4]'''
        inbounds = Piece.is_inbounds(pos_X, pos_Y, B)
        in_defined_moves = self.in_defined_moves(pos_X, pos_Y)
        if inbounds and in_defined_moves:
            is_blocked = self.is_destination_blocked(pos_X, pos_Y, B)
            return not is_blocked
        else:
            return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on
        board B according to all chess rules
        Example:
        >>> from io import StringIO
        >>> b = read_board_txt(StringIO("""4
        ... Kd2, Ra1, Bb2
        ... Rb4, Kd4"""))
        >>> Kd4 = piece_at(4, 4, b)
        >>> for i in range(1, 5):
        ...     for j in range(1, 5):
        ...         if Kd4.can_move_to(i, j, b):
        ...             print(f'Kd4 can move -> ({i}, {j})')
        ...
        Kd4 can move -> (3, 4)
        '''
        captured_piece = None
        if self.can_reach(pos_X, pos_Y, B):
            if is_piece_at(pos_X, pos_Y, B):
                captured_piece = piece_at(pos_X, pos_Y, B)
                B[1].remove(captured_piece)

            # temporarily move the piece to see if in check
            orig_X = self.pos_x
            orig_Y = self.pos_y
            self.pos_x = pos_X
            self.pos_y = pos_Y
            is_valid = not is_check(self.side, B)

            # reverse move and replace captured piece
            self.pos_x = orig_X
            self.pos_y = orig_Y
            if captured_piece is not None:
                B[1].append(captured_piece)
            return is_valid
        else:
            return False

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates
        pos_X, pos_Y on board B assumes this move is valid according to
        chess rules
        WARNING: this mutates the original board and then
        returns a reference to the mutated board.
        '''
        # WARNING: this mutates the original board
        if is_piece_at(pos_X, pos_Y, B):
            captured_piece = piece_at(pos_X, pos_Y, B)
            B[1].remove(captured_piece)
        self.pos_x = pos_X
        self.pos_y = pos_Y
        return B

    def in_defined_moves(self, pos_X: int, pos_Y: int) -> bool:
        '''King can only move 1 square in any direction.
        Returns true if the move is 1 square in any direction.
        Checking for zero move is done elsewhere.
        '''
        x_delta = abs(self.pos_x - pos_X)
        y_delta = abs(self.pos_y - pos_Y)
        return x_delta <= 1 and y_delta <= 1


def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    get_king = filter(lambda p: type(p) is King and p.side == side, B[1])
    king = next(get_king)
    pieces = filter(lambda p: p.side != side, B[1])
    return any(p.can_reach(king.pos_x, king.pos_y, B) for p in pieces)


def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints:
    - use is_check
    - use can_reach
    '''


def read_board(filename: str) -> Board:
    '''
    Reads board configuration from file in current directory in plain format.
    Raises IOError exception if file is not valid (see section Plain board
    configurations). Raises FileNotFoundError if valid file cannot be located.
    Example:
    >>> from pprint import pprint
    >>> pprint(read_board('board_examp.txt'))
    (5,
     [Bishop(1, 1, white),
      Rook(1, 2, white),
      Bishop(5, 2, white),
      Rook(1, 5, white),
      King(3, 5, white),
      King(2, 3, black),
      Rook(4, 3, black),
      Rook(2, 4, black),
      Rook(5, 4, black)])
    '''
    fullname = FILEPATH + filename
    with open(fullname, 'r') as f:
        board = read_board_txt(f)
    return board


def read_board_txt(stream: TextIO) -> Board:
    """Reads board configuration from a text IO stream.
    Raises IOError exception if text does not represent
    a valid board. Example:
    >>> from io import StringIO
    >>> stream = StringIO('''4
    ... Kd2
    ... Kd4''')
    >>> read_board_txt(stream)
    (4, [King(4, 2, white), King(4, 4, black)])
    """
    def tolerant_readline(stream: TextIO) -> str:
        'fault tolerant readline that re-raises IOError upon any exception'
        try:
            line = stream.readline().strip()
        except Exception:
            raise IOError(f'file {MSG_IOERROR}')
        return line

    # read size
    line1 = tolerant_readline(stream)
    if not line1.isdigit():
        raise IOError(f"'{line1}' {MSG_IOERROR}")
    size = int(line1)
    if size < 2 or size > 26:
        raise IOError(f"'{line1}' {MSG_IOERROR}")

    # populate white pieces
    board: Board = (size, [])
    white_data = tolerant_readline(stream)
    Piece.create_pieces(white_data, True, board)

    # add black pieces
    black_data = tolerant_readline(stream)
    Piece.create_pieces(black_data, False, board)
    return board


def save_board(filename: str) -> None:
    '''saves board configuration into file in current directory in plain format'''


def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y
    according to chess rules assumes there is at least one black piece that
    can move somewhere

    Hints:
    - use methods of random library
    - use can_move_to
    '''


def conf2unicode(B: Board) -> str:
    '''converts board cofiguration B to unicode format string
    (see section Unicode board configurations)'''
    space = '\u2001'
    size, pieces = B
    piece_array = [[space] * size for _ in range(size)]
    for p in pieces:
        # y starts from bottom upwards
        i = size - p.pos_y
        j = p.pos_x - 1
        piece_array[i][j] = p.unicode
    return '\n'.join(''.join(s) for s in piece_array)


def prompt_file() -> Optional[Board]:
    '''Prompts user for file, keeps asking until a valid file provided
    or the user typed 'QUIT'. Returns the board populated with pieces
    or None if user typed 'QUIT'.
    '''
    # trick for tab: autocompletion
    readline.parse_and_bind('tab: complete')
    board = None
    err_msg = ''
    prompt_msg = 'File name for initial configuration:\n'
    while True:
        user_input = input(err_msg + prompt_msg)
        if user_input == CMD_QUIT:
            break
        try:
            board = read_board(user_input)
            break
        except IOError:
            # IOError is alias for OSError
            # and also parent of FileNotFoundError
            err_msg = '\nThis is not a valid file. '
    # end tab completion
    readline.parse_and_bind('tab: ""')
    return board


def main() -> None:
    '''
    Runs the play, using a text input prompt
    1. Ask for 'File name for initial configuration', keeps asking until
    a valid file provided or user types 'QUIT'.

    2. Loads board from the file and displays initial configuration on
    the screen.

    3. Ask for 'Next move of White', keeps asking until game over or user
    types 'QUIT'.

    4. After white's move update the board and display on the screen.

    5. After black's move print message stating 'Next move of Black is ...'
    and display on screen.

    6. If user types 'QUIT' prompt for 'File name to store the configuration'

    7. After game over, print winner.
    '''
    while True:
        board = prompt_file()
        if board is None:
            return
        print('\nThe initial configuration is:')
        print(conf2unicode(board) + '\n')


if __name__ == '__main__':  # keep this in
    main()
