# STUDENT-QSYSTEM Readme #

This page contains basic installation and usage instructions for the student-qsystem program.

## Installation ##

The installation instructions already assume that the following are installed and are accessible from your path:
  * An answer set solver (currently clingo, dlv, and smodels are supported).
> > -- qsystem has been tested with:
> > > clingo v3.03 found at:
> > > > http://potassco.sourceforge.net/

> > > dlv release 2010-10-14 found at:
> > > > http://www.dlvsystem.com/dlvsystem/index.php/DLV#Download

> > > smodels found at:
> > > > http://www.tcs.hut.fi/Software/smodels/
> > > > .
  * A Python interpreter (version 2.5 and greater, the 3.X branch is currently unsupported).

  * A Prolog interpreter (two versions of qsystem, one for Sicstus Prolog and another SWI prolog).

> > -- currently the system has been tested with Sicstus v4.1.3 and SWI v5.10.x.

  * mkatoms found at
> > http://www.cs.ttu.edu/research/krlab/#software  --> mkatoms


Once the file code has been downloaded, extract the files to some directory on your path (normally somewhere in your home directory).

Next, create an environment variable `QSYSTEM` which points to this directory. On UNIX system (and on Mac OS X) if you are using the Bourne shell (bash) this can be done as by adding the following line to the file `.profile` in the root of my home directory (assuming that I extracted student-qsystem to the directory `$HOME/Scripts/qsystem`):
```
export QSYSTEM=$HOME/Scripts/qsystem
```

Lastly make sure that the files qsystem.py, qprep.py, and patoms.py are executable on your system. On Unix based systems this is done as follows:
```
bash$ chmod a+x qsystem.py
bash$ chmod a+x qprep.py
bash$ chmod a+x patoms.py
```

## Usage ##

student-qsystem is designed as a command-line application and may be run as follows:
```
python qsystem.py --solver=clingo --file=sample.lp
```

student-qsystem is defined with the following command-line options:
| `-h, --help` | _Show a help message and exit._ |
|:-------------|:--------------------------------|
| `--solver=SOLVER` | _Specify the answer-set solver to use (defaults to clingo). Currently the supported solvers are dlv, smodels, and clingo._ |
| `--file=FILE` | _Specify the name of the logic program to use as a knowledge base._ |

## Queries ##

Suppose that we have the following logic program `test1.lp`:
```
p | -p :- x.
x.
a :- x.
-b :- x.
my_atom(p).
my_atom(x).
my_atom(a).
my_atom(b).
```

To query this program we invoke student-qsystem using the default answer set solver Clingo (make sure that you are calling the system from the directory in which qsystem has been installed):

```
bash$ python qsystem.py --file=test.lp 
SICStus 4.1.3 (i386-darwin-9.8.0): Wed Sep 22 21:21:12 CEST 2010
Licensed to SP4ttu.edu
% compiling /Users/gregory/Documents/Projects/Query Answering/general_queries.pl...
%  compiling /Users/gregory/Documents/Projects/Query Answering/query_utilities.pl...
%   module query_utilities imported into user
%  compiled /Users/gregory/Documents/Projects/Query Answering/query_utilities.pl in module query_utilities, 0 msec 1024 bytes
% compiled /Users/gregory/Documents/Projects/Query Answering/general_queries.pl in module user, 10 msec 3688 bytes
% compiling /Users/gregory/Documents/Projects/Query Answering/qsystem_data.pl...
% compiled /Users/gregory/Documents/Projects/Query Answering/qsystem_data.pl in module user, 0 msec 256 bytes
% .....
| ?-
```

student-qsystem loads a number of related modules and brings the user to a standard Prolog prompt. At the prompt the user may ask any defined Prolog query. The remainder of this readme focuses solely on those queries defined by student-qsystem.

student-qsystem provides a single set of queries of the form `query(Term, Result)`, where
Term ranges over values given by statements of the form: my\_atom(Term) and
Result is either yes,no,or maybe.
To check whether or not the term `x` is positively entailed by our logic program, we use the following query:

```
| ?- query(x, yes).
yes
```

To check if `b` is negatively entailed we ask the following query:

```
| ?- query(b, no).
yes
```

As `p` is neither positively nor negatively entailed, the following query returns `unknown`:
```
| ?- query(p, X).
X = unknown
```

Furthermore, to find the set of all terms which are positively entailed by our logic program we use the following query:

```
| ?- query(X,yes).
 [a,x]
```

In short, `query(Term, Result)` is defined as follows:
  * If the term is positively entailed, `Result = yes`.
  * If the term is negatively entailed, `Result = no`.
  * If the term is neither positively nor negatively entailed, `Result = unknown`.
  * if the term is not defined by sort 'my\_atom', the result of the query is:
> > illegal\_query\_symbol: term is not of sort 'my\_atom'

  * If the input program does not have an answer set, all queries will result in the
> > message 'inconsistent program'.

As in all Prolog systems, the query need not be entered in ground form.

Lastly, to exit the system use the standard Prolog command `halt.`