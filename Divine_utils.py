import pprint as pp
from tf.app import use
import numpy as np
import random
A = use('bhsa:hot', hoist=globals())

#### NAIVE BAYES FUNCTIONS START ####

def gen_verse(book, chapter, verse, verbose=0):
    """
    returns a list of lexemes of a selected verse
    :param book: Book name as string
    :param chapter: number of the chapter
    :param verse:  number of the verse
    :param verbose: 1 for printing 0 for not printing the verse
    :return: returns a list of lexemes from the selected verse
    """
    indices = L.d(T.nodeFromSection((book, chapter, verse)), 'word')
    verse_by_lexemes = [F.lex_utf8.v(word_idx) for word_idx in indices]
    if verbose == 1:
        print(verse_by_lexemes)
    return verse_by_lexemes, book

def gen_book_vocab(books, chapters = None, verses = None):
    """
    This function receives a book and optionally a chapter and a verse and outputs a dictionary of all unique lexemes
    comprising the desires corpus. Creates a database from selected books
    :param books: list of books for vocabulary creation
    :param chapters: list of chapters
    :param verses: list of verses
    :return:    word_occurrences -  Dictionary containing other dictionaries, one per corpus,
                                    containing words and their recurrence
                vocab - a list of all the unique lexemes in the corpra
                unique_word_panCorpora - A dictionary containing all unique words in all corpora and their absolute
                                         probability of each word to belong to a given corpus.
                word_probs_softmax - a dictionary that contains a dictionary for every book with the unique lexemes and
                                     their respective softmax probabilities to belong to said book
    """
    vocab = [] # A vocabulary containing all unique words in all corpora
    word_occurrences = {} # Dictionary containing other dictionaries, one per corpus, containing words and their recurrence
    unique_word_panCorpora = {} # A dictionary containing all unique words in all corpora and their absolute probability of each word to belong to a given corpus.
    word_probs_softmax = {} # A dictionary containing entries similar to unique_words_panCorpora, but instead of the absolute probability of each word to belong to a given corpus - it calculates the softmax value thereof
    titles = []

    for i in range(len(books)):

        word_occurences_this = {} # Dictionary of word occurrences of the given corpus which will be added to word_occurrences

        # Extracting word indices of the desired corpus and generating a title string for the key in the main dictionary
        if chapters is not None and verses is not None:
            all_words = T.nodeFromSection((books[i], chapters[i], verses[i]))  # index of the target text in the DB
            title = "{0}_{1}_{2}".format(books[i], chapters[i], verses[i])
        elif chapters is not None and verses is None:
            all_words = T.nodeFromSection((books[i], chapters[i],))
            title = "{0}_{1}".format(books[i], chapters[i])
        elif chapters is None and verses is None:
            all_words = T.nodeFromSection((books[i],))
            title = "{0}".format(books[i])

        titles.append(title)  # List of titles of the main dictionary for easy access

        word_indices = L.d(all_words, 'word')
        # retrieve the word nodes with L.d(). A list of the indices of the words in the target text
        word_count = len(word_indices)  # Counting all words in this corpus

        # Looping over all word indices to count the words and add them to word_occurences_this
        for word_idx in word_indices:

            word_lexeme = F.lex_utf8.v(word_idx)

            if word_lexeme in word_occurences_this:
                word_occurences_this[word_lexeme] += 1
                # word_occurrences[T.text(word_idx)] += 1
            else:
                word_occurences_this[word_lexeme] = 1
                # word_occurrences[T.text(word_idx)] = 1

            #### Appending unique word to vocabulary
            if word_lexeme not in vocab:
                vocab.append(word_lexeme)


        word_occurences_this["word_count"] = word_count
        word_occurences_this = dict(sorted(word_occurences_this.items(), key=lambda item: item[1]))
        word_occurrences[title] = word_occurences_this

    word_count_total = np.sum(np.array([word_occurrences[titles[i]]["word_count"] for i in range(len(titles))])) # Total amount of words in all corpora

    # Looping over unique words and summing up their occurences NORMALIZED BY WORD_COUNT of the given corpus in all corpora
    for word in vocab:
        unique_word_panCorpora[word] = [(word_occurrences[titles[i]].get(word, 0) / word_occurrences[titles[i]]["word_count"]) * (word_occurrences[titles[i]]["word_count"] / word_count_total) for i in range(len(titles))]
        word_probs_softmax[word] = [np.exp(np.log(unique_word_panCorpora[word][i])) / np.sum(np.array(np.exp(np.log(unique_word_panCorpora[word])))) for i in range(len(titles))]

    return word_occurrences, vocab, unique_word_panCorpora, word_probs_softmax

def predictor(word_probs_softmax, verse, verbose = 0, prob_limits = 0.05):
    """
    This function uses the softmax vocabulary per word to predict which corpus the text belongs to
    :param word_probs_softmax:
    :param verse: a list of lexemes of a verse
    :return: a list of softmax probabilities of the verse belonging to each book in the database
    """
    nr_corpora = len(random.choice(list(word_probs_softmax.items()))[1]) # Choosing some random key in the dictionary to check the amount of relevant corpora
    prob = np.zeros((len(verse), nr_corpora))
    existing_words = 0. # normalizing by this value will keep the softmax of order unity, even if not all words of the input text exist in the class corpora

    for word_idx in range(len(verse)):
        word = verse[word_idx]
        if word in word_probs_softmax:
            existing_words += 1.
            for corpus in range(nr_corpora):
                if word_probs_softmax[word][corpus] < (1. / nr_corpora) - prob_limits or word_probs_softmax[word][corpus] > (1. / nr_corpora) + prob_limits:
                    prob[word_idx][corpus] = word_probs_softmax[word][corpus]
                else:
                    if verbose == 1:
                        print("The word {0} seems to be equally distributed in all corpora ({1} for corpus nr. {2}). Ignoring".format(word, word_probs_softmax[word][corpus], corpus))
                    existing_words -= 1.
                    break

    prob = np.sum(prob, axis=0) / existing_words

    print("result for a {} limit margins".format(prob_limits))

    return prob
