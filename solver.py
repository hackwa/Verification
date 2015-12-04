#!/usr/bin/python

import sys
import argparse
import random
from satlib import SATRep

class incrementalSolver(SATRep):

    def __init__(self):
        super(incrementalSolver, self).__init__()
        pass
    # initialize the watchlist
    def  _init_watch(self):
        self.wlist = []
        for  clause in self.sentence:
            self.wlist.append(clause[0])
        print(self.wlist)
        pass
    # Conflict detection happens here
    def _update_watch():
        pass

    def  solve(self):
        self.queue = self.variables
        self.assignments = []
        self._init_watch()
        pass

    def satisfies(self,sentence):
        None

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