#!/usr/bin/python

import sys
import time
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
        self.deduced = []
        self.graph = dagraph()
        self.stack = []
        self.assignments = []
        temp = []
        self.queue = deque()
        for i in self.unit:
            temp.append(i[0])
            self.queue.append(i)
        self.unassigned = []
        for i in self.variables:
            if i not in temp:
                self.unassigned.append(self.var_map[i])
        random.shuffle(self.unassigned)
        print("Random Queue: ",self.unassigned)
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
        print("Deciding to add: ",var)
        self.queue.append([var,self.level])
        return 1
        # choose an unassigned variable and add to queue
        # return false if all decisions have been made

    def chooseNextAssignment(self):
        if len(self.queue) == 0:
            if self.makeDecision() is None:
                self.satisfies = True
                print("Satisfied!")
                return False
        self.chosenOne = self.queue.popleft()
        print("unassigned: ",self.unassigned)
        return True

    def _addassignment(self,val,cause):
        self.graph.add_node(val,self.level)
        if cause is not None:
            for i in cause:
                self.graph.add_prev(val,i)
        self.stack.append([val,self.level])
        if val not in self.assignments:
            self.assignments.append(val)
        print("val: ",val)
        try:
            self.unassigned.remove(val >> 1)
        except:
            return

    def _search(self,clause):
        for i in range(2,len(clause)):
            if clause[i] ^1 not in self.assignments:
                return i
        return None

    def _conflictAnalysis(self):
        nodes = self.graph.getnodes()
        print("nodes: ",nodes)     
        for  i in self.assignments:
            if i in nodes and i^1 in nodes:
                history = self.graph.get_prev(i) + self.graph.get_prev(i^1)
                history = list(set(history))
                print("History: ",history)
                break
        #time.sleep(10)
        return [x^1 for x in history]

    def _deduce(self):
        last = self.stack[-1][0]
        result = []
        self.graph.add_node(last,self.level)
        print("stack = ",self.stack)
        falseval = last ^ 1
        #print("falseval: ",falseval)
        for clause in self.sentence:
            if len(clause) < 2:
                continue
            if clause[0] in self.assignments or clause[1] in self.assignments:
                continue
            if clause[0] ^ 1 in self.assignments and clause[1] ^1 in self.assignments:
                print("A conflict has occured",clause,self.assignments)
                if self.level == 0:
                    return "unsat"
                cause = [ x^1 for x  in clause[1:]]
                self._addassignment(clause[0],cause)
                learn = self._conflictAnalysis()
                self.add_clause(learn)
                #time.sleep(10)
                return False
            if clause[0] == falseval or clause[1] == falseval:
                retval = self._search(clause)
                if retval is None:
                    if len(clause) > 2:
                        cause = [falseval] + [x^1 for x in clause [2:]]
                    else:
                        cause = [falseval]
                    print("a unit clause!",clause,cause)
                    if clause[0] == falseval:
                        result.append([clause[1],cause])
                    else:
                        result.append([clause[0],cause])
                else:
                    #print("Swapping!")
                    index = 0 if clause[0] == falseval else 1
                    newclause = clause[retval]
                    clause[retval] = clause[index]
                    clause[index] = newclause
        if len(result) > 0:
            for i in result:
                if i not in self.deduced:
                    self.deduced.append(i)
            return True


    def _cdcl(self):
        self._initialise()
        while self.chooseNextAssignment() is True:
            print("Chosen one:",self.chosenOne)
            self.stack.append(self.chosenOne)
            self.assignments.append(self.chosenOne[0])
            # add the choseone to the stack and call deduce
            while True:
                val = self._deduce()
                if val is True or len(self.deduced) > 0:
                    if val is False:
                        print("restarting")
                        return "restart"
                    if val is "unsat":
                        print("Unsatisfiable!")
                        return "unsat"
                    tmp = self.deduced.pop()
                    self._addassignment(tmp[0],tmp[1])
                elif val is "unsat":
                    print("Unsatisfiable!")
                    return "unsat"
                elif val is False:
                        print("restarting")
                        return "restart"
                else:
                    break
        return True

    def  solve(self):
        while self._cdcl() is "restart":
            print("Added a clause and restarting")
            print(self.sentence)
        print("process ended!")

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