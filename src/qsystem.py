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

import optparse, os, sys

# utility classes

class QuerySystemRuntimeException(Exception):
    """
    Defines a class for representing exceptions which are thrown in the event
    of a general runtime error.
    """
    def __init__(self, source):
        super(QuerySystemRuntimeException, self).__init__()
        self.source = source
    
    def __repr__(self):
        return str(self.source) + " has failed"
    
    def __str__(self):
        return self.__repr__()
    


class UndefinedPrologInterpreterException(Exception):
    """
    Defines a class for representing exceptions which are thrown in the event of
    an undefined prolog interpreter being specified.
    """
    def __init__(self, interpreter):
        super(UndefinedPrologInterpreterException, self).__init__()
        self.interpreter = interpreter
    
    def __repr__(self):
        return str(self.interpreter) + " is an undefined prolog interpreter"
    
    def __str__(self):
        return self.__repr__()
    


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
    


# global constant definitions

QSYSTEM_DIR = os.environ['QSYSTEM'] + os.sep

QSYSTEM_PREFIX = QSYSTEM_DIR.replace("\\", "/")

QSYSTEM_MODULES = {
    "PATOMS":    QSYSTEM_PREFIX + "patoms.py",
    "QPREP":     QSYSTEM_PREFIX + "qprep.py",
    "DATASTORE": QSYSTEM_PREFIX + "qsystem_data.pl",
    "QUERIES":   QSYSTEM_PREFIX + "general_queries.pl",
}

DEFINED_SOLVERS = {
    "smodels":"lparse",
    "dlv":"other",
    "clasp":"lparse",
}

DEFINED_INTERPRETERS = [
    "sic",
    "swi",
]

# utility functions

def wrap(text, lchar, rchar):
    """
    Returns the given text wrapped by the specified left and right characters.
    """
    return str(lchar) + text + str(rchar)


def create_atomic_string(text):
    """
    Returns a prolog atom created from the given text.
    """
    return wrap(text, "\'", "\'")


def parse_options():
    """
    Returns the options passed to the program. Options are parsed from sys.argv.
    """
    parser = optparse.OptionParser()
    parser.add_option("-p", "--prolog", dest = "prolog", default = "sic",
                      help = "specify the prolog interpreter to use (defaults to sicstus)")
    parser.add_option("-s", "--solver", dest = "solver", default = "dlv",
                      help = "specify the answer-set solver to use (defaults to dlv)")
    parser.add_option("-f", "--file", dest = "file",
                      help = "specify the name of the logic program to use as a knowledge base")
    (options, args) = parser.parse_args()
    return options


def is_microsoft_platform():
    """
    Returns True if the platform invoking the query system is a Microsoft Windows
    platform and False otherwise.
    """
    return sys.platform[:3] == "win"


def is_valid_solver(solver):
    """
    Returns True if solver is an answer set solver known by the query system,
    and False otherwise.
    """
    return DEFINED_SOLVERS.has_key(solver)


def is_lparse_based_command(command):
    """
    Returns True if options.command is an answer set solver that obtains its input from
    smodels and False otherwise.
    """
    return DEFINED_SOLVERS.has_key(command) and DEFINED_SOLVERS[command] == "lparse"


def is_defined_prolog_interpreter(interpreter):
    """
    Returns True if interpreter is a prolog interpreter known to the query system,
    and False otherwise.
    """
    return interpreter in DEFINED_INTERPRETERS


def generate_lparse_based_command(options):
    """
    Returns a command line which will invoke lparse on options.file and pass the resulting
    grounded program to options.solver.
    """
    return "lparse --true-negation " + options.file + " | " + options.solver


def generate_solver_command(options):
    """
    Returns the correct command line to invoke in order to compute the stable models
    of the logic program specified by options.file using the answer set solver specified
    by options.solver.
    """
    if not os.path.exists(options.file):
        raise QuerySystemRuntimeException("datastore generation")
    
    if not is_valid_solver(options.solver):
        raise UndefinedAnswerSetSolverException(options.solver)
    
    if is_lparse_based_command(options.solver):
        return generate_lparse_based_command(options)
    else:
        return options.solver + " " + options.file


def generate_call_to_qprep():
    """
    Returns the correct command to invoke qprep receiving input from stdin.
    """
    if is_microsoft_platform():
        return "python " + QSYSTEM_MODULES['QPREP']
    else:
        return QSYSTEM_MODULES['QPREP']


def generate_call_to_patoms(options):
    """
    Returns the correct command to invoke patoms with the specified solver.
    """
    command = QSYSTEM_MODULES['PATOMS'] + " --solver=" + str(options.solver)
    if is_microsoft_platform():
        return "python " + command
    else:
        return command


def generate_datastore(options):
    """
    Returns the correct command line to invoke in order to compute the stable models
    of the logic program specified by options.file using the answer set solver specified
    by options.solver, processing the resulting models to be used by the query system,
    and saving the results to the file defined by the constant DEFAULT_DATASTORE.
    """
    solver_command = generate_solver_command(options)
    command = solver_command + " | " + generate_call_to_patoms(options) + " | " + generate_call_to_qprep() + " > "  + QSYSTEM_MODULES['DATASTORE']
    os.system(command)


def files_to_consult(files):
    """
    Returns a string representation of the prolog command to consult all of the files
    in the given list of file names. The names of the files in the list are assumed to
    not contain any illegal characters and file extensions.
    """
    file_atoms = map(create_atomic_string, files)
    return wrap(",".join(file_atoms), "\"[", "].\"")


def generate_call_to_prolog(options):
    """
    Returns the correct command line to invoke in order to call the prolog system
    specified by options.prolog, loading the query module and datastore in the
    process. If options.prolog specifies an interpreter not known by the system,
    an exception of the type UndefinedPrologInterpreterException is raised.
    """
    if not is_defined_prolog_interpreter(options.prolog):
        raise UndefinedPrologInterpreterException(options.prolog)
    
    QSYSTEM_QUERY_FILES = [
        QSYSTEM_MODULES['DATASTORE'],
        QSYSTEM_MODULES['QUERIES'],
    ]
    
    files = files_to_consult(QSYSTEM_QUERY_FILES)
    
    if options.prolog == "sic":
        return "sicstus --goal " + files
    elif options.prolog == "swi":
        # SWI-Prolog uses different commands depending on whether or
        # not it is installed on a Microsoft platform or a Unix-based
        # platform
        if is_microsoft_platform():
            return "plcon -g " + files
        else:
            return "swipl -g " + files


def invoke_prolog(options):
    """
    Invokes the prolog interpreter specified by the given options. If the prolog
    interpreter is not known to the query system, an UndefinedPrologInterpreterException
    is raised. If the interpreter is valid but fails to launch and terminate correctly
    due to a runtime error and exception of the type QuerySystemRuntimeException is raised.
    """
    command = generate_call_to_prolog(options)
    os.system(command)


# main function

def main():
    """
    Main entry point into qsystem. Parses all of the command lines, and using the specified
    parameters generates the datastore and launches prolog automatically consulting the
    query modules.
    """
    try:
        options = parse_options()
        generate_datastore(options)
        invoke_prolog(options)
    except UndefinedAnswerSetSolverException, exception:
        print exception
    except UndefinedPrologInterpreterException, exception:
        print exception
    except QuerySystemRuntimeException, exception:
        print exception


if __name__ == "__main__":
    main()
