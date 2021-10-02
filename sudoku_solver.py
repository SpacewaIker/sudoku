import pandas as pd


class Sudoku():
    ''' Sudoku problem as pandas DataFrame.
        Methods:
            solve:
                solves the sudoku problem'''

    def __init__(self, path):
        ''' Stores the sudoku problem as self.grid
            A&P:
                path:
                    str, path of the file'''

        if path.endswith('.xlsx'):
            self.grid = pd.read_excel(
                path, dtype='Int64', header=None).fillna(0)
        elif path.endswith('.csv'):
            self.grid = pd.read_csv(path, dtype='Int64', header=None)
        else:
            print('Incorrect path')

    def __str__(self):
        grid = ''
        for i in range(self.grid.shape[0]):
            if i % 3 == 0 and i != 0:
                grid += '------|-------|------\n'

            for j in range(self.grid.shape[1]):
                if j % 3 == 0 and j != 0:
                    grid += '| '

                value = self.grid.loc[i, j]
                # value = str(value) if pd.isna(value) is False else '-'
                value = '-' if value == 0 else str(value)
                grid += value + ('\n' if j == 8 else ' ')

        return grid

    def number_is_valid(self, number, position):
        ''' Checks whether a certain number is possible at a certain position
            A&P:
                number:
                    int, number to check
                position:
                    tuple of 2 int, row and column of the number'''

        # row:
        for i in range(self.grid.shape[1]):
            if self.grid.loc[position[0], i] == number and i != position[1]:
                return False
        # column:
        for i in range(self.grid.shape[0]):
            if self.grid.loc[i, position[1]] == number and i != position[0]:
                return False
        # subgrid:
        subgrid = self.subgrid(position).copy()
        subgrid.loc[position[0], position[1]] = 0
        if subgrid.isin([number]).any().any():
            return False

        return True

    def subgrid(self, position):
        ''' Returns the subgrid at a certain position
            A&P:
                position:
                    tuple of 2 int, row and column'''

        x = position[0] // 3
        y = position[1] // 3

        return self.grid.loc[x*3:x*3 + 2, y*3:y*3 + 2]

    def find_empty_box(self):
        ''' Finds an empty box in the sudoku'''

        for row in range(self.grid.shape[0]):
            for column in range(self.grid.shape[1]):
                if self.grid.loc[row, column] == 0:
                    return (row, column)

    def solve(self, save_path=None):
        ''' Solves the sudoku
            A&P:
                save_path:
                    str, path to save the sudoku
                    if None, sudoku will not be saved'''

        empty_box_position = self.find_empty_box()

        if empty_box_position is None:
            return True
        else:
            row, column = empty_box_position

        for number in range(1, 10):
            if self.number_is_valid(number, empty_box_position):
                self.grid.loc[row, column] = number

                if self.solve():
                    return True

                self.grid.loc[row, column] = 0

        return False


sudoku1 = Sudoku('sudoku1.xlsx')
sudoku2 = Sudoku('sudoku2.xlsx')
sudoku3 = Sudoku('sudoku3.csv')

print(sudoku1)
sudoku1.solve()
print(sudoku1)
