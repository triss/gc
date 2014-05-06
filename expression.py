from copy import deepcopy


class Expression(object):
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

    def pretty_print(self):
        """'Pretty prints' expression trees in C type format"""

        # if expresions function is not a string turn it in to one
        c_expression = self.func.pretty_print()

        # wrap operands in brackets and descend expression tree
        if len(self.operands) > 0:
            c_expression += '('

            # deal with first op on its own since it's not preceeded
            # by a comma
            c_expression += self.operands[0].pretty_print()

            # append comma's and other operands to our string
            for o in self.operands[1:]:
                c_expression += ', ' + o.pretty_print()

            # add a closing bracket
            c_expression += ')'

        return c_expression

    def __eq__(self, other):
        # convert to string and test equality!
        return self.pretty_print() == other.pretty_print()

    def __deepcopy__(self, memo_dict):
        return Expression(self.func, *deepcopy(self.operands))
