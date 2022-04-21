import numpy as np
import matplotlib.pyplot as plt

nummoves = 4
samplecount = 50

spscalep = 10
slscalep = 4
searchp = 200

from game_functions import initialize_game, random_move,\
                            move_down, move_left,\
                            move_right, move_up,\
                            check_for_win, add_new_tile

                        

def usesearchjparam(move_number):
    howmanychecks = spscalep * (1+(move_number // searchp))
    howfarcheck = slscalep * (1+(move_number // searchp))
    return howmanychecks, howfarcheck

def moving(board, howmanychecks, searchp):
    firstmove = [move_left, move_up, move_down, move_right]
    scoresfirsts = np.zeros(nummoves)
    for first_move_index in range(nummoves):
        first_move_function =  firstmove[first_move_index]
        board_with_first_move, first_move_made, first_move_score = first_move_function(board)
        if first_move_made:
            board_with_first_move = add_new_tile(board_with_first_move)
            scoresfirsts[first_move_index] += first_move_score
        else:
            continue
        for _ in range(howmanychecks):
            move_number = 1
            search_board = np.copy(board_with_first_move)
            game_valid = True
            while game_valid and move_number < searchp:
                search_board, game_valid, score = random_move(search_board)
                if game_valid:
                    search_board = add_new_tile(search_board)
                    scoresfirsts[first_move_index] += score
                    move_number += 1
    best_move_index = np.argmax(scoresfirsts)
    best_move = firstmove[best_move_index]
    search_board, game_valid, score = best_move(board)
    return search_board, game_valid

def ai_play(board):
    move_number = 0
    valid_game = True
    while valid_game:
        move_number += 1
        number_of_simulations, search_length = usesearchjparam(move_number)
        board, valid_game = moving(board, number_of_simulations, search_length)
        if valid_game:
            board = add_two(board)
        if check_for_win(board):
            valid_game = False
        print(board)
        print(move_number)
    print(board)
    return np.amax(board)

def ai_plot(move_func):
    tick_locations = np.arange(1, 12)
    final_scores = []
    for _ in range(samplecount):
        print('thing is ', _)
        board = initialize_game()
        game_is_win = ai(board)
        final_scores.append(game_is_win)
    all_counts = np.zeros(11)
    unique, counts = np.unique(np.array(final_scores), return_counts=True)
    unique = np.log2(unique).astype(int)
    index = 0

    for tick in tick_locations:
        if tick in unique:
            all_counts[tick-1] = counts[index]
            index += 1

    plt.bar(tick_locations, all_counts)
    plt.xticks(tick_locations, np.power(2, tick_locations))
    plt.xlabel("Score of Game", fontsize = 24)
    plt.ylabel(f"Frequency per {samplecount} runs", fontsize = 24)
    plt.show()



	