#!/usr/bin/python

import sys
import argparse
import random
from satlib import SATRep
from graph import dagraph
from collections import deque

class incrementalSolver(SATRep):

    def __init__(self):
        self.satisfies = None
        super(incrementalSolver, self).__init__()

    def _initialise(self):
        self.graph = dagraph()
        self.stack = []
        temp = []
        self.queue = deque()
        for i in self.unit:
            temp.append(unit[0])
            self.queue.append(i)
        self.unassigned = []
        for i in self.variables:
            if i not in temp:
                self.unassigned.append(self.var_map[i])
        random.shuffle(self.unassigned)
        self.chosenOne = None
        self.level = 0
        self.ctr = 0
        print("Initialization done")

    def makeDecision(self):
        if len(self.unassigned) is 0:
            return None
        self.level += 1
        negation = random.randint(0,1)
        var = self.unassigned.pop() << 1 | negation
        self.queue.append([var,self.level])
        return 1
        # choose an unassigned variable and add to queue
        # return false if all decisions have been made

    def chooseNextAssignment(self):
        if len(self.queue) == 0:
            print("Making decision")
            if self.makeDecision() is None:
                self.satisfies = True
                print("Satisfied!")
                return False
        print(self.unassigned)
        self.chosenOne = self.queue.popleft()
        return True

    def _addassignment(self,val):
        self.graph.add_node(val,self.level)
        self.graph.add_prev(val,stack[-1][0])
        self.stack.append([val,self.level])
    
    def _deduce(self):
        last = stack[-1]
        self.dagraph.add_node(last,self.level)
        falseval = last ^ 1
        for clause in self.sentence:
            if clause[0] == falseval or clause[1] == falseval:
                newclause = self._search()
                if newclause is None:
                    if clause[0] == last:
                        self._addassignment(clause[1])
                    else:
                        self._addassignment(clause[0])

    def _cdcl(self):
        self._initialise()
        while self.chooseNextAssignment() is True:
            print(self.chosenOne)
            self.stack.append(self.chosenOne)
            # add the choseone to the stack and call deduce
            self._deduce()
        return True

    def  solve(self):
        self.satisfies = self._cdcl()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f","--fname",help="filename to read",default="data")
    args = ap.parse_args()
    formula = incrementalSolver()
    formula.readfile(args.fname)
    print(formula.sentence)
    print(formula.var_map)
    formula.show()
    formula.solve()
    print(formula.stack)

if __name__ == "__main__":
    main()