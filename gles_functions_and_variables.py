# operators with one operand
unary_funcs = set([
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
    'unisin', 'unicos', 'unitan', 'uniasin', 'uniacos', 'uniatan',
    'exp', 'log', 'exp2', 'log2', 'sqrt',
    'abs', 'sign', 'floor', 'ceil', 'fract', 'fnot'])

# list of binary operators
binary_funcs = set([
    'add', 'sub', 'mul', 'div', 'pow',
    'mod', 'min', 'max', 'step',
    'gt', 'lt',
    'gta', 'lta', 'gtb', 'gtb',
    'and', 'or', 'xor',
    'anda', 'ora', 'xora', 'andb', 'orb', 'xorb'])

# operators with 3 params
ternary_funcs = set(['clamp', 'mix', 'smoothstep', 'iff'])

# variables
variables = set(['uv.x', 'uv.y', 'iGlobalTime'])

# list of all funcs ordered by number of operands
functions = [unary_funcs, binary_funcs, ternary_funcs]
