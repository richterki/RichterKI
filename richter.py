# Programmiert am 07.06.2019,
#
# Richter KI von TeamPyKI ------------------------------------------------------
# Programmiert von Jakob Speer, Anya Wu, Leo Semmelmann
#


# Imports ----------------------------------------------------------------------

import torch
import torch.nn as nn
import readDatabase as rdb
import string
from torch.autograd import Variable
import random
import matplotlib.pyplot as plt
import progressbar
import os
import torch.optim as optim

# Variablen --------------------------------------------------------------------

letters = string.ascii_letters + ".,:'"

widgets = [
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',
]

#  ====== Main ======  ---------------------------------------------------------

# Fall abfragen

# input_fall = input("Bitte geben Sie die Anschuldigung ein >> ")

# Datenverarbeitung ------------------------------------------------------------

faelle = rdb.getFall()

fall_schlagwoerter = str(faelle).replace("['", "").replace("']", "").split(", ")


def charToIndex(char):
    return letters.find(char)


def charToTensor(char):
    ret = torch.zeros(1, len(letters))  # ret.size = (1, len(letters))
    ret[0][charToIndex(char)] = 1
    return ret


def anklageToTensor(urteil_t):
    ret = torch.zeros(len(urteil_t), 1, len(letters))
    for i, char in enumerate(urteil_t):
        ret[i][0][charToIndex(char)] = 1
    return ret


def anklage_f():
    al = []
    # print(len(faelle))
    for fall in faelle:
        al.append(fall[2])
        # print(fall[2])
    # print(al)
    return al


data = {}
urteile = []

# print(faelle)
# anklage_f()

anklage = anklage_f()

for fall in faelle:
    fall_id = fall[0]
    stadt_id = fall[1]
    # anklage = fall[2]
    verurteilt = fall[3]
    urteil = fall[4]
    schlagwoerter = fall[5]
    urteile.append(urteil)
    data[urteil] = anklage

n_categories = len(urteile)

"""
    if input_fall in fall[5]:

        print("Fall gefunden: ")
        print("ID: " + str(fall_id))
        print(fall)

    else:
        continue
    """

# print(data)
# print(urteile)

# Netz -------------------------------------------------------------------------


class Netz(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Netz, self).__init__()

        self.hidden_size = hidden_size

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax()

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return Variable(torch.zeros(1, self.hidden_size))


n_hidden = 128
n_epochs = 100000
print_every = 5000
plot_every = 1000
learning_rate = 0.005  # If you set this too high, it might explode. If too low, it might not learn


if os.path.isfile('Netz.pt'):
    model = torch.load('Netz.pt')


def urteilFromOutput(out):
    top_n, top_i = output.data.topk(1)  # Tensor out of Variable with .data
    category_i = top_i[0][0]
    return urteile[category_i], category_i


# print(anklage)
# print(random.choice(urteile))
# print(random.choice(data[urteil]))


def getTrainData():
    urteil = random.choice(urteile)
    anklage = random.choice(data[urteil])
    anklage_tensor = Variable(anklageToTensor(anklage))
    urteil_tensor = Variable(torch.LongTensor([urteile.index(urteil)]))
    return urteil, anklage, urteil_tensor, anklage_tensor


model = Netz(n_letters, n_hidden, n_categories)
optimizer = torch.optim.SGD(rnn.parameters(), lr=learning_rate)
criterion = nn.NLLLoss()


def train(urteil_tensor, anklage_tensor):
    hidden = model.initHidden()
    optimizer.zero_grad()

    for i in range(anklage_tensor.size()[0]):
        output, hidden = model(anklage_tensor[i], hidden)

    loss = criterion(output, urteil_tensor)
    loss.backward()

    optimizer.step()

    return output, loss.data[0]


confusion = torch.zeros(n_categories, n_categories)
n_confusion = 10000


def evaluate(anklage_tensor):
    hidden = model.initHidden()

    for i in range(anklage_tensor.size()[0]):
        output, hidden = model(anklage_tensor[i], hidden)

    return output


# Go through a bunch of examples and record which are correctly guessed
def predict(input_line, n_predictions=3):
    print('\n> %s' % input_line)
    with torch.no_grad():
        output = evaluate(anklageToTensor(input_line))

        # Get top N categories
        topv, topi = output.topk(n_predictions, 1, True)
        predictions = []

        for i in range(n_predictions):
            value = topv[0][i].item()
            category_index = topi[0][i].item()
            print('(%.2f) %s' % (value, urteile[category_index]))
            predictions.append([value, urteile[category_index]])


avg = []
sum = 0
lern_rate = 0.1


with progressbar.ProgressBar(max_value=1000) as bar:
    for i in range(1, 1000):
        urteil, anklage, urteil_tensor, anklage_tensor = getTrainData()
        output, loss = train(urteil_tensor, anklage_tensor, lern_rate)
        sum = sum + loss.data

        if i % 100 == 0:
            # lern_rate = lern_rate / 2
            avg.append(sum/100)
            sum = 0
            # print(i/100, "% done.")
            bar.update(i)

torch.save(model, 'Netz.pt')
print("Netz gespeichert...")


plt.figure()
plt.plot(avg)
plt.show()

# predict('Einbruch')
