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
            wlist.append(clause[0])
        return wlist
        print(wlist)

    def eliminate_ptr_to(self,n,wlist):
        clause = self.sentence[n]
        for i in range(len(clause)):
            if clause[i] not in self.blacklist:
                wlist[n] = clause[i]
                return True
        return False

    # Conflict detection happens here
    def _update_watch(self,var,value,wlist):
        ret = True
        code = self.var_map[var]
        if value is True:
            eliminate = code << 1 | 1            
        elif value is False:
            eliminate  = code << 1 | 0
        self.blacklist.append(eliminate)
        for i in range(self.nclauses):
            if wlist[i] == eliminate:
                ret = self.eliminate_ptr_to(i,wlist)
                if ret is False:
                    print("Conflict!")
                    break
        return ret


    def _recurse(self,depth,wlist):
        if depth == len(self.variables):
            self.satisfied = 1
            print("Satisfied!")
            return True
        var = self.variables[depth]
        print("Setting %s to True"%var)
        self.stack.append([var,True])
        if self._update_watch(var,True,wlist):
            self._recurse(depth+1,wlist)
        else:
            print("Setting %s to False"%var)
            self.stack[-1][1] = False
            if self._update_watch(var,False,wlist):
                self._recurse(depth+1,wlist)
        self.blacklist.pop()
        self.stack.pop()
        return False


    def  solve(self):
        wlist = self._init_watch()
        self.stack = []
        self.blacklist = []
        depth = 0
        self.satisfies = self._recurse(depth,wlist)

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
