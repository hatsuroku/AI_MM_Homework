"""
    计算方法第四次作业
    求(x-1)(x-2)..(x-10)各项系数
    以及eps等于各值的扰动方程
"""

import math

# 原本采用多次多层嵌套循环的解法
def cal_coefficient_of_seven():
    k = 7
    coefficient = [0 for i in range(k + 1)]

    # for_selected 待选择集合
    fs = [-i for i in range(1, 1 + k)]
    selected = set()
    for i in range(k):
        # 如果已经选过就不再选
        if (fs[i] in selected):
            continue
        # 计算
        selected.add(fs[i])
        coefficient[k - 1] += fs[i]
        # 去除已选的计算剩余的
        fs.remove(fs[i])
        rest = 1
        for r in fs:
            rest *= r
        coefficient[1] += rest
        fs = [-i for i in range(1, k + 1)]

    selected.clear()
    for i in range(k):
        for j in range(i + 1, k):
            v1 = fs[i]
            v2 = fs[j]
            g = (v1, v2)
            if (g in selected):
                continue

            selected.add(g)
            coefficient[k - 2] += fs[i] * fs[j]

            fs.remove(v1)
            fs.remove(v2)
            rest = 1
            for r in fs:
                rest *= r
            coefficient[2] += rest
            fs = [-i for i in range(1, k + 1)]

    selected.clear()
    for i in range(k):
        for j in range(i + 1, k):
            for a in range(j + 1, k):
                v1 = fs[i]
                v2 = fs[j]
                v3 = fs[a]
                g = (v1, v2, v3)
                if (g in selected):
                    continue

                selected.add(g)
                coefficient[k - 3] += fs[i] * fs[j] * fs[a]

                fs.remove(v1)
                fs.remove(v2)
                fs.remove(v3)
                rest = 1
                for r in fs:
                    rest *= r
                coefficient[3] += rest
                fs = [-i for i in range(1, k + 1)]

    coefficient[0] = math.factorial(k) * (-1) ** k
    coefficient[k] = 1

    return coefficient


"""
    g : 已选择的整数，是个列表
    num : 一共要选择的个数
    k : fs的长度
    d : 循环层数
    selected : 集合，包含已选择过的数的列表
    coefficient : 系数列表
"""
# 采用了把多层循环写成递归的形式
def select(g, num, k, d, selected, coefficient):
    fs = [-i for i in range(1, k + 1)]
    start = 0
    if(d != 1):
        start = -g[-1]
    for i in range(start, k):
        g.append(fs[i])
        if(d == num):
            # 因为list不能拥有哈希值，所以要转成元组才能加入集合
            t = tuple(g)
            if(t in selected):
                # 这里如果不pop，上一个同层循环的元素就会留下
                g.pop()
                continue
            else:
                selected.add(t)

            sele = 1
            for e in g:
                sele *= e
                fs.remove(e)
            coefficient[k - num] += sele
            rest = 1
            for r in fs:
                rest *= r
            coefficient[num] += rest
            # 这里如果不pop，上一个同层循环的元素就会留下
            g.pop()
            fs = [-i for i in range(1, k + 1)]
        else:
            select(g, num, k, d+1, selected, coefficient)
            # 这里如果不pop，上一个同层循环的元素就会留下
            g.pop()


# 计算(x-1)(x-2)(x-3)...(x-k)的系数
def cal_coefficient(k):
    coefficient = [0 for i in range(k + 1)]
    coefficient[0] = math.factorial(k) * (-1)**k
    coefficient[k] = 1

    for i in range(1, k//2 + 1):
        g = []
        selected = set()
        select(g, i, k, 1, selected, coefficient)
    return coefficient


if __name__ == '__main__':
    coefficient = cal_coefficient(10)
    for i in range(len(coefficient) - 1, -1, -1):
        print(i, " : ",coefficient[i])