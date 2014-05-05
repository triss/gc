from copy import deepcopy
from random import random, randrange, choice
from program_components import Variable, Literal, Function


class Expression:
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
        """Return's wether this expression is equal to the other expression"""
        # convert to string and test equality!
        return self.pretty_print() == other.pretty_print()

    def __deepcopy__(self, memo_dict):
        return Expression(self.func, *deepcopy(self.operands))

    def mutate(self, rate, functions, variables, depth=1, max_depth=10):
        # keep track of whether mutation has occured yet
        # exp_before = deepcopy(self)

        # loop around until something has actually mutated
        # while exp_before == self:
            # mutate this expression node?
            if random() < rate:
                # choose a mutation type
                CHANGE_FUNC, REPLACE_OP, WRAP_OP, UNWRAP_OP = range(0, 4)
                mutation = choice([REPLACE_OP, WRAP_OP, UNWRAP_OP])

                if mutation == REPLACE_OP:
                    # choose an operand and generate new expression to
                    # replace it with
                    chosen_op = randrange(len(self.operands))

                    if type(self.operands[chosen_op]) is Function:
                        return_type = self.operands[chosen_op].type_sig.return_type

                    else:
                        return_type = self.operands[chosen_op].typ

                    self.operands[chosen_op] = grow_random_expression_tree(
                        functions, variables,
                        return_type,
                        max_depth - depth)

                elif mutation == WRAP_OP:
                    # choose an operator to wrap
                    chosen_op = randrange(len(self.operands))

                    # store away the expression being wrapped as an operand
                    # for new expression
                    new_ops = [self.operands[chosen_op]]

                    # choose a new function with a first input type thats the
                    # same as what the expressins we're wrapping has
                    func = choice([f for f in functions
                                if self.func.type_sig.input_types[0]
                                == f.type_sig.return_type])

                    # randomly generate any extra required operands
                    for t in self.func.type_sig.input_types[1:]:
                        new_ops += [grow_random_expression_tree(
                            functions, variables, t, max_depth - depth)]

                    # embed the new expression in the tree
                    self.operands[chosen_op] = Expression(func, *new_ops)

                elif mutation == UNWRAP_OP:
                    # choose an operator to wrap
                    op_to_unwrap = self.operands[randrange(len(self.operands))]

                    if type(op_to_unwrap) is Expression:
                        self.function = op_to_unwrap.func
                        self.operands = op_to_unwrap.operands

            elif len(self.operands) > 0:
                # if we aren't mutating expression at this level wizz
                # down through operands and possibly mutate them
                for o in self.operands:
                    o.mutate(rate, functions, variables, depth+1)

            else:
                if type(self.func) is Function:
                    # replace this expression's function with
                    # function with same sig
                    self.func = choice([f for f in functions
                                        if self.func.type_sig
                                        == f.type_sig])

                elif type(self.func) is Variable:
                    self.func = choice([v for v in variables
                                        if self.func.typ == v.typ])

                elif type(self.func) is Literal:
                    self.func.mutate(rate)


def grow_random_expression_tree(
        functions, variables, return_type=None, max_depth=10,
        exp_prob=0.75, var_prob=0.95, depth=0):

    """Returns a randomly generated expression tree that utilizes the
    functions and variables passed in to it. It filter's these functions
    and variables by return type if possible

    functions   - the functions we can make our expression from
    variables   - the variable we can make our expression from
    return_type - the required return type for the expression"""

    # filter down variables and functions to those useful when building
    # expressions of this type
    poss_funcs = filter(
        lambda f: f.type_sig.return_type == return_type, functions)
    poss_vars = filter(
        lambda v: v.typ == return_type, variables)

    # if we aren't too deep choose between making a  function call,
    # referencing a variable or putting in a literal
    if random() < exp_prob and depth < max_depth:
        # choose a random function
        function = choice(poss_funcs)

        operands = []

        # populate operands
        for input_type in function.type_sig.input_types:
            operands.append(
                grow_random_expression_tree(
                    functions, variables, input_type,
                    max_depth, exp_prob, var_prob, depth + 1))

        return Expression(function, *operands)

    else:
        if random() < var_prob and len(poss_vars) > 1:
            # choose a random variable
            function = choice(poss_vars)

            # don't repeat this variable in this function call - arbitrary
            # semantic decision
            poss_vars.remove(function)
        else:
            # otherwise create a random literal
            function = return_type.random_literal()

        # return the expression
        return Expression(function)


def mutate_expression(expression, rate, functions, variables):
    # create list of possible mutations
    WRAP, REPLACE, MUTATE_LITERAL, MUTATE_OP, PULL_OUT_OP, CHANGE_F = range(6)
    possible_mutations = [WRAP, REPLACE]

    # what type of thing does this expression need to return after mutation
    desired_type = None

    # is this a literal, variable ref or bigger expression
    expression_type = type(expression)

    # work out what type of expression we're mutating and what sorts of
    # mutations are valid dependant on expression type
    if expression_type == Variable:
        desired_type = expression.typ

    elif expression_type == Literal:
        desired_type = expression.typ
        possible_mutations += [MUTATE_LITERAL]

    elif expression_type == Expression:
        desired_type = expression.type_sig.return_type
        possible_mutations += [CHANGE_F, MUTATE_OP, PULL_OUT_OP]

    while mutated_exp == expression:
        # choose the mutation type
        chosen_mutation = choice(possible_mutations)

        if chosen_mutation == WRAP:
            # Find functions that take expression type we're wrapping as input
            # and retunr something of same type that wraps it
            def func_has_input_and_return_type(f):
                return (len(f.type_sig.input_types) > 0 and
                        f.type_sig.input_types[0] == desired_type and
                        f.type_sig.return_type == desired_type)

            function = choice(filter(func_has_input_and_return_type, functions))

            operands = [expression]

            for input_type in function.type_sig.input_types[1:]:
                operands.append(
                    grow_random_expression_tree(
                        functions, variables, input_type, 3))

            mutated_exp = Expression(function, *operands)

        if chosen_mutation == REPLACE:
            mutated_exp = grow_random_expression_tree(
                        functions, variables, desired_type, 3)

        if chosen_mutation == MUTATE_LITERAL:
            mutated_exp = deepcopy(expression)
            mutated_exp.mutate(rate)

        if chosen_mutation == MUTATE_OP:
            mutated_exp = deepcopy(expression)

            op_to_mutate = randrange(len(expression.operands))

            expression.operands[op_to_mutate] = mutate_expression(
                expression.operands[op_to_mutate], rate, functions, variables)

            mutated_exp = expression

        if chosen_mutation == PULL_OUT_OP:
            op_to_pull_out = randrange(len(expression.operands))

            mutated_exp = expression.operands[op_to_pull_out]

        if chosen_mutation == CHANGE_F:
            mutated_exp = deepcopy(expression)
            mutated_exp.func = choice(filter(
                lambda f: f.type_sig == expression.type_sig, functions))

    return mutated_exp
