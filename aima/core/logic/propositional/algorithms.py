from aima.core.logic.common import AndTerm
from aima.core.logic.propositional.parsing import PLParser, PLLexer
from aima.core.logic.propositional.visitors import SymbolsCollector, Model

__author__ = 'Ivan Mushketik'
__docformat__ = 'restructuredtext en'

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
        sentence = self.parser.parse(PLLexer(str))
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
        l = len(self.sentences)
        if l == 0:
            return None
        elif l == 1:
            return self.sentences[0]
        else:
            right_and = AndTerm(self.sentences[l - 2], self.sentences[l - 1])

            lst = list(range(l - 2))
            lst.reverse()
            for i in lst:
                right_and = AndTerm(self.sentences[i], right_and)

            return right_and

# function TT-Entails?(KB, alpha) returns true or false
#   inputs: KB, the knowledge base, a sentence in propositional logic
#           alpha, the query, a sentence in propositional logic
#
#   symbols <- a list of proposition symbols in KB and alpha
#   return TT-Check-All(KB, alpha, sumbols, [])
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
        query_sentence = PLParser().parse(PLLexer(alpha))

        collector = SymbolsCollector()
        kb_symbols = collector.collect_symbols(kb_sentence)
        query_symbols = collector.collect_symbols(query_sentence)

        # symbols <- a list of proposition symbols in KB and alpha
        symbols_list = list(kb_symbols.union(query_symbols))
        # return TT-Check-All(KB, alpha, sumbols, [])
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

            trueModel = model.extend(symbol, True)
            falseModel = model.extend(symbol, False)

            # return TT-Check-All(KB, alpha, rest, Extend(P, true, model) and
            # TT-Check-All(KB, alpha, rest, Extend(P, false, model)
            return self.tt_check_all(kb_sentence, query_sentence, copy_list, trueModel) and \
                   self.tt_check_all(kb_sentence, query_sentence, copy_list, falseModel)


