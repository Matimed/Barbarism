from functools import reduce
from time import time
from src.model import Cell
from lib.abstract_data_types.matrix import Matrix
from lib.chunk import Chunk
from lib.position import Position

def generate(order):
    with open('tests/position_generation.log', 'a') as log:
        print_log(file=log)
        print_log("-"*35, file=log)
        print_log ("Atempt to generate "+ str(order) + " positions:", file = log)
        print_log(file=log)

        start_time = time()
        positions = _generate_positions(order)
        last_time = time() - start_time
        print_log("Positions:   " +  seconds_to_str(last_time), file = log)

        chunks = _generate_chunks(25, order, positions)
        last_time = time() - (start_time + last_time)
        print_log("Chunks:      "+ seconds_to_str(last_time), file = log)

        cells = _generate_cells(positions)
        last_time = time() - (start_time + last_time)
        print_log("Cells:       "+ seconds_to_str(last_time) , file = log)

        print_log("Total:       "+ seconds_to_str(time() - start_time), file = log) 
        print_log("-"*35, file = log)


def print_log(text = '', file = None):
    print (text)
    print(text, file=file)


def seconds_to_str(t):
    minutes =  "%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60])
    return minutes + " minutes."


def _generate_positions(order):
    """ Generates a Matrix of Position type objects 
        based on the given size (order).
    """

    return Matrix(Position.create_collection((0,0), (order -1 ,order -1)))


def _generate_chunks(min_size:int, order, positions):
    """ Returns a Matrix of Chunk objects based on a given size 
        (the minimum number of cells that can fit in a Chunk).
    """

    size = min_size
    while True:
        if not (order%size):
            break
        size +=1

    splited_positions = positions.split(order/size)

    return Matrix([[Chunk(positions, (y,x)) for x, positions in enumerate(row)]
        for y, row in enumerate(splited_positions.iter_rows())])


def _generate_cells(positions):
    """ Receives a Matrix of Position type objects and
        generate a dict of Cell type objects with a position as key.
    """
    
        
    return {position:Cell() for row in positions.iter_rows() 
        for position in row}


#generate(order)
