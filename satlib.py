import sys

class SATRep():

    def __init__(self):
        self.variables = []
        self.var_map = {}
        self.sentence = []
        self.nclauses = 0
        self.stack = []

    def preprocess(self,literal,negated):
        truth = True if  negated is 0 else False
        self.stack.append([literal,truth,0])
        

    def add_clause(self, line):
        clause = []
        arr = line.split(" ")
        for literal in arr:
            negated = 1 if literal.startswith("~") else 0
            var = literal[negated:]
            if var not in self.variables:
                no = len(self.variables)
# Encoding is length * 2  + negation
                self.variables.append(var)
                self.var_map[var] = no
            coding = self.var_map[var] << 1 | negated
            clause.append(coding)
        self.sentence.append(tuple(clause))
        self.nclauses += 1
        if len(arr) is 1:
            self.preprocess(var,negated)

    def readfile(self,fname):
        try:
            clauses = [line.rstrip('\n') for line in open(fname)]
        except:
            print("Error while read operation")
            sys.exit(1)
        [self.add_clause(line) for line in clauses]
        print("Successfully read ",fname)

    def show(self):
        vals = list(self.var_map.values())
        keys = list(self.var_map.keys())
        for clause in self.sentence:
            ls = []
            for literal in clause:
# Advantage of the encoding lets us check for negation with negligible cost
                pre =  "~" if literal & 1 else ""
                literal = literal >> 1
                ls.append(pre + keys[vals.index(literal)])
            print(ls)
