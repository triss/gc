from expression import Expression

def grow_random_expression(
        variables, functions, var_rate=0.75, scaler_range=1, max_depth=10):

    """Grows a random expression tree and returns it.

    Keyword arguments:
    variables       -- variables available for growing expressions
    functions       -- variables available for growing expressions

    var_rate        -- probability of using var instead of scaler in exp
    scaler_range    -- the max number for our scaler
    max_depth       -- maximum depth of our tree"""

    num_operands = 0

    # if tree is not too deep already randomly choose number of operands
    if max_depth > 0:
        num_operands = randrange(len(functions) + 1)

    # if num operands is 0
    if num_operands == 0:
        # choose wether to input a random scaler or a variable definition
        if random() > var_rate and num_operands > 1:
            # or a random scaler
            function = random() * scaler_range
        else:
            # choose a variable
            function = choice(list(variables))

    else:
        # otherwise choose a function
        function = choice(list(functions[num_operands - 1]))

    # populate expressions operands
    operands = []
    for i in range(num_operands):
        # create expressions for each operand
        operands.append(
            grow_random_expression(
                variables, functions, var_rate, scaler_range, max_depth - 1))

    return Expression(function, *operands)

