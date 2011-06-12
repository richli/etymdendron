""" This module contains some helper functions needed for the command line """

###
# Input functions
def get_search_word():
    """ Just a wrapper to input a search word
    """
    #NB: for Python3, this is input(...), not raw_input(...)
    word = raw_input('Input a word to search for: ') 
    #TODO: Make sure it doesn't contain illegal characters, such as numbers?
    return word

def get_num_choice(prompt='Input: ',min_num=0,max_num=10):
    """ Get a number choice with prompt, only allow integers 
        between min_num and max_num
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

###
# Display functions
def display_tree(tree, word):
    """ For a given word and tree, display the rest of the tree 
    """
    print('Root: {0}, {1}'.format(tree.attrib['text'], tree.attrib['lang']))
    display_children(tree, 1)

def display_children(node, depth):
    """ Recursive function to display children of a node
        depth is what level we're on
    """
    # The len() of a node returns how many children it has
    if len(node) > 0:
        for child in node.iterchildren():
            depth_marker = '  '*depth
            print('{0}Child: {1}, {2}'.format(
                depth_marker, child.attrib['text'], child.attrib['lang']))
            display_children(child, depth+1)
    else:
        # The base of the recursion simply does nothing
        pass
