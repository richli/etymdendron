""" This module contains some helper functions needed for the command line """

def get_search_word():
    #NB: for Python3, this is input(...), not raw_input(...)
    word = raw_input('Input a word to search for: ') 

    #TODO: Make sure it doesn't contain illegal characters, such as numbers?
    return word

def display_tree(tree, word):
    """ For a given word and tree, display the rest of the tree 
    """
    print('Root: {0}, {1}'.format(tree.attrib['text'],tree.attrib['lang']))
    display_children(tree,1)

def display_children(node,depth):
    """ Recursive function to display children of a node
        depth is what level we're on
    """
    # The len() of a node returns how many children it has
    if len(node) > 0:
        for child in node.iterchildren():
            depth_marker = '  '*depth
            print('{0}Child: {1}, {2}'.format(
                depth_marker,child.attrib['text'],child.attrib['lang']))
            display_children(child,depth+1)
    else:
        # The base of the recursion simply does nothing
        pass
