import math
import time
import datetime

def f(x):
    return 1/(1 + x*x)

def d(x):
    return 1/x

# 用于高斯勒让德公式中的函数转换
def g(f, t, a, b):
    return f((b-a)/2 * t + (a+b)/2)

# 复化梯形求积分
def complex_trapezoid(f, a, b, n):
    h = (b-a)/n
    ans = 0
    for k in range(1, n):
        ans += f(a + k*h)
    ans *= 2
    ans += f(a) + f(b)
    ans *= h / 2
    return ans

# 复化辛普森求积分
def complex_simpson(f, a, b, n):
    h = (b - a) / n
    half_h = h / 2
    ans = 0
    for k in range(0, n):
        xk = a + k*h
        ans += f(xk) + 4 * f(xk + half_h) + f(xk + h)
    ans *= h / 6
    return ans

# 得到最初的T00
def getT00(f, a, b):
    h = b - a
    return h/2 * (f(a) + f(b))

# 由Tmk得到Tm(k+1)
# n是进行二分之前的n
def getTmkplus1(Tmk, f, a, b, n):
    h = (b - a) / n
    half_h = h / 2
    right_part = 0
    for k in range(0, n):
        right_part += f(a + k*h + half_h)
    right_part *= h/2
    return 0.5*Tmk + right_part

# 由Tmk和Tm(k+1)得到T(m+1)k
def getTmplus1k(Tmk, Tmkplus1, f, a, b, n, m):
    Tmplus1k = (4**m * Tmkplus1 - Tmk) / (4**m - 1)
    return Tmplus1k



# 龙贝格算法
def romberg(f, a, b, max):
    # T00是一切的开始
    Tmk = getT00(f, a, b)
    n = 0
    # result是一个二维list，result[m][k]就是Tm(k+m)
    result = []
    for m in range(0, max + 1):
        # 每次迭代前先添加个空列表
        result.append([])
        # m == 0的时候是初始情况，特殊处理
        if (m == 0):
            result[0].append(Tmk)
            n = 1
            for i in range(1, max + 1):
                Tmk = getTmkplus1(Tmk, f, 0, 1, n)
                n *= 2
                result[0].append(Tmk)
        else:
            for k in range(1, len(result[m - 1])):
                Tmkminus1 = getTmplus1k(result[m-1][k-1], result[m-1][k], f, a, b, n, m)
                result[m].append(Tmkminus1)
    return result[max][0]



# 高斯勒让德求积公式，积分范围转化为[-1, 1]
# n的最大值只能取6
def gauss_legendre(g, f, a, b, n):
    # x
    x = [
            [0],
            [-1/math.sqrt(3), 1/math.sqrt(3)],
            [0, -math.sqrt(3/5), math.sqrt(3/5)],
            [
                -math.sqrt(525 - 70*math.sqrt(30)) / 35,    math.sqrt(525 - 70*math.sqrt(30)) / 35,
                -math.sqrt(525 + 70*math.sqrt(30)) / 35,    math.sqrt(525 + 70*math.sqrt(30)) / 35,
            ],
            [
                0,
                -math.sqrt(245 - 14*math.sqrt(70)) / 21,    math.sqrt(245 - 14*math.sqrt(70)) / 21,
                -math.sqrt(245 + 14*math.sqrt(70)) / 21,    math.sqrt(245 + 14*math.sqrt(70)) / 21
            ],
            [
                -0.9324695142, 0.9324695412,
                -0.6612093865, 0.6612093865,
                -0.2386191861, 0.2386191861
            ],
            [
                0,
                -0.9491079123, 0.9491079123,
                -0.7415311856, 0.7415311856,
                -0.4058451514, 0.4058451514,
            ]
    ]

    # weight
    w = [
            [2],
            [1, 1],
            [8/9, 5/9, 5/9],
            [
                (18 + math.sqrt(30)) / 36,    (18 + math.sqrt(30)) / 36,
                (18 - math.sqrt(30)) / 36,    (18 - math.sqrt(30)) / 36
            ],

            [
                128/225,
                (322 + 13*math.sqrt(70)) / 900,     (322 + 13*math.sqrt(70)) / 900,
                (322 - 13*math.sqrt(70)) / 900,     (322 - 13*math.sqrt(70)) / 900
            ],

            [
                0.1713244924, 0.1713244924,
                0.3607615370, 0.3607615370,
                0.4679139346, 0.4679139346
            ],
            [
                0.4179591837,
                0.1294849662, 0.1294849662,
                0.2797053915, 0.2797053915,
                0.3818300505, 0.3818300505
            ]
    ]
    ans = 0
    for k in range(0, n+1):
        ans += w[n][k] * g(f, x[n][k], a, b)
    return ans * (b-a)/2


if __name__ == "__main__":
    tennum = 0.7853981633
    eps = 1e-11
    print("==========%s============" % "complex_trapezoid")
    n = 20000
    print("n(num of segment) = %2d:" % (n), complex_trapezoid(d, 1, math.e, n))
    n = 25000
    print("n(num of segment) = %2d:" % (n), complex_trapezoid(d, 1, math.e, n))

    print("\n==========%s============" % "complex_simpson")
    n = 6
    print("n(num of segment) = %2d:" % (n),complex_simpson(d, 1, math.e, n))
    n = 50
    print("n(num of segment) = %2d:" % (n),complex_simpson(d, 1, math.e, n))

    print("\n==========%s============" % "romberg")
    for i in range(0, 11):
        print("%2d: " % i, romberg(d, 1, math.e, i))
    #
    # print("\n==========%s============" % "gauss_legendre")
    # for i in range(0, 6+1):
    #     # 因为f刚好是偶函数，所以高斯勒让德求积的结果除以二就是积分结果
    #     print("%2d:" % i ,gauss_legendre(g, f, 0, 1, i))

    print("\n==========%s============" % "gauss_legendre, dx")
    for i in range(0, 6 + 1):
        # 因为f刚好是偶函数，所以高斯勒让德求积的结果除以二就是积分结果
        print("%2d:" % i, gauss_legendre(g, d, 1, math.e, i))