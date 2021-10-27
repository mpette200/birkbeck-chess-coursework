import pytest
from chess_puzzle import Bishop, King, Rook, \
    location2index, index2location, is_piece_at, piece_at, \
    is_check, is_checkmate, read_board, conf2unicode


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
    br2b = Rook(2, 5, False)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2b, br3, wr2, wk])
    assert not is_checkmate(True, B2)


def test_read_board1() -> None:
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  # we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]:  # we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and type(piece) == type(piece1):
                found = True
        assert found


def test_conf2unicode1() -> None:
    assert conf2unicode(B1) == "♖ ♔  \n ♜  ♜\n ♚ ♜ \n♖   ♗\n♗    "
