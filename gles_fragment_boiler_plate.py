header = """
#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_TEXLIGHT_SHADER

uniform sampler2D video;
uniform float time;

varying vec4 vertColor;
varying vec4 vertTexCoord;

// basic operands for addition, subtraction,
// multiplication and division
float add(float a, float b) { return a + b; }
float sub(float a, float b) { return a - b; }
float div(float a, float b) { return a / b; }
float mul(float a, float b) { return a * b; }

vec2 add(vec2 a, float b) { return a + b; }
vec2 sub(vec2 a, float b) { return a - b; }
vec2 div(vec2 a, float b) { return a / b; }
vec2 mul(vec2 a, float b) { return a * b; }

vec2 add(vec2 a, vec2 b) { return a + b; }
vec2 sub(vec2 a, vec2 b) { return a - b; }
vec2 div(vec2 a, vec2 b) { return a / b; }
vec2 mul(vec2 a, vec2 b) { return a * b; }

vec3 add(vec3 a, float b) { return a + b; }
vec3 sub(vec3 a, float b) { return a - b; }
vec3 div(vec3 a, float b) { return a / b; }
vec3 mul(vec3 a, float b) { return a * b; }

vec3 add(vec3 a, vec3 b) { return a + b; }
vec3 sub(vec3 a, vec3 b) { return a - b; }
vec3 div(vec3 a, vec3 b) { return a / b; }
vec3 mul(vec3 a, vec3 b) { return a * b; }

vec4 add(vec4 a, float b) { return a + b; }
vec4 sub(vec4 a, float b) { return a - b; }
vec4 div(vec4 a, float b) { return a / b; }
vec4 mul(vec4 a, float b) { return a * b; }

vec4 add(vec4 a, vec4 b) { return a + b; }
vec4 sub(vec4 a, vec4 b) { return a - b; }
vec4 div(vec4 a, vec4 b) { return a / b; }
vec4 mul(vec4 a, vec4 b) { return a * b; }

// convert from bools to floats and back again
float btof(bool b) { return b ? 1.0 : 0.0; }
vec2 btof(bvec2 b) { return vec2(btof(b.x), btof(b.y)); }
vec3 btof(bvec3 b) { return vec3(btof(b.x), btof(b.y), btof(b.z)); }
vec4 btof(bvec4 b) { return vec4(btof(b.x), btof(b.y), btof(b.z), btof(b.w)); }

bool ftob(float f) { return f > 0.5; }
bvec2 ftob(vec2 f) { return bvec2(ftob(f.x), ftob(f.y)); }
bvec3 ftob(vec3 f) { return bvec3(ftob(f.x), ftob(f.y), ftob(f.z)); }
bvec4 ftob(vec4 f) { return bvec4(ftob(f.x), ftob(f.y), ftob(f.z), ftob(f.w)); }

// boolean functions
bool and(bool a, bool b) { return a && b; }
bool or (bool a, bool b) { return a || b; }
bool xor(bool a, bool b) { return a ^^ b; }
bvec2 and(bvec2 a, bvec2 b) { return bvec2(a.x && b.x, a.y && b.y); }
bvec2 or (bvec2 a, bvec2 b) { return bvec2(a.x || b.x, a.y || b.y); }
bvec2 xor(bvec2 a, bvec2 b) { return bvec2(a.x ^^ b.x, a.y ^^ b.y); }
bvec3 and(bvec3 a, bvec3 b) { return bvec3(a.x && b.x, a.y && b.y, a.z && b.z); }
bvec3 or (bvec3 a, bvec3 b) { return bvec3(a.x || b.x, a.y || b.y, a.z || b.z); }
bvec3 xor(bvec3 a, bvec3 b) { return bvec3(a.x ^^ b.x, a.y ^^ b.y, a.z ^^ b.z); }
bvec4 and(bvec4 a, bvec4 b) { return bvec4(a.x && b.x, a.y && b.y, a.z && b.z, a.w && b.w); }
bvec4 or (bvec4 a, bvec4 b) { return bvec4(a.x || b.x, a.y || b.y, a.z || b.z, a.w || b.w); }
bvec4 xor(bvec4 a, bvec4 b) { return bvec4(a.x ^^ b.x, a.y ^^ b.y, a.z ^^ b.z, a.w ^^ b.w); }

// weird pseudo boolean functions that return one of there inputs
// written since dissapearance in to boolean calculation land can be
// a little unfruitful
float anda(float a, float b) { return ftob(a) && ftob(b) ? a : 0.; }
float andb(float a, float b) { return ftob(a) && ftob(b) ? b : 0.; }
float ora (float a, float b) { return ftob(a) || ftob(b) ? a : 0.; }
float orb (float a, float b) { return ftob(a) || ftob(b) ? b : 0.; }
float xora(float a, float b) { return ftob(a) ^^ ftob(b) ? a : 0.; }
float xorb(float a, float b) { return ftob(a) ^^ ftob(b) ? b : 0.; }

vec2 anda(vec2 a, vec2 b) { return all(and(ftob(a), ftob(b))) ? a : vec2(0.); }
vec2 andb(vec2 a, vec2 b) { return all(and(ftob(a), ftob(b))) ? b : vec2(0.); }
vec2 ora (vec2 a, vec2 b) { return all(or (ftob(a), ftob(b))) ? a : vec2(0.); }
vec2 orb (vec2 a, vec2 b) { return all(or (ftob(a), ftob(b))) ? b : vec2(0.); }
vec2 xora(vec2 a, vec2 b) { return all(xor(ftob(a), ftob(b))) ? a : vec2(0.); }
vec2 xorb(vec2 a, vec2 b) { return all(xor(ftob(a), ftob(b))) ? b : vec2(0.); }

vec3 anda(vec3 a, vec3 b) { return all(and(ftob(a), ftob(b))) ? a : vec3(0.); }
vec3 andb(vec3 a, vec3 b) { return all(and(ftob(a), ftob(b))) ? b : vec3(0.); }
vec3 ora (vec3 a, vec3 b) { return all(or (ftob(a), ftob(b))) ? a : vec3(0.); }
vec3 orb (vec3 a, vec3 b) { return all(or (ftob(a), ftob(b))) ? b : vec3(0.); }
vec3 xora(vec3 a, vec3 b) { return all(xor(ftob(a), ftob(b))) ? a : vec3(0.); }
vec3 xorb(vec3 a, vec3 b) { return all(xor(ftob(a), ftob(b))) ? b : vec3(0.); }

vec4 anda(vec4 a, vec4 b) { return all(and(ftob(a), ftob(b))) ? a : vec4(0.); }
vec4 andb(vec4 a, vec4 b) { return all(and(ftob(a), ftob(b))) ? b : vec4(0.); }
vec4 ora (vec4 a, vec4 b) { return all(or (ftob(a), ftob(b))) ? a : vec4(0.); }
vec4 orb (vec4 a, vec4 b) { return all(or (ftob(a), ftob(b))) ? b : vec4(0.); }
vec4 xora(vec4 a, vec4 b) { return all(xor(ftob(a), ftob(b))) ? a : vec4(0.); }
vec4 xorb(vec4 a, vec4 b) { return all(xor(ftob(a), ftob(b))) ? b : vec4(0.); }

// float -> bool greater than less than etc
bool lessThan(float a, float b)         { return a < b; }
bool lessThanEqual(float a, float b)    { return a <= b; }
bool greaterThan(float a, float b)      { return a > b; }
bool greaterThanEqual(float a, float b) { return a >= b; }
bool equal(float a, float b)            { return a == b; }
bool notEqual(float a, float b)         { return a != b; }

// if, then, else
float iff(bool b, float then, float els) { return b ? then : els; }
vec2 iff(bvec2 b, vec2 then, vec2 els) {
    return vec2(b.x ? then.x : els.x, b.y ? then.y : els.y); }
vec3 iff(bvec3 b, vec3 then, vec3 els) {
    return vec3(b.x ? then.x : els.x, b.y ? then.y : els.y, b.z ? then.z : els.z); }
vec4 iff(bvec4 b, vec4 then, vec4 els) {
    return vec4(b.x ? then.x : els.x, b.y ? then.y : els.y, b.z ? then.z : els.z, b.w ? then.w : els.w); }

// unipolar versions of bipolar functions
float usin(float f) { return sin(f) * 0.5 + 0.5; }
float ucos(float f) { return cos(f) * 0.5 + 0.5; }
float utan(float f) { return tan(f) * 0.5 + 0.5; }
float uasin(float f) { return asin(f) * 0.5 + 0.5; }
float uacos(float f) { return acos(f) * 0.5 + 0.5; }
float uatan(float f) { return atan(f) * 0.5 + 0.5; }
vec2 usin (vec2 f) { return sin(f) * 0.5 + 0.5; }
vec2 ucos (vec2 f) { return cos(f) * 0.5 + 0.5; }
vec2 utan (vec2 f) { return tan(f) * 0.5 + 0.5; }
vec2 uasin(vec2 f) { return asin(f) * 0.5 + 0.5; }
vec2 uacos(vec2 f) { return acos(f) * 0.5 + 0.5; }
vec2 uatan(vec2 f) { return atan(f) * 0.5 + 0.5; }
vec3 usin (vec3 f) { return sin(f) * 0.5 + 0.5; }
vec3 ucos (vec3 f) { return cos(f) * 0.5 + 0.5; }
vec3 utan (vec3 f) { return tan(f) * 0.5 + 0.5; }
vec3 uasin(vec3 f) { return asin(f) * 0.5 + 0.5; }
vec3 uacos(vec3 f) { return acos(f) * 0.5 + 0.5; }
vec3 uatan(vec3 f) { return atan(f) * 0.5 + 0.5; }
vec4 usin (vec4 f) { return sin(f) * 0.5 + 0.5; }
vec4 ucos (vec4 f) { return cos(f) * 0.5 + 0.5; }
vec4 utan (vec4 f) { return tan(f) * 0.5 + 0.5; }
vec4 uasin(vec4 f) { return asin(f) * 0.5 + 0.5; }
vec4 uacos(vec4 f) { return acos(f) * 0.5 + 0.5; }
vec4 uatan(vec4 f) { return atan(f) * 0.5 + 0.5; }

vec3 rgb2hsv(vec3 c) {
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));

    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

vec4 getVideoColour(vec2 xy) { return texture2D(video, fract(xy)); }
vec4 getVideoColour(float x, float y) { return texture2D(video, fract(vec2(x, y))); }

void main() {
    vec4 videoColour = getVideoColour(vertTexCoord.st);

    vec3 rgb = """

footer = """;

    gl_FragColor = vec4(fract(rgb), 1.0);
}"""
