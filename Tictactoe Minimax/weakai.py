import numpy as np

# Define player and opponent tokens
player,opponent = 'x','o'

# Function to check if tokens are valid
def valid_tokens(t1, t2):
    return t1 != '_' and t2 != '_' and t1 != t2

# Function to let the user choose tokens( can not use underscore)
def select_tokens():
    global player, opponent
    while(True):    # Take input until valid Input Given
        in_str = input("Enter Tokens as (user/ai): ");
        if valid_tokens(in_str[0], in_str[1]): break
        else: print(f"Invalid Input {in_str}. Do not use Underscore")
    player = in_str[1]; opponent = in_str[0]    # Set Tokens as given input
    print(f"Tokens Chosen: You are {opponent}, Ai is {player}")

# Function to decide who goes first(User or AI)
def first_move():
    while(True):    # Take input until valid input given
        in_str = input("Enter to play 1(st) or 2(nd) :");
        if in_str in ['1','2']: break
        else: print(f"Invalid Input {in_str}. Enter 1 or 2")
    return player if in_str == '1' else opponent

# Function to display the game board
def display(board):
    for line in board: print(line)
    print()

# Function to check if a move is valid
def valid_move(board, move):
    a,b = move
    return a>=0 and a<3 and b>=0 and b<3 and board[move] == '_'

# Function generate a random valid move on board
def randomMove(board):
    r = -1; c = -1
    while not valid_move(board,(r,c)):
        r = np.random.randint(0,3)
        c = np.random.randint(0,3)
    return r,c

# Initialize score table for Heuristic Calculation
score_table=np.zeros((4,4),dtype=int)
for index in range(0,4):
    score_table[index,0]=10**index
    score_table[0,index]=10**index

# Score of a line where line is 3 consecutive cells (row, col, diag)
def eval_line(line, token=player):
    opp = opponent if token == player else player
    p_count = list(line).count(token)
    o_count = list(line).count(opp)
    return score_table[p_count,o_count]

# Calculate heuristic value for a board state
def heuristic(board,token=player):
    grid = np.array(board); h_val = 0
    for i in range(3):
        h_val += eval_line(grid[i],token)
        h_val += eval_line(grid[:,i],token)
    h_val += eval_line(grid.diagonal(),token)
    ld = [grid[0,2],grid[1,1],grid[2,0]]
    h_val += eval_line(ld, token)
    return h_val

# Get all possible moves given board state
def getmoves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                moves.append((i,j))
    return moves

# Check if game ended(-10 or 10) or not(0)
def evaluate(b) :
    # Checking Rows for x or o victory.
    for row in range(3) :
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]) :
            if (b[row][0] == player) : return 10
            elif (b[row][0] == opponent) : return -10

    # Checking Columns for x or o victory.
    for col in range(3) :
        if (b[0][col] == b[1][col] and b[1][col] == b[2][col]) :
            if (b[0][col] == player) : return 10
            elif (b[0][col] == opponent) : return -10

    # Checking Diagonals for x or o victory.
    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]) :
        if (b[0][0] == player) : return 10
        elif (b[0][0] == opponent) : return -10
    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]) :
        if (b[0][2] == player) : return 10
        elif (b[0][2] == opponent) : return -10

    # If none have won then return 0
    return 0

# Check if a player won
def checkWin(board):
    score = evaluate(board)
    if score == -10: return opponent
    elif score == 10: return player
    else: return None

# Remove unusable moves for AI
def clear_unusable(moves,move):
    try: moves.remove(move)
    except: pass

# Get heuristic scores for all possible moves
def getscores(board, moves):
    grid = np.array(board)
    scores = np.zeros(len(moves),dtype=int)
    for i,move in enumerate(moves):
        grid[move] = player
        scores[i] = heuristic(grid)
        grid[move] = '_'
    return scores

# Select a move based on probability
def prob_select(board,cantuse=None):
    moves = getmoves(board)                     # Get possible moves
    if cantuse: clear_unusable(moves, cantuse)  # Remove unusable tile
    if not moves: return cantuse                # If no moves available, use unusable
    elif len(moves) == 1: return moves[0]       # If only 1 move left, use it

    scores = getscores(board, moves)            # Calculate scores of all moves
    total = sum(scores)
    
    # Divide scores by total to get selection probability
    probs = [score/total for score in scores]
    idx = np.random.choice(len(scores),p=probs)
    return moves[idx]

# Function for AI to select a move
def ai_move(board,cantuse):
    move = prob_select(board,cantuse)
    print("\nAi Played:",move)
    return move

# Function for user to input a move
def player_move(board,c=None):
    move = (-1,-1)
    while(True):    # Take input until valid move entered
        in_str = input("Enter your move(0..2,0..2): ")
        try: 
            i,j = in_str[0],in_str[1]
            move = (int(i),int(j))
        except:
            if in_str == 'end': return in_str
        if valid_move(board, move): break
        print("Invalid Input: ", in_str)
    print("You played: ", move)
    return move

# Main game Loop
def tictactoe():
    # Define Board
    board = np.array([['_','_','_'],
                     ['_','_','_'],
                     ['_','_','_']])
    select_tokens()
    taketurn = None
    token = first_move(); 
    cantuse = randomMove(board)         # Pick random unusable tile
    played = 9-len(getmoves(board))     # No of playable moves
    print("Ai will not use: ", cantuse)

    for _ in range(played, 9):
        token = opponent if token == player else player         # Alternate Tokens
        taketurn = ai_move if token == player else player_move  # Alternate Players
        display(board)

        move = taketurn(board,cantuse)                  # Execute Move Selection Function
        if token == player and move == cantuse:         # Notify AI will use unsuable tile
            print("Only unusable tile left. Using it")
        if move == 'end': break
        board[move] = token
        
        winner = checkWin(board)
        if winner is not None: break

    display(board)
    if winner is None: print("Draw!!")
    else: print(f"{winner} won the game!!")

tictactoe()