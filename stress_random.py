import random
import chess_puzzle
import queue
from multiprocessing import Process, Queue, Lock
from chess_puzzle import index2location


class PatchIO:
    def __init__(self, board_filename: str, board_size: int,
                 seed: int, out_limit: int) -> None:
        'Patcher to supply inputs, get outputs from program'
        self.board_filename = board_filename
        self.board_size = board_size
        self.outputs: Queue = Queue(out_limit)
        self.out_limit = out_limit
        self.lock = Lock()
        self.pending_validation = ''
        self.i = 0
        random.seed(seed)

    def input(self, msg: str) -> str:
        if self.i == 0:
            self.i += 1
            out = self.board_filename
            self.print(msg)
            self.print(out)
        else:
            x1 = random.randint(1, self.board_size)
            y1 = random.randint(1, self.board_size)
            x2 = random.randint(1, self.board_size)
            y2 = random.randint(1, self.board_size)
            source = index2location(x1, y1)
            dest = index2location(x2, y2)
            out = source + dest
            self.pending_validation = out
        return out

    def print(self, msg: str) -> None:
        if "after White's move" in msg:
            self.print(self.pending_validation)
        # falls through
        with self.lock:
            while True:
                try:
                    self.outputs.put_nowait(msg)
                    break
                except queue.Full:
                    self.outputs.get(timeout=0.2)

    def get_outputs(self) -> str:
        out: list[str] = []
        with self.lock:
            while len(out) < self.out_limit:
                try:
                    out.append(self.outputs.get(timeout=0.2))
                except queue.Empty:
                    break
            return '\n'.join(out)


def run_process_patch_inputs(board_filename: str,
                             size: int, seed: int) -> None:
    out_limit = 20
    timeout = 10
    patch = PatchIO(board_filename, size, seed, out_limit)
    chess_puzzle.input = patch.input
    chess_puzzle.print = patch.print
    p = Process(target=chess_puzzle.main)
    p.start()
    print('Running ' + board_filename + ': ', end='', flush=True)
    t = 0
    while p.exitcode is None and t < timeout:
        # print a dot for each second elapsed
        p.join(1)
        print('.', end='', flush=True)
        t += 1
    print()
    print(patch.get_outputs(), flush=True)
    if p.exitcode is not None:
        print('\nGame ended')
    else:
        print('\nGame still not finished, terminating')
        p.terminate()
        p.join()
    p.close()


if __name__ == '__main__':
    seed = 228
    chess_puzzle.RANDOM_SEED = seed
    run_process_patch_inputs('board_large_fair.txt', 12, seed)
    run_process_patch_inputs('board_large_white_adv.txt', 12, seed)
    for _ in range(5):
        seed += 1
        chess_puzzle.RANDOM_SEED = seed
        run_process_patch_inputs('board_examp.txt', 5, seed)
    for _ in range(5):
        seed += 1
        chess_puzzle.RANDOM_SEED = seed
        run_process_patch_inputs('board_small_valid.txt', 4, seed)
