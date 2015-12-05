#!/usr/bin/python

import sys
import argparse
import random
from satlib import SATRep
from collections import deque

class incrementalSolver(SATRep):

    def __init__(self):
        self.satisfies = None
        super(incrementalSolver, self).__init__()

    # initialize the watchlist
    def  _init_watch(self):
        self.wlist = []
        for  clause in self.sentence:
            self.wlist.append(clause[0])
        print(self.wlist)

    def _analyzeclause(self,i):
            for j in range(len(self.sentence[i])):
                if self.sentence[i][j] is not in falseval:
                    return self.sentencqe[i][j]
            return None


    # Conflict detection happens here
    def _update_watch(self,falseval):
    # Add conflict clauses to watchlist
        if len(self.wlist) < self.nclauses:
            for i in xrange(len(self.wlist),self.nclauses):
                self.wlist.append(sentence[i][0])
        for i in range(self.nclauses):
            if self.wlist[i] = falseval
                newval = _analyzeclause(i)
                if newval is None:
                    return None
                else:
                    self.wlist[i] = newval
        return 1

    def _recurse(self):
        if len(self.assignments) is 0:
            return True
        var = self.assignments.popleft()
        assign = var << 1 | 0
        self.falseval.append(assign)
        if _update_watch(assign) is 1:
            _recurse()
        else:
            falseval.pop()
            assign = assign | 1
            falseval.append(assign)
            _recurse()
        return None



    def  solve(self):
        self._init_watch()
        self.assignments = deque()
        for i in range(len(self.variables)):
            self.assignments.append(variables)
        self.falseval = []
        self.satisfies = _recurse()

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

if __name__ == "__main__":
    main()