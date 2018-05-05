from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
import numpy as np

import yahtzee
import csv
import sys

categories = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "FH",
    "S",
    "C",
    "Y",
    "E",
]

all_categories = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "3K",
    "4K",
    "FH",
    "SS",
    "LS",
    "C",
    "Y",
]


def to_string(l):
    res = "["
    for i in l:
        res += str(i)
    res += "]"
    return res


def max_count(board):
    res = 0
    for i in board:
        res = max(res, board.count(i))
    return res


def find_max(board):
    res = 0
    for i in board:
        res = max(res, int(i))
    return str(res)


def classification():
    dataset = csv.reader(open('ori.dat', newline=''), delimiter=',')

    for index, row in enumerate(dataset):
        label = []
        # print(f'-------{index}---{row[-1]}-------------')
        if '[' in row[-1] and ']' in row[-1]:
            # initial the roll
            target = row[-1]
            roll = yahtzee.YahtzeeRoll()
            roll = roll.parse(row[-3])
            reroll = row[-2]

            board = row[-3]
            optimal = target[1:-1]

            # initial the sheet
            sheet = yahtzee.YahtzeeScoresheet()
            for cat in str(row[0]).split():
                if 'UP' in cat:
                    break
                if cat == 'Y+':
                    sheet.scores[-1] = 1
                else:
                    sheet.scores[sheet.categories.index(cat)] = 1

            # try for 1~6s:
            if len(target) > 2:
                try_num = 0
                not_nums = False
                for i in target[1:-1]:
                    if try_num != 0 and try_num != int(i):
                        not_nums = True
                        break
                    try_num = int(i)
                if not_nums is not True:
                    res = roll.select_all([try_num])
                    if to_string(res.as_list()) == target \
                            and sheet.scores[sheet.categories.index(str(try_num))] is None:
                        label.append(str(try_num))

            # try for FH, S, C, Y
            for i in categories:
                if i == "FH" and len(label) == 0:
                    res = roll.select_for_full_house()
                    if to_string(res.as_list()) == target:
                        if sheet.scores[sheet.categories.index("FH")] is None:
                            label.append("FH")
                elif i == "S" and len(label) == 0:
                    res = roll.select_for_straight(sheet)
                    # 4 different dices in optimal count as S
                    arr = set()
                    for c in optimal:
                        arr.add(c)
                    if to_string(res.as_list()) == target or len(arr) > 2:
                        if sheet.scores[sheet.categories.index("LS")] is None \
                                or sheet.scores[sheet.categories.index("SS")] is None:
                            label.append("S")
                elif i == "Y" and len(label) == 0:
                    res = roll.select_for_n_kind(sheet, int(reroll))
                    if to_string(res.as_list()) == target:
                        label.append("Y")
                elif i == "C" and len(label) == 0:
                    res = roll.select_for_chance(int(reroll))
                    if to_string(res.as_list()) == target:
                        if sheet.scores[sheet.categories.index("C")] is None:
                            label.append("C")

            # deal with not found case
            if len(label) == 0:
                # if only one opening
                if sheet.scores.count(None) == 1:
                    res = all_categories[sheet.scores.index(None)]
                    if res == '3K' or res == '4K' or res == 'Y':
                        res = 'Y'
                    elif res == 'LS' or res == 'SS':
                        res = 'S'
                    label.append(res)
                else:
                    # target is []:
                    if len(target) == 2:
                        label.append('E')
                        # print(f'{row} meet Empty cases')
                    else:
                        # [ab] case
                        if len(optimal) == 2 and optimal[0] != optimal[1]:
                            if sheet.scores[sheet.categories.index("LS")] is None \
                                    or sheet.scores[sheet.categories.index("SS")] is None:
                                label.append("S")
                            else:
                                if sheet.scores[sheet.categories.index(optimal[0])] is None:
                                    label.append(optimal[0])
                                elif sheet.scores[sheet.categories.index(optimal[1])] is None:
                                    label.append(optimal[1])

                        # [xxxa] or [xxxxa] or [xxa] for Y, then FH
                        if len(label) == 0 and max_count(optimal) > 1:
                            if sheet.scores[sheet.categories.index('3K')] is None \
                                    or sheet.scores[sheet.categories.index('4K')] is None \
                                    or sheet.scores[sheet.categories.index('Y')] is None:
                                label.append('Y')
                            elif sheet.scores[sheet.categories.index('FH')] is None:
                                label.append('FH')

                        # case [a]
                        if len(label) == 0 and len(optimal) == 1:
                            if sheet.scores[sheet.categories.index("LS")] is None \
                                    or sheet.scores[sheet.categories.index("SS")] is None:
                                label.append('S')

                        # [ab] not processed, treat as C
                        if len(label) == 0 and len(optimal) == 2:
                            label.append('C')
                        # if len(label) == 0 and

                        # case [a] a is max in board
                        if len(label) == 0 and optimal == find_max(board):
                            if sheet.scores[sheet.categories.index("C")] is None:
                                label.append('C')
                        # if len()
                        # rest deal as Y
                        if len(label) == 0:
                            if len(optimal) == 1:
                                label.append('Y')
                            elif len(optimal) == 3:
                                label.append('S')
                            '''
                            out = ''
                            for i, n in enumerate(sheet.scores):
                                if n is None:
                                    out += all_categories[i] + " "
                            print(f'{out} {board} {reroll} [{optimal}]')
                            '''
        # reroll == 0 cases
        elif row[-1] == 'LS' or row[-1] == 'SS':
            label.append('S')
        elif row[-1] == '3K' or row[-1] == '4K' or row[-1] == 'Y':
            label.append('Y')
        else:
            label.append(str(row[-1]))
        if len(label) > 1:
            print(f'------label size > 1')
        line = ""
        for n in row:
            line += str(n) + ","
        line += str(label[0])
        # print(label[0])
        with open('label.dat', 'a') as f:
            f.write(line+'\n')


def normalization():
    # load dataset
    dataset = csv.reader(open('label.dat', newline=''), delimiter=',')
    X = []
    Y = []
    '''
    1 2 3 4 5 6 3K 4K FH SS LS C Y(Y+), UP, board, reroll: (op) 
    label[10] -> 1 2 3 4 5 6 FH S C Y E
    '''
    for index, row in enumerate(dataset):
        line_x = [0] * (len(all_categories) + 1 + 6 + 1)
        line_y = [0] * (len(categories))
        # encode sheet
        for cat in str(row[0]).split():
            if 'UP' in cat:
                line_x[13] = min(float(cat[2:])/63, 1)
                break
            if 'Y+' == cat:
                cat = 'Y'
            line_x[all_categories.index(cat)] = 1
        # encode dices
        for i in range(6):
            c = str(i + 1)
            line_x[i + 14] = row[1].count(c)

        # encode reroll
        line_x[20] = float(row[2]) / 2

        # encode the label
        line_y[categories.index(row[-1])] = 1

        # print(line_x)
        X.append(line_x)

        # print(line_y)
        Y.append(line_y)

        line = ""
        for i in line_x:
            line += str(i) + ","
        for i in line_y:
            line += str(i) + ","
        line = line[:-1]
        # print(line)
        with open('training.dat', 'a') as f:
            f.write(line+'\n')


# input: training examples
# output: trained neural network

def train():
    np.random.seed(7)
    x = []
    y = []
    # read from stdin
    for line in sys.stdin:
        line = line[:-1]
        llist = list(map(float, line.split(',')))
        line_x = llist[0:21]
        line_y = llist[21:]
        x.append(line_x)
        y.append(line_y)

    test_size = int(len(x)/5)
    train_size = len(x) - test_size

    x_train = np.matrix(x[:train_size])
    y_train = np.matrix(y[:train_size])

    x_test = np.matrix(x[train_size:])
    y_test = y[train_size:]

    # define a full-connected network structure with 3 layers
    model = Sequential()
    model.add(Dense(300, input_dim=x_train.shape[1], activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(y_train.shape[1], activation='sigmoid'))

    # compile the model
    # sgd = SGD(lr=0.1, decay=1e-6, momentum=0.8, nesterov=True)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # fit the model
    model.fit(x_train, y_train, epochs=100, batch_size=50)

    # test data result
    y_predict = [max(enumerate(y), key=lambda x: x[1])[0] for y in model.predict(x_test)]
    y_correct = [max(enumerate(y), key=lambda x: x[1])[0] for y in y_test]
    print(sum((1 if y[0] == y[1] else 0) for y in zip(y_predict, y_correct)) / len(y_predict))


class NNstrategy:
    # parameter: object returned from train()
    def __index__(self, nn_object):
        self.nn = nn_object

    # meet yahtzee.evaluate_strategy
    def choose_dice(self, sheet, roll, reroll):
        pass

    # meet yahtzee.evaluate_strategy
    def choose_category(self, sheet, roll):
        pass


if __name__ == "__main__":
    # classification()
    # normalization()
    train()