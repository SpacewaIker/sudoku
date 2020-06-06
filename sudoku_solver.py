import pandas as pd

def get_subgrid(sudoku, col, row): #Finds and returns the subgrid in which the box is in.
    '''Finds and returns the subgrid in which the box is in.
    ARGS- sudoku: sudoku problem as a pandas DataFrame
        col: column of the box
        row: row of the box'''

    if col in range(3):
        subgrid = sudoku.loc[:, 0:2]
    elif col in range(3, 6):
        subgrid = sudoku.loc[:, 3:5]
    elif col in range(6, 9):
        subgrid = sudoku.loc[:, 6:8]

    if row in range(3):
        subgrid = subgrid.loc[0:2, :]
    elif row in range(3, 6):
        subgrid = subgrid.loc[3:5, :]
    elif row in range(6, 9):
        subgrid = subgrid.loc[6:8, :]

    return subgrid

def find_possible_numbers(sudoku, col, row): #Finds and returns the possible numbers for a box of a sudoku.
    '''Finds and returns the possible numbers for a box of a sudoku.
    ARGS- sudoku: sudoku problem as a pandas DataFrame
        col: column of the box
        row: row of the box'''
    
    possible_numbers = []

    for i in range(1, 10):
        number_is_possible = True

        while number_is_possible: 
            # allow to exit loop directly if a condition is not met

            # check row
            if sudoku.loc[row, :].isin([i]).any():
                number_is_possible = False

            # check column
            if sudoku.loc[:, col].isin([i]).any():
                number_is_possible = False

            # check subgrid
            subgrid = get_subgrid(sudoku, col, row)
            if subgrid.isin([i]).any().any():
                number_is_possible = False

            break

        if number_is_possible:
            possible_numbers.append(i)
    
    return possible_numbers

def solve_iterate(sudoku): #Function to fill in sudoku boxes by using iteration.
    '''Function to fill in sudoku boxes by using iteration. 
    Not suitable for more complex sudokus.
    If it iterates twice through the hole sudoku without filling in it will stop iterating and return 
    the sudoku
    ARGS- sudoku: sudoku problem as a pandas DataFrame'''

    iter_wo_fill = 0 #iterations without being able to fill in something

    while (sudoku.isnull().any().any()) and (iter_wo_fill < 2): 
        #while sudoku is not completely full 
        # and there hasn't been 2 full iterations without filling in a box

        filled_st = False #was something filled in this whole iteration?

        for current_col in range(9):
            for current_row in range(9):
                if pd.isna(sudoku.loc[current_row, current_col]): #checks that the box is not already filled

                    possible_numbers = find_possible_numbers(sudoku, current_col, current_row)

                    if len(possible_numbers) == 1: #checks that there's only one option possible
                        sudoku.loc[current_row, current_col] = possible_numbers[0]
                        if filled_st == False: filled_st = True #something *was* filled in this whole iteration
                        iter_wo_fill = 0 #resets iterations without filling counter

                    
                    elif len(possible_numbers) == 0: #error
                        print('Error: len(possible_numbers) == 0. \n Col: {0} \n Row: {1}\n'.format(
                            current_col, current_row
                        ))

        if filled_st == False: #nothing was filled during this whole iteration
            iter_wo_fill += 1 

    return sudoku

def solve_sudoku(sudoku, savefile=None): #Solves a sudoku problem.
    '''Solves a sudoku problem.
    ARGS- sudoku: sudoku problem as a pandas DataFrame, 
        savefile: if not None, name of the file saved'''

    sudoku_solve_iterate = solve_iterate(sudoku)
    if sudoku_solve_iterate.isnull().any().any() == True:
        print('Not full')
        #proceed with other type of filling

    else: #sudoku is filled with only iteration
        sudoku = sudoku_solve_iterate

    if savefile != None:
        sudoku.to_csv('projects\sudoku\{}.csv'.format(str(savefile)), header=False, index=False)

    return sudoku

sudoku1 = pd.read_excel(
    'projects\sudoku\sudoku1.xlsx',
    dtype='Int64',
    header=None
)

sudoku2 = pd.read_excel(
    'projects\sudoku\sudoku2.xlsx',
    dtype='Int64',
    header=None
)

print(
    solve_sudoku(sudoku1)
)