import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import random

data_set = []
all_data = []
x = []
y = []
training = []
testing = []

def pre_processing():
    # 读入文件
    with open('svm_data.csv', 'r') as f:
        for li in f.read().splitlines():
            data = li.split(",")
            data_set.append(data)
    # 把每行的字符串转换成浮点数
    for li in data_set:
        tmp_x = []
        ele = []
        for i in range(len(li) - 1):
            tmp_x.append(float(li[i]))
        ele.append(tmp_x)
        ele.append(int(li[-1]))
        all_data.append(ele)

    # 打乱整个数据的顺序
    random.shuffle(all_data)

    global training
    global testing
    # 分成训练集和测试集
    cut = int(len(all_data) / 10) * 6
    training = all_data[0:cut]
    testing = all_data[cut:]
    for e in training:
        x.append(e[0])
        y.append(e[1])

if __name__ == "__main__":
    pre_processing()
    # for i in range(len(x)):
    #     print(x[i], y[i])

    testing_x = []
    testing_y = []
    for i in testing:
        testing_x.append(i[0])
        testing_y.append(i[1])

    # 把要调整的参数以及其候选值 列出来；
    param_grid = {"gamma": [0.001, 0.01, 0.1, 1, 10, 100],
                  "C": [0.001, 0.01, 0.1, 1, 10, 100],
                  "kernel": ["linear", "poly", "rbf", "sigmoid"]}
    print("Parameters:{}".format(param_grid))

    grid_search = GridSearchCV(SVC(), param_grid, cv=5)

    grid_search.fit(x, y)
    print("Test set score:{:.2f}".format(grid_search.score(testing_x, testing_y)))
    print("Best parameters:{}".format(grid_search.best_params_))
    print("Best score on train set:{:.2f}".format(grid_search.best_score_))

    # clf = SVC(kernel='linear')
    # clf.fit(x, y)
    # cnt = 0
    # testing_x = []
    # for i in testing:
    #     testing_x.append(i[0])
    # res = clf.predict(testing_x)
    # for i in range(len(testing_x)):
    #     if(testing[i][1] == res[i]):
    #         cnt += 1
    # print("accuracy: ", cnt/len(testing))
