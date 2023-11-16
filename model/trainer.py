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

from model import PredModel
from keras.models import load_model

mappers = dict()


def getInitialData():
    content = pd.read_csv('data/students_data_FIX.csv')
    headers = list(content.columns)
    print("headers num is: ", len(headers))
    print(headers)
    np.save('data/headers.npy', np.array(headers))
    number_mapper = dict()
    for i in range(101):
        index = i
        base = str(index)
        number_mapper[base] = index
    for header in headers:
        mapper = dict()
        index = 1
        if header in ['raisedhands', 'VisitedResources', 'AnnouncementsView', 'Discussion']:
            mappers[header] = number_mapper
            continue
        elif header == 'Class':
            mapper['1'] = 0
            mapper['2'] = 1
            mapper['3'] = 2
            mappers[header] = mapper
            continue
        for i in content[header]:
            if i not in mapper.keys():
                mapper[i] = index
                index += 1
        mappers[header] = mapper
    jsmappers = json.dumps(mappers)
    with open('data/mappers.json', 'w') as f:  # 保存映射信息
        f.write(jsmappers)
    for header in headers:
        if header not in ['raisedhands', 'VisitedResources', 'AnnouncementsView', 'Discussion', 'Class']:
            content[header] = content[header].map(mappers[header])
    return content.to_numpy().astype(int)


def data_process(content):
    np.save('data/content.npy', content)

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


def train():
    data_content = getInitialData()
    if os.path.exists("data/model.keras"):
        old_model = load_model('data/model.keras')
        print('train from checkpoint......')
    else:
        old_model = None
    X0, Y0, X1, Y1 = data_process(data_content)
    model = PredModel()
    model.load_model(old_model)
    model.train(X0, Y0)
    model.save()
    right = model.evaluate(X1, Y1)
    print('Evaluation Accuracy:  ' + str(right*100)+"%")
    temp_dict = {'right': right}
    with open('data/eval_result.json', 'w') as f:
        json.dump(temp_dict, f)

if __name__=='__main__':
    train()

# model_train()
