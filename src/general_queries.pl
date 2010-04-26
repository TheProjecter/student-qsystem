% =============================================================================
% Copyright (c) 2010, Gregory Gelfond <logicprogrammer@gmail.com>
% All rights reserved.
%
% Redistribution and use in source and binary forms, with or without
% modification, are permitted provided that the following conditions are met:
%     * Redistributions of source code must retain the above copyright
%       notice, this list of conditions and the following disclaimer.
%     * Redistributions in binary form must reproduce the above copyright
%       notice, this list of conditions and the following disclaimer in the
%       documentation and/or other materials provided with the distribution.
%     * Neither the name of the <organization> nor the
%       names of its contributors may be used to endorse or promote products
%       derived from this software without specific prior written permission.
%
% THIS SOFTWARE IS PROVIDED BY GREGORY GELFOND ``AS IS'' AND ANY
% EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
% WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
% DISCLAIMED. IN NO EVENT SHALL GREGORY GELFOND BE LIABLE FOR ANY
% DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
% (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
% LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
% ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
% (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
% SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
% =============================================================================

:- use_module(query_utilities).

% positively_entailed(Term)
% True if Term is positively entailed by the logic program and false
% otherwise.

positively_entailed(Term) :-
    query(Term, yes).

% negatively_entailed(Term)
% True if Term is negatively entailed by the logic program and false
% otherwise.

negatively_entailed(Term) :-
    query(Term, no).

% query(Term, Reply):
% Reply = yes if Term is true in all answer sets passed to the program,
% no if Term is false in all answer sets passed to the program, and
% maybe otherwise.

query(Term, yes) :-
    true_in_all_models(Term).

query(Term, no) :-
    false_in_all_models(Term).

query(Term, maybe) :-
    true_in_model(Term, X),
    false_in_model(Term, Y),
    X =\= Y.

% true_in_all_models(Term)
% True if Term is true in all models and false otherwise.

true_in_all_models(Term) :-
    number_of_models(N),
    Max is N - 1,
    list_expansion(Max, Models),
    true_in_all_models(Term, Models).

% true_in_all_models(Term, ModelList)
% An auxiliary predicate for true_in_all_models/1. True if Term is
% true in all of the models specified by the given list and false
% otherwise.

true_in_all_models(_, []).

true_in_all_models(Term, [Model | Models]) :-
    pos(Model, Term),
    true_in_all_models(Term, Models).

% true_in_model(Term, Model)
% True if the given Term is denoted to be true in the given Model.

true_in_model(Term, Model) :-
    pos(Model, Term).

% false_in_all_models(Term)
% True if Term is false in all models and false otherwise.

false_in_all_models(Term) :-
    number_of_models(N),
    Max is N - 1,
    list_expansion(Max, Models),
    false_in_all_models(Term, Models).

% false_in_all_models(Term, ModelList)
% An auxiliary predicate for false_in_all_models/1. True if Term is
% false in all of the models specified by the given list and false
% otherwise.

false_in_all_models(_, []).

false_in_all_models(Term, [Model | Models]) :-
    neg(Model, Term),
    false_in_all_models(Term, Models).

% false_in_model(Term, Model)
% True if the given Term is denoted to be false in the given Model.

false_in_model(Term, Model) :-
    neg(Model, Term).