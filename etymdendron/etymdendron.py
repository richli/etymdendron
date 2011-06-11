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

    ###
    # Display the tree

    ###
    # That's all!
    sys.exit(0)

if __name__ == '__main__':
    main()
