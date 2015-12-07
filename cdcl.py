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

    def _initialise(self):
        self.queue = []
        for i in range(self.variables):
            self.queue.append([self.variables[i],None])
        self.blacklist = []        

    def _propagate():
        pass

    def _cdcl(self):
        pass

    def  solve(self):
        self._initialise()
        depth = 0
        self.satisfies = self._cdcl(depth)

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
