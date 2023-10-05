class Literal:
    def __init__(self, name, negated=False):
        self.name = name
        self.negated = negated

    def __str__(self):
        return f"¬{self.name}" if self.negated else self.name

class HornClause:
    def __init__(self, body, head):
        # Body is a list of Literals
        self.body = body
        # Head is a Literal
        self.head = head

    def __str__(self):
        body_str = " ∧ ".join(str(literal) for literal in self.body)
        return f"{body_str} => {self.head}"

class KnowledgeBaseHorn:
    def __init__(self):
        self.clauses = list()
        self.known_true = list()  # This will serve as  agenda

    def tell(self, observation):
            
        location = [observation['x'], observation['y']]
        # print(f"current location: {location}")
        if observation['breeze']:
            self.add_known_true(f'B{location[0]}{location[1]}')
            clause=self.generate_horn_clauses("breeze", location)
        # if observation['breeze']==False:
        #     self.append_known_true(f'(¬B{location[0]}{location[1]})') 

        if observation['stench']:
            self.add_known_true(f'S{location[0]}{location[1]}')
            clause=self.generate_horn_clauses("stench", location)
       
        # if observation['stench']==False:
        #     self.clauses.append(f'(¬S{location[0]}{location[1]})')
        # Assumes clause is an instance of HornClause

    def add_known_true(self, literal):
        literal=Literal(literal)
        self.known_true.append(literal)
    
    def ask(self, query):
        query_literal=Literal(query)
        return self.forward_chaining(query_literal)

    def print_kb(self):
        print("--" * 20)
        print("These are the Horn Clauses in the KB:")
        for clause in self.clauses:
            print(clause)
            
        print("--" * 20)
        print("These are the known true literals:")
        
        for literal in self.known_true:
            print(literal)
        
        print("--" * 20)
        

    def generate_horn_clauses(self,perception,location):
        x,y=location
        if perception=="breeze":
            nieghbors=self.get_neighboring_fields(x,y)
            for field in nieghbors:
                neighbors_neighbors=self.get_neighboring_fields(field[0],field[1])
                hornclause= HornClause([Literal(f"B{neighbor[0]}{neighbor[1]}") for neighbor in neighbors_neighbors],Literal(f"P{field[0]}{field[1]}"))
                self.clauses.append(hornclause)
                
        if perception=="stench":
            nieghbors=self.get_neighboring_fields(x,y)
            for field in nieghbors:
                neighbors_neighbors=self.get_neighboring_fields(field[0],field[1])
                hornclause= HornClause([Literal(f"S{neighbor[0]}{neighbor[1]}")for neighbor in neighbors_neighbors],Literal(f"W{field[0]}{field[1]}"))
                self.clauses.append(hornclause)


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


    def forward_chaining(self, q):
        # Initialize count and inferred
        count = {clause: len(clause.body) for clause in self.clauses}
        inferred = {literal.name: False for clause in self.clauses for literal in (clause.body + [clause.head])}
        agenda=list(self.known_true.copy())
        
        while agenda:
            # Take the first item from the agenda
            p = agenda.pop(0)
            if p.name == q.name:
                print(f"The query {q} has been inferred as true")
                return True
            # If this literal has not been inferred already
            if not inferred[p.name]:
                # Mark it as inferred
                inferred[p.name] = True

                # Go through each clause in the knowledge base
                for clause in self.clauses:
                    # If the literal is in the body of the clause
                    if p.name in [body.name for body in clause.body]:
                    # if p.name in clause.body:
                        # Decrease the count of unfulfilled premises for this clause
                        count[clause] -= 1
                        # If all premises of the clause are fulfilled
                        if count[clause] == 0:
                            # Add the head of the clause to the agenda
                            agenda.append(clause.head)

        print(f"The query {q} has been inferred as false")
        return False