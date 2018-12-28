import math as m
import numpy as np
import random
import matplotlib.pyplot as plt

# 用于表示染色体所需要的位数
x_bit_num = 40


# 用于计算的函数
def f(x1, x2):
    sum1 = 0
    for j in range(1, 6):
        sum1 += j * m.cos((j+1)*x1 + j)
    sum2 = 0
    for j in range(1, 6):
        sum2 += j * m.cos((j+1)*x2 + j)
    return sum1 * sum2


# 解码得到原来的x值
def get_original_x(x_str):
    return -10 + int(x_str, 2)/(2**x_bit_num-1) * 20


def selection_cross(gene_set, adap_set, pc = 0.7):
    # 轮盘赌选择
    # 计算累积概率
    adap_sum = 0
    adap_sum_set = []
    for e in adap_set:
        adap_sum += e
        adap_sum_set.append(adap_sum)
    for i in range(len(adap_sum_set)):
        adap_sum_set[i] /= adap_sum
        # print(e)

    new_group = []
    while(len(new_group) < len(gene_set)):
        # 选择
        selected = []
        # 选择两个元素 采用轮盘赌选择
        for i in range(2):
            r = np.random.uniform(0, 1)
            for j in range(len(adap_sum_set)):
                if(j == 0):
                    if(r <= adap_sum_set[j]):
                        selected.append(gene_set[j])
                        break
                else:
                    if(adap_sum_set[j-1] < r and r <= adap_sum_set[j]):
                        selected.append(gene_set[j])
                        break
        # 交叉
        r = np.random.uniform(0, 1)
        offspring = []
        if(r <= pc):
            # 在这里r是染色体断掉的点
            r = np.random.randint(0, x_bit_num)
            offspring.append([selected[0][0][0:r] + selected[1][0][r:], selected[0][1][0:r] + selected[1][1][r:]])
            offspring.append([selected[1][0][0:r] + selected[0][0][r:], selected[1][1][0:r] + selected[0][1][r:]])
        else:
            offspring = selected
        for e in offspring:
            new_group.append(e)
    return new_group


def mutation(gene_set, pm = 0.001):
    new_gene_set = []
    for e in gene_set:
        if(np.random.uniform(0, 1) <= pm):
            new_ele = []
            # 此时r为变化的位数
            r = np.random.randint(0, x_bit_num)
            # 两个元素突变，可能只突变一个，也可能两个都变
            # 01, 10, 11三种情况
            situation = np.random.randint(1, 4)
            # 因为python的str是不可变对象
            # 所以只能转成int用异或操作转置一位
            # 然后再转回字符串
            if(situation == 1):
                num = int(e[0], 2)
                num ^= 1 << r
                new_ele.append("{0:b}".format(num))
                new_ele.append(e[1])
            elif (situation == 2):
                new_ele.append(e[0])
                num = int(e[1], 2)
                num ^= 1 << r
                new_ele.append("{0:b}".format(num))
            elif (situation == 3):
                num = int(e[0], 2)
                num ^= 1 << r
                new_ele.append("{0:b}".format(num))
                num = int(e[1], 2)
                num ^= 1 << r
                new_ele.append("{0:b}".format(num))
            new_gene_set.append(new_ele)
        else:
            new_gene_set.append(e)
    return new_gene_set

# 得到每个函数体的适应性
def cal_adaptability(gene_set):
    adaptability_set = []
    for ele in gene_set:
        x1 = ele[0]
        x2 = ele[1]
        # print(get_original_x(x1), get_original_x(x2))
        res = f(get_original_x(x1), get_original_x(x2))
        if(res > 0):
            y = 0
        else:
            y = abs(res)
        adaptability_set.append(y)
    return adaptability_set

def generate_group(num):
    group = []
    for i in range(num):
        ele = []
        # 二元函数 所以需要生成两个x
        for k in range(2):
            ele_str = ""
            for j in range(x_bit_num):
                ele_str += str(np.random.randint(0, 2))
            ele.append(ele_str)
        group.append(ele)
    return group

g_num = 500
iteration = 300
if __name__ == "__main__":
    # 创建种群
    gene_set = generate_group(g_num)
    # for i in gene_set:
    #     print(get_original_x(i[0]), get_original_x(i[1]))
    adaptability_set = []
    mini = []
    ave = []
    for i in range(iteration):
        result = []
        for i in range(len(gene_set)):
            x1 = get_original_x(gene_set[i][0])
            x2 = get_original_x(gene_set[i][1])
            result.append(f(x1, x2))
        mini.append(np.min(result))
        ave.append(np.mean(result))

        # 计算适应值
        adaptability_set = cal_adaptability(gene_set)
        # for i in range(len(adaptability_set)):
        #     print(get_original_x(gene_set[i][0]), get_original_x(gene_set[i][1]), adaptability_set[i])
        # plt.scatter(np.linspace(0, 1, g_num), adaptability_set)
        # plt.show()

        # 进行选择和交叉
        gene_set = selection_cross(gene_set, adaptability_set)

        # 突变
        gene_set = mutation(gene_set)
    for i in range(len(gene_set)):
        x1 = get_original_x(gene_set[i][0])
        x2 = get_original_x(gene_set[i][1])
        print("{:.6f} {:.6f} {:.6f}".format(x1, x2, f(x1, x2)))
    plt.plot(mini)
    plt.plot(ave, color='c')
    plt.show()
