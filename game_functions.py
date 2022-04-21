import numpy as np

posmoves = 4
cells = 4
numsquare = cells * cells
newtilerng = np.array([2, 2, 2, 2, 2, 2, 2, 2 ,2, 4])

def startgame():
    map = np.zeros((numsquare), dtype="int")
    starttile = np.random.default_rng().choice(numsquare, 2, replace=False)
    map[starttile] = 2
    map = map.reshape((cells, cells))
    return map

def push_board_right(map):
    new = np.zeros((cells, cells), dtype="int")
    done = False
    for yuh in range(cells):
        count = cells - 1
        for yas in range(cells - 1, -1, -1):
            if map[yuh][yas] != 0:
                new[yuh][count] = map[yuh][yas]
                if yas != count:
                    done = True
                count -= 1
    return (new, done)


def merge_elements(map):
    score = 0
    done = False
    for yuh in range(cells):
        for yas in range(cells - 1, 0, -1):
            if map[yuh][yas] == map[yuh][yas-1] and map[yuh][yas] != 0:
                map[yuh][yas] *= 2
                score += map[yuh][yas]
                map[yuh][yas-1] = 0
                done = True
    return (map, done, score)


def move_up(map):
    rotated_board = np.rot90(map, -1)
    pushed_board, has_pushed = push_board_right(rotated_board)
    merged_board, has_merged, score = merge_elements(pushed_board)
    second_pushed_board, _ = push_board_right(merged_board)
    rotated_back_board = np.rot90(second_pushed_board)
    move_made = has_pushed or has_merged
    return rotated_back_board, move_made, score

    
def move_down(map):
    map = np.rot90(map)
    map, has_pushed = push_board_right(map)
    map, has_merged, score = merge_elements(map)
    map, _ = push_board_right(map)
    map = np.rot90(map, -1)
    move_made = has_pushed or has_merged
    return map, move_made, score


def move_left(map):
    map = np.rot90(map, 2)
    map, has_pushed = push_board_right(map)
    map, has_merged, score = merge_elements(map)
    map, _ = push_board_right(map)
    map = np.rot90(map, -2)
    move_made = has_pushed or has_merged
    return map, move_made, score


def move_right(map):
    map, has_pushed = push_board_right(map)
    map, has_merged, score = merge_elements(map)
    map, _ = push_board_right(map)
    move_made = has_pushed or has_merged
    return map, move_made, score


def fixed_move(map):
    move_order = [move_left, move_up, move_down, move_right]
    for func in move_order:
        new_board, move_made, _ = func(map)
        if move_made:
            return new_board, True
    return map, False


def random_move(map):
    move_made = False
    move_order = [move_right, move_up, move_down, move_left]
    while not move_made and len(move_order) > 0:
        move_index = np.random.randint(0, len(move_order))
        move = move_order[move_index]
        map, move_made, score  = move(map)
        if move_made:
            return map, True, score
        move_order.pop(move_index)
    return map, False, score


def add_new_tile(map):
    tile_value = newtilerng[np.random.randint(0, len(newtilerng))]
    tile_row_options, tile_col_options = np.nonzero(np.logical_not(map))
    tile_loc = np.random.randint(0, len(tile_row_options))
    map[tile_row_options[tile_loc], tile_col_options[tile_loc]] = tile_value
    return map


def check_for_win(map):
    return 2048 in map