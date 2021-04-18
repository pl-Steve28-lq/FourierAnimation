import json

L = json.loads(
    '[' + ''.join(map(lambda x: x+",", filter(lambda x: x != '\n', open('path.txt').readlines())))[:-1] + ']'
)
L = tuple(map(lambda x: 2*x/max(L)-1, L))

wakgood = tuple(zip(L[::2], map(lambda x: -x, L[1::2])))
