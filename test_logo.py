import json

def _getLogo(path):
    L = json.loads(
        '[' + ''.join(map(lambda x: x+",", filter(lambda x: x != '\n', open(path).readlines())))[:-1] + ']'
    )
    return tuple(map(lambda x: 2*x/max(L)-1, L))

def Points(L, xR, yR):
    return tuple(zip(map(lambda x: (1-2*xR)*x, L[::2]), map(lambda y: (1-2*yR)*y, L[1::2])))

def getLogo(path, xReverse=False, yReverse=False):
    return Points(_getLogo(path), xReverse, yReverse)

wakgood = getLogo('./logos/wakgood.txt', yReverse=True)
minecraft = getLogo('./logos/minecraft.txt')
