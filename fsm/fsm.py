from pygraphviz import AGraph

prog = ['neato'|'dot'|'twopi'|'circo'|'fdp'|'nop']

class FSM(object):
    '''Finite State Machine'''

    def __init__(self, finite_states, directed=True):
        self.states = finite_states
        nodes = {
            state : []
            for state in finite_states
        }
        self.graph = AGraph(nodes, directed=directed, strict=False)
        self.edgesize = len(nodes) / 5.0
        return

    def validate(self, *args):
        for arg in args:
            assert arg in self.states, arg
        return

    def transition(self, src, dest, label='', **kwargs):
        self.validate(src, dest)
        self.graph.add_edge(src, dest, label=label, len=self.edgesize, **kwargs)
        return

    def success(self, src, dest, label=''):
        self.transition(src, dest, label, color='green')

    def fail(self, src, dest, label=''):
        self.transition(src, dest, label, color='red')

    def save(self,name='graph',prog='dot'):
        self.graph.layout(prog=prog)
        self.graph.draw('{}.png'.format(name))
        return
