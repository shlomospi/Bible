import sys, collections, os
import pprint as pp
from tf.app import use
A = use('bhsa:hot', hoist=globals())

#### This function receives a book and optionally a chapter and a verse and outputs a dictionary of all unique lexemes comprising the desires corpus
def gen_book_vocab(books, chapters = None, verses = None):

    vocab = [] # A vocabulary containing all unique words in all corpora
    word_occurences = {} # Dictionary containing other dictionaries, one per corpus, containing words and their recurrence
    unique_word_panCorpora = {} # A dictionary containing all unique words in all corpora and their occurence in each.
    titles = []

    for i in range(len(books)):

        word_occurences_this = {}
        word_count = 0

        #### Extracting word indices of the desired corpus and generating a title string for the key in the main dictionary
        if chapters != None and verses != None:
            all_words = T.nodeFromSection((books[i], chapters[i], verses[i]))
            title = "{0}_{1}_{2}".format(books[i], chapters[i], verses[i])
        elif chapters != None and verses == None:
            all_words = T.nodeFromSection((books[i], chapters[i],))
            title = "{0}_{1}".format(books[i], chapters[i])
        elif chapters == None and verses == None:
            all_words = T.nodeFromSection((books[i],))
            title = "{0}".format(books[i])

        titles.append(title) # List of titles of the main dictionary for easy access

        word_indices = L.d(all_words, 'word')  # retrieve the word nodes with L.d()
        word_count += len(word_indices) # Counting all words in this corpus

        #### Looping over all word indices to count the words and add them to the vocabulary
        for word_idx in word_indices:

            word_lexeme = F.lex.v(word_idx)

            if word_lexeme in word_occurences_this:
                word_occurences_this[word_lexeme] += 1
                # word_occurences[T.text(word_idx)] += 1
            else:
                word_occurences_this[word_lexeme] = 1
                # word_occurences[T.text(word_idx)] = 1

            #### Appending unique word to vocabulary
            if word_lexeme not in vocab:
                vocab.append(word_lexeme)

        word_occurences_this["word_count"] = word_count
        word_occurences_this = dict(sorted(word_occurences_this.items(), key=lambda item: item[1]))
        word_occurences[title] = word_occurences_this

    #### Looping over unique words and summing up their occurences in all corpora ####
    for word in vocab:
        unique_word_panCorpora[word] = [word_occurences[titles[i]].get(word, 0) for i in range(len(titles))]

    return word_occurences, vocab, unique_word_panCorpora

word_occurences, vocab, unique_word_panCorpora = gen_book_vocab(["Genesis", "Exodus"],)

print(vocab)
# print(len(word_occurences))
# print(word_occurences["Exodus"])
# print(unique_word_panCorpora)
