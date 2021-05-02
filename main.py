import sys, collections, os
import pprint as pp
from tf.app import use
A = use('bhsa:hot', hoist=globals())

#### This function receives a book and optionally a chapter and a verse and outputs a dictionary of all unique lexemes comprising the desires corpus
def gen_book_vocab(books, chapters = None, verses = None):

    word_occurences = {}
    word_count = 0.

    for i in range(len(books)):

        if chapters != None and verses != None:
            all_words = T.nodeFromSection((books[i], chapters[i], verses[i]))
        elif chapters != None and verses == None:
            all_words = T.nodeFromSection((books[i], chapters[i],))
        elif chapters == None and verses == None:
            all_words = T.nodeFromSection((books[i],))

        word_indices = L.d(all_words, 'word')  # retrieve the word nodes with L.d()
        word_count += len(word_indices)

        for word_idx in word_indices:

            word_lexeme = F.lex.v(word_idx)

            if word_lexeme in word_occurences:
                word_occurences[word_lexeme] += 1
                # word_occurences[T.text(word_idx)] += 1
            else:
                word_occurences[word_lexeme] = 1
                # word_occurences[T.text(word_idx)] = 1

        word_occurences = sorted(word_occurences.items(), key=lambda x: x[1], reverse=True)
        return word_occurences, word_count

word_occurences, word_count = gen_book_vocab(["Genesis", "Exodus"],)

print(word_count)
print(len(word_occurences))
print(word_occurences)
