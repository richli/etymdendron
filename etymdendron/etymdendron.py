#!/usr/bin/env python

# This file is the main driver for the program

###
# Imports
import sys
import argparse
#import xml.etree.ElementTree as ET
from lxml import etree as ET

import cli_funcs

###
# Global constants
WORDS_FILE='words.xml'

def main():
    """ The main routine """
    ###
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run etymdendron')
    parser.add_argument('word', help='Word to search for (will be asked for if not specified)', nargs='?', default=None)
    args = parser.parse_args()

    ###
    # First let's load the XML
    words_tree = ET.ElementTree()
    words_tree.parse(WORDS_FILE)

    ###
    # Search for a word
    if args.word is None:
        search_word = cli_funcs.get_search_word()
    else:
        search_word = args.word

    # We go through each of the possible trees
    matched_words = []
    for root in words_tree.getroot().iterchildren():
        for word in root.iterdescendants():
            if word.attrib['text'] == search_word:
                # Add the found word to our list
                matched_words.append((root,word))

    # Now remove non-unique roots (using the set container)
    matched_roots = [match[0] for match in matched_words]
    unique_roots = set(matched_roots)
    num_trees = len(unique_roots)

    # No match
    if num_trees == 0:
        print('{0} is not found in {1}'.format(search_word,WORDS_FILE))
        sys.exit(0)
    # Multiple matches
    elif num_trees > 1:
        print('{0} is found in more than one tree'.format(search_word))
    # One match
    elif num_trees == 1:
        print('{0} is found in one tree'.format(search_word))

    ###
    # Display the tree

    ###
    # That's all!
    sys.exit(0)

if __name__ == '__main__':
    main()
