#!/usr/bin/python

import random


# Board Dimensions
WIDTH = 7
HEIGHT = 6
CONNECT_N = 4

# Constants
RED, YELLOW = True, False


def generate_masks():
    """
    Generate all masks:
    7x3 cols, 6x4 rows, 24 diags = 69 masks
    """
    masks = []
    # Rows eg.
    # RRRR
    base_mask = 2 ** CONNECT_N - 1
    for i in range(0, WIDTH * HEIGHT, WIDTH):
        for j in range(WIDTH - CONNECT_N + 1):
            mask = base_mask << (i + j)
            masks.append(mask)

    # Cols eg.
    # R
    # R
    # R
    # R
    base_mask = 0b0
    for r in range(CONNECT_N):
        base_mask |= (0b1 << (WIDTH * r))
    for i in range(0, WIDTH):
        for j in range(HEIGHT - CONNECT_N + 1):
            mask = base_mask << (i + j * WIDTH)
            masks.append(mask)

    # Forward-slash diagonals eg.
    #    R
    #   R
    #  R
    # R
    base_mask = 0b0
    for r in range(CONNECT_N):
        base_mask |= (0b1 << ((WIDTH + 1) * r))
    for h in range(HEIGHT - CONNECT_N + 1):
        for w in range(WIDTH - CONNECT_N + 1):
            shift = WIDTH * h + w
            masks.append(base_mask << shift)

    # Back-slash diagonals eg.
    # R
    #  R
    #   R
    #    R
    base_mask = 0b0
    for r in range(CONNECT_N):
        base_mask |= (0b1 << (r * (WIDTH - 1) + CONNECT_N - 1))
    for h in range(HEIGHT - CONNECT_N + 1):
        for w in range(WIDTH - CONNECT_N + 1):
            shift = WIDTH * h + w
            masks.append(base_mask << shift)

    return masks


class Board(object):
    """
    Connect 4 boards consist of 7 columns, 6 rows.
    
    bit boards starting from bottom left
     
    red = '1000000001111111'
    yel = '0111111110000000'
     
    represents:
    ...
    _______
    _______
    YR_____
    YYYYYYY
    RRRRRRR
    
    i.e least significant digit refers to bottom left.
    """

    def __init__(self, bits_red=0, bits_yel=0):
        self.bits_red = bits_red
        self.bits_yel = bits_yel

    def is_connect4(self, masks, turn):
        if turn == RED:
            bits = self.bits_red
        elif turn == YELLOW:
            bits = self.bits_yel

        for mask in masks:
            if mask & bits == mask:
                return True
        return False

    def get_moves(self, turn):
        """
        Return list of possible boards that can result from player<turn> making a move.
        """
        moves = []

        occupied = self.bits_red | self.bits_yel

        for col in range(0, WIDTH):
            for i in range(0, HEIGHT):
                sq = 0b1 << (col + WIDTH * i)
                if occupied & sq == 0:
                    if turn == RED:
                        new_board = Board(bits_red=(self.bits_red | sq), bits_yel=self.bits_yel)
                    else:
                        new_board = Board(bits_yel=(self.bits_yel | sq), bits_red=self.bits_red)
                    moves.append(new_board)
                    break
        return moves

    def __str__(self):
        rows = []
        mask = 1
        row = ''
        for h in range(WIDTH * HEIGHT):
            sq = 'R' if self.bits_red & mask else 'Y' if self.bits_yel & mask else '_'
            row += sq
            mask <<= 1
            if (h + 1) % WIDTH == 0:
                rows.append(row)
                row = ''
        return '\n'.join(reversed(rows)) + '\n'


def main():
    masks = generate_masks()

    b = Board(0b0, 0b0)
    print(b)

    turn = RED

    while True:

        moves = b.get_moves(turn)
        if moves:
            i = random.choice(range(len(moves)))
            print 'Move:', i
            b = moves[i]
            print(b)
            if b.is_connect4(masks, turn):
                print('Connect {1} {0}!'.format('red' if turn == RED else 'yellow', str(CONNECT_N)))
                break
            turn = not turn


        else:
            break


if __name__ == '__main__':
    main()
