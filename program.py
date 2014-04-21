from random import choice, randrange

from assignment import Assignment
from expression_grower import grow_random_expression

class Program(object):
    def __init__(self, functions, variables):
        # initially np assignments made
        self.assignments = []

        # list of possible functions and variables
        # that can be used in expressions
        self.functions = functions
        self.variables = variables

    def add_assignment(self, name, expression):
        """Add an assigmnet statement to our program"""

        # add to our list of assignments
        self.assignments.append(Assignment(name, expression))

        # add to our list of possible variables when for building an
        # expression tree
        self.variables.add(name)

    def remove_assignment(self, index):
        """Remove's an assignment from our program and no sub-expressions
        rely on it but randomly replacing refernces to it with references to
        other variables."""

        # store var name used in assignment so we can check expression trees
        # are still valid
        var_name = self.assignments[index].variable

        # delete this particular assignment
        del self.assignments[index]

        # confirm that this variable still has value assigned
        still_assigned = False
        for a in self.assignments:
            still_assigned = a.variable == var_name
            if still_assigned:
                break

        # if this variable is no longer assigned a value
        if not still_assigned:
            # remove variable from list of definitions
            self.variables.discard(var_name)

            # randomly replace references to variable with references to other
            # variables
            for a in self.assignments:
                a.expression.replace_all_calls_to(
                    var_name, choice(list(self.variables)))

    def add_random_assigment(self):
        # we'll use single char var names for our random assigments
        var_name = chr(randrange(26) + 97)

        self.add_assignment(var_name, grow_random_expression())
