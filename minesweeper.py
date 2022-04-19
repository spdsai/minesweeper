
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.

        """
        if len(self.cells) == self.count :
            return self.cells

        return None

        




        

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        

        if self.count == 0:
            return self.cells

        return None


        
        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        minecells = set()
        for item in self.cells :
            if cell == item :
                minecells.add(item)
                self.count -= 1

        self.cells = self.cells - minecells

            
        
           
          

        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        temp2 = set()
        for xyz in self.cells :
            if xyz == cell :
                temp2.add(cell)

        self.cells = self.cells - temp2


             
        
            
        


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
         #self.knowledge.append(Sentence(cell,count))
         #3
        c1 = list()

        a,b = cell

        
        
        for rn in range(a-1, a+2):
            for cn in range(b-1, b+2):
                if (rn >= 0 and rn < 8) \
                and (cn >= 0 and cn <8) \
                and (rn, cn) != cell \
                and (rn, cn) not in self.safes \
                and (rn, cn) not in self.mines:
                    c1.append((rn, cn))
                if (rn, cn) in self.mines:
                    count -= 1

        
        
        s = Sentence(c1,count)
        self.knowledge.append(s)

        #4
        newresults = list()
        for y in self.knowledge :

            if y == s :
                continue

            elif y.cells.issuperset(s.cells):

                setdif = y.cells - s.cells
                
                #safes found
                if y.count == s.count :
                    for safefound in setdif :
                        self.mark_safe(safefound)

                #mines found
                elif len(setdif) == y.count -s.count :
                    for minefound in setdif :
                        self.mark_mine(minefound)
                
                else :
                    newresults.append(Sentence(setdif, y.count - s.count)) 

            elif s.cells.issuperset(y.cells):
                setdif = s.cells - y.cells

                #safes found
                if y.count == s.count :
                    for safefound in setdif :
                        self.mark_safe(safefound)

                #mines found
                elif len(setdif) == s.count -y.count :
                    for minefound in setdif :
                        self.mark_mine(minefound)
                
                else :
                    newresults.append(Sentence(setdif, s.count - y.count)) 


        self.knowledge.extend(newresults)
        







        
        #5 removing duplicates in knowledge if any

       
        unique_knowledge = []
        for s in self.knowledge:
            if s not in unique_knowledge:
                unique_knowledge.append(s)
        self.knowledge = unique_knowledge

        #checking last time for if there are obviuos len = count or safes present in out knowledge base
    
        final_knowledge = []
        for s in self.knowledge:
            final_knowledge.append(s)
            if s.known_mines():
                for mineFound in s.known_mines():
                    self.mark_mine(mineFound)
                final_knowledge.pop(-1)
            elif s.known_safes():
                for safeFound in s.known_safes():
                    self.mark_safe(safeFound)
                final_knowledge.pop(-1)
        self.knowledge = final_knowledge





           








    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        #for a in self.safes :
        #    if a not in self.moves_made :
        #       return a
        # 
        safeCells = self.safes - self.moves_made
        if not safeCells:
            return None 
           
        move = safeCells.pop() #returning the last value of the set 
        return move 

            #how to return none in this function

        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        counthere = 0 
        while counthere <64 :
            i = random.randint(0,7)
            j = random.randint(0,7)
            a = (i,j)
            if a not in self.moves_made :
                if a not in self.mines:
                    counthere += 1
                    return a 
            else:
                counthere += 1 

        return None
        
