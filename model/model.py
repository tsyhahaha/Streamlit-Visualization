from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras import losses

import numpy as np

class PredModel(object):
    """build the forcast model"""

    def __init__(self):
        """
        to determine the model structure: Dence-Dence-Dence
        """
        self.model = Sequential()
        self.model.add(Dense(32, activation='relu', input_dim=16 * 1))
        self.model.add(Dense(16, activation='relu'))
        self.model.add(Dense(3))
        self.model.add(Activation('softmax'))
        self.model.compile(optimizer='adam', loss='mse')

    def load_model(self, m):
        if m is None:
            return
        self.model = m

    def train(self, X, y):
        """train the model"""
        self.model.fit(X, y, batch_size=50, epochs=100, shuffle=False)

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
        self.model.save('data/model.keras')
        return

    def printDense(self):
        dense1_layer, b1 = self.model.get_layer(index=0).get_weights()
        dense2_layer, b2 = self.model.get_layer(index=1).get_weights()
        dense3_layer, b3 = self.model.get_layer(index=2).get_weights()
        print("the first layer: ", dense1_layer.shape, "\ncontent:\n", dense1_layer)
        print("the second layer: ", dense2_layer.shape, "\ncontent:\n", dense2_layer)
        print("the third layer: ", dense3_layer.shape, "\ncontent:\n", dense3_layer)

