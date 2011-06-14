#!/usr/bin/env python
""" This file is the main driver for the program """

###
# Imports (global)
import sys
import argparse
try:
    from lxml import etree as ET
except ImportError as err:
    print('lxml is missing\n{0}'.format(err))

# Imports (local)
from global_opts import WORDS_FILE
import cli_funcs

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
    words_tree = ET.ElementTree()
    try:
        words_tree.parse(WORDS_FILE,ET.XMLParser(dtd_validation=True))
    except ET.XMLSyntaxError as err:
        print("ERROR: Error parsing {0}".
                format(WORDS_FILE))
        print('  {0}'.format(err))
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

    # We go through each of the possible trees
    matched_words = []
    for tree in words_tree.getroot().iterchildren():
        for word in tree.iterdescendants(tag='word'):
            for text in word.iterchildren(tag='text'):
                if text.text == search_word:
                    # Add the found word to our list
                    matched_words.append((tree, word))

    # Now remove non-unique roots (using the set container)
    matched_roots = [match[0] for match in matched_words]
    unique_roots = list(set(matched_roots))
    num_trees = len(unique_roots)

    # Concatenate all matched words
    matched_words_ur = [match[1] for match in matched_words]

    ###
    # Display the tree if we have matches
    # No match
    if num_trees == 0:
        print('{0} is not found in {1}'.format(search_word, WORDS_FILE))
        sys.exit(0)
    # Multiple matches
    elif num_trees > 1:
        print('{0} is found in {1} trees'.format(search_word,num_trees))
        chosen_root, chosen_word = cli_funcs.choose_word_from_many(matched_words)
        cli_funcs.display_tree(chosen_root,chosen_word)
    # One match
    elif num_trees == 1:
        print('{0} is found in one tree'.format(search_word))
        cli_funcs.display_tree(unique_roots[0], matched_words_ur)

    ###
    # That's all!
    sys.exit(0)

if __name__ == '__main__':
    main()
