""" This module contains some helper functions needed for the command line """

import common_funcs as cf

###
# Input functions
def get_search_word():
    """ Just a wrapper to input a search word

    """
    #NB: for Python3, this is input(...), not raw_input(...)
    word = raw_input('Input a word to search for: ') 
    #TODO: Make sure it doesn't contain illegal characters, such as numbers?
    return word

def get_num_choice(prompt='Input: ', min_num=0, max_num=10):
    """ Prompt for an integer between min_num and max_num

    """
    while True:
        num = raw_input(prompt)
        try:
            num = int(num)
            if min_num <= num <= max_num:
                return num
            else:
                print('{0} is out of range'.format(num))
                continue
        except ValueError:
            print('That is an invalid number')


def choose_word_from_many(words):
    """ From a list of matched words, prompts the user to select which one

        words is a list of tuples, each tuple is (tree,word).
        Returns the one (tree,word) tuple.

    """
    # Find the morphemes,language for each instance
    mor_lan = []
    word_text = cf.loadWordDetails(words[0][1])['text'][0]
    for item in words:
        word = item[1]
        word_details = cf.loadWordDetails(word)
        mor_lan.append( (word_details['morpheme'], word_details['lang']) )

    print('For the word {0}, {1} options are available:'.format(
        word_text, len(mor_lan)))
    for item in enumerate(mor_lan, 1):
        print('  {0}: In {1}, choose the {2} morpheme'.format(
            item[0], item[1][1], item[1][0]))
    item_select = get_num_choice(min_num=1, max_num=len(mor_lan))

    print('{0} morpheme of {1} chosen'.format(
        mor_lan[item_select-1][0], word_text))
    return words[item_select-1]

###
# Display functions
def display_tree(tree, word, search_word):
    """ For a given word and tree, display the rest of the tree 

        The search_word is emphasized.

    """
    # Encapsulate word in a list if it isn't already
    if type(word) is not list:
        word = [word]

    tree_details = cf.loadWordDetails(tree)
    print('Root: {0} ({1})'.format(tree_details['text'][0],
        tree_details['lang']))
    display_children(tree, 1, word, search_word)

def display_children(node, depth, word, search_word):
    """ Recursive function to display children of a node

        depth is what level we're on.
        word is the word element we're looking for (it will be emphasized
        in the tree).
        search_word is the word text we're looking for.

    """
    # The len() of a node returns how many children it has
    if cf.countWordChildren(node) > 0:
        for child in cf.loadWordChildren(node):
            depth_marker = '  '*depth
            child_markup = ''
            child_details = cf.loadWordDetails(child)
            if child in word:
                # First we have the emphasized word
                # Then the other matches, if there
                child_markup = ', '.join(['*{0}*'.format(text_var)
                    for text_var in child_details['text'] 
                    if text_var == search_word])
                child_markup_rest = ', '.join(['{0}'.format(text_var)
                    for text_var in child_details['text'] 
                    if text_var != search_word])
                if child_markup_rest is not '':
                    child_markup = ', '.join([child_markup, child_markup_rest])
            else:
                child_markup = ', '.join(['{0}'.format(text_var)
                    for text_var in child_details['text']])

            print(u'{0}Child: {1} ({2}, "{3}")'.format(
                depth_marker, child_markup, child_details['lang'],
                child_details['def']))
            display_children(child, depth+1, word, search_word)
    else:
        # The base of the recursion simply does nothing
        pass
