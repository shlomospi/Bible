import sys, collections, os
import pprint as pp
from pylab import *
from tf.app import use
import numpy as np
from Divine_utils import *
import matplotlib.pyplot as plt
# A = use('bhsa:hot', hoist=globals())

books = ["Genesis", "Exodus", "Deuteronomy"]
word_occurences, vocab, unique_word_panCorpora, word_probs_softmax = gen_book_vocab(books,)

# print(word_probs_softmax)
# exit()

verse_by_lexemes, book = gen_verse("Exodus", 2, 2, verbose = 1)
limits = [0, 0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
prob_list = np.zeros((len(books), len(limits)))
for i, limit in enumerate(limits):

    prob = predictor(word_probs_softmax, verse_by_lexemes, verbose = 0, prob_limits = limit)
    prob_list[:, i] = prob
    print("\n")
print(prob_list)
for book in range(len(books)):
    plt.plot(limits, prob_list[book], "*", label = books[book])
plt.legend()
plt.show()
