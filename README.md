Open
====



Modular routing
===============

An example module called `example.py` would be mounted under the `/api/example/` namespace.
The following code example would register a url handler for `/api/example/test`.

	@app.route('^/$')
	class IndexRoute(object):
		def do_GET(self, request):
			return '<h1>Working!</h1>'
