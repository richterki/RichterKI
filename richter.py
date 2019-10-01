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

# Variablen --------------------------------------------------------------------

letters = string.ascii_letters + ".,:'"

#  ====== Main ======  ---------------------------------------------------------

# Fall abfragen

input_fall = input("Bitte geben Sie die Anschuldigung ein >> ")

# Datenverarbeitung ------------------------------------------------------------

faelle = rdb.getFall()

fall_schlagwoerter = str(faelle).replace("['", "").replace("']", "").split(", ")


data = {}


def charToIndex(char):
    return letters.find(char)


def charToTensor(char):
    ret = torch.zeros(1)


for fall in faelle:
    fall_id = fall[0]
    stadt_id = fall[1]
    anklage = fall[2]
    verurteilt = fall[3]
    urteil = fall[4]
    schlagwoerter = fall[5]
    if input_fall in fall[5]:

        print("Fall gefunden: ")
        print("ID: " + str(fall_id))
        print(fall)

        data[anklage] = urteil

    else:
        continue

# Netz -------------------------------------------------------------------------
