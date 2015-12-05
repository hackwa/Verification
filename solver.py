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
        wlist = []
        for  clause in self.sentence:
            self.wlist.append(clause[0])
        return wlist
        print(wlist)

    def self.eliminate_ptr_to(val):
          for i in xrange(self.nclauses):
              if wlist[i] == val:
                clause = self.sentence[i]

    # Conflict detection happens here
    def _update_watch(self,var,value,wlist):
        code = self.var_map[var]
        if value is True:
            eliminate = code << 1 | 1            
        elif value is False:
            eliminate  = code << 1 | 0
        for i in xrange(nclauses):
            pass


    def _recurse(self,depth,wlist,blacklist):
        if depth == len(self.variables):
            print("Satisfied!")
            return True
        var = self.variables[depth]
        print("Setting %d to True"%var)
        self.stack.append([var,True])
        if self._update_watch(var,True,wlist):
            self._recurse(depth+1)
        else:
            print("Setting %d to False"%var)
            self.stack[-1][1] = False
            if self._update_watch(var,False,wlist):
                self._recurse(depth+1)
        else:
            self.stack.pop()
            return False


    def  solve(self):
        wlist = self._init_watch()
        self.stack = []
        blacklist = []
        depth = 0
        self.satisfies = self._recurse(depth,wlist,blacklist)

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
    print(formula.satisfies)

if __name__ == "__main__":
    main()