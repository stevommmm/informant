Informant
=========

Modular, self documenting API server using Python


Informant is a very basic WSGI server that allows for quick API protyping and processing, with minimal setup required and an extremely basic


Modular routing
===============

Every instance of Engine is a singleton, registering to the same shared route list. To implement modules at a basic level all Informant requires is an instance of `Engine` and a route registration decorator as shown below

	app = Engine()
	@app.register(StringRoute('test'))
	class IndexRoute(object):
		def do_GET(self, request):
			return {'status': 'working'}
	app.run()
