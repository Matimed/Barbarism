import functools as ft
import itertools as it
import random

from typing import Any
from typing import Union


class Matrix:
    """ Two-dimensional array that implements
        the main python built-in methods.
    """

    @staticmethod
    @ft.lru_cache(maxsize=None)
    def decompose(number):
        """ Returns the list of prime numbers 
            in which the given number can be decomposed. 
        """

        factors = [int(number)]
        while True:

            decomposed_factors=list()
            for factor in factors:

                residing = int(factor**(1/2))
                for n in range(residing, 1, -1):

                    if factor % n == 0:
                        decomposed_factors.extend([n, factor // n])
                        break

                else: decomposed_factors.append(int(factor))
                
            if factors == decomposed_factors: return factors

            factors = decomposed_factors


    @staticmethod
    @ft.lru_cache(maxsize=None)
    def get_divisors(number):
        """ Returns a set of all prime divisors of a given number.
        """

        factors = list(Matrix.decompose(number))
        combinations = set()

        for i in range(0,len(factors)+1):
            combinations = combinations.union(it.combinations(factors,i))
        
        divisors = set()
        for combination in combinations:
            product = 1
            for element in combination:
                product *= element
            
            divisors.add(product)

        return sorted(divisors)


    @staticmethod
    def get_squarest_length(lengths):
        """ Receive a list of tuples and decide which of them 
            forms the most square-like figure. 
        """

        remainders = []
        for length in lengths:

            remainder = abs(length[0] - length[1])
            if remainder == 0: return length
            else: remainders.append(remainder)
                
        return lengths[remainders.index(min(remainders))]


    def __init__(self, rows = list()):
        """ Optionally receive a list of rows (which in turn are list as well) 
            and create the matrix from them.
        """

        self.rows = []

        # Only is used when the matrix is iterated.
        self.iteration_index = None 
        
        if rows:
            try:
                [self.append_row(row) for row in rows]

            except TypeError:
                raise AssertionError("'rows' has to be a list of lists")


    def get_element(self, index: tuple):
        """ Returns the element found at the given index. 
        """

        assert len(index) == 2, \
            "The index must be a tuple of one position in y and one in x"

        if (index[0] >= self.length()[0] or index[1] >= self.length()[1] 
            or index[0] < 0 or index[1] < 0): 
            
            raise IndexError("matrix index out of range")

        return self.rows[index[0]][index[1]]


    def set_element(self, index:tuple, element):
        """ Replace the element found at the given index for a new one. 
        """

        assert len(index) == 2, \
            "The index must be a tuple of one position in y and one in x"

        assert self.length() != (0,0),  \
            "Empty matrices do not support element assignment"

        if index[0] > self.length()[0] or index[1] > self.length()[1]:
            raise IndexError("matrix element assignment index out of range")

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


    def split (self, quantity:int):
        """ Divides the matrix into the requested number of smaller matrices
            ensuring they are all the same size. (The matrix must be able 
            to be divided by the quantity without leaving a remainder).
            Returns a Matrix composed of smaller Matrix.
        """
 
        assert self.length() != (0,0), "Cannot divide an empty matrix"

        total = (self.length()[0]*self.length()[1]) //quantity

        assert total > 0, \
            "The matrix cannot be splited into a such a high number of parts"

        divisors = self.get_divisors(quantity)
        y_options = [self.length()[0] // divisor for divisor in divisors]
        x_options = [self.length()[1] // divisor for divisor in divisors]

        posible_lengths=[]

        for y_option in  y_options:
            for x_option in x_options:
                if y_option * x_option == total:
                    posible_lengths.append((y_option, x_option))
                    x_options.remove(x_option)
                    break

        assert len(posible_lengths)!= 0, (
            "It is impossible to divide the matrix "
            "into the ordered quantity of parts"
        )

        new_length = self.get_squarest_length(posible_lengths)
        grand_matrix = Matrix()

        for row in range(0, self.length()[0],new_length[0]) :
            matrix_row = []

            for column in range(0, self.length()[1],new_length[1]):

                small_matrix = Matrix()
                for y in range(new_length[0]):
                    new_row=[]
                    for x in range(new_length[1]):
                        new_row.append(self.get_element((row+y,column+x)))
                    small_matrix.append_row(new_row)

                matrix_row.append(small_matrix)

            grand_matrix.append_row(matrix_row)

        return grand_matrix


    def get_next_index(self, index:tuple):
        """ Receives an index and return the next one 
            and if receives None returns (0,0).
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


    @ft.lru_cache
    def get_adjacencies(self, index:tuple):
        """ Returns all the elements contiguous to the one 
            of the given index.
        """
 
        elements = []
        
        min_index = [0,0]
        for i in range(len(index)):
            if index[i]!= 0: min_index[i]= index[i]-1
            else: min_index[i]= index[i]


        for row in range (min_index[0], (index[0]+2)):
            for column in range(min_index[1], (index[1]+2)):
                if index == (row, column):
                    continue
                try:
                    elements.append(self.rows[row][column])
                except IndexError:
                    continue
        return elements


    def append_row(self, row: list):
        """ Receives a list of elements and places it 
            under the last row of the matrix.
        """

        if self.rows:
            assert len(row)==self.length()[1], \
                "The length of the row must be the same as the others"
        
        self.rows.append(row)


    def append_column(self, column: list):
        """ Receives a list of elements and places it 
            after the last column of the matrix.
        """

        if self.rows:
            assert len(column)==self.length()[0], \
                "The length of the column must be the same as the others"

            [row.append(column[i]) for i,row in enumerate(self.rows)]

        else:
            [self.rows.append(element) for element in column]


    def pop_row(self, index = -1) -> list:
        """ Removes and returns the row that is in the given index.
        """

        return self.rows.pop(index)


    def pop_column(self, index = -1) -> list:
        """ Removes and returns the column that is in the given index.
        """

        if self.length() == (0,0): raise IndexError("pop from empty matrix")
        return [row.pop(index) for row in self.rows]


    def get_row(self, index) -> list:
        """ Returns the row that is in the given index.
        """

        try:
            return self.rows[index]
        except IndexError:
            raise IndexError("row index out of range")


    def get_column(self, index) -> list:
        """ Returns the column that is in the given index.
        """

        try:
            if self.length() == (0,0): IndexError()
            return [row[index] for row in self.rows]
        except IndexError:
            raise IndexError("column index out of range")


    def get_center(self):
        """ Returns the element in the center of it self.
        """

        assert self.length() != (0,0), \
            "Cannot find the center of an empty matrix"
        
        return self.get_element((self.length()[0] // 2, self.length()[1] // 2))


    def copy(self):
        """ Returns a new Matrix object that have the same values of this one.
        """

        return Matrix([row.copy() for row in self.rows])


    def length(self) -> tuple[int,int]:
        """ Returns a tuple that represent the size of the matrix 
            (number of rows, number of columns).
        """

        if self.rows: return (len(self.rows), len(self.rows[-1]))
        else: return (0,0)

    def insert_row(self, index: int, row: list):
        """ Inserts a given row (list of elements) 
            before the position of the given index.
        """

        if self.length() != (0,0):
            assert len(row)==self.length()[1], \
                "The length of the row must be the same as the others"
            self.rows.insert(index, row)

        else:
            self.append_row(row)


    def insert_column(self, index: int, column: list):
        """ Inserts a given column (list of elements) 
            before the position of the given index.
        """

        if self.length() != (0,0):
            assert len(column)==self.length()[0], \
                "The length of the column must be the same as the others."

            [row.insert(index, column[i]) for i,row in enumerate(self.rows)]
        
        else: 
            self.append_column(column)


    def iter_rows(self):
        """ Returns a iterator for the rows.
        """
        
        return iter(self.rows)


    def random(self):
        """ Returns a random element from the Matrix.
        """

        assert self.length()!= (0,0), \
            "Can't pick a random element from an empty array"

        return random.choice(random.choice(self.rows))


    def get_first_index(self):
        """ Returns the index of the first element 
            of the Matrix that isn't False.
        """

        for element in self:
            if element:
                return self.index(element)


    def get_last_index(self):
        """ Returns the index of the last element 
            of the Matrix that isn't False.
        """

        for row in range(self.length()[0], 0, -1):
            for column in range(self.length()[1], 0, -1):
                if self.get_element((row-1,column-1)):
                    return (row-1,column-1)


    def is_complete(self):
        """ It returns False if there is any empty element in the matrix,
            otherwise it returns true.
        """

        if self.length() == (0,0): return False

        for element in self:
            if not element:
                return False
        
        return True


    def __bool__(self):
        """ It returns False if there is any empty element in the matrix,
            otherwise it returns true.
        """

        return bool(list(filter(bool,self.iter_rows())))


    def __iter__(self):
        """ Returns a restarted iterator.
        """
        
        self.iteration_index = None
        return self

 
    def __next__(self):
        """ Return the next element in the sequence.
        """

        if self.length() == (0,0): raise StopIteration

        # One is subtracted from the length 
        # because the index starts counting from (0,0).
        try: 
            iteration_max = (self.length()[0] -1 ,self.length()[1] - 1)

        except: 
            raise StopIteration
        
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

