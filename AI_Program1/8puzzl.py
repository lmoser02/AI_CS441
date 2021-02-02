#Program: 8 Puzzle with heuristics
#AI Winter 2021
#Leah Moser
#This program is designed to solve the 8 puzzle from a random shuffle using 
#Different AI heuristics 


import random
import math

goal_state = [[1,2,3],
               [4,5,6],
               [7,8,0]]

def index(object, sequence):
    """global function to help get the index"""
    if object in sequence:
        return sequence.index(object)
    else:
        return -1

class Eightpuzzle:
    def __init__(self):
        #constructor
        self.depth = 0
        self.hval = 0
        self.parent = None
        self.adj = []
        for i in range(3):
            self.adj.append(goal_state[i][:])

    def copy_cc(self):
        #simutlates copy constructor 
        puz = Eightpuzzle()
        for i in range(3):
            puz.adj[i] = self.adj[i][:]
        return puz

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj == other.adj

    def __str__(self):
        #make look pretty
        s = ''
        for row in range(3):
            s += ' '.join(map(str, self.adj[row]))
            s += '\n'
        return s

    def get_moves(self):
        """Returns list that can be swapped"""
        # get row and column of the empty piece
        row, col = self.find(0)
        empty = []
        
        # get possible to moves
        if row > 0:
            empty.append((row - 1, col))
        if col > 0:
            empty.append((row, col - 1))
        if row < 2:
            empty.append((row + 1, col))
        if col < 2:
            empty.append((row, col + 1))
        return empty

    def make_moves(self):
        """Finds the moves to be made"""
        free = self.get_moves()
        zero = self.find(0)

        def swap_and_copy(a, b):
            puz = self.copy_cc()
            puz.swap(a,b)
            puz.depth = self.depth + 1
            puz.parent = self
            return puz

        return map(lambda pair: swap_and_copy(zero, pair), free)

    def get_path(self, path):
        """Finds the path"""
        if self.parent == None:
            return path
        else:
            path.append(self)
            return self.parent.get_path(path)

    def shuffle(self, step_count):
        for i in range(step_count):
            row, col = self.find(0)
            free = self.get_moves()
            target = random.choice(free)
            self.swap((row, col), target)            
            row, col = target

    def find(self, value):
        """returns the row/col"""
        for row in range(3):
            for col in range(3):
                if self.adj[row][col] == value:
                    return row, col
    
    def peek(self, row, col):
        """returns the value at the row and column"""
        return self.adj[row][col]

    def poke(self, row, col, value):
        """sets the value at the row and column"""
        self.adj[row][col] = value

    def swap(self, a, b):
        """swaps values"""
        temp = self.peek(*a)
        self.poke(a[0], a[1], self.peek(*b))
        self.poke(b[0], b[1], temp)

    def a_star_search(self, h):
        """A* search to goal state. Using h to call the different heuristics
        """
        def is_solved(puzzle):
            return puzzle.adj == goal_state
        
        open_list = [self]
        closed_list = []
        move_count = 0
        while len(open_list) > 0:
            puzz = open_list.pop(0)
            move_count += 1
            if (is_solved(puzz)):
                if len(closed_list) > 0:
                    if puzz.get_path([]):
                        return puzz.get_path([]), move_count
                    elif move_count > 2000:
                        print "Solution not found max steps reach"
                        return [], 0
                else:
                    return [puzz]

            the_moves = puzz.make_moves()
            index_open = index_closed = -1
            for move in the_moves:
                index_open = index(move, open_list)
                index_closed = index(move, closed_list)
                current_hval = h(move)
                #the main difference from BFS is here 
                #f(n) = h(n) + g(n)
                fval = current_hval + move.depth

                if index_closed == -1 and index_open == -1:
                    move.hval = current_hval
                    open_list.append(move)
                elif index_open > -1:
                    copy = open_list[index_open]
                    if fval < copy.hval + copy.depth:
                        copy.hval = current_hval
                        copy.parent = move.parent
                        copy.depth = move.depth
                elif index_closed > -1:
                    copy = closed_list[index_closed]
                    if fval < copy.hval + copy.depth:
                        move.hval = current_hval
                        closed_list.remove(copy)
                        open_list.append(move)
            
            closed_list.append(puzz)
            open_list = sorted(open_list, key=lambda p: p.hval + p.depth)
        if len(open_list) < 0:
            print "Failed to solve"
            return [], 0

    def best_first_search(self, h):
        """Best First Search. Using the h fucntion to grab the hueristic
        """
        def is_solved(puzzle):
            return puzzle.adj == goal_state
        open_list = [self]
        closed_list = []
        move_count = 0
        while len(open_list) > 0:
            puzz = open_list.pop(0)
            move_count += 1
            if (is_solved(puzz)):
                if len(closed_list) > 0:
                    if puzz.get_path([]):
                        return puzz.get_path([]), move_count
                    elif move_count > 2000:
                        print "Cant find solution max steps reached"
                        return [], 0
                    else:
                        print "Cant find solution"
                        return [], 0
                else:
                    return [puzz]

            the_moves = puzz.make_moves()
            index_open = index_closed = -1
            for move in the_moves:
                index_open = index(move, open_list)
                index_closed = index(move, closed_list)
                current_hval = h(move)
                #the main difference from A* is here 
                #f(n) = h(n) 
                fval = current_hval
            
                if index_closed == -1 and index_open == -1:
                    move.hval = current_hval
                    open_list.append(move)
                elif index_open > -1:
                    copy = open_list[index_open]
                    if fval < copy.hval + copy.depth:
                        copy.hval = current_hval
                        copy.depth = move.depth
                        copy.parent = move.parent
                elif index_closed > -1:
                    copy = closed_list[index_closed]
                    if fval < copy.hval + copy.depth:
                        move.hval = current_hval
                        closed_list.remove(copy)
                        open_list.append(move)
            closed_list.append(puzz)
            open_list = sorted(open_list, key=lambda p: p.hval + p.depth)
            
        if len(open_list) < 0:
            print "Failed to solve"
            return [], 0

########end of 8 puzzle class attributes######

def heur(puzzle, curr_total, total_calc):
    """
    General hueristic that finds the current and target position toltal
    """
    total = 0
    for row in range(3):
        for col in range(3):
            num = puzzle.peek(row, col) - 1
            target_col = num % 3
            target_row = num / 3
            if target_row < 0: 
                target_row = 2

            total += curr_total(row, target_row, col, target_col)

    return total_calc(total)

#####This is where the hueristics live####
def h_manhattan(puzzle):
    """One of the fastest hueristic using lambda to return the calculation to huer function"""
    return heur(puzzle,
                lambda r, tr, c, tc: (abs(tr - r) + abs(tc - c)), lambda a : a)

def h_default(puzzle):
    """This runs a Bredth first Equivalent"""
    return 0

def h_greedy(puzzle):
    """This returns the smallest path to the huer. Always the easiest path"""
    return heur(puzzle, lambda r, tr, c, tc: min(abs(tr - r), abs(tc - c)), lambda a: a)

def misplaced(puz1, puz2):
        """returns the amount of misplaced tiles"""
        val = 0
        for row in range(3):
            for col in range(3):
                if puz1.adj[row][col] != puz2.adj[row][col]:
                    val += 1
        return huer(puzzle, lambda r, tr, c, tc: val, 0, lambda a: a)

def h_linear_conflict(puzzle):
    """This uses math to associate the linear conflict method"""
    return heur(puzzle, lambda r, tr, c, tc: math.sqrt(math.sqrt((tr - r)**2 + (tc - c)**2)),lambda a: a)

if __name__ == "__main__":
    ###driver code####
    p = Eightpuzzle()
    p.shuffle(20)
    print (p)
    path, steps1 = p.a_star_search(h_default)
    if path or steps1 < 0:
                print "Solution not found"
    path.reverse()
    moves = 0
    for i in path: 
        moves+=1
        print (i)
    path, steps2 = p.a_star_search(h_manhattan)
    print "Done with Manhattan heur using A* in", steps2, "steps"
    path, steps3 = p.a_star_search(h_greedy)
    print "Done with Misplaced Tiles heur using A* in ", steps3, "steps"
    path, steps4 = p.best_first_search(h_manhattan) 
    print "Done with Mannhattan huer using Best First Search in ", steps4
    path, steps5 = p.best_first_search(h_greedy)
    print "Done with Misplaced Tiles heur using Best First Search in", steps5
    path, steps6 = p.a_star_search(h_linear_conflict)
    print "Done with Linear Conflict using A* search ", steps6
    path, steps7 = p.best_first_search(h_linear_conflict)
    print "Done with Linear Conflict using Best First Search", steps7
    print "Done with Breadth First Search(no heuristic) in", steps1, "steps"