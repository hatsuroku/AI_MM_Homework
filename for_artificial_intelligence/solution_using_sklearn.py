from sklearn.datasets import fetch_mldata
from sklearn.neural_network import MLPClassifier
import sklearn
import random
import pandas as pd
import numpy as np

iris_data_set = []
iris_data = []
iris_result = []
domains = 4

def iris():
    # 读入文件
    with open('iris_data.txt', 'r') as f:
        for li in f.read().splitlines():
            data = li.split(",")
            iris_data_set.append(data)
    # 把每行的字符串转换成浮点数
    for li in iris_data_set:
        tmp = []
        for j in range(0, domains):
            tmp.append(float(li[j]))
        iris_data.append(tmp)
        iris_result.append(li[4])

    print(iris_data)
    print(iris_result)

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 4), random_state=1)

    clf.fit(iris_data, iris_result)

    print(clf.predict([[3.6, 2.3, 6.8, 7.3], [6.7, 3.0, 5.0, 1.7]]))

if __name__ == "__main__":
    df = pd.read_csv('wine.txt')
    y = df.iloc[:, 0]
    x = df.iloc[:, 1:].values
    # data = [(x0, y0) for x0, y0 in zip(x, y)]
    # # 打乱数据
    # random.shuffle(data)
    x = sklearn.preprocessing.scale(x)
    # print(x)
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(5, 4), random_state=1)

    clf.fit(x, y)
    test = [[13.39,1.77,2.62,16.1,93,2.85,2.94,.34,1.45,4.8,.92,3.22,1195],
            [12.72,1.81,2.2,18.8,86,2.2,2.53,.26,1.77,3.9,1.16,3.14,714],
            [13.08,3.9,2.36,21.5,113,1.41,1.39,.34,1.14,9.40,.57,1.33,550]]
    test = sklearn.preprocessing.scale(test)
    print(clf.predict(test))