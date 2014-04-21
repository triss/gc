from copy import deepcopy
from random import random, randrange, choice
from expression_grower import grow_random_expression


class Expression():
    def __init__(self, func, *operands):
        self.func = func

        # ensures an object is an Expression
        def to_expression(obj):
            if isinstance(obj, Expression):
                return obj
            else:
                return Expression(obj)

        # ensure all operands are expressions
        self.operands = map(to_expression, operands)

    def mutate(
            self, probability, variables, functions, max_depth=3, depth=0):

        """
        Mutates an expression with a probability of mutation_rate, whilst
        limiting depth of the tree to max_depth.

        depth is not typically user specified and is used as a to track how
        deep down the tree we've gone.
        """

        # combine variables and functions in to operators list to ease random
        # selection and align index of num operands with resultant list
        operators = list(variables) + functions

        # keep attempting mutations until at least one change has been made
        prev_self = deepcopy(self)
        while prev_self == self:
            # if we're going to mutate this expression
            if random() < probability:
                # choose the new number of operands for expression
                new_num_operands = randrange(4)

                # choose a new operator for expression
                self.func = choice(operators[new_num_operands])

                # delete operands if required
                while len(self.operands) > new_num_operands:
                    self.operands.pop()

                # recurse over remaining operands
                for o in self.operands:
                    o.mutate(
                        probability, variables, functions,
                        max_depth, depth + 1)

                # add more operands if required - done post operator mutation
                # since no need to mutate a new expression
                while len(self.operands) < new_num_operands:
                    self.operands.append(
                        grow_random_expression(
                            variables, functions, 0.75, 1,
                            max_depth - depth))

    def replace_all_calls_to(self, search_func, repl_func):
        """Replaces all calls to search_func with calls to repl_func"""

        # if this expression is call to search_func
        if self.func == search_func:
            # replace it
            self.func = repl_func

        # recurse over operands
        for o in self.operands:
            o.replace_all_calls_to(search_func, repl_func)

    def to_c_expression(self):
        """'Pretty prints' expression trees in C type format"""

        # if expresions function is not a string turn it in to one
        if type(self.func) is not str:
            c_expression = repr(self.func)
        else:
            c_expression = self.func

        # wrap operands in brackets and descend expression tree
        if len(self.operands) > 0:
            c_expression += '('

            # deal with first op on its own since it's not preceeded
            # by a comma
            c_expression += self.operands[0].to_c_expression()

            # append comma's and other operands to our string
            for o in self.operands[1:]:
                c_expression += ', ' + o.to_c_expression()

            # add a closing bracket
            c_expression += ')'

        return c_expression

    def __eq__(self, other):
        """Return's wether this expression is equal to the other expression"""
        # convert to string and test equality! - hacky but it works
        return self.to_c_expression() == other.to_c_expression()
