import numpy as np
import time

class Literal:
    def __init__(self, name, negated=False):
        self.name = name
        self.negated = negated

    def __str__(self):
        return f"¬{self.name}" if self.negated else self.name
    
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.negated == other.negated
        return False

    #less than method used to compare two literals using sorted method
    def __lt__(self, other):
        return str(self) < str(other)
    
    def __hash__(self):
        return hash((self.name, self.negated))

    

class CNFClause:
    def __init__(self, cnfclauses):
        # Body is a list of Literals
        self.literals = cnfclauses
        self.remove_duplicates() 

    def __str__(self):
        return f' {" V ".join(str(literal) for literal in self.literals)}'
    
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return sorted(self.literals) == sorted(other.literals)
        return False

    def remove_duplicates(self):
        self.literals = list(set(self.literals))
        self.literals.sort()
        
class KnowledgeBaseCNF:
    def __init__(self):
        self.clauses = list()
        self.score=0

    def tell(self, observation):
        
        location = [observation['x'], observation['y']]
        if observation['breeze']:
            self.add_known_true(f'B{location[0]}{location[1]}')

            self.generate_cnf_clauses("breeze", location)


        if observation['breeze']==False:
            self.add_known_true(f'¬B{location[0]}{location[1]}') 

        if observation['stench']:
            self.add_known_true(f'S{location[0]}{location[1]}')
            self.generate_cnf_clauses("stench", location)
       
        if observation['stench']==False:
            self.add_known_true(f'¬S{location[0]}{location[1]}')

        if np.diff([self.score, observation['score']]) <= 999:
            self.add_known_true(f'¬P{location[0]}{location[1]}')
            self.add_known_true(f'¬W{location[0]}{location[1]}')

        self.score=observation['score']

    def add_known_true(self, literal):

        if "¬" in literal:
            literal=Literal(literal[1:],negated=True)
        else:
            literal=Literal(literal)
        self.clauses.append(CNFClause([literal]))
    
    def ask(self, query):
        return self.resolution(query)

    def print_kb(self):
        print("--" * 20)
        print("These are the CNF Clauses in the KB:")
        for clause in self.clauses:
            print(str(clause))
            
        print("--" * 20)

        

    def generate_cnf_clauses(self,perception,location):
        x,y=location
        cnf_clauses=[]
        if perception=="breeze":
            neighbors=self.get_neighboring_fields(x,y)
            cnf_clauses.append(CNFClause([Literal(f"B{x}{y}",negated=True)] + [Literal(f"P{neighbor[0]}{neighbor[1]}") for neighbor in neighbors]))
            for neighbor in neighbors:
                cnf_clauses.append(CNFClause([Literal(f"B{x}{y}"), Literal(f"P{neighbor[0]}{neighbor[1]}", negated=True)]))


        if perception=="stench":
            neighbors=self.get_neighboring_fields(x,y)
            cnf_clauses.append(CNFClause([Literal(f"S{x}{y}",negated=True)] + [Literal(f"W{neighbor[0]}{neighbor[1]}") for neighbor in neighbors]))
            for neighbor in neighbors:
                cnf_clauses.append(CNFClause([Literal(f"S{x}{y}"), Literal(f"W{neighbor[0]}{neighbor[1]}", negated=True)]))

        self.clauses.extend(cnf_clauses)

    def get_neighboring_fields(self, x, y):
        neighbors = []

        # For each neighboring square
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy

            # If the neighboring square is within the grid boundaries
            if 0 <= new_x <= 3 and 0 <= new_y <= 3:
                # Add the coordinates to the neighbors list
                neighbors.append((new_x, new_y))

        return neighbors


    def resolve(self, c1, c2):
        resolvents = []

        for literal_c1 in c1.literals:
            for literal_c2 in c2.literals:
                #literal_c1 and literal_c2 are instances of Literal
                # Check if there's a literal in c1 that is the negation of a literal in c2
                if literal_c1.name == literal_c2.name and literal_c1.negated != literal_c2.negated:
                    new_literal1 = [literal for literal in c1.literals if literal != literal_c1]
                    new_literal2 = [literal for literal in c2.literals if literal != literal_c2]
                  
                    new_literals = new_literal1 + new_literal2
                    if not new_literals: # return an empty clause if new_literals is empty
                        return [CNFClause([])]
                    else:
                        resolvents.append(CNFClause(new_literals))

        # Return the resolvents if there are any

        if resolvents:
            return resolvents
        #Otherwise None
        return None

    def resolution(self, alpha):
  
        clauses = self.clauses.copy()
      
        #clauses is a list of CNFClause
        #CNFClause is a list of Literal
        #add negation in list of CNFClause
        clauses.append(CNFClause([self.negate(alpha)]))

        new = []
        while True:
            n_clauses = len(clauses)
            
            for i in range(n_clauses):
                for j in range(i + 1, n_clauses):
                    c1 = clauses[i]
                    c2 = clauses[j]

                    resolvents = self.resolve(c1, c2)

                    if resolvents is None:
                        continue
                    
                    for resolvent in resolvents:
                        if not resolvent.literals:
                            return True
                        #COMPARE THIS                        
                        # if not any(self.equal_clauses(clause, resolvent) for clause in new):
                        #     new.append(resolvent)
                        #WITH THIS
                        found=False
                        new_copy=new.copy()
                        for clause in new_copy:
                            if self.equal_clauses(clause, resolvent):
                                found=True
                                break
                        if not found:
                            new.append(resolvent)

            if not new:
                return False  
        
            if all(any(self.equal_clauses(c, n) for c in clauses) for n in new):
                return False

            clauses.extend(new)


    def negate(self, literal):

        if "¬" in literal:
            return Literal(literal[1:], negated=False)
        
        return Literal(literal, negated=True)
    
        
    def equal_clauses(self, c1, c2):
        # Extract the literals from each clause and sort them
        literals_c1 = sorted([str(l) for l in c1.literals])
        literals_c2 = sorted([str(l) for l in c2.literals])
      
        # Compare the sorted literals using python built in list comparison
        return literals_c1 == literals_c2

    