from program_components import Function, TypeSignature
from gles_types import float_t, bool_t, vec2_t, vec3_t, vec4_t, bvec2_t, bvec3_t, bvec4_t


# list of known functions to call
functions = []

###############################################################################
# First off define all the builtin OpenGL-ES functions
###############################################################################

# all the different vector types
all_vec_types = [vec2_t, vec3_t, vec4_t]
all_bvec_types = [bvec2_t, bvec3_t, bvec4_t]

# length - takes vector gives float
for vec_type in all_vec_types:
    functions.append(Function('length', TypeSignature([vec_type], float_t)))

# create functions that turn pairs of vectors to floats
vec_to_float_funcs = "distance dot"

for vec_type in all_vec_types:
    # create appropriate type sig for functions
    type_sig = TypeSignature([vec_type] * 2, float_t)

    # add each function to funvtions list
    for name in vec_to_float_funcs.split():
        functions.append(Function(name, type_sig))


# functions that turn vectors to bvecs
vec_to_bvec_funcs = ('lessThan lessThanEqual greaterThan greaterThanEqual ' +
                     'equal notEqual')

# TODO what's the dealy-oh with these maybe iff needs forgiving?
# is it me or my understanding or gles?

# type signatures for functions that take two vectors size n and
# return a bvec of size n
vec_to_bvec_type_sigs = [TypeSignature([float_t] * 2, bool_t),
                         TypeSignature([vec2_t] * 2, bvec2_t),
                         TypeSignature([vec3_t] * 2, bvec3_t),
                         TypeSignature([vec4_t] * 2, bvec4_t)]

# just won't add them to functions list for now

# for type_sig in vec_to_bvec_type_sigs:
#     for name in vec_to_bvec_funcs.split():
#         functions.append(Function(name, type_sig))

# functions that take a bvec and return a bool
bvec_to_bool_funcs = 'any all'

bvec_to_bool_type_sigs = [TypeSignature([bvec2_t], bool_t),
                          TypeSignature([bvec3_t], bool_t),
                          TypeSignature([bvec4_t], bool_t)]

for type_sig in bvec_to_bool_type_sigs:
    for name in bvec_to_bool_funcs.split():
        functions.append(Function(name, type_sig))

# functions which take a bvec and return a bvec

# bvec_to_bvec = 'not' - don't bother with list
# since there is only one in GLES spec

bvec_to_bvec_type_sigs = [TypeSignature([bvec2_t], bvec2_t),
                          TypeSignature([bvec3_t], bvec3_t),
                          TypeSignature([bvec4_t], bvec4_t)]

for type_sig in bvec_to_bvec_type_sigs:
    functions.append(Function('not', type_sig))

# set up functions that can be applied to anything and return type
# they were given

# list of all vector types
types = [float_t, vec2_t, vec3_t, vec4_t]


def make_polymorphic_functions(names, num_operands=1):
    for t in types:
        type_sig = TypeSignature([t] * num_operands, t)

        for name in names.split():
            functions.append(Function(name, type_sig))


# polymorphic functions with a single operand
single_op_functions = ('radians degrees sin cos tan asin acos ' +
                       'usin ucos utan uasin uacos ' +
                       'exp log exp2 log2 sqrt abs sign ' +
                       'floor ceil fract normalize')

make_polymorphic_functions(single_op_functions)

# polymorphic functions with two operands
two_op_functions = 'add sub div mul atan pow mod min max step'
make_polymorphic_functions(two_op_functions, 2)

# polymorphic functions with three operands
three_op_functions = 'clamp mix smoothstep'
make_polymorphic_functions(three_op_functions, 3)


###############################################################################
# self defined functions
# defined in boiler plate
###############################################################################

# these functions translate between boolean and float types
float_types = [float_t, vec2_t, vec3_t, vec4_t]
bool_types = [bool_t, bvec2_t, bvec3_t, bvec4_t]

conversions = zip(float_types, bool_types)

functions += map(lambda t: Function(
    'ftob', TypeSignature([t[0]], t[1])), conversions)

functions += map(lambda t: Function(
    'btof', TypeSignature([t[1]], t[0])), conversions)

# standard boolean funtions - and, xor, or
functions += map(lambda t: Function('and', TypeSignature([t, t], t)), bool_types)
functions += map(lambda t: Function( 'or', TypeSignature([t, t], t)), bool_types)
functions += map(lambda t: Function('xor', TypeSignature([t, t], t)), bool_types)

# weird boolean functions that convert floats to bools and then return a float
# when true anda, andb, ora, xora etc.
functions += map(lambda t: Function('anda', TypeSignature([t, t], t)), float_types)
functions += map(lambda t: Function('xora', TypeSignature([t, t], t)), float_types)
functions += map(lambda t: Function( 'ora', TypeSignature([t, t], t)), float_types)
functions += map(lambda t: Function('andb', TypeSignature([t, t], t)), float_types)
functions += map(lambda t: Function('xorb', TypeSignature([t, t], t)), float_types)
functions += map(lambda t: Function( 'orb', TypeSignature([t, t], t)), float_types)

# TODO wtf is with iff?
# functions += map(lambda t: Function('iff', TypeSignature([t[1], t[0], t[0]], t[0])), conversions)

# Sims had these
functions += [Function('rgb2hsv', TypeSignature([vec3_t], vec3_t)),
              Function('hsv2rgb', TypeSignature([vec3_t], vec3_t)),
              Function('getVideoColour', TypeSignature([vec2_t], vec4_t)),
              Function('getVideoColour', TypeSignature([float_t, float_t], vec4_t))]
