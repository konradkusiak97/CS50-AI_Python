import sys

from crossword import *
from collections import deque
import copy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        newDomains = copy.deepcopy(self.domains)
        for var in newDomains:
            for word in newDomains[var]:
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        foundMatch = False
        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return False
        result = False
        newDomains = copy.deepcopy(self.domains)
        for x_word in newDomains[x]:
            for y_word in newDomains[y]:
                if y_word[overlap[1]] == x_word[overlap[0]]:
                    foundMatch = True
            if not foundMatch:
                self.domains[x].remove(x_word)
                result = True
        return result

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Initilizing the queue
        if arcs == None:
            queue = deque()
            for v in self.crossword.variables:
                for vArc in self.crossword.neighbors(v):
                    queue.append((v, vArc))
        else:
            queue = deque(arcs)

        # revising each variable form queue
        while len(queue) != 0:
            arc = queue.popleft()
            if self.revise(arc[0], arc[1]):
                if len(self.domains[arc[0]]) == 0:
                    return False
                for v in self.crossword.neighbors(arc[0]) - {arc[1]}:
                    queue.append((v, arc[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment:
                return False
            if assignment[var] == None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check for repetitions in values 
        l = 0
        checkingSet = set()
        for var in assignment:
            checkingSet.add(assignment[var])
            l += 1
        if l != len(checkingSet):
            return False

        # Check if length of value is correct
        for var in assignment:
            if var.length != len(assignment[var]):
                return False
        
        # Check for conflicts between neighbors
        for var in assignment:
            neighbors = self.crossword.neighbors(var)
            for n in neighbors:
                pair = self.crossword.overlaps[var, n]
                if n in assignment:
                    if assignment[var][pair[0]] != assignment[n][pair[1]]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """ 
        neighbors = self.crossword.neighbors(var)
        hashMap = dict()
        sortedValues = []
        for value in self.domains[var]:
            count = 0
            for n in neighbors:
                if n not in assignment:
                    indx = self.crossword.overlaps[var, n]
                    for nval in self.domains[n]:
                        if nval[indx[1]] != value[indx[0]]:
                            count += 1
            hashMap[value] = count
            sortedValues.append(value)
        sortedValues.sort(key=hashMap.get)
        return sortedValues
        
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassignedVars = set(self.domains.keys()) - set(assignment.keys())
        hashMap = dict()
        hashMapAdd = dict()
        sortedVars = []
        for var in unassignedVars:
            hashMap[var] = len(self.domains[var])
            hashMapAdd[var] = len(self.crossword.neighbors(var))
            sortedVars.append(var)

        sortedVars.sort(key=hashMap.get)
        equalNum = []
        for i in range(len(sortedVars)-1):
            if len(self.domains[sortedVars[i]]) == len(self.domains[sortedVars[i+1]]):
                equalNum.append(sortedVars[i])
                equalNum.append(sortedVars[i+1])
            else:
                break
        if len(equalNum) == 0:
            return sortedVars[0]

        equalNum.sort(key=hashMapAdd.get,reverse=True)
        return equalNum[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                arcs = set()
                for n in self.crossword.neighbors(var):
                    arcs.add((n, var))
                currentDomain = copy.deepcopy(self.domains)
                inference = self.ac3(arcs)
                if not inference:
                    self.domains = currentDomain
                else:
                    infr = set()
                    for v in self.domains:
                        if len(self.domains[v]) == 1:
                            assignment[v] = self.domains[v].pop()
                            infr.add(v)
                result = self.backtrack(assignment)
                if result != None:
                    return result
                del assignment[var]
                for v in infr:
                    del assignment[v]
            else:
                del assignment[var]

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words =  sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main() 