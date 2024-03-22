from sudoku import Sudoku
import queue
import copy
import timeit

'''
Parameters: Takes as input the curr_board state and the puzzle
Returns: True if the current board state is the goal and False if not
Note: Existing version solves the puzzle everytime you test for goal
      feel free to change the implementation to save time
'''
def test_goal(curr_board,puzzle):
    puzzle_solution = puzzle.solve()
    try:
        solution_board = puzzle_solution.board
        for i in range(len(solution_board)):
            for j in range(len(solution_board[i])):
                assert(curr_board[i][j]==solution_board[i][j])
        return True
    except Exception as e:
        return False

'''
Parameters: Takes as input a puzzle board and puzzle size
Returns: True if the puzzle board is valid and False if not
'''    
def valid_puzzle(puzzle_size,puzzle_board):
    puzzle=Sudoku(puzzle_size,board=puzzle_board)
    return puzzle.validate()

'''
Parameters: Takes as input a puzzle board
Returns: Returns all the cells in the grid that are empty
'''
def empty_cells(puzzle_board):
    empty_cell_list=[]
    for i in range(len(puzzle_board)):
        for j in range(len(puzzle_board[i])):
            if puzzle_board[i][j] is None:
                empty_cell_list.append([i,j])
    return empty_cell_list

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
# Breadth-first search (bfs): You must maintain a FIFO queue for the frontier

def bfs(puzzle):
    start_timer = timeit.default_timer() # Timer
    puzzle_size = puzzle.size # Size of the board
    start_state = puzzle.board # Get the initial state of the puzzle
    frontier = queue.Queue(0) # Initialize a FIFO queue for the frontier
    frontier.put(start_state) # Adding the start of the puzzle to the frontier

    while frontier: # While frontier is not empty

        working_board = copy.deepcopy(frontier.get()) # Makes first element in the deque the correct board
        
        empty_cell_list = empty_cells(puzzle.board) # A list of all empty cells on board

        for cell in empty_cell_list:  # for each cell in the empty cell list
            for num in range(1, puzzle_size + 1):  # Runs from 1 to size of board, to know range of values for each cell
                filled_board = copy.deepcopy(working_board) # Deep copy of correct board with filled in cells
                filled_board[cell[0]][cell[1]] = num
                frontier.put(filled_board)
                if test_goal(filled_board, puzzle): # Returns the correct board if it passes the test
                    return print("BFS Test: ", filled_board, " | Total time: ", timeit.default_timer()-start_timer, " seconds")
'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def dfs(puzzle):
    start_timer = timeit.default_timer() # Timer
    puzzle_size = puzzle.size
    start_state = puzzle.board  # The starting board
    frontier = queue.LifoQueue() # Initalizing the frontier
    frontier.put(start_state) # Adding start state to frontier
    explored = []
    while frontier: # While frontier is not empty
        working_board = frontier.get() # Makes first element in the deque the correct board
        empty_cell_list = empty_cells(puzzle.board) # A list of all empty cells on board
        explored.append(working_board) # Holds the explored sudoku boards, garbage collector 

        for cell in empty_cell_list:  # for each cell in the empty cell list
            for num in range(1, puzzle_size + 1):  # Runs from 1 to size of board, to know range of values for each cell
                filled_board = copy.deepcopy(working_board) # Deep copy of correct board with filled in cells
                filled_board[cell[0]][cell[1]] = num
                if filled_board not in explored: # Adds board to frontier if the board is not in explored already
                    frontier.put(filled_board)
                if test_goal(filled_board, puzzle): # Returns the correct board if it passes the test
                    return print("DFS Test: ", filled_board, " | Total time: ", timeit.default_timer() - start_timer, " seconds")
    return(None)

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def bfs_with_prunning(puzzle):
    start_timer = timeit.default_timer() # Timer
    puzzle_size = puzzle.size # Size of the board
    start_state = puzzle.board # Get the initial state of the puzzle
    frontier = queue.Queue(0) # Initialize a FIFO queue for the frontier
    frontier.put(start_state) # Adding the start of the puzzle to the frontier

    while frontier: # While frontier is not empty

        working_board = copy.deepcopy(frontier.get()) # Makes first element in the deque the correct board
        
        empty_cell_list = empty_cells(puzzle.board) # A list of all empty cells on board

        for cell in empty_cell_list:  # for each cell in the empty cell list
            for num in range(1, puzzle_size + 1):  # Runs from 1 to size of board, to know range of values for each cell
                filled_board = copy.deepcopy(working_board) # Deep copy of correct board with filled in cells
                filled_board[cell[0]][cell[1]] = num
                if valid_puzzle(2, filled_board) == True:
                    frontier.put(filled_board)
                if test_goal(filled_board, puzzle): # Returns the correct board if it passes the test
                    return print("BFS with prunning test: ", filled_board, " | Total time: ", timeit.default_timer() - start_timer, " seconds")
                
    return None


'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def dfs_with_prunning(puzzle):
    start_timer = timeit.default_timer() # Timer
    puzzle_size = puzzle.size
    start_state = puzzle.board  # The starting board
    frontier = queue.LifoQueue() # Initalizing the frontier
    frontier.put(start_state) # Adding start state to frontier
    explored = []
    while frontier: # While frontier is not empty
        working_board = frontier.get() # Makes first element in the deque the correct board
        empty_cell_list = empty_cells(puzzle.board) # A list of all empty cells on board
        explored.append(working_board) # Holds the explored sudoku boards, garbage collector 

        for cell in empty_cell_list:  # for each cell in the empty cell list
            for num in range(1, puzzle_size + 1):  # Runs from 1 to size of board, to know range of values for each cell
                filled_board = copy.deepcopy(working_board) # Deep copy of correct board with filled in cells
                filled_board[cell[0]][cell[1]] = num
                if (valid_puzzle(2, filled_board) == True) and (filled_board not in explored):# Adds board to frontier if the board is not in explored already
                    frontier.put(filled_board)
                if test_goal(filled_board, puzzle): # Returns the correct board if it passes the test
                    return print("DFS with prunning Test: ", filled_board, " | Total time: ", timeit.default_timer()-start_timer, " seconds")
    return None

if __name__ == "__main__":
    puzzle = Sudoku(2,2).difficulty(0.2) # Constructs a 2 x 2 puzzle
    puzzle.show() # Pretty prints the puzzle
    solution = puzzle.solve()
    print("Is puzzle valid? " + str(valid_puzzle(2,puzzle.board))) # Checks if the puzzle is valid
    print("The test goal: " + str(test_goal(puzzle.board,puzzle))) # Checks if the given puzzle board is the goal for the puzzle
    print("The empty cells: " + str(empty_cells(puzzle.board))) # Prints the empty cells as row and column values in a list for the current puzzle board
    print("The puzzle solution: " + str(solution.board),)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # 2x2 tests at 0.2 to 0.9 Difficulty 
    print("2x2 at 0.2 difficulty")
    bfs(puzzle)
    dfs(puzzle)
    bfs_with_prunning(puzzle)
    dfs_with_prunning(puzzle)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("2x2 at 0.3 difficulty")
    puzzle_Test_5 = Sudoku(2,2).difficulty(0.3)
    bfs(puzzle_Test_5)
    dfs(puzzle_Test_5)
    bfs_with_prunning(puzzle_Test_5)
    dfs_with_prunning(puzzle_Test_5)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("2x2 at 0.4 difficulty")
    puzzle_Test_6 = Sudoku(2,2).difficulty(0.4)
    bfs(puzzle_Test_6)
    dfs(puzzle_Test_6)
    bfs_with_prunning(puzzle_Test_6)
    dfs_with_prunning(puzzle_Test_6)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("2x2 at 0.5 difficulty")
    puzzle_Test_7 = Sudoku(2,2).difficulty(0.5)
    bfs(puzzle_Test_7)
    dfs(puzzle_Test_7)
    bfs_with_prunning(puzzle_Test_7)
    dfs_with_prunning(puzzle_Test_7)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("2x2 at 0.6 difficulty")
    puzzle_Test_8 = Sudoku(2,2).difficulty(0.6)
    bfs(puzzle_Test_8)
    dfs(puzzle_Test_8)
    bfs_with_prunning(puzzle_Test_8)
    dfs_with_prunning(puzzle_Test_8)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("2x2 at 0.7 difficulty")
    puzzle_Test_9 = Sudoku(2,2).difficulty(0.7)
    bfs(puzzle_Test_9)
    dfs(puzzle_Test_9)
    bfs_with_prunning(puzzle_Test_9)
    dfs_with_prunning(puzzle_Test_9)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("2x2 at 0.8 difficulty")
    puzzle_Test_10 = Sudoku(2,2).difficulty(0.8)
    bfs(puzzle_Test_10)
    dfs(puzzle_Test_10)
    bfs_with_prunning(puzzle_Test_10)
    dfs_with_prunning(puzzle_Test_10)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("2x2 at 0.9 difficulty")
    puzzle_Test_11 = Sudoku(2,2).difficulty(0.9)
    bfs(puzzle_Test_11)
    dfs(puzzle_Test_11)
    bfs_with_prunning(puzzle_Test_11)
    dfs_with_prunning(puzzle_Test_11)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # 3x3 and 4x4 at 0.2 difficultyRuntime Tests
    print("3x3 at 0.2 difficulty")
    puzzle_Test_3 = Sudoku(3,3).difficulty(0.2)
    bfs(puzzle_Test_3)
    dfs(puzzle_Test_3)
    bfs_with_prunning(puzzle_Test_3)
    dfs_with_prunning(puzzle_Test_3)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("4x4 at 0.2 difficulty")
    puzzle_Test_4 = Sudoku(4,4).difficulty(0.2)
    bfs(puzzle_Test_4)
    dfs(puzzle_Test_4)
    bfs_with_prunning(puzzle_Test_4)
    dfs_with_prunning(puzzle_Test_4)


    