import sys

class SATRep():

    def __init__(self):
        self.variables = []
        self.var_map = {}
        self.sentence = []
        self.nclauses = 0
        self.unit = []

    def preprocess(self,code):
        self.unit.append([code,0])
        
    def  add_clause(self,clause):
        if len(clause) == 1:
            self.preprocess(clause[0])
        if clause not in self.sentence:
            self.sentence.append(clause)

    def add_clause_file(self, line):
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
        self.sentence.append(clause)
        self.nclauses += 1
        if len(arr) is 1:
            self.preprocess(coding)

    def remove_clause(self,clause):
        for i in range(self.nclauses):
            if self.sentence[i] == clause:
                del self.sentence[i]
                self.nclauses -= 1
        if len(clause) == 1:
            for i in range(len(self.unit)):
                if clause == self.unit[i]:
                    del self.unit[i]

    def readfile(self,fname):
        try:
            clauses = [line.rstrip('\n') for line in open(fname)]
        except:
            print("Error while read operation")
            sys.exit(1)
        [self.add_clause_file(line) for line in clauses]
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