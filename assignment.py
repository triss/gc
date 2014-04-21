class Assignment(object):
    def __init__(self, variable_name, expression):
        self.variable = variable_name
        self.expression = expression

    def to_c_expression(self):
        return self.variable + " = " + self.expression.to_c_expression() + ";\n"
