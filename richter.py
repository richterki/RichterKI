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

# Main -------------------------------------------------------------------------

# Fall abfragen

input_fall = input("Bitte geben Sie die Anschuldigung ein >> ")

# Datenverarbeitung ------------------------------------------------------------

"""
db_fall = rdb.getFall()
schlagwoerter_list = db_fall.split("', '")[2]
schlagwoerter = str(schlagwoerter_list.split(","))
print(schlagwoerter)

if fall in schlagwoerter:
    print("Fall gefunden")
    fall_id_list = str(db_fall.split("', '")).split(", ")[0]
    fall_id = fall_id_list.split('["(')[1]
    print("Fall-ID: " + fall_id)

else:
    ("keinen Fall gefunden")

"""
faelle = rdb.getFall()
fall_id = str(rdb.get_fall_id()).replace("['", "").replace("']", "")
fall_schlagwoerter = str(faelle).replace("['", "").replace("']", "").split(", ")
# print(type(fall_schlagwoerter))
print(fall_id)

print(fall_schlagwoerter)

for fall in fall_schlagwoerter:
    if input_fall in fall_schlagwoerter:
        print("Fall gefunden: ")
        print("ID: " + fall_id)
        print(fall)

    else:
        continue

        # print(fall)

        # Netz -------------------------------------------------------------------------


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 3x3 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 6 * 6, 120)  # 6*6 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        # If the size is a square you can only specify a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


net = Net()
print(net)

output = net(input)
target = torch.randn(10)  # a dummy target, for example
target = target.view(1, -1)  # make it the same shape as output
criterion = nn.MSELoss()

loss = criterion(output, target)
print(loss)
