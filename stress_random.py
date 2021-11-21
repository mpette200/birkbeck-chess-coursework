import random
from io import StringIO
from multiprocessing import Process
from chess_puzzle import \
    read_board_txt, is_checkmate, get_all_moves


def do_test() -> None:
    '''Computer repeatedly makes random moves for both white and black
    until game ends.
    '''
    random.seed(1231)
    # advantage_board = '''12
    # Kj1, Ra1, Rb1, Rc1, Rd1, Re1, Rf1, Ra3, Rb3, Rc3, Rd3, Re3, Rf3''' + \
    # ''', Bg3, Bh3, Bi3, Bj3, Bk3, Bl3, Bg5, Bh5, Bi5, Bj5, Bk5, Bl5
    # Kj12, Ra12, Rb12, Rc12, Bh10, Bi10, Bj10, Bk10'''

    fair_board = '''12
        Kj1, Ra1, Rb1, Rc1, Bh3, Bi3, Bj3, Bk3
        Kj12, Ra12, Rb12, Rc12, Bh10, Bi10, Bj10, Bk10'''
    b = read_board_txt(StringIO(fair_board))
    cur_side = True
    iter_limit = 100_000
    i = 0
    while i < iter_limit:
        i += 1
        # check for termination
        if is_checkmate(cur_side, b) or get_all_moves(cur_side, b) == []:
            break

        # make move
        piece, x, y = random.choice(get_all_moves(cur_side, b))
        piece.move_to(x, y, b)
        cur_side = not cur_side
    print('End of game')


if __name__ == '__main__':
    p = Process(target=do_test)
    p.start()
    print('Running game: ', end='', flush=True)
    t = 0
    while p.exitcode is None and t < 10:
        # print a dot for each second elapsed
        p.join(1)
        print('.', end='', flush=True)
        t += 1
    if p.exitcode is not None:
        print('\nGame ended normally')
    else:
        print('\nGame still not finished, terminating')
        p.terminate()
        p.join()
    p.close()
