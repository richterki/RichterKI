# Programmiert am 07.06.2019,
#
# Richter KI von TeamPyKI ------------------------------------------------------
# Programmiert von Jakob Speer, Anya Wu, Leo Semmelmann
#


# Imports ----------------------------------------------------------------------

import torch
import torch.nn as nn
import torch.nn.functional as F

# Main -------------------------------------------------------------------------


class MeinNetz(nn.Module):
    def __init__(self):
        super(MeinNetz(), self).__init__()
        self.lin1 = nn.Linear(10, 10)
        self.lin2 = nn.Linear(10, 10)

    def forward(self, x):
        pass

    def num_flat_features(self, x):
        pass


netz = MeinNetz()
print(netz)
