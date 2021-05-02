import sys, collections, os
import pprint as pp
from tf.app import use
A = use('bhsa:hot', hoist=globals())

#### This function receives a book and optionally a chapter and a verse and outputs a dictionary of all unique lexemes comprising the desires corpus
def gen_book_vocab(book_name, chapter = None, verse = None):

    if chapter != None and verse != None:
        all_words = T.nodeFromSection((book_name, chapter, verse))
    elif chapter != None and verse == None:
        all_words = T.nodeFromSection((book_name, chapter,))
    elif chapter == None and verse == None:
        all_words = T.nodeFromSection((book_name,))

    word_indices = L.d(all_words, 'word')  # retrieve the word nodes with L.d()

    word_occurences = {}

    for word_idx in word_indices:

        word_lexeme = F.lex.v(word_idx)

        if word_lexeme in word_occurences:
            word_occurences[word_lexeme] += 1
            # word_occurences[T.text(word_idx)] += 1
        else:
            word_occurences[word_lexeme] = 1
            # word_occurences[T.text(word_idx)] = 1

    return word_occurences

output = gen_book_vocab("Genesis", 1)

print(len(output))
