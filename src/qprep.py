#!/usr/bin/env python

"""
Copyright (c) 2010, Gregory Gelfond
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY GREGORY GELFOND ``AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL GREGORY GELFOND BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import optparse, sys

# utility functions

def parse_options():
    """
    Returns the options passed to the program. Options are parsed from sys.argv.
    """
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", dest = "filename", help = "specify the name of an input file")
    (options, args) = parser.parse_args()
    return options


def get_input_source():
    if len(sys.argv) == 1:
        return sys.stdin
    else:
        options = parse_options()
        return open(options.filename, "r")


def is_mkatoms_delimiter(text):
    """
    Returns True if text is an mkatoms delimiter string and False
    otherwise.
    """
    return text == "::endmodel" or text == "%%endmodel"


def is_positive_literal(literal):
    """
    Returns True if the given literal is positive and false otherwise. By
    convention negative literals start with a '-'.
    """
    return not literal.startswith('-')


def wrap(literal, model):
    """
    If the given literal is positive returns a string of the form pos(model, literal),
    otherwise returns a string of the form neg(model, atom) where atom is the positive
    form of the given literal.
    """
    if is_positive_literal(literal):
        return "pos(" + str(model) + "," + literal.strip('.') + ")"
    else:
        return "neg(" + str(model) + "," + literal[1:].strip('.') + ")"


def normalize(literal, model):
    """
    Returns a normalized form of the given literal with repsect to the given model.
    """
    wrapped_literal = wrap(literal, model)
    return wrapped_literal + '.'


def normalize_input(model_data):
    """
    Normalizes all of the literals in the given list.
    """
    model = 0
    normalized_text = []
    
    for text in model_data:
        if is_mkatoms_delimiter(text):
            model = model + 1
        else:
            normalized_text.append(normalize(text, model))
    
    normalized_text.sort()
    for text in normalized_text:
        print text
    
    print "number_of_models(" + str(model) + ")."


# main function

def main():
	"""
	Main entry point into qprep. Formats all of the literals on the
	input source specified by sys.argv for use by qsystem.
	"""
    model_data = [x.strip() for x in get_input_source().readlines()]
    normalize_input(model_data)


if __name__ == '__main__':
    main()
