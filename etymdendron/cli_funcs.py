""" This module contains some helper functions needed for the command line """

def get_search_word():
    #NB: for Python3, this is input(...), not raw_input(...)
    word = raw_input('Input a word to search for: ') 

    #TODO: Make sure it doesn't contain illegal characters, such as numbers?
    return word
