from aima.core.logic.common import AndTerm, NotTerm, OrTerm, TokenTypes, SymbolTerm
from aima.core.logic.propositional.parsing import PLParser, PLLexer
from aima.core.logic.propositional.visitors import SymbolsCollector, Model, CNFTransformer, CNFClauseGatherer, CNFOrGatherer

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

def create_symbols_connection(connector_ctor, symbols, none_value):
     l = len(symbols)
     if l == 0:
        return none_value
     elif l == 1:
        return symbols[0]
     else:
        right_connector = connector_ctor(symbols[l - 2], symbols[l - 1])

        lst = list(range(l - 2))
        lst.reverse()
        for i in lst:
            right_connector = connector_ctor(symbols[i], right_connector)

        return right_connector

class KnowledgeBase:
    """
    Knowledge base that stores information in propositional logic
    """
    def __init__(self):
        self.sentences = []
        self.parser = PLParser()

    def tell_str(self, str):
        """
        Add new statement in to knowledge base

        :param str (str): Propositional logic expression
        :return: None
        """
        sentence = self.parser.parse(str)
        self.tell(sentence)

    def tell(self, term):
        """
        Add new statement to knowledge base

        :param term (Term): Root term of propositional logic expression
        :return: None
        """
        self.sentences.append(term)

    def tell_all_str(self, strs):
        """
        Add several statements to knowledge base

        :param strs (iterable(str)): Experssions to add to knowledge base
        :return: None
        """
        for str in strs:
            self.tell_str(str)

    def tell_all(self, terms):
        """
        Add all expressions to knowledge base

        :param terms (iterable(Term)): root terms of expressions that should be added to knowledge base
        :return: None
        """
        for term in terms:
            self.tell(term)

    def size(self):
        """
        Get number of statements in knowledge base

        :return (int): number of expressions in knowledge base
        """
        return len(self.sentences)

    def as_sentence(self):
        """
        Get all statements connected by AND operator as a single sentence. For example if there are expressions "A", "B",
        "NOT C", this will return A AND B AND (NOT C)

        :return (Term): root term of connected statements if any statements added to the knowledge base, None otherwise
        """

        return create_symbols_connection(AndTerm, self.sentences, None)

# function TT-Entails?(KB, alpha) returns true or false
#   inputs: KB, the knowledge base, a sentence in propositional logic
#           alpha, the query, a sentence in propositional logic
#
#   symbols <- a list of proposition symbols in KB and alpha
#   return TT-Check-All(KB, alpha, symbols, [])
#
# function TT-Check-All(KB, symbols, model) returns true or false
#   if Empty?(symbols) then
#       if PL-True?(KB, model) then return PL-True?(alpha, model)
#       else return true
#   else
#       P <- First(symbols); rest <- Rest(symbols)
#       return TT-Check-All(KB, alpha, rest, Extend(P, true, model) and
#              TT-Check-All(KB, alpha, rest, Extend(P, false, model)

class TTEntails:
    # function TT-Entails?(KB, alpha) returns true or false
    def tt_entails(self, knowledge_base, alpha):
        kb_sentence = knowledge_base.as_sentence()
        query_sentence = PLParser().parse(alpha)

        collector = SymbolsCollector()
        kb_symbols = collector.collect_symbols(kb_sentence)
        query_symbols = collector.collect_symbols(query_sentence)

        # symbols <- a list of proposition symbols in KB and alpha
        symbols_list = list(kb_symbols.union(query_symbols))
        # return TT-Check-All(KB, alpha, symbols, [])
        return self.tt_check_all(kb_sentence, query_sentence, symbols_list, Model())

    # function TT-Check-All(KB, symbols, model) returns true or false
    def tt_check_all(self, kb_sentence, query_sentence, symbols_list, model):
        # if Empty?(symbols) then
        if len(symbols_list) == 0:
            # if PL-True?(KB, model) then return PL-True?(alpha, model)
            if model.is_true(kb_sentence):
                return model.is_true(query_sentence)
            # else return true
            else:
                return True
        else:
            # P <- First(symbols); rest <- Rest(symbols)
            copy_list = list(symbols_list)
            symbol = copy_list.pop()

            true_model = model.extend(symbol, True)
            false_model = model.extend(symbol, False)

            # return TT-Check-All(KB, alpha, rest, Extend(P, true, model) and
            # TT-Check-All(KB, alpha, rest, Extend(P, false, model)
            return self.tt_check_all(kb_sentence, query_sentence, copy_list, true_model) and \
                   self.tt_check_all(kb_sentence, query_sentence, copy_list, false_model)

class EmptyClause:
    def __eq__(self, other):
        return isinstance(other, EmptyClause)

    def __hash__(self):
        # Just a prime number
        return 3163

# function PL-Resolution(KB, alpha) returns true or false
#   inputs: KB, the knowledge base, a sentence in propositional logic
#           alpha, the query, a sentence in propositional logic
#
#   clauses = <- the set of clauses in the CNF representation of KB AND (NOT alpha)
#   new <- {}
#   loop do
#     for each Ci, Cj in clauses do
#       resolvents <- PL-Resolve(Ci, Cj)
#       if resolvents contains the empty clause then return true
#       new <- new U resolvents
#     if new is subset of clauses then return false
#     clauses <- clauses U new
class PLResolution:
    # function PL-Resolution(KB, alpha) returns true or false
    #   inputs: KB, the knowledge base, a sentence in propositional logic
    #           alpha, the query, a sentence in propositional logic
    def pl_resolution(self, knowledge_base, alpha):
        resolution_sentence = self._create_resolution_sentence(knowledge_base, alpha)
        cnf_resolution_sentence = CNFTransformer().transform(resolution_sentence)

        # clauses = <- the set of clauses in the CNF representation of KB AND (NOT alpha)
        clauses = CNFClauseGatherer().collect(cnf_resolution_sentence)

        # loop do
        while True:
            # new <- {}
            new = set()
            # for each Ci, Cj in clauses do
            for ci in clauses:
                for cj in clauses:
                    if ci != cj:
                        # resolvents <- PL-Resolve(Ci, Cj)
                        resolvent = self._pl_resolve(ci, cj)
                        # if resolvents contains the empty clause then return true
                        if EmptyClause() == resolvent:
                            return True
                        # new <- new U resolvents
                        new.add(resolvent)
            # if new is subset of clauses then return false
            if new.issubset(clauses):
                return False
            # clauses <- clauses U new
            clauses = new | clauses

    def _create_resolution_sentence(self, knowledge_base, alpha):
        kb_sentence = knowledge_base.as_sentence()
        return AndTerm(kb_sentence, NotTerm(alpha))

    def _pl_resolve(self, ci, cj):
        or_gatherer = CNFOrGatherer()
        (ci_symbols, ci_not_symbols) = or_gatherer.collect(ci)
        (cj_symbols, cj_not_symbols) = or_gatherer.collect(cj)

        symbols = cj_symbols | ci_symbols
        not_symbols = cj_not_symbols | ci_not_symbols

        unique_symbols = symbols - not_symbols
        unique_not_symbols = not_symbols - symbols

        not_symbols_set = {NotTerm(not_symbol) for not_symbol in unique_not_symbols}

        return create_symbols_connection(OrTerm, list(unique_symbols | not_symbols_set), EmptyClause())

# function PL-FC-Entails?(KB, q) returns true or false
#   inputs: KB, the knowledge base, a set of propositional Horn clauses
#           q, the query, a propositional symbol
#   local variables: count, a table, indexed by clause, initially the number or premises
#                    inferred, a table, indexed by symbol, each entry initially false
#                    agenda, a list of symbols, initially the symbols known to be true in KB
#
#   while agenda is not empty do
#     p <- Pop(agenda)
#     unless inferred[p] do
#       inferred[p] <- true
#       for each Horn clause c in whose premise p appears do
#         decrement count[c]
#         if count[c] = 0 then do
#           if Head[c] = q then return true
#           Push(Head[c], agenda)
#   return false
class PLFCEntails:
    class HornClause:
        def __init__(self, root_term):
            self.head = None
            self.premise_symbols = None

            if root_term.type == TokenTypes.IDENTIFIER:
                self.head = root_term
                self.premise_symbols = []
            elif root_term.type != TokenTypes.IMPLICATION:
                raise ValueError("Sentence " + str(root_term) + " isn't a horn clause")
            else:
                self.head = root_term.children[1]

                collector = SymbolsCollector()
                premise_expression = root_term.children[0]
                self.premise_symbols = [SymbolTerm(name) for name in collector.collect_symbols(premise_expression)]

        def __eq__(self, other):
            if not isinstance(other, HornClause):
                return False

            if self.head != other.head:
                return False

            if len(self.premise_symbols) != len(other.premise_symbols):
                return False

            for i in range(len(self.premise_symbols)):
                if self.premise_symbols[i] != other.premise_symbols[i]:
                    return False

            return True

        def __hash__(self):
            h = 17
            for symbol in  self.premise_symbols:
                h ^= hash(symbol)
            h ^= hash(self.head)

            return h

        def __str__(self):
            result = self.head.name

            l = len(self.premise_symbols)

            if l != 0:
                result = " => " + result

                for i in range(l):
                    result = self.premise_symbols[i].name + result
                    if i != l - 1:
                        result = " AND " + result


            return result

    def __init__(self):
        self.count = {}
        self.infered = {}
        self.agenda = []


    # function PL-FC-Entails?(KB, q) returns true or false
    #   inputs: KB, the knowledge base, a set of propositional Horn clauses
    def plfc_entails(self, knowledge_base, question):
        horn_clauses = self._as_horn_clauses(knowledge_base.sentences)

        # while agenda is not empty do
        while len(self.agenda) > 0:
            # p <- Pop(agenda)
            p = self.agenda.pop()

            # unless inferred[p] do
            if not self.infered[p]:
                # inferred[p] <- true
                self.infered[p] = True

                # for each Horn clause c in whose premise p appears do
                for horn_clause in horn_clauses:
                    if p in horn_clause.premise_symbols:
                        # decrement count[c]
                        self.count[horn_clause.head] -= 1

                        # if count[c] = 0 then do
                        if self.count[horn_clause.head] == 0:
                            # if Head[c] = q then return true
                            if horn_clause.head == question:
                                return True
                            # Push(Head[c], agenda)
                            self.agenda.append(horn_clause.head)
        # return false
        return False

    def _as_horn_clauses(self, sentences):
        horn_clauses = [self.HornClause(sentence) for sentence in sentences]

        for horn_clause in horn_clauses:
            self.infered[horn_clause.head] = False

            if len(horn_clause.premise_symbols) == 0:
                self.count[horn_clause.head] = 0
                self.agenda.append(horn_clause.head)

            for symbol in horn_clause.premise_symbols:
                self.infered[symbol] = False

            self.count[horn_clause.head] = len(horn_clause.premise_symbols)

        return horn_clauses






