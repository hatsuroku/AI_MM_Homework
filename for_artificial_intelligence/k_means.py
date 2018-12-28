import pandas as pd
import math
import random
import sklearn.preprocessing

def cal_euclid_distance(p1, p2):
    dstc = 0.0
    for i in range(len(p1)):
        dstc += (p1[i] - p2[i]) ** 2
    return math.sqrt(dstc)


def read_data():
    raw = pd.read_csv('wine.txt')
    raw_data = raw.values
    data = raw_data[0:, 1:]
    return data

def proceed(k, data):
    center = []
    eps = 0.1
    max_iter = 100
    e = float(0x3f3f3f3f)
    iter = 0
    for i in range(k):
        center.append(data[random.randint(0, len(data))])
    means = center * 1
    cluster = [[] for i in range(k)]
    while(e > eps and iter < max_iter):
        # 归类
        for ele in data:
            dis = float(0x3f3f3f3f)
            ele_type = 0
            for i in range(len(center)):
                new_dis = cal_euclid_distance(ele, center[i])
                if(new_dis < dis):
                    dis = new_dis
                    ele_type = i
            cluster[ele_type].append(ele)

        # 计算均值
        for i in range(len(cluster)):
            sum_v = [0.0 for i in range(len(cluster[0][0]))]
            for ele in cluster[i]:
                for j in range(len(ele)):
                    sum_v[j] += ele[j]
            for j in range(len(sum_v)):
                sum_v[j] /= len(cluster[i])
            means[i] = sum_v

        # 计算误差
        error = 0.0
        for i in range(len(cluster)):
            for ele in cluster[i]:
                error += cal_euclid_distance(ele, means[i])
        e = math.sqrt(error)

        # 准备下一次迭代
        center = means * 1
        iter += 1

    return cluster



if __name__ == '__main__':
    k = 3
    data = read_data()
    data = sklearn.preprocessing.scale(data)
    res = proceed(k, data)
    for i in res:
        print("===========================")
        for j in i:
            print(j)