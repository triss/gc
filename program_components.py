from random import choice


class Type(object):
    """Everything has a type in our expression tree's/programs.

    Instances of type represent the different types our programmer
    knows about."""

    def __init__(self, name, rand_literal_func, mutate_literal_func):
        self.name = name
        self.rand_literal_func = rand_literal_func
        self.mutate_literal_func = mutate_literal_func

    def __eq__(self, other):
        return self is other or self.name == other.name

    def random_literal(self):
        return Literal(self, self.rand_literal_func())

    def mutate_literal(self, literal, rate):
        return self.mutate_literal_func(literal, rate)

    def pretty_print_literal(self, literal):
        # handle strings and floats differently
        to_str = type(literal.values[0]) is str and str or repr

        # return 'name(values[0], values[1], ...)'
        return self.name + '(' + ', '.join(map(to_str, literal.values)) + ')'

    def pretty_print_variable_def(self, variable):
        # TODO need to make this easier to override/define/pass in
        return self.name + ' ' + variable.name


class Variable(object):
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ

    def __eq__(self, other):
        return self is other or self.name == other.name

    def pretty_print(self):
        return self.name



class Assignment(object):
    """Our programs contain assignments"""
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def mutate(self, rate):
        self.expression.mutate(rate)

    def __eq__(self, other):
        return (self is other or
                (self.variable == other.variable and
                 self.expression == self.expression))

    def pretty_print(self):
        return self.variable.name + " = " + self.expression.pretty_print()


class Literal(object):
    """Written under the assumption Array Literals are pretty much the same as
    normal Literals. Safe for most things... Fine for GLSL shaders."""

    def __init__(self, typ, values):
        self.values = values
        self.typ = typ

    def __eq__(self, other):
        return self is other or self.values == other.values

    def mutate(self, rate=0.1):
        turn_up_or_down_by_rate = lambda x: x * choice([1 + rate, 1 - rate])

        self.values = map(turn_up_or_down_by_rate, self.values)

    def pretty_print(self):
        return self.typ.pretty_print_literal(self)


class Function(object):
    def __init__(self, name, type_sig, definition=None):
        """Creates a function

        name        - a string that is the functions name
        type_def    - the type definition for the function"""

        self.name = name
        self.type_sig = type_sig

    def __eq__(self, other):
        return ((self is other) or
                (self.name == other.name and
                 self.type_def == other.type_def))

    def pretty_print(self):
        return self.name


class TypeSignature(object):
    def __init__(self, input_types, return_type):
        """Creates a type definition for a function.

        input_types - the types of input for this type definition
        return_type - the type returned by this function"""

        self.input_types = input_types
        self.return_type = return_type
        self.num_inputs = len(input_types)

    def __eq__(self, other):
        return ((self is other) or
                (self.input_types == other.input_types and
                 self.return_type == other.return_type))
