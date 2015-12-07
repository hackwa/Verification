class dagnode():

    def __init__(self,value,level):
        self.value = value
        self.level = level
        self.prev = []
        self.next = []

    def add_prev(self,arg):
        self.prev.append(arg)

    def add_next(self,arg):
        self.next.append(arg)

class dagraph():
    """docstring for dagraph"""
    def __init__(self):
        self.nodes = []
        self.nnodes = 0
        
    def  add_node(self,value,level):
        node = dagnode(value,level)
        self.nodes.append(node)
        self.nnodes += 1

    def getnodes(self):
        return [i.value for i in self.nodes]

    def getnodelevels(self):
        return [[i.value,i.level] for i in self.nodes]

    def add_prev(self,current,previous):
        for i in self.nodes:
            if i.value == current:
                i.add_prev(previous)
            if i.value == previous:
                i.add_next(current)

    def add_next(self,current,next):
        for i in self.nnodes:
            if i.value == current:
                i.add_next(next)
            if i.value == next:
                i.add_prev(current)