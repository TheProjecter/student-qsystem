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

import optparse, re, sys

DEFINED_SOLVERS = [
    "dlv",
    "smodels",
    "clasp",
]

# utility classes

class UndefinedAnswerSetSolverException(Exception):
    """
    Defines a class for representing exceptions which are thrown in the event of
    an undefined prolog interpreter being specified.
    """
    def __init__(self, solver):
        super(UndefinedAnswerSetSolverException, self).__init__()
        self.solver = solver
    
    def __repr__(self):
        return str(self.solver) + " is an undefined answer set solver"
    
    def __str__(self):
        return self.__repr__()
    


# utility functions

def parse_options():
    """
    Returns the options passed to the program. Options are parsed from sys.argv.
    """
    parser = optparse.OptionParser()
    parser.add_option("-a", "--aprolog", action="store_true", dest = "aprolog",
                      help = "output models as A-Prolog code")
    parser.add_option("-s", "--solver", dest = "solver", default = "dlv",
                      help = "define the system providing the input stream (defaults to dlv)")
    (options, args) = parser.parse_args()
    return options


def is_valid_solver(solver):
    """
    Returns True if solver is an answer set solver known by the query system,
    and False otherwise.
    """
    return solver in DEFINED_SOLVERS


def dlv_text(text):
    """
    Returns a list of all models output by dlv.
    """
    pattern = re.compile(r'\{(.*?)\}', re.MULTILINE)
    return pattern.findall(text)


def smodels_text(text):
    """
    Returns a list of all models ouput by smodels.
    """
    pattern = re.compile(r'Stable Model:(.*)', re.MULTILINE)
    return pattern.findall(text)


def clasp_text(text):
    """
    Returns a list of all models output by clasp.
    """
    pattern = re.compile(r'Answer: \d+\n(.*)', re.MULTILINE)
    return pattern.findall(text)


def literals_in_model(text):
    """
    Given a string whose contents represent a model, returns a list of all of
    literals making up the model.
    """
    return [literal.rstrip(",") for literal in text.split()]


def write_as_text(model):
    """
    Writes the model as plain text.
    """
    for literal in literals_in_model(model):
        print literal
    print "::endmodel"


def write_as_code(model):
    """
    Writes the model as valid prolog/a-prolog code.
    """
    for literal in literals_in_model(model):
        print literal + "."
    print "%%endmodel"


def select_writer(output_as_code):
    """
    Returns the function to use for writing the models.
    """
    if output_as_code:
        return write_as_code
    else:
        return write_as_text


def write_output(options, models):
    """
    Given a list of models, write the models. By default models are written to stdout.
    If no models are found nothing is written.
    """
    writer = select_writer(options.aprolog)
    map(writer, models)


def rewrite_text(options, text):
	"""
	Rewrites the answer sets denoted by text according to the specified
	command-line options.
	"""
    if not is_valid_solver(options.solver):
        raise UndefinedAnswerSetSolverException(options.solver)
    
    if options.solver == "dlv":
        models = dlv_text(text)
    elif options.solver == "smodels":
        models = smodels_text(text)
    elif options.solver == "clasp":
        models = clasp_text(text)
    write_output(options, models)


# main function

def main():
    """
    Reformats the contents of stdin.
    """
    options = parse_options()
    text = sys.stdin.read()
    rewrite_text(options, text)


if __name__ == "__main__":
    main()
