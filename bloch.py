
import numpy as np
from numpy.linalg import eig

from collections import defaultdict

X = np.array([[0,1],[1,0]])
Y = np.array([[0,-1j],[1j, 0]])
Z = np.array([[1,0],[0,-1]])

rot_names = {
    str(X): 'X',
    str(Y): 'Y',
    str(Z): 'Z',
}

x0, x1 = eig(X)[1]
y0, y1 = eig(Y)[1]

pole_names = {
    str(tuple(x0  )) : 'x0',
    str(tuple(-x0 )) : '-x0',
    str(tuple(x1  )) : 'x1',
    str(tuple(-x1 )) : '-x1',


    str(tuple(y0  )) : 'y0',
    str(tuple(-y0 )) : '-y0',
    str(tuple(y1  )) : 'y1',
    str(tuple(-y1 )) : '-y1',
}

def dfs(unseen, rots):
    seen = []
    graph = defaultdict(list)
    while len(unseen) > 0:
        print(seen, unseen, graph)
        node = unseen.pop()
        seen.append(node)
        for rot in rots:
            new = rot @ node
            for old in seen:
                if like(new, old):
                    graph[tuple(node)] += [[old, rot]]
                    break
            else: #no break
                graph[tuple(node)] += [[new, rot]]
                unseen.append(new)
    return graph

def prettify(graph):
    for node, entries in graph.items():
        for adj, edge in entries:
            fmt = []
            for elem, namer in zip([node, edge, tuple(adj)], [pole_names, rot_names, pole_names]):
                try:
                    fmt += [namer[str(elem)]]
                except KeyError:
                    fmt += [str(elem)]
            print('{} {} {}'.format(*fmt))


def like(a, b):
    ratio = a/b
    same = ratio == 1
    flip = ratio == -1
    return same.all() or flip.all()
