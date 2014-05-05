from random import choice, random
from expression import Expression


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
