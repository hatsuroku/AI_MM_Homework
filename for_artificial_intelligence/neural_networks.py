import math

iris_data_set = []
neu_set = [[], [], []]
iris_max = [0.0, 0.0, 0.0, 0.0]
iris_min = [0.0, 0.0, 0.0, 0.0]
theta = 0.2
alpha = 0.01
domains = 4


# 归一化
def scaling_to_unit(l, domain):
    norm = 0.0
    for j in range(0, domain):
        norm += l[j] ** 2
    for j in range(0, domain):
        l[j] /= math.sqrt(norm)


# 调整权值
def adjust_weight(Wi, Xi, alpha):
    delta_Wi = [0.0, 0.0, 0.0, 0.0]
    for i in range(0, domains):
        delta_Wi[i] = alpha * (Xi[i] - Wi[i])
    new_Wi = Wi * 1
    for i in range(0, domains):
        new_Wi[i] += delta_Wi[i]
    return new_Wi

def do_process(the_neu_set, the_list, domains):
    # li是一个数据向量(Xi)
    flag = True
    while(flag):
        for li in the_list:
            product = [0.0, 0.0, 0.0]
            # neu是一个神经元向量(Wi)
            for i in range(0, len(the_neu_set)):
                # j是一个neu向量的下标
                # 计算XW^T（内积）
                for j in range(0, domains):
                    product[i] += the_neu_set[i][j] * li[j]
            max_product = 0.0
            # neu_no是胜出的神经元的编号
            neu_no = 0
            for i in range(0, 3):
                if(product[i] > max_product):
                    max_product = product[i]
                    neu_no = i
            if(neu_no != 0):
                print(neu_no)
            old_neu = the_neu_set[neu_no]
            the_neu_set[neu_no] = adjust_weight(the_neu_set[neu_no], li, alpha)
            # 根据欧几里得距离判断是否应该结束
            esp = 0.0
            for i in range(0, domains):
                esp += (old_neu[i] - the_neu_set[neu_no][i]) ** 2
            if(math.sqrt(esp) < 0.001):
                flag = False
            # 对新权值进行归一化
            scaling_to_unit(the_neu_set[neu_no], domains)


def get_min_max(the_list, domain):
    min = float(0x3f3f3f3f)
    max = 0.0
    for li in the_list:
        if(li[domain] < min):
            min = li[domain]
        if(li[domain] > max):
            max = li[domain]
    return min, max


if __name__ == "__main__" :
    # 读入文件
    with open('iris_data.txt', 'r') as f:
        for li in f.read().splitlines():
            data = li.split(",")
            iris_data_set.append(data)
    # 把每行的字符串转换成浮点数
    for li in iris_data_set:
        for j in range(0, domains):
            li[j] = float(li[j])
        print(li)
    # 归一化
    for li in iris_data_set:
        scaling_to_unit(li, domains)
    # 给神经元赋予初始权值
    for i in neu_set:
        for j in range(0, domains):
            i.append(0.5)

    do_process(neu_set, iris_data_set, domains)
    for neu in neu_set:
        print(neu)