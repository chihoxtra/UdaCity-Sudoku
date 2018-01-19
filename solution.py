
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#custom:
diag_units = [[(rows[i]+cols[i]) for i in range(len(rows))],[(rows[i]+cols[8-i]) for i in (range((len(rows))))]]
diagGame = True

unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
if diagGame == True:
    unitlist = unitlist + diag_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def isSolved(values):

    solvedStatus = True

    if type(values) != bool:

        for arr in unitlist:
            sub_total = 0
            for u in arr:
                sub_total += int(values[u])

            if sub_total != 45:
                solvedStatus = False
    else:
        print("Unsolved!")

    return solvedStatus

def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    for unit_key, related_units in units.items():
        if len(values[unit_key]) == 2:
            for related_units_arr_index in range(len(related_units)): #len could be 3 or 4

                #valid range of naked twins applies to related units ONLY
                doubledigit_value = [] #keep track of all occurence of 2-digit entry
                doubledigit_unit = []
                twins_units = []
                twins_value = []
                twins_domain = []

                """
                print(unit_key)
                print(related_units_arr_index)
                print(len(related_units))
                print(related_units[related_units_arr_index])
                """

                for u in related_units[related_units_arr_index]:
                    if len(values[u]) == 2:
                        if values[u] in doubledigit_value and values[u] not in twins_value: #there is a twin found
                            if doubledigit_unit[doubledigit_value.index(values[u])] != u: #a new unit found
                                ind = doubledigit_value.index(values[u])

                                twins_locs = []
                                twins_locs.append(doubledigit_unit[ind])
                                twins_locs.append(u)

                                twins_units.append(twins_locs)
                                twins_value.append(values[u])
                                twins_domain.append(related_units_arr_index)

                        else:
                            doubledigit_value.append(values[u])
                            doubledigit_unit.append(u)


                if len(twins_units) > 0 and len(twins_units) == len(twins_value):

                    for twin_index in range(len(twins_value)):

                        this_twin_locs = twins_units[twin_index] #list
                        this_twin_value = twins_value[twin_index] #the value
                        this_twin_domain = twins_domain[twin_index]
                        #print(this_twin_value, this_twin_locs)

                        for t in twins_value[twin_index]:
                            for this_twin_loc in this_twin_locs:

                                twins_related_units = units[this_twin_loc]

                                for u in twins_related_units[this_twin_domain]:

                                    if u not in this_twin_locs and t in values[u]:
                                        if len(values[u]) > 1 and this_twin_value != values[u]:
                                            values[u] = values[u].replace(t,'')

    return values

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    """if a box is assigned, remove the same value from candidate list of related nbhd boxes"""

    for key, val in values.items():
        if len(val) == 1:      #assigned single value
            for unit_arr in units[key]:
                for b in unit_arr: #scan thru the 3types of units in "units"
                    if val in values[b] and val != values[b]:
                        values[b] = values[b].replace(val, '')

                        #values = assign_value(values, b, values[b].replace(val, ''))

    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for box, nhb_units_array in units.items():

        possible_val_list = values[box]  # for each unit extract the potential candidate list
        #print(box)

        if len(possible_val_list) > 1: # not consider those assigned

            for this_val in possible_val_list:  #iterate thru each candidates

                for nhb_units_row in nhb_units_array:  #nhb_units_array has len of 3 OR 4 if diag

                    count = 0

                    for u in nhb_units_row:

                        if this_val in values[u] and box != u:
                            count += 1

                    if count == 0:                #if there is no other occurance
                        values[box] = this_val
                        #print(box, this_val)

                        #values = assign_value(values, box, this_val)

    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # add naked_twins strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    # Choose one of the unfilled squares with the fewest possibilities

    status = isSolved(values)

    if status == False: #trial and error approach

        # find the box with fewest possible options
        min_box = ''
        min_length = 9
        for r in row_units:
            for u in r:
                if type(values) != bool and len(values[u]) > 1 and len(values[u]) < min_length:
                    min_box = u
                    min_length = len(values[u])


        #display(values)
        if min_box != '': # try different values and continue down the tree
            for pos_val in values[min_box]:

                tmp_values = dict(values) #create temp values, disgard if found to be deadend

                tmp_values[min_box] = pos_val

                tmp_val = search(tmp_values)

                if type(tmp_val) != bool:
                    values = tmp_val
                    return values
        else:

            status = isSolved(values)

            if status == False:
                values = status

            return values

    else:
        #Puzzle should be solved!!!
        #display(values)

        if status == False:
            values = status

        return values

    status = isSolved(values)

    if status == False:
        values = status

    return values


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid0 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid1 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid2 = '6....4......7...1........3.....8.....31...59.....7.....2........9...3......6....7'
    diag_sudoku_grid3 = '.....1..66.....894.7.....1........41..2...9..76........8.....2.356.....81..6.....'


    display(grid2values(diag_sudoku_grid2))
    result = solve(diag_sudoku_grid2)
    display(result)
    '''
    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
    '''
