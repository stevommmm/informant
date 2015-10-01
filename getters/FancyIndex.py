
import json
from collections import OrderedDict
from informant import engine, __author__, __description__, __version__

app = engine()

@app.route('^/$')
class WebIndexRoute(object):
	def get_class_routes(self, cl):
		"""Iterate over a classes defined methods and return any starting with do_"""
		for key in cl.__class__.__dict__.keys():
			if key.startswith('do_'):
				yield key[3:]

	def iterroutes(self):
		routes = {}
		for route in app.routes.items():
			routes[route[0].pattern] = {
				'handler': route[1].__class__.__name__,
				'methods': list(self.get_class_routes(route[1])),
			}
		return routes


	def do_GET(self, request):
		return pretty_html_print(OrderedDict([
			('__project__', 'Informant'),
			('__description__', __description__),
			('__author__', __author__),
			('__version__', __version__),
			('routes', self.iterroutes()),
		]))


def pretty_html_print(rawdict):
	try:
		from pygments import highlight
		from pygments.lexers import JsonLexer
		from pygments.formatters import HtmlFormatter

		formatter = HtmlFormatter(full=True) #noclasses=True, 
		return highlight(json.dumps(rawdict, indent=4), JsonLexer(), formatter)
	except ImportError:
		return '<pre>' + json.dumps(rawdict, indent=4) + "</pre>"