import cherrypy
import simplejson
import os
from random_gles_frag_shader import make_random_gles_frag_shader

breeding_pool = []
populations = []

# strange organisms
# stops breeding once enough of its children get killed


def generate_children():
    pass

class GLShaderServer:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def set_population_fitness(self):
        input_json = cherrypy.request.json

        population_id = input_json['population_id']

        print population_id

        return input_json

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def get_population(self):
        input_json = cherrypy.request.json

        if 'population_id' in input_json:
            population_id = input_json['population_id']
        else:
            population_id = None

        # get population with id or newest population

        return { 'test': 10 }

    @cherrypy.expose
    def get_random_frag_shader(self):
        return make_random_gles_frag_shader()


conf = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(os.getcwd(), 'ui/html')}}


cherrypy.quickstart(GLShaderServer(), '/', config=conf)
