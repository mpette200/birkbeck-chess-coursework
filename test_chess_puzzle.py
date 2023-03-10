import pytest
from io import StringIO
from chess_puzzle import \
    Piece, Bishop, King, Rook, Board, MSG_IOERROR, \
    location2index, index2location, is_piece_at, piece_at, \
    is_check, is_checkmate, read_board, conf2unicode, read_board_txt

# --------------------------------
# Initial tests from starter code
# --------------------------------


def test_location2index1() -> None:
    assert location2index("e2") == (5, 2)


def test_index2location1() -> None:
    assert index2location(5, 2) == "e2"


wb1 = Bishop(1, 1, True)
wr1 = Rook(1, 2, True)
wb2 = Bishop(5, 2, True)
bk = King(2, 3, False)
br1 = Rook(4, 3, False)
br2 = Rook(2, 4, False)
br3 = Rook(5, 4, False)
wr2 = Rook(1, 5, True)
wk = King(3, 5, True)

B1 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
'''
♖ ♔  
 ♜  ♜
 ♚ ♜ 
♖   ♗
♗    
'''


def test_is_piece_at1() -> None:
    assert not is_piece_at(2, 2, B1)


def test_piece_at1() -> None:
    assert piece_at(4, 3, B1) is br1


def test_can_reach1() -> None:
    assert not wr2.can_reach(4, 5, B1)


br2a = Rook(1, 5, False)
wr2a = Rook(2, 5, True)


def test_can_move_to1() -> None:
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2a, wk])
    assert not wr2a.can_move_to(2, 4, B2)


def test_is_check1() -> None:
    wr2b = Rook(2, 4, True)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2b, wk])
    assert is_check(True, B2)


def test_is_checkmate1() -> None:
    br2b = Rook(4, 5, False)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2b, br3, wr2, wk])
    assert is_checkmate(True, B2)


def test_read_board1() -> None:
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  # we check if every piece in B is also present in B1;
        # if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y \
                    and type(piece) == type(piece1) \
                    and piece.side == piece1.side:
                found = True
        assert found

    for piece1 in B1[1]:  # we check if every piece in B1 is also present
        # in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y \
                    and type(piece) == type(piece1) \
                    and piece.side == piece1.side:
                found = True
        assert found


def test_conf2unicode1() -> None:
    assert conf2unicode(B1) == "♖ ♔  \n ♜  ♜\n ♚ ♜ \n♖   ♗\n♗    "


# --------------------------------
# Test board reading and creation
# --------------------------------
class TestBoardCreation:
    def test_location2index_valid(self) -> None:
        assert location2index('a1') == (1, 1)
        assert location2index('z26') == (26, 26)
        assert location2index('c7') == (3, 7)
        assert location2index('c8') == (3, 8)
        assert location2index('g12') == (7, 12)

    @pytest.mark.parametrize('locations', [
        'bb',  # don't accept missing row number
        'D3',  # don't accept capital letter
        'ab95',  # out of range
        'a-9'  # negative number not accepted
    ])
    def test_location2index_errors(self, locations: str) -> None:
        with pytest.raises(IOError):
            location2index(locations)

    def test_index2location(self) -> None:
        assert index2location(1, 5) == 'a5'
        assert index2location(26, 1) == 'z1'
        assert index2location(3, 5) == 'c5'
        assert index2location(5, 15) == 'e15'
        assert index2location(2, 4) == 'b4'

    def board_small_valid(self) -> Board:
        '''Small board for use across multiple tests
        4
        Kd2, Ra1, Bb2, Ba2
        Bb3, Ra4, Kd4, Rc3
        ♜  ♚
         ♝♜ 
        ♗♗ ♔
        ♖   
        '''
        white = True
        black = False
        wk4_2 = King(4, 2, white)
        wr1_1 = Rook(1, 1, white)
        wb2_2 = Bishop(2, 2, white)
        wb1_2 = Bishop(1, 2, white)
        bb2_3 = Bishop(2, 3, black)
        br1_4 = Rook(1, 4, black)
        bk4_4 = King(4, 4, black)
        br3_3 = Rook(3, 3, black)

        # change the order around to be sure test doesn't depend on order
        b = (4, [wr1_1, wb2_2, wb1_2, wk4_2,
                 bb2_3, br1_4, br3_3, bk4_4])
        return b

    def test_is_piece_at_occupied(self) -> None:
        board = self.board_small_valid()
        assert is_piece_at(1, 1, board)
        assert is_piece_at(1, 2, board)
        assert is_piece_at(1, 4, board)
        assert is_piece_at(2, 2, board)
        assert is_piece_at(2, 3, board)
        assert is_piece_at(3, 3, board)
        assert is_piece_at(4, 2, board)
        assert is_piece_at(4, 4, board)

    def test_is_piece_at_empty_squares(self) -> None:
        board = self.board_small_valid()
        assert not is_piece_at(1, 3, board)
        assert not is_piece_at(2, 1, board)
        assert not is_piece_at(2, 4, board)
        assert not is_piece_at(3, 1, board)
        assert not is_piece_at(3, 2, board)
        assert not is_piece_at(3, 4, board)
        assert not is_piece_at(4, 1, board)
        assert not is_piece_at(4, 3, board)

    def test__eq__and__ne__(self) -> None:
        '''test overloaded == operator because it is
        important for other tests'''
        white = True
        black = False

        # side / colour is different
        assert King(2, 3, white) != King(2, 3, black)

        # x-coord is different
        assert King(2, 3, white) != King(3, 3, white)

        # y-coord is different
        assert King(2, 3, white) != King(2, 2, white)

        # piece type is different
        assert King(2, 3, white) != Rook(2, 3, white)

        # check that these all match
        assert King(2, 3, white) == King(2, 3, white)
        assert Rook(4, 2, black) == Rook(4, 2, black)
        assert Bishop(16, 3, black) == Bishop(16, 3, black)

    def test_piece_at_small_valid(self) -> None:
        '''relies on overloaded == operator'''
        white = True
        black = False
        board = self.board_small_valid()
        assert piece_at(1, 1, board) == Rook(1, 1, white)
        assert piece_at(2, 3, board) == Bishop(2, 3, black)
        assert piece_at(3, 3, board) == Rook(3, 3, black)
        assert piece_at(4, 2, board) == King(4, 2, white)
        assert piece_at(4, 4, board) == King(4, 4, black)

    def test_read_board_valid(self) -> None:
        '''relies on overloaded == operator'''
        size_a, pieces_a = self.board_small_valid()
        size_b, pieces_b = read_board('board_small_valid.txt')
        assert size_a == size_b
        assert all(p in pieces_a for p in pieces_b)
        assert all(p in pieces_b for p in pieces_a)

    @pytest.mark.parametrize('filenames', [
        'board_missing_row.txt',
        'board_no_black_king.txt',
        'board_no_white_king.txt',
        'board_out_of_bounds.txt',
        'board_two_coincide.txt',
        'board_small_valid.png',
    ])
    def test_read_board_errors(self, filenames: str) -> None:
        with pytest.raises(IOError) as excinfo:
            read_board(filenames)
        # IOError is alias of OSError since python 3.3
        # and FileNotFoundError is a subclass of this
        # this test should ignore any FileNotFoundError
        assert not isinstance(excinfo.value, FileNotFoundError)
        assert MSG_IOERROR in str(excinfo.value)

    def test_read_board_filenotfound(self) -> None:
        with pytest.raises(FileNotFoundError):
            read_board('NO__SUCH__FILE')

    def test_conf2unicode_diff_piece_types(self) -> None:
        white_Rb2: Piece = Rook(2, 2, True)
        white_Kb2: Piece = King(2, 2, True)
        white_Bb2: Piece = Bishop(2, 2, True)

        black_Rb2: Piece = Rook(2, 2, False)
        black_Kb2: Piece = King(2, 2, False)
        black_Bb2: Piece = Bishop(2, 2, False)

        # white pieces
        b = (3, [white_Rb2])
        assert conf2unicode(b) == '   \n ♖ \n   '
        b = (3, [white_Kb2])
        assert conf2unicode(b) == '   \n ♔ \n   '
        b = (3, [white_Bb2])
        assert conf2unicode(b) == '   \n ♗ \n   '

        # black pieces
        b = (3, [black_Rb2])
        assert conf2unicode(b) == '   \n ♜ \n   '
        b = (3, [black_Kb2])
        assert conf2unicode(b) == '   \n ♚ \n   '
        b = (3, [black_Bb2])
        assert conf2unicode(b) == '   \n ♝ \n   '

    def test_conf2unicode_diff_locations(self) -> None:
        Ka1: Piece = King(1, 1, True)
        Ka3: Piece = King(1, 3, True)
        Kc1: Piece = King(3, 1, True)
        Kc3: Piece = King(3, 3, True)
        Kb1: Piece = King(2, 1, True)

        b = (3, [Ka1])
        assert conf2unicode(b) == '   \n   \n♔  '
        b = (3, [Ka3])
        assert conf2unicode(b) == '♔  \n   \n   '
        b = (3, [Kc1])
        assert conf2unicode(b) == '   \n   \n  ♔'
        b = (3, [Kc3])
        assert conf2unicode(b) == '  ♔\n   \n   '
        b = (3, [Kb1])
        assert conf2unicode(b) == '   \n   \n ♔ '


# --------------------------------
# Test moving of pieces
# --------------------------------
class TestMovePieces:

    def duplicate_board(self, board: Board) -> Board:
        'makes deep copy of board for testing'
        size = board[0]
        new_board: Board = (size, [])
        for piece in board[1]:
            x = piece.pos_x
            y = piece.pos_y
            side = piece.side
            if type(piece) is King:
                new_board[1].append(King(x, y, side))
            elif type(piece) is Rook:
                new_board[1].append(Rook(x, y, side))
            elif type(piece) is Bishop:
                new_board[1].append(Bishop(x, y, side))
        return new_board

    def test_rook_can_reach_same_row_or_column(self) -> None:
        Rc3: Piece = Rook(3, 3, False)
        board = (5, [Rc3])
        valid_destinations = [
            (1, 3),
            (2, 3),
            (4, 3),
            (5, 3),
            (3, 1),
            (3, 2),
            (3, 4),
            (3, 5)
        ]
        for x in range(1, 6):
            for y in range(1, 6):
                if (x, y) in valid_destinations:
                    assert Rc3.can_reach(x, y, board)
                else:
                    assert not Rc3.can_reach(x, y, board)

    # all of these assume that board reading is correct
    def rook_test_board(self) -> Board:
        '''
         ♜ ♚
            
         ♗ ♔
        ♖   
        '''
        layout = StringIO(
            '''4
            Kd2, Ra1, Bb2
            Rb4, Kd4''')
        return read_board_txt(layout)

    def test_rook_can_reach_valid_locs(self) -> None:
        board = self.rook_test_board()
        Rb4 = piece_at(2, 4, board)
        # left
        assert Rb4.can_reach(1, 4, board)
        # right
        assert Rb4.can_reach(3, 4, board)
        # down
        assert Rb4.can_reach(2, 3, board)
        # can capture other piece
        assert Rb4.can_reach(2, 2, board)

    def test_rook_can_reach_isfalse_ifinvalid(self) -> None:
        board = self.rook_test_board()
        Rb4 = piece_at(2, 4, board)
        # cannot go diagonal
        assert not Rb4.can_reach(3, 3, board)
        # cannot capture its own colour
        assert not Rb4.can_reach(4, 4, board)
        # cannot move to itself
        assert not Rb4.can_reach(2, 4, board)
        # cannot leap over
        assert not Rb4.can_reach(2, 1, board)
        # not a horizontal or vertical move
        assert not Rb4.can_reach(4, 2, board)

    def test_rook_can_move_to_leap_over(self) -> None:
        '''
        ♚      
           ♝   
               
         ♝ ♜ ♝ 
               
           ♝   
        ♔      
        '''
        b = read_board_txt(StringIO(
            '''7
            Ka1
            Ka7, Rd4, Bb4, Bd6, Bf4, Bd2'''
        ))
        copy_b = self.duplicate_board(b)
        Rd4 = piece_at(4, 4, b)
        valid_destinations = [
            (3, 4),
            (4, 5),
            (5, 4),
            (4, 3)
        ]
        for x in range(1, 8):
            for y in range(1, 8):
                if (x, y) in valid_destinations:
                    assert Rd4.can_move_to(x, y, b)
                else:
                    assert not Rd4.can_move_to(x, y, b)
        # check that original board is not modified
        assert b == copy_b

    def test_rook_can_move_to_out_of_check(self) -> None:
        board = self.rook_test_board()
        copy_board = self.duplicate_board(board)
        # king is in check so only valid move
        # is rook takes bishop b2
        Rb4 = piece_at(2, 4, board)
        only_valid_move = (2, 2)
        for x in range(1, 5):
            for y in range(1, 5):
                if (x, y) == only_valid_move:
                    assert Rb4.can_move_to(x, y, board)
                else:
                    assert not Rb4.can_move_to(x, y, board)
        # check that original board is not modified
        assert board == copy_board

    def test_bishop_can_reach_diagonals(self) -> None:
        Bc3: Piece = Bishop(3, 3, True)
        board = (5, [Bc3])
        valid_destinations = [
            (1, 5),
            (2, 4),
            (1, 1),
            (2, 2),
            (4, 4),
            (5, 5),
            (4, 2),
            (5, 1)
        ]
        for x in range(1, 6):
            for y in range(1, 6):
                if (x, y) in valid_destinations:
                    assert Bc3.can_reach(x, y, board)
                else:
                    assert not Bc3.can_reach(x, y, board)

    def bishop_test_board(self) -> Board:
        '''
         ♚  
         ♖  
          ♝♔
         ♜  
        '''
        layout = StringIO(
            '''4
            Kd2, Rb3
            Bc2, Kb4, Rb1''')
        return read_board_txt(layout)

    def test_bishop_can_reach_valid_locs(self) -> None:
        board = self.bishop_test_board()
        Bc2 = piece_at(3, 2, board)
        # can capture other piece
        assert Bc2.can_reach(2, 3, board)
        # right-up
        assert Bc2.can_reach(4, 3, board)
        # right-down
        assert Bc2.can_reach(4, 1, board)

    def test_bishop_can_reach_isfalse_if_invalid(self) -> None:
        board = self.bishop_test_board()
        Bc2 = piece_at(3, 2, board)
        # cannot capture its own colour
        assert not Bc2.can_reach(2, 1, board)
        # cannot leap over
        assert not Bc2.can_reach(1, 4, board)
        # cannot move to itself
        assert not Bc2.can_reach(3, 2, board)
        # not on a diagonal
        assert not Bc2.can_reach(3, 4, board)
        # not on a diagonal
        assert not Bc2.can_reach(1, 2, board)

    def test_bishop_can_move_to_leap_over(self) -> None:
        '''
           ♔   
         ♖   ♖ 
               
           ♗   
               
         ♖   ♖ 
           ♚   
        '''
        b = read_board_txt(StringIO(
            '''7
            Kd7, Bd4, Rb2, Rf6, Rb6, Rf2
            Kd1'''
        ))
        copy_b = self.duplicate_board(b)
        Bd4 = piece_at(4, 4, b)
        valid_destinations = [
            (3, 5),
            (5, 5),
            (3, 3),
            (5, 3)
        ]
        for x in range(1, 8):
            for y in range(1, 8):
                if (x, y) in valid_destinations:
                    assert Bd4.can_move_to(x, y, b)
                else:
                    assert not Bd4.can_move_to(x, y, b)
        # check that original board is not modified
        assert b == copy_b

    def test_bishop_can_move_to_out_of_check(self) -> None:
        board = self.bishop_test_board()
        copy_board = self.duplicate_board(board)
        # king is in check so only valid move
        # is bishop takes rook b3
        Bc2 = piece_at(3, 2, board)
        only_valid_move = (2, 3)
        for x in range(1, 5):
            for y in range(1, 5):
                if (x, y) == only_valid_move:
                    assert Bc2.can_move_to(x, y, board)
                else:
                    assert not Bc2.can_move_to(x, y, board)
        # check that original board is not modified
        assert board == copy_board

    def test_king_can_reach_adjacent(self) -> None:
        Kc3: Piece = King(3, 3, False)
        board = (5, [Kc3])
        valid_destinations = [
            (2, 4),
            (3, 4),
            (4, 4),
            (2, 3),
            (4, 3),
            (2, 2),
            (3, 2),
            (4, 2)
        ]
        for x in range(1, 6):
            for y in range(1, 6):
                if (x, y) in valid_destinations:
                    assert Kc3.can_reach(x, y, board)
                else:
                    assert not Kc3.can_reach(x, y, board)

    def king_test_board(self) -> Board:
        '''
           ♚
         ♖  
          ♔ 
           ♜
        '''
        layout = StringIO(
            '''4
            Kc2, Rb3
            Kd4, Rd1
            ''')
        return read_board_txt(layout)

    def test_king_can_reach_valid_locs(self) -> None:
        board = self.king_test_board()
        Kc2 = piece_at(3, 2, board)
        # up
        assert Kc2.can_reach(3, 3, board)
        # right-up
        assert Kc2.can_reach(4, 3, board)
        # left
        assert Kc2.can_reach(2, 2, board)
        # right
        assert Kc2.can_reach(4, 2, board)
        # left-down
        assert Kc2.can_reach(2, 1, board)
        # down
        assert Kc2.can_reach(3, 1, board)
        # can capture other piece
        assert Kc2.can_reach(4, 1, board)

    def test_king_can_reach_isfalse_if_invalid(self) -> None:
        board = self.king_test_board()
        Kc2 = piece_at(3, 2, board)
        # cannot capture its own colour
        assert not Kc2.can_reach(2, 3, board)
        # cannot move to itself
        assert not Kc2.can_reach(3, 2, board)
        # cannot move more than one square away
        assert not Kc2.can_reach(1, 1, board)
        # cannot move more than one square away
        assert not Kc2.can_reach(4, 4, board)
        # cannot move more than one square away
        assert not Kc2.can_reach(2, 4, board)

    def test_king_can_move_to(self) -> None:
        board = self.king_test_board()
        copy_board = self.duplicate_board(board)
        # king can only move to 2 squares
        # without putting itself in check
        Kc2 = piece_at(3, 2, board)
        valid_moves = [
            (2, 2),
            (4, 1)
        ]
        for x in range(1, 5):
            for y in range(1, 5):
                if (x, y) in valid_moves:
                    assert Kc2.can_move_to(x, y, board)
                else:
                    assert not Kc2.can_move_to(x, y, board)
        # check that original board is not modified
        assert board == copy_board

    def test_is_check_white_only(self) -> None:
        '''
          ♗ 
          ♚ 
        ♔♜  
        ♖   
        '''
        b = read_board_txt(StringIO(
            '''4
            Ka2, Bc4, Ra1
            Kc3, Rb2'''
        ))
        assert is_check(True, b)
        assert not is_check(False, b)

    def test_is_check_neither_side(self) -> None:
        '''
         ♚  
           ♗
          ♝ 
        ♖ ♔ 
        '''
        b = read_board_txt(StringIO(
            '''4
            Kc1, Ra1, Bd3
            Kb4, Bc2'''
        ))
        assert not is_check(True, b)
        assert not is_check(False, b)

    def test_is_check_by_king(self) -> None:
        '''
            
        ♜ ♖♔
           ♚
            
        '''
        b = read_board_txt(StringIO(
            '''4
            Kd3, Rc3
            Kd2, Ra3'''
        ))
        assert is_check(True, b)
        assert is_check(False, b)

    def test_is_check_by_rook(self) -> None:
        '''
            
           ♔
            
          ♖♚
        '''
        b = read_board_txt(StringIO(
            '''4
            Kd3, Rc1
            Kd1'''
        ))
        assert not is_check(True, b)
        assert is_check(False, b)

    def test_is_check_by_bishop(self) -> None:
        '''
            
         ♗ ♔
            
           ♚
        '''
        b = read_board_txt(StringIO(
            '''4
            Kd3, Bb3
            Kd1'''
        ))
        assert not is_check(True, b)
        assert is_check(False, b)

    def test_is_checkmate_false_king_can_move(self) -> None:
        '''
          ♗ 
          ♚ 
        ♔♜  
        ♖   
        '''
        b = read_board_txt(StringIO(
            '''4
            Ka2, Bc4, Ra1
            Kc3, Rb2'''
        ))
        assert not is_checkmate(True, b)

    def test_is_checkmate_false_king_can_capture(self) -> None:
        '''
        ♚ ♗ 
            
        ♔♜  
        ♖   
        '''
        b = read_board_txt(StringIO(
            '''4
            Ka2, Bc4, Ra1
            Ka4, Rb2'''
        ))
        assert not is_checkmate(True, b)

    def test_is_checkmate_false_bishop_can_capture(self) -> None:
        '''
        ♜   
          ♚ 
        ♔   
        ♖♖ ♗
        '''
        b = read_board_txt(StringIO(
            '''4
            Ka2, Bd1, Ra1, Rb1
            Kc3, Ra4'''
        ))
        assert not is_checkmate(True, b)

    def test_is_checkmate_true_king_rook(self) -> None:
        '''
        ♜   
          ♚ 
        ♔   
        ♖♖  
        '''
        b = read_board_txt(StringIO(
            '''4
            Ka2, Ra1, Rb1
            Kc3, Ra4'''
        ))
        assert is_checkmate(True, b)

    def test_is_checkmate_true_three_bishops(self) -> None:
        '''
           ♚
        ♔   
        ♗   
        ♗♗  
        '''
        b = read_board_txt(StringIO(
            '''4
            Ka3, Ba1, Ba2, Bb1
            Kd4'''
        ))
        assert is_checkmate(False, b)
