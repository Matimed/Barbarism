from typing import Any
from typing import Union


class Matrix:
    """ Two-dimensional array that implements
        the main python built-in methods.
    """

    def __init__(self, rows = list()):
        """ Optionally receive a list of rows (which in turn are list as well) 
            and create the matrix from them.
        """

        self.rows = []
        self.iteration_index = None 
        # Only is used when the matrix is iterated.
        
        if rows:
            for row in rows:
                self.append_row(row)



    def get_element(self, index: tuple):
        """ Returns the element found at the given index. 
        """

        assert len(index) == 2, \
            "The index must be a tuple of one position in x and one in y."

        assert index[0] < self.length()[1] and index[1] < self.length()[0], \
            "Index out of range."

        return self.rows[index[0]][index[1]]


    def set_element(self, index:tuple, element):
        """ Replace the element found at the given index for a new one. 
        """

        assert len(index) == 2, \
            "The index must be a tuple of one position in x and one in y."

        assert index[0] < self.length()[1] and index[1] < self.length()[0], \
            "Index out of range."

        self.rows[index[0]][index[1]] = element


    def index(self, element: Any) -> Union[tuple[int, int] , bool]: 
        """ Returns the index (tuple) of the first element
            in the matrix that matches the given element 
            and if it cannot find any, it returns False.
        """

        for row_index, row in enumerate(self.rows):
            if element in row:
                return  (row_index, row.index(element))

        return False


    def get_next_index(self, index:tuple):
        """ Recives an index and return the next one 
            and if recives None returns (0,0).
        """

        if index == None: return (0,0)

        length = self.length()
        if index[1] == length[1] - 1:
            if index[0]  == length[0] - 1:
                raise IndexError
            else:
                return (index[0]+ 1, 0)
        else:
            return (index[0], index[1] + 1)


    def append_row(self, row: list):
        """ Receives a list of elements and places it 
            under the last row of the matrix.
        """

        if self.rows:
            assert len(row)==self.length()[1], \
                "The length of the row must be the same as the others."
        
        self.rows.append(row)


    def append_column(self, column: list):
        """ Receives a list of elements and places it 
            after the last column of the matrix.
        """

        if self.rows:
            assert len(column)==self.length()[0], \
                "The length of the column must be the same as the others."

            for i, row in enumerate(self.rows):
                row.append(column[i])

        else:
            for element in column:
                self.rows.append([element])


    def pop_row(self, index = -1) -> list:
        """ Removes and returns the row that is in the given index.
        """

        return self.rows.pop(index)


    def pop_column(self, index = -1) -> list:
        """ Removes and returns the column that is in the given index.
        """

        column = []
        for row in self.rows:
            column.append(row.pop(index))
        return column


    def copy(self):
        """ Returns a new Matrix object that have the same values of this one.
        """

        rows = []
        for row in self.rows:
            rows.append(row.copy())

        return Matrix(rows)


    def length(self) -> tuple:
        """ Returns a tuple that represent the size of the matrix 
            (number of rows, number of columns).
        """

        rows = len(self.rows)
        columns = len(self.rows[-1])
        return (rows,columns)
    

    def insert_row(self, index: int, row: list):
        """ Inserts a given row (list of elements) 
            before the position of the given index.
        """

        if self.rows:
            assert len(row)==self.length()[1], \
                "The length of the row must be the same as the others."
            self.rows.insert(index, row)

        else:
            self.append_row(row)


    def insert_column(self, index: int, column: list):
        """ Inserts a given column (list of elements) 
            before the position of the given index.
        """

        if self.rows:
            assert len(column)==self.length()[0], \
                "The length of the column must be the same as the others."

            for i, row in enumerate(self.rows):
                    row.insert(index,column[i])
        
        else: 
            self.append_column(column)


    def iter_rows(self):
        """ Returns a iterator for the rows.
        """
        
        return iter(self.rows)


    def __iter__(self):
        """ Returns a restarted iterator.
        """
        
        self.iteration_index = None
        return self

 
    def __next__(self):
        """ Return the next element in the sequence.
        """

        # One is subtracted from the length 
        # because the index starts counting from (0,0).
        iteration_max = (self.length()[0] -1 ,self.length()[1] - 1)

        if self.iteration_index == iteration_max:
            raise StopIteration

        self.iteration_index = self.get_next_index(self.iteration_index)
        return self.get_element(self.iteration_index)


    def __str__(self) -> str:
        """ Returns a string which represents the matrix.
        """

        rows = []
        for row in self.rows:
            rows.append(' '.join(map(str, row)))
        
        return ' \n'.join(rows)

