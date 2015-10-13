""" Analyzes the word frequencies in a book downloaded from Project Gutenberg """

import string as s
import re

def get_word_list(file_name):
    """ Reads the specified project Gutenberg book.  Header comments,
        punctuation, and whitespace are stripped away.  The function
        returns a list of the words used in the book as a list.
        All words are converted to lower case.
    """
    f = open(file_name, 'r')
    lines = f.readlines()
    curr_line = 0
    fin_line = 0
    while (lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1):
        curr_line += 1
    while (lines[fin_line].find('END OF THIS PROJECT GUTENBERG EBOOK') == -1):
        fin_line += 1
    lines = lines[curr_line+1:fin_line]
    words = []
    for line in lines:
        line_list = s.split(line)
        words.append(line_list)
    flattened = [ele for sublist in words for ele in sublist]
    lowered = [s.lower(ele) for ele in flattened]
    stripped = [re.sub("[()/\,';.?!-]", '', ele) for ele in lowered]
    return stripped

def get_top_n_words(word_list, n):
    """ Takes a list of words as input and returns a list of the n most frequently
        occurring words ordered from most to least frequently occurring.

        word_list: a list of words (assumed to all be in lower case with no
        punctuation
        n: the number of words to return
        returns: a list of n most frequently occurring words ordered from most
        frequently to least frequently occurring
    """
    word_count = {}
    for word in word_list:
        if word in word_count:
            val = word_count[word]
            word_count[word] = val + 1
        else:
            word_count[word] = 1
    ordered_by_frequency = sorted(word_count, key=word_count.get, reverse=True)
    return ordered_by_frequency[:n]

def unique_words(word_list):
    """ Takes a list of words as input and return number of unique words, and the
        ratio of unique words to total words

        word_list: a list of words (assumed to all be in lower case with no
        punctuatio
    """
    word_count = {}
    for word in word_list:
        if word in word_count:
            val = word_count[word]
            word_count[word] = val + 1
        else:
            word_count[word] = 1
    ordered_by_frequency = sorted(word_count, key=word_count.get, reverse=True)
    x = len(ordered_by_frequency)
    y = len(word_list)
    z = float(x)/float(y)
    return [x, z]

def print_func(text):
    """ Print various results of this script """
    words = get_word_list(text)
    freq = get_top_n_words(words, n)
    unique = unique_words(words)
    print text[:-4], freq, unique

n = 10
print_func('Ulysses.txt')
print_func('Portrait.txt')
print_func('Proust.txt')
print_func('Voyage.txt')
print_func('NightDay.txt')
print_func('Oz.txt')