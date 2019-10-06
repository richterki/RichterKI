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
import time
import math

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
    for fall in faelle:
        al.append(fall[2])
    return al


data = {}
urteile = []


# anklage = anklage_f()

for fall in faelle:
    fall_id = fall[0]
    stadt_id = fall[1]
    anklage = fall[2]
    verurteilt = fall[3]
    urteil = fall[4]
    schlagwoerter = fall[5]
    urteile.append(urteil)
    data[urteil] = anklage

n_categories = len(urteile)
n_letters = len(letters)
# model = Netz(len(letters), 128, len(data))


# Netz -------------------------------------------------------------------------


class Netz(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(Netz, self).__init__()

        self.hidden_size = hidden_size

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

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
print_every = 1000
plot_every = 1000
learning_rate = 0.005  # If you set this too high, it might explode. If too low, it might not learn


if os.path.isfile('Netz.pt'):
    model = torch.load('Netz.pt')


def urteilFromOutput(out):
    top_n, top_i = output.data.topk(1)  # Tensor out of Variable with .data
    category_i = top_i[0][0]
    return urteile[category_i], category_i


def randomChoice(l):
    return l[random.randint(0, len(l) - 1)]


def randomTrainingPair():
    category = randomChoice(urteile)
    line = data.get(category)
    category_tensor = Variable(torch.LongTensor([urteile.index(category)]))
    line_tensor = Variable(anklageToTensor(line))
    return category, line, category_tensor, line_tensor


randomTrainingPair()


def getTrainData():
    urteil = random.choice(urteile)
    anklage = random.choice(data[urteil])
    anklage_tensor = Variable(anklageToTensor(anklage))
    urteil_tensor = Variable(torch.LongTensor([urteile.index(urteil)]))
    return urteil, anklage, urteil_tensor, anklage_tensor


model = Netz(n_letters, n_hidden, n_categories)
optimizer = optim.SGD(model.parameters(), lr=learning_rate)
criterion = nn.NLLLoss()


def train(urteil_tensor, anklage_tensor):
    hidden = model.initHidden()
    optimizer.zero_grad()

    for i in range(anklage_tensor.size()[0]):
        output, hidden = model(anklage_tensor[i], hidden)

    loss = criterion(output, urteil_tensor)
    loss.backward()

    optimizer.step()

    return output, loss.data


confusion = torch.zeros(n_categories, n_categories)
n_confusion = 10000


avg = []
sum = 0

current_loss = 0
all_losses = []


def timeSince(since):
    now = time.time()
    s = now - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


start = time.time()

"""
for epoch in range(1, n_epochs + 1):
    category, line, category_tensor, line_tensor = randomTrainingPair()
    output, loss = train(category_tensor, line_tensor)
    current_loss += loss

    # Print epoch number, loss, name and guess
    if epoch % print_every == 0:
        guess, guess_i = urteilFromOutput(output)
        correct = '✓' if guess == category else '✗ (%s)' % category
        print('%d %d%% (%s) %.4f %s / %s %s' %
              (epoch, epoch / n_epochs * 100, timeSince(start), loss, line, guess, correct))

    # Add current loss avg to list of losses
    if epoch % plot_every == 0:
        all_losses.append(current_loss / plot_every)
        current_loss = 0

torch.save(model, 'Netz.pt')


plt.figure()
plt.plot(all_losses)
plt.show()
"""


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


predict(input("Bitte geben sie die Anklage ein: "))
