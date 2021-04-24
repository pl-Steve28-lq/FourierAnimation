class Vec2d:
    def __init__(self, x=.0, y=.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif len(other) == 2 and isinstance(other[0], (int, float)) and isinstance(other[1], (int, float)):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            raise ValueError('Unsupported type for Vec2d `+` operator')

    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif len(other) == 2 and isinstance(other[0], (int, float)) and isinstance(other[1], (int, float)):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            raise ValueError('Unsupported type for Vec2d `-` operator')

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2d(self.x * other, self.y * other)
        else:
            raise ValueError('Unsupported type for Vec2d `*` operator')

    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Vec2d(self.x / other, self.y / other)
        else:
            raise ValueError('Unsupported type for Vec2d `/` operator')

    @property
    def int_tuple(self):
        return (int(self.x), int(self.y))

    @property
    def float_tuple(self):
        return (float(self.x), float(self.y))

    def dist(self, other):
        x, y = self.float_tuple
        z, w = other.float_tuple
        return ((x-z)**2 + (y-w)**2)**.5


from math import atan2
class Wave:
    def __init__(self, k, X_k):
        self.freq = k
        self.amp = (X_k.real ** 2 + X_k.imag ** 2)**.5
        self.phase = atan2(X_k.imag, X_k.real)

    def __str__(self):
        return f'Wave(freq={self.freq}, amp={self.amp}, phase={self.phase})'

    def point(self, x='t'):
        return rf'({self.cos(x)},{self.sin(x)})'

    def cos(self, x='t'):
        return rf'{self.amp:.3f}\cos\left({self.freq}{x}+{self.phase:.3f}\right)'

    def sin(self, x='t'):
        return rf'{self.amp:.3f}\sin\left({self.freq}{x}+{self.phase:.3f}\right)'


def mapf(value, a=(0, 1), b=(0, 1)):
    return b[0] + (value - a[0]) / (a[1] - a[0]) * (b[1] - b[0])

from numpy.fft import fft
def dft(x):
    return (fft(x)/len(x)).tolist()


def getCircles(points, x='t'):
    f = dft([complex(*p)for p in points])
    wave = [Wave(k,c)for k,c in enumerate(f)]
    res = []
    idx = 1
    while idx < len(wave):
        w0 = wave[idx-1]
        w1 = wave[idx]
        res += [f'X_1=0', f'Y_1=0']if idx==1 else[f'X_{"{"}{idx}{"}"}=X_{"{"}{idx-1}{"}"}+{w0.cos(x)}', f'Y_{"{"}{idx}{"}"}=Y_{"{"}{idx-1}{"}"}+{w0.sin(x)}']
        res += [f'(x-X_{"{"}{idx}{"}"})^2+(y-Y_{"{"}{idx}{"}"})^2={w1.amp}^2']
        idx += 1
    res += [f'(X_{"{"}{idx-1}{"}"}+{wave[idx-1].cos(x)}, Y_{"{"}{idx-1}{"}"}+{wave[idx-1].sin(x)})']
    return res

from test_logo import youtube

