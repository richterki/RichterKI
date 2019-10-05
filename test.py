from richter import *
import torch
import sys

rnn = torch.load('Netz.pt')


def evaluate(anklage_tensor):
    hidden = rnn.initHidden()

    for i in range(anklage_tensor.size()[0]):
        output, hidden = rnn(anklage_tensor[i], hidden)

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

    return predictions


if __name__ == '__main__':
    predict(sys.argv[1])
