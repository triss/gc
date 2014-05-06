from program_components import Variable
from itertools import permutations
from gles_types import float_t, vec2_t, vec3_t, vec4_t


vec4_var_names = ['vertColor', 'vertTexCoord', 'videoColour']

variables = map(lambda v: Variable(v, vec4_t), vec4_var_names)


def add_suffixs(v, typ, num_components):
    return map(lambda suffix: Variable(v + '.' + suffix, typ),
               map(lambda permutation: "".join(permutation),
                   permutations(['x', 'y', 'z'], num_components)))

vec_types = [float_t, vec2_t, vec3_t, vec4_t]

for v in vec4_var_names:
    for i, vt in enumerate(vec_types):
        variables += add_suffixs(v, vt, i + 1)

variables += [Variable('time', float_t)]
