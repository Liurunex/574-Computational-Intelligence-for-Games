from keras.models import Sequential
from keras.layers import Dense

model = Sequential()
model.add(Dense(units=64, activation='relu', input_dim=100))
model.add(Dense(units=10, activation='softmax'))


# input: training examples
# output: trained neural network
def train():
    pass


class NNstrategy:
    # parameter: object returned from train()
    def __index__(self, nn_object):
        pass

    # meet yahtzee.evaluate_strategy
    def choose_dice(self):
        pass

    # meet yahtzee.evaluate_strategy
    def choose_category(self):
        pass
