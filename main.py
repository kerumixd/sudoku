import random
import copy

# Step 4: Solver used for checking uniqueness
def solve_board(board, solutions, row=0, col=0):
    if row == 9:
        solutions[0] += 1
        return
    if board[row][col] != 0:
        next_row, next_col = (row + (col + 1) // 9, (col + 1) % 9)
        solve_board(board, solutions, next_row, next_col)
    else:
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row][col] = num
                next_row, next_col = (row + (col + 1) // 9, (col + 1) % 9)
                solve_board(board, solutions, next_row, next_col)
                board[row][col] = 0

# Step 3: Remove numbers to create puzzle
def remove_numbers(board, attempts=30):
    count = 0
    while count < attempts:
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        backup = board[row][col]
        board[row][col] = 0

        # Make a copy and try solving it again to ensure uniqueness
        board_copy = copy.deepcopy(board)
        solutions = [0]
        solve_board(board_copy, solutions)
        if solutions[0] != 1:
            board[row][col] = backup  # revert if not unique
        else:
            count += 1

def is_valid(board, row, col, num):
    # Check row and column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num: #check same row or same column
            return False

    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board): #backtracking
    for row in range(9): #0-9
        for col in range(9): #0-9
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num #temporarily place a valid num
                        #find the first valid number then continue recursively
                        if fill_board(board): #only the correct solution that leads to board being fully filled do not backtrack
                            return True
                        board[row][col] = 0 #backtracking. even if num is valid, it could still lead to dead end
                return False #invalid number we tried return false
    return True

def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)] #initialise board
    fill_board(board)
    solution = copy.deepcopy(board)
    remove_numbers(board, attempts=40)
    return board, solution

def board_full(board) -> bool:
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0: return False
    return True

def print_board(board):
    print(" "," "," ".join(str(i) for i in range(1, 10)))
    print(" ".join('_'*11))
    for i, row  in enumerate(board):
        print(i+1, '|'," ".join(str(num) if num != 0 else "." for num in row))


if __name__ == "__main__":
    sudoku_board, sudoku_solution = generate_sudoku()
    print_board(sudoku_solution)
    print()
    print_board(sudoku_board)
    game_over = False
    #game start
    while not game_over:
        input_string = input("Try to fill in the missing numbers (in <y> <x> <num> style): ")
        input_list = input_string.split()
        if len(input_list) != 3:
            print("Invalid input length. Try again.")
            continue
        input_y = int(input_list[0])
        input_x = int(input_list[1])
        input_num = int(input_list[2])
        #border detection
        if input_num < 1 or input_num > 9:
            print("Invalid input number. Try again.")
            continue
        if input_x < 1 or input_x > 9:
            print("x out of bound. Try again.")
            continue
        if input_y < 1 or input_y > 9:
            print("y out of bound. Try again.")
            continue
        correct_num = sudoku_solution[input_y-1][input_x-1]
        cur_num = sudoku_board[input_y-1][input_x-1]
        if cur_num != 0:
            print("Oops! There's already a number there. Try a different spot.")
            continue
        if input_num == correct_num:
            sudoku_board[input_y-1][input_x-1] = input_num
            print_board(sudoku_board)
            if board_full(sudoku_board):
                game_over = True
                print("You won!!")
            else:
                print("You are correct with that one! Keep it up.")
        else:
            print("Sorry, that's not the correct num. Try again.")