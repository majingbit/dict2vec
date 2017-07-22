#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from collections import defaultdict


def flatten(l):
    """Convert list of list to a list"""
    return [ el for sub_l in l for el in sub_l ]

def load_vocabulary(fn):
    """Read the file fn and return a set containing all the words
    of the vocabulary."""
    vocabulary = set()
    with open(fn) as f:
        for line in f:
            vocabulary.add(line.strip())

    return vocabulary

def clean_defs(definitions, output_file, vocab):
    """Load fetched definitions and regroup words with all their definitions."""

    regouped_dictionary = defaultdict(list)

    with open(definitions) as f:
        for line in f:
            line = line.strip()
            ar = line.split()[1:] # first token is the name of the dictionary
            word, defs = ar[0], ar[1:]
            regouped_dictionary[word].append(defs)

    # Regroup together all definitions of a word. Remove words
    # that are not in vocabulary.
    of = open(output_file, "w")

    if len(vocab) == 0: # No vocabulary given so no words removed.
        for w in regouped_dictionary:
            definition = ' '.join([el for el in flatten(regouped_dictionary[w])
                                   if len(el) > 1])
            of.write("%s %s\n" % (w, definition))
    else:
        vocabulary = load_vocabulary(vocab)
        for w in regouped_dictionary:
            definition = ' '.join([el for el in flatten(regouped_dictionary[w])
                                   if len(el) > 1 and el in vocabulary])
            of.write("%s %s\n" % (w, definition))

    of.close()
    print("Done.")


if __name__ == "__main__":
    dest_fn = "all-definitions-cleaned.txt"

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--definitions', help="""file containing the
                        definitions downloaded with the ./main.py""",
                        required=True)
    parser.add_argument("-v", "--vocab", help="""file containing a list of
                        words. The script will remove all words in definitions
                        that are not in this vocab""", default="",
                        required=True)

    args = parser.parse_args()


    print("Writing the new definitions file as %s." % (dest_fn))
    clean_defs(args.definitions, dest_fn, args.vocab)