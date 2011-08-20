#!/usr/bin/env python
""" This file is a CLI interface to the program 

    Note, this is no longer feature-complete since the GUI implements more 
    functions than this one. I don't have the time or interest to finish this
    off, but I have tried to keep the functions such that whether a GUI or CLI
    calls them, the result is the same.

"""

###
# Imports (global)
import sys
import argparse

# Imports (local)
from global_opts import WORDS_FILE
import cli_funcs
from common_funcs import loadDB, searchDB

def main():
    """ The main routine """
    ###
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run etymdendron')
    parser.add_argument('word', help='Word to search for (will be asked for '
        'if not specified)', nargs='?', default=None)
    args = parser.parse_args()

    ###
    # First let's load the XML
    words_tree = loadDB(WORDS_FILE)
    if type(words_tree) is str:
        print(words_tree) # This holds the error message
        sys.exit(1)

    ###
    # Display a header
    print('=========================')
    print('====   Etymdendron   ====')
    print('=========================')
    print('{0} loaded, {1} trees found'.format(WORDS_FILE,
        len(words_tree.getroot())))

    ###
    # Search for a word
    if args.word is None:
        search_word = cli_funcs.get_search_word()
    else:
        search_word = args.word

    num_trees, matched_words = searchDB(words_tree, search_word)

    ###
    # Display the tree if we have matches
    # No match
    if num_trees == 0:
        print('{0} is not found in {1}'.format(search_word, WORDS_FILE))
        sys.exit(0)
    # Multiple matches
    elif num_trees > 1:
        print('{0} is found in {1} trees'.format(search_word, num_trees))
        chosen_root, chosen_word = cli_funcs.choose_word_from_many(
                matched_words)
    # One match
    elif num_trees == 1:
        print('{0} is found in one tree'.format(search_word))
        # Extract the tree and all matched words separately
        # Just pick the first entry (m_w[...][0] are the same in this case)
        chosen_root = matched_words[0][0]
        chosen_word = [match[1] for match in matched_words]

    # And now display the tree
    cli_funcs.display_tree(chosen_root, chosen_word, search_word)

    ###
    # That's all!
    sys.exit(0)

if __name__ == '__main__':
    main()
