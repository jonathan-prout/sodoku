# -*- coding: utf-8 -*-
"""
Simple hobby sudoku solver
for educational use only
"""

cells = {}


class cell(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.possibilities = list(range(1,10))
        
    def possible(self, n):
        return n in self.possibilities
    
    def fix(self, n = None):
        if n not in self.possibilities:
            if n == None:
                if len(self.possibilities) == 1:
                    n = self.possibilities[0]
                    print("fix {} -> {}".format(self,n))
                else:
                    raise ValueError()
            else:
                raise ValueError("{d} is not possible for {s}".format(n, self))
        self.possibilities = [n]
        
        rowfix(self)
        colfix(self)
        blockfix(self)
        
    @property
    def fixed(self):
        return len(self.possibilities) == 1
    
    @property
    def row(self):
        return rows[self.y]
    
    @property
    def col(self):
        return cols[self.x]
    
    @property
    def block(self):
        return blocks[ int(self.x/3) , int(self.y/3)]
        
    def remove(self, n):
         if self.possibilities == [n]:
             raise ValueError("{} must be {}, but remove called".format(
                     self, n))
             return
         if n  in self.possibilities:
             self.possibilities.remove(n)
             if len(self.possibilities) == 1:
                 self.fix()
    def __repr__(self):
        return "cell {},{}".format(self.x, self.y)


class container(object):
    def members_with(self, n):
        for member in self.members:
            if member.possible(n):
                yield(member)
                
    def fixed_numbers(self, n = None):
        for member in self.members:
            if member.fixed:
                if n is None:
                    yield(member.possibilities[0])
                else:
                    if member.possibilities[0] == n:
                        return member
    
    
class row(container):
    def __init__(self, x):
        self.x = x
    @property
    def members(self):
        return [cells[(self.x, y)] for y in range(0,9)]
    
    
    def blocks(self):
        for block in blocks.vaues:
            if int(self.x/3) == block.x:
                yield block
                
    def __repr__(self):
        return "row {}".format(self.x)

class col(container):
    def __init__(self, y):
        self.y = y
    @property
    def members(self):
        return [cells[( x, self.y)] for x in range(0,9)]
    def __repr__(self):
        return "col {}".format(self.y)
    def blocks(self):
        for block in blocks.vaues:
            if int(self.y/3) == block.y:
                yield block
    
class block(container):
    def __init__(self, x,y):
        self.x = x
        self.y = y
    @property
    def rows(self):
        return range(self.x, self.x + 3)
    @property
    def cols(self):
        return range(self.y, self.y + 3)
    @property
    def members(self):
        members = []
        for x in range(3):
            for y in range(3):
             members.append(cells[(( self.x * 3) + x, (self.y * 3) + y )])
        return members
          
    def __repr__(self):
        return "block {},{}".format(self.x, self.y)
    
rows = {}
cols = {}
blocks = {}
for i in range(9):
    rows[i] = row(i)
    cols[i] = col(i)

for x in range(3):
    for y in range(3):
        blocks[(x,y)] = block(x,y)
        
for x in range(9):
    for y in range(9):
        cells[(x,y)] = cell(x,y)
        
def rowfix(cell):
    if len(cell.possibilities) != 1:
        raise ValueError("row called for {} but it has {} possibilities".format(
                cell, cell.possibilities))
    n = cell.possibilities[0]
    row = rows[cell.x]
    for c in row.members:
        if c != cell:
            c.remove(n)
 
def colfix(cell):
    if len(cell.possibilities) != 1:
        raise ValueError("colfix called for {} but it has {} possibilities".format(
                cell, cell.possibilities))
    n = cell.possibilities[0]
    col = cols[cell.y]
    for c in col.members:
        if c != cell:
            c.remove(n)
    
def blockfix(cell):
    if len(cell.possibilities) != 1:
        raise ValueError("block called for {} but it has {} possibilities".format(
                cell, cell.possibilities))
    n = cell.possibilities[0]
    block = blocks[( int(cell.x/3), int(cell.y/3) )]
    for c in block.members:
        if c != cell:
            c.remove(n)
def show():
    print ("  |" +"|".join([" {} ".format(y) for y in range(9)]))
    for x in range(9):
        print("-"*39)
        
        if x % 3 == 0:
            print("-"*39)
        
        for i in range(3):
            if i %3 == 1:
                print ("{} ".format(x), end="")
            else:
                print ("  ", end="")
            for y in range(9):
                if y % 3 == 0:
                   print ("|", end="") 
                cell = cells[(x,y)]
                for j in range(3):
                    n = (3*i) + j + 1
                    print([" ", n][cell.possible(n)], end="")
                print ("|", end="")
                
            print("", end="\n")
            
def find_single(container):
    found = 0
    fixed = list(container.fixed_numbers())
    for i in range(1,10):
        if i not in fixed:
            members_with = list(container.members_with(i))
            if len(members_with) == 1:
                cell = members_with[0]
                print("single {} -> {}".format(cell,i))
                cell.fix(i)
                found +=1
    return found

def find_double(container):
    found = 0
    for cell in container.members:
        if len(cell.possibilities) == 2:
            for othercell in container.members:
                if othercell != cell:
                    if othercell.possibilities == cell.possibilities:
                        for remainder in container.members:
                            if remainder not in [cell, othercell]:
                                for n in cell.possibilities:
                                    if remainder.possible(n):
                                        print("{} and {} are double of {}. Removing {} from {}".format(
                                                cell, othercell, cell.possibilities, n, remainder))
                                        remainder.remove(n)
                                        found += 1
    return found

                    
def block_row_col(blockcontainer):

    found = 0
    for i in range(1, 10):
        rows_with_n = []
        cols_with_n = []
        for c in blockcontainer.members:
            if c.possible(i):
                if not c.x in rows_with_n:
                    rows_with_n.append(c.x)
                if not c.y in cols_with_n:
                    cols_with_n.append(c.y)
        if len(rows_with_n) == 1: 
            r = rows[rows_with_n[0]]
            for c in r.members:
                if c.block != blockcontainer:
                    if c.possible(i):
                        print("{} must be on {} of block {}. Removing from {}".format(
                                        i, r, blockcontainer, c))
                        c.remove(i)
                        found += 1
        if len(cols_with_n) == 1: 
            r = cols[cols_with_n[0]]
            for c in r.members:
                if c.block != blockcontainer:
                    if c.possible(i):
                        print("{} must be on {} of block {}. Removing from {}".format(
                                        i, r, blockcontainer, c))
                        c.remove(i)
                        found += 1
    return found

def block_block(block1, block2):
    found = 0
    for i in range(1, 10):
        rows_with_n = []
        cols_with_n = []
        for c in block1.members:
            if c.possible(i):
                if not c.x in rows_with_n:
                    rows_with_n.append(c.x)
                if not c.y in cols_with_n:
                    cols_with_n.append(c.y)    
        for c in block2.members:
            if c.possible(i):
                if not c.x in rows_with_n:
                    rows_with_n.append(c.x)
                if not c.y in cols_with_n:
                    cols_with_n.append(c.y) 
        if block1.x == block2.x:
            if len(rows_with_n) == 2: 
                blocks_in_row = [blocks[(block1.x, 0)],blocks[(block1.x, 1)],blocks[(block1.x, 2)]]
                blocks_in_row.remove(block1)
                blocks_in_row.remove(block2)
                other_block = blocks_in_row[0]
                for c in other_block.members:
                    if c.x in rows_with_n:
                        if i in c.possibilities:
                            print("{} must be on rows {} of blocks {} {}. Removing from {}".format(
                                        i, rows_with_n, block1, block2, c))
                            c.remove(i)
                            found += 1
        if block1.y == block2.y:
            if len(cols_with_n) == 2: 
                blocks_in_col = [blocks[(0, block1.y)],blocks[(1, block1.y)],blocks[(2, block1.y)]]
                blocks_in_col.remove(block1)
                blocks_in_col.remove(block2)
                other_block = blocks_in_col[0]
                for c in other_block.members:
                    if c.y in cols_with_n:
                        if i in c.possibilities:
                            print("{} must be on cols {} of blocks {} {}. Removing from {}".format(
                                        i, cols_with_n, block1, block2, c))
                            c.remove(i)
                            found += 1
    return found
        
    
    

def solved():
    for c in cells.values():
        if not c.fixed:
            return False
    return True

def tally():
    t = 0
    for c in cells.values():
        if c.fixed:
            t += 1
    return t

def parse(filename):
    import csv
    x = 0
    with open(filename, "r") as fobj:
        reader = csv.reader(fobj, delimiter=',', quotechar='"')
        for row in reader:
            if x >8:
                break
            if len(row) < 9:
                continue
            y =0
            for c in row:
                if y >8:
                    break
                try:
                    n = int(c)
                    if n in range(1,10):
                        cells[(x,y)].fix(n)
                
                except:
                    pass
                print (c, end=".")
                y += 1
            x += 1
            print(".")
            
def solve():
    while not solved():
        found = 0
        for i in range(9):
            found += find_single(rows[i])
            found += find_single(cols[i])
        for x in range(3):
            for y in range(3):
                found += find_single(blocks[(x,y)])
        for i in range(9):
            found += find_double(rows[i])
            found += find_double(cols[i])
        for x in range(3):
            for y in range(3):
                found += find_double(blocks[(x,y)])
        
        for x in range(3):
           for y in range(3):
                found += block_row_col(blocks[(x,y)])      
        for x in range(3):
            for y in range(1, 3):
                found += block_block(blocks[(x,0)], blocks[(x,y)])  
        for y in range(3):
            for x in range(1, 3):
                found += block_block(blocks[(0,y)], blocks[(x,y)])  
        if not found:
            return False
        else:
            print("found {}".format(found))
    return True
        


