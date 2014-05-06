from random import random, choice

from program_components import Type

# the following two functions define how to generate random instances
# of a type

# a random floating point between low and high
random_float = lambda: random()


# factory for generating functions that return random vectors between low
# and high
def random_vec_fact(num_scalers):
    return lambda: map(lambda x: random_float(), range(num_scalers))


def mutate_floats(values, rate):
    turn_up_or_down_by_rate = lambda x: x * choice([1 + rate, 1 - rate])

    values = map(turn_up_or_down_by_rate, values)

    return values

# actual type definitions
float_t = Type('float', random_vec_fact(1), mutate_floats)
vec2_t = Type('vec2', random_vec_fact(2), mutate_floats)
vec3_t = Type('vec3', random_vec_fact(3), mutate_floats)
vec4_t = Type('vec4', random_vec_fact(4), mutate_floats)


# TODO Would be neater to allow description of possible values for types!
# rather than this messy low high being ignored thing going on below for
# booleans

# a random choice between true and false
random_bool = lambda: choice(['true', 'false'])


# factory for generating functions that return random vectors between low
# and high
def random_bvec_fact(num_bools):
    return lambda: map(lambda x: random_bool(), range(num_bools))

# boolean types
bool_t = Type('bool', random_bvec_fact(1), random_bvec_fact(1))
bvec2_t = Type('bvec2', random_bvec_fact(2), random_bvec_fact(2))
bvec3_t = Type('bvec3', random_bvec_fact(3), random_bvec_fact(3))
bvec4_t = Type('bvec4', random_bvec_fact(4), random_bvec_fact(4))

# handy list of all types
types = [float_t, vec2_t, vec3_t, vec4_t, bool_t, bvec2_t, bvec3_t, bvec4_t]
