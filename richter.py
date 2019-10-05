# Programmiert am 07.06.2019,
#
# Richter KI von TeamPyKI ------------------------------------------------------
# Programmiert von Jakob Speer, Anya Wu, Leo Semmelmann
#


# Imports ----------------------------------------------------------------------

import torch
import torch.nn as nn
import torch.nn.functional as F
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
    def __init__(self, input, hiddens, output):
        super(Netz, self).__init__()
        self.hiddens = hiddens
        self.hid = nn.Linear(input + hiddens, hiddens)
        self.out = nn.Linear(input + hiddens, output)
        self.logsoftmax = nn.LogSoftmax(dim=1)

    def forward(self, x, hidden):
        x = torch.cat((x, hidden), 1)
        new_hidden = self.hid(x)
        output = self.logsoftmax(self.out(x))
        return output, new_hidden

    def initHidden(self):
        return Variable(torch.zeros(1, self.hiddens))


# print(len(data))

model = Netz(len(letters), 128, len(data))

if os.path.isfile('Netz.pt'):
    model = torch.load('Netz.pt')


def urteilFromOutput(out):
    _, i = out.data.topk(1)
    return urteile[i[0][0]]


# print(anklage)
# print(random.choice(urteile))
# print(random.choice(data[urteil]))


def getTrainData():
    urteil = random.choice(urteile)
    anklage = random.choice(data[urteil])
    anklage_tensor = Variable(anklageToTensor(anklage))
    urteil_tensor = Variable(torch.LongTensor([urteile.index(urteil)]))
    return urteil, anklage, urteil_tensor, anklage_tensor


criterion = nn.NLLLoss()


def train(urteil_tensor, anklage_tensor, lern_rate):
    hidden = model.initHidden()
    model.zero_grad()
    for i in range(anklage_tensor.size()[0]):
        output, hidden = model(anklage_tensor[i], hidden)
    loss = criterion(output, urteil_tensor)
    loss.backward()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    optimizer.step()

    return output, loss


def test():
    model.eval()
    anklage = input("Bitte geben sie die anklage ein: ")
    anklage_eval_tensor = anklageToTensor(anklage)
    anklage_eval_tensor.unsqueeze_(0)
    data = Variable(anklage_eval_tensor)
    out = model(data, torch.Tensor(128))
    print(out)


avg = []
sum = 0
lern_rate = 0.1

"""
with progressbar.ProgressBar(max_value=10000) as bar:
    for i in range(1, 10000):
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
"""

plt.figure()
plt.plot(avg)
plt.show()

test()
