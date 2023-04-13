# _*_ coding: utf-8 _*_
"""
@File       : initializer.py
@Author     : Tao Siyuan
@Date       : 2022/8/1
@Desc       :...
"""
import os.path
import random

import numpy as np
import pandas as pd
import json

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from tensorflow import keras

mappers = dict()


def getInitialData():
    content = pd.read_csv('students_data_FIX.csv')
    headers = list(content.columns)
    print("headers num is: ", len(headers))
    print(headers)
    np.save('headers.npy', np.array(headers))
    number_mapper = dict()
    for i in range(101):
        index = i
        base = str(index)
        number_mapper[base] = index
    for header in headers:
        mapper = dict()
        index = 1
        # if header in ['raisedhands', 'VisitedResources', 'AnnouncementsView', 'Discussion']:
        #     mappers[header] = number_mapper
        #     continue
        # elif header == 'Class':
        #     mapper['1'] = 0
        #     mapper['2'] = 1
        #     mapper['3'] = 2
        #     mappers[header] = mapper
        #     continue
        for i in content[header]:
            if i not in mapper.keys():
                mapper[i] = index
                index += 1
        mappers[header] = mapper
    jsmappers = json.dumps(mappers)
    with open('mappers.json', 'w') as f:  # 保存映射信息
        f.write(jsmappers)
    for header in headers:
        if header not in ['raisedhands', 'VisitedResources', 'AnnouncementsView', 'Discussion', 'Class']:
            content[header] = content[header].map(mappers[header])
    return content.to_numpy().astype(int)


def data_process(content):
    np.save('content.npy', content)

    def data_split(full_list, ratio, shuffle=False):
        n_total = len(full_list)
        offset = int(n_total * ratio)
        if n_total == 0 or offset < 1:
            return [], full_list
        if shuffle:
            random.shuffle(full_list)
        sublist_1 = full_list[:offset]
        sublist_2 = full_list[offset:]
        return sublist_1, sublist_2

    train, valid = data_split(content, 0.8, True)
    train_X = train[:, :-1]
    train_Ys = train[:, -1]
    train_Y = []
    for i in range(len(train_X)):
        tmp = [0, 0, 0]
        tmp[train_Ys[i]-1] = 1
        train_Y.append(tmp)
    valid_X = valid[:, :-1]
    valid_Ys = valid[:, -1]
    valid_Y = []
    for i in range(len(valid_X)):
        tmp = [0, 0, 0]
        tmp[valid_Ys[i]-1] = 1
        valid_Y.append(tmp)
    train_Y = np.array(train_Y)
    valid_Y = np.array(valid_Y)
    print('train number is: X---{0}, Y--{1}'.format(len(train_X), len(train_Y)))
    print('valid number is: X---{0}, Y--{1}'.format(len(valid_X), len(valid_Y)))
    return train_X, train_Y, valid_X, valid_Y


class pred_model(object):
    """build the forcast model"""

    def __init__(self):
        """
        to determine the model structure: Dence-Dence-Dence
        """
        self.model = Sequential()
        self.model.add(Dense(32, activation='relu', input_dim=16 * 1))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(32, activation='relu'))
        # self.model.add(Conv1D(1, kernel_size=3, activation='relu', input_shape=(16, 1),
        #                       ))
        # self.model.add(MaxPool2D(pool_size=4, strides=4))
        # self.model.add(Conv1D(1, kernel_size=3, activation='relu',
        #                       ))
        self.model.add(Dense(3))
        self.model.add(Activation('softmax'))
        self.model.compile(optimizer='adam', loss='mse')

    def load_model(self, m):
        if m is None:
            return
        self.model = m

    def train(self, X, y):
        """train the model"""
        self.model.fit(X, y, batch_size=50, epochs=10, shuffle=False)

    def predict(self, X):
        """prediction"""
        pred = self.model.predict(X)
        return pred

    def evaluate(self, X, y):
        """evaluate the model by compute its RMSD and trend consistency"""
        pred = self.predict(X)  # pred is the predict result and y is the right result
        # print('pred is: ', pred)
        # print('valid result is: ', y)
        pred_re = []
        for line in pred:
            line = list(line)
            pred_re.append(line.index(max(line)))
        pred_re = np.array(pred_re)
        y_re = []
        for line in y:
            line = list(line)
            y_re.append(line.index(max(line)))
        y_re = np.array(y_re)
        judge = pred_re == y_re
        return np.sum(judge) / len(y)

    def save(self):
        self.model.save('data_forcast.h5')
        return

    def printDense(self):
        dense1_layer, b1 = self.model.get_layer(index=0).get_weights()
        dense2_layer, b2 = self.model.get_layer(index=1).get_weights()
        dense3_layer, b3 = self.model.get_layer(index=2).get_weights()
        print("the first layer: ", dense1_layer.shape, "\ncontent:\n", dense1_layer)
        print("the second layer: ", dense2_layer.shape, "\ncontent:\n", dense2_layer)
        print("the third layer: ", dense3_layer.shape, "\ncontent:\n", dense3_layer)


def model_train():
    data_content = getInitialData()
    if os.path.exists("data_forcast.h5"):
        old_model = keras.models.load_model('data_forcast.h5')
    else:
        old_model = None
    X0, Y0, X1, Y1 = data_process(data_content)
    model = pred_model()
    model.load_model(old_model)
    model.train(X0, Y0)
    model.save()
    right = model.evaluate(X1, Y1)
    print('正确率： ' + str(right*100)+"%")
    temp_dict = {'right': right}
    with open('data.json', 'w') as f:
        json.dump(temp_dict, f)


# model_train()
