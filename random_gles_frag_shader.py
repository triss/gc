from gles_functions import functions
from gles_variables import variables
from gles_types import vec3_t
from gles_fragment_boiler_plate import header, footer

from expression_grower import grow_random_expression_tree
from expression_mutator import mutate_expression

def make_random_gles_frag_shader():
    e = grow_random_expression_tree(functions, variables, vec3_t, 10)
    return header + e.pretty_print() + footer


e = grow_random_expression_tree(functions, variables, vec3_t, 10)
type(e)
e.pretty_print()


for i in range(20):
    print mutate_expression(e, 0.1, functions, variables).pretty_print()

