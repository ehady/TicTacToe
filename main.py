from collections import Counter

BOARD_EMPTY = 0
BOARD_PLAYER_X = 1
BOARD_PLAYER_O = -1


# THE CONSTANTS ARE THE MEANING OF EACH NUMBER IN THE STATE
# take in a current state and print the current state to the user
def print_board(state):  # s is the current state of the board
    def convert(num):  # we take a numerical representation and convert it to a symbol
        if num == BOARD_PLAYER_X:  # if its equal to 1
            return 'X'
        if num == BOARD_PLAYER_O:  # if its equal to -1
            return 'O'
        return '_'  # empty cells
    i = 0  # initialize it so we can use it to iterate through the elements
    for _ in range(3):  # this represents the rows of the board.
        for _ in range(3):  # this represents the columns of the board.
            print(convert(state[i]), end=' ')  # we print the symbol corresponding to the current element in the state
            i += 1
        print()


# take the state of the game and return whose turn it is. x or o
def player(state):
    counter = Counter(state)
    x_counter = counter[1]  # count how many X's on the board
    o_counter = counter[-1]  # count how many O's on the board

    if x_counter + o_counter == 9:  # the board is full
        return None
    elif x_counter > o_counter:  # if there are more X than O, it's O's turn
        return BOARD_PLAYER_O
    else:
        return BOARD_PLAYER_X


# we take in a state and return the list of available moves.
# the list contains all moves, desirable or undesirable
def actions(state):
    which_player = player(state)
    actions_list = [(which_player, i) for i in range(len(state)) if
                    state[i] == BOARD_EMPTY]  # we go through to state to look for empty cells.
    # we return a list where (p,i) p is the player and i is the index for the next move
    return actions_list


# state of the board, a is the tuple of the player and the index they want to play
def new_state(state, action):
    (player, index) = action
    s_copy = state.copy()  # we create a copy to avoid modifying the original state in place
    s_copy[index] = player  # update the copy by placing the current player's symbol in the specified cell
    return s_copy  # return the final state

# we take in the state of the game
def check_winner(state):
    for i in range(3):  # go row by row
        # Checking if a row is filled and equal.
        if state[3 * i] == state[3 * i + 1] == state[3 * i + 2] != BOARD_EMPTY:
            return state[3 * i]  # If so, return the winning symbol
        # Checking if a column is filled and equal.
        if state[i] == state[i + 3] == state[i + 6] != BOARD_EMPTY:
            return state[i]

    # Checking if a diagonal is filled and equal.
    if state[0] == state[4] == state[8] != BOARD_EMPTY:
        return state[0]
    if state[2] == state[4] == state[6] != BOARD_EMPTY:
        return state[2]

    # if the game is a tie.
    if player(state) is None:
        return 0

    # If the game is not over
    return None


# depth tells us how  deep the algorithm had to go till it reached terminal
def score_calculate(state, depth):  # take the current state as a parameter, and return the score of that state
    winner = check_winner(state)
    if winner is not None: # if we have a winner
        # Return the depth of reaching the terminal state
        return (winner, depth)  # term is the winning symbol ( 1 or -1 or 0 )
    # get the list of actions available
    action_list = actions(state)
    scores = []
    # calculate "score" for each possible action and store in "scores" list
    for action in action_list:
        # create a new state applying the action to current state
        new_s = new_state(state, action)
        # add the score of the new state to a list
        # Every recursion will be an increment in the cost (depth)
        scores.append(score_calculate(new_s, depth + 1))  # result is appended to the "scores" list

    # Remember the associated depth with the score of the state.
    current_score = scores[0][0]
    associated_depth = scores[0][1]
    current_player = player(s)
    if player(state) == BOARD_PLAYER_X:
        return max(scores, key=lambda x: x[0])
    else:
        return min(scores, key=lambda x: x[0])



# return the desired action to take for a given state s
def minimax(state):
    action_list = actions(state)
    scores = []
    for action in action_list:
        new_s = new_state(state, action)
        scores.append((action, score_calculate(new_s, 1)))
    # Each item in scores contains the action associated
    # the score and "depth" of that action.

    # if scores has no objects(no possible actions), then return a default action and score
    if len(scores) == 0:
        return ((0, 0), (0, 0))

    # Sort the list in ascending order of depth.
    sorted_list = sorted(scores, key=lambda l: l[1][1])
    # Since the computer shall be Player O,
    # It is safe to return the object with minimum score.
    action = min(sorted_list, key=lambda l: l[1])
    return action


if __name__ == '__main__':
    # Initializing the state
    s = [BOARD_EMPTY for _ in range(9)]
    print('|------- WELCOME TO TIC TAC TOE -----------|')
    print('You are X while the Computer is O')

    # Run the program while the game is not terminated
    while check_winner(s) is None:
        play = player(s)
        if play == BOARD_PLAYER_X:
            # Take input from user
            print('\n\nIt is your turn', end='\n\n')
            x = int(input('Enter the x-coordinate [0-2]: '))
            y = int(input('Enter the y-coordinate [0-2]: '))
            index = 3 * x + y #we convert the 3d coordinates to 2d

            if not s[index] == BOARD_EMPTY:
                print('That coordinate is already taken. Please try again.')
                continue

            # Apply the action and print the board
            s = new_state(s, (BOARD_PLAYER_X, index))
            print_board(s)
        else:
            print('\n\nThe is computer is playing its turn')
            # Get the action by running the minimax algorithm
            action = minimax(s)
            # Apply the returned action to the state and print the board
            s = new_state(s, action[0])
            print_board(s)

    # We know that terminal(s) is not None
    # determine the winner
    winner = check_winner(s)
    if winner == BOARD_PLAYER_X:
        print("You have won!")
    elif winner == BOARD_PLAYER_O:
        print("You have lost!")
    else:
        print("It's a tie.")
