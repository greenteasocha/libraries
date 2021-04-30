import math
import cmath

class XI():
    def __init__(self, sep):
        self.sep = sep
        self.val = []

        xi_base = 1 + 0j
        xi_rot = complex(math.cos(2 * math.pi / sep), math.sin(2 * math.pi / sep))

        self.val.append(xi_base)
        for i in range(sep - 1):
            xi_base *= xi_rot
            self.val.append(xi_base)

    def get(self, n, i):
        # return xi_n^i = exp(2*pi*i*j/n) : j is imaginary unit
        i = i % n
        return self.val[i * (self.sep // n)]

    def inverse(self):
        self.val = [1 + 0j] + list(reversed(self.val[1:]))

def fft(a, deg, xi):
    if deg == 1:
        return [a[0] * xi.get(1, 0)]

    f0 = []
    f1 = []
    for i, c_i in enumerate(a):
        if i % 2:
            f1.append(c_i)
        else:
            f0.append(c_i)

    f0_hat = fft(f0, deg // 2, xi)
    f1_hat = fft(f1, deg // 2, xi)

    ret = []
    for i in range(deg):
        tmp = f0_hat[i % (deg//2)] + xi.get(deg, i) * f1_hat[i % (deg//2)]
        ret.append((tmp))

    return ret

def conv(a, b):
    na, nb = len(a), len(b)
    deg = 1
    while deg < na + nb:
        deg *= 2

    xi = XI(deg)
    a = a + [0] * (deg - na)
    b = b + [0] * (deg - nb)
    fft_a = fft(a, deg, xi)
    fft_b = fft(b, deg, xi)

    fft_ab = []
    for i, j in zip(fft_a, fft_b):
        fft_ab.append(i*j)

    xi.inverse()
    ab = fft(fft_ab, deg, xi)

    ret = [round(x.real) // deg for x in ab]
    return ret

def main():
    # a = [1,2,3,4,5]
    # b = [6,7,8,9,10,11]

    # ret = conv(a, b)
    # print(ret)

    n = int(input())

    a = []
    b = []
    for i in range(n):
        aa, bb = map(int, input().split())
        a.append(aa)
        b.append(bb)

    res = conv(a, b)
    print(0)
    for r in res[:n*2-1]:
        print(r)



def xi_verification():
    xi = XI(16)

    # values
    print("xi_16")
    for i in range(16):
        print(math.degrees(cmath.phase(xi.get(16, i))))
    print("xi_8")
    for i in range(8):
        print(math.degrees(cmath.phase(xi.get(8, i))))
    print("xi_4")
    for i in range(4):
        print(math.degrees(cmath.phase(xi.get(4, i))))

    # Orthogonality
    print("Orthogonality")
    for j in range(16):
        s = 0
        for i in range(16):
            x = xi.get(16, i * j)
            s += x.real
            # print(math.degrees(cmath.phase(xi.get(16, i))))
            # print(xi.get(16, i).real)
        print(s)

if __name__ == "__main__":
    main()
    # xi_verification()