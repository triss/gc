from copy import deepcopy
from random import choice, randrange
from expression_grower import grow_random_expression_tree
from program_components import Variable, Literal, Function
from expression import Expression


def mutate_expression(expression, rate, functions, variables):
    # create list of possible mutations
    WRAP, REPLACE, MUTATE_LITERAL, MUTATE_OP, PULL_OUT_OP, CHANGE_F = range(6)

    # expression's can always be wrapped or replaced
    possible_mutations = [WRAP, REPLACE]

    # what type of thing does this expression need to return after mutation
    desired_type = None

    # is this a literal, variable ref or bigger expression
    expression_type = type(expression.func)

    # work out what type of expression we're mutating and what sorts of
    # mutations are valid dependant on expression type
    if expression_type is Variable:
        desired_type = expression.func.typ

    elif expression_type is Literal:
        desired_type = expression.func.typ
        possible_mutations += [MUTATE_LITERAL]

    elif expression_type is Function:
        desired_type = expression.func.type_sig.return_type
        possible_mutations += [CHANGE_F, MUTATE_OP, PULL_OUT_OP]

    mutated_exp = deepcopy(expression)

    while mutated_exp == expression:
        # choose the mutation type
        chosen_mutation = choice(possible_mutations)

        if chosen_mutation == WRAP:
            # Find functions that take expression type we're wrapping as input
            # and retunr something of same type that wraps it
            def has_input_and_return_type(f):
                return (len(f.type_sig.input_types) > 0 and
                        f.type_sig.input_types[0] == desired_type and
                        f.type_sig.return_type == desired_type)

            function = choice(filter(has_input_and_return_type, functions))

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
            mutated_exp.mutate(rate)

        if chosen_mutation == MUTATE_OP:
            op_to_mutate = randrange(len(expression.operands))

            expression.operands[op_to_mutate] = mutate_expression(
                expression.operands[op_to_mutate], rate, functions, variables)

            mutated_exp = expression

        if chosen_mutation == PULL_OUT_OP:
            op_to_pull_out = randrange(len(expression.operands))

            mutated_exp = expression.operands[op_to_pull_out]

        if chosen_mutation == CHANGE_F:
            mutated_exp.func = choice(filter(
                lambda f: f.type_sig == expression.func.type_sig, functions))

    return mutated_exp
