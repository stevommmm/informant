import cgi
import json
import logging
import re
import urlparse
logging.basicConfig(format='%(process)-6d %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

__author__ = 'Stephen McGregor <s.mcgregor@griffith.edu.au>'
__description__ = """Modular, self documenting API server using Python"""
__version__ = '0.0.31'
__license__ = 'MIT'

def filter_by_list(fdict, flist):
	def inner(key):
		return key[0] in flist
	return dict(filter(inner, fdict.items()))

class __Route(object):
	def __init__(self, path, version="v1", notAPI=False):
		if notAPI:
			self.path = path
		else:
			self.path = '/' + '/'.join(['api', version, path.lstrip('/')])

	def __eq__(self, *args):
		return False

class StringRoute(__Route):
	def __eq__(self, wsgi_path):
		return self.path == wsgi_path

class RegexRoute(__Route):
	def __init__(self, path, **kwargs):
		super(RegexRoute, self).__init__(path, **kwargs)
		self.path = "^" + self.path
		self.regex = re.compile(self.path)

	def __eq__(self, wsgi_path):
		return self.regex.match(wsgi_path)

class Request(object):
	def __init__(self, environ):
		self.headers = {'content-type': 'text/html'}
		self.status = '200 OK'
		self.method = environ['REQUEST_METHOD']
		self._ENV = environ
		self._GET = self.__split_get()
		self._POST = self.__split_post()

	def set_status(self, status):
		self.status = status

	def set_header(self, header, value):
		self.headers.update({header: value})

	def __split_get(self):
		return urlparse.parse_qs(self._ENV.get('QUERY_STRING', ''), keep_blank_values=True)

	def __split_post(self):
		safe_env = filter_by_list(self._ENV, ['CONTENT_LENGTH', 'CONTENT_TYPE', 'REQUEST_METHOD'])
		return cgi.FieldStorage(fp=self._ENV['wsgi.input'], environ=safe_env, keep_blank_values=1)

class Engine(object):
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Engine, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		if not hasattr(self, 'routes'):
			self.routes = []

	def register(self, path_handler, handler=None):
		'''Route decorator, @application_instance.route('^regex$')'''

		def wrapper(handler):
			func_handler = path_handler

			if isinstance(path_handler, str):
				func_handler = StringRoute(path_handler)

			logger.info("Registered route %s to %s", func_handler.path, handler.__name__)
			
			if isinstance(func_handler, RegexRoute): # We want more specific string routes before globbing regex
				self.routes.append((func_handler, handler()))
			else:
				self.routes.insert(0, (func_handler, handler()))
		return wrapper

	def wsgi(self, environ, start_response):
		'''WSGI compliant callable, only ever called from __call__'''

		path = environ['PATH_INFO']
	
		for path_handler in self.routes:
			if path_handler[0] == path:
				try:
					handler = path_handler[1]
					req = Request(environ)

					if hasattr(handler, 'do_' + req.method):
						func_output = getattr(handler, 'do_' + req.method)(req)
					else:
						start_response('405 Method Not Allowed', [('content-type', 'text/html')])
						return (repr(req.method) + ' Method Not Allowed',)

					if type(func_output) == dict:
						func_output = json.dumps(func_output)
						req.set_header('content-type', 'application/json')
					elif type(func_output) == list:
						func_output = ''.join(func_output)
					elif type(func_output) == unicode:
						func_output = func_output.encode('utf8')

					start_response(req.status, req.headers.items())
					return func_output
				except Exception as e:
					import traceback
					logger.error("%s\t%s", e, traceback.format_exc())
					start_response('500 Internal Server Error', [('content-type', 'text/plain')])
					return "An incident has been recorded:\n" + repr(e)

		start_response('404 Not Found', [('content-type', 'text/html')])
		return ('Not Found',)

	def __call__(self, environ, start_response):
		return self.wsgi(environ, start_response)

	def run(self, host="0.0.0.0", port=8000):
		'''Run this instance of engine using simple_server'''
		from wsgiref.simple_server import make_server
		srv = make_server(host, port, self)
		try:
			srv.serve_forever()
		except KeyboardInterrupt:
			print "Got CTRL + C. Sent shutdown to server."


if __name__ == '__main__':
	app = Engine()
	@app.register(StringRoute('/'))
	class IndexRoute(object):
		def do_GET(self, request):
			return '<h1>Working!</h1>'
	app.run()