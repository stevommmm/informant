Informant
=========

Modular, self documenting API server using Python


Informant is a very basic WSGI server that allows for quick API protyping and processing, with minimal setup required and an extremely basic


Modular routing
---------------

Every instance of Engine is a singleton, registering to the same shared route list. To implement modules at a basic level all Informant requires is an instance of `Engine` and a route registration decorator as shown below

	app = Engine()
	@app.register(StringRoute('test'))
	class IndexRoute(object):
		def do_GET(self, request):
			return {'status': 'working'}
	app.run()

Routing Benchmarks
------------------

Each routing method has a different performance characteristic, the below tests base their results off the `modules/test.py` file where StringRoute and RegexRoute are tested

*Server configuration*

	gunicorn -w 4 main:app


*Siege test for StringRoute*

	smcgregor@smcgregor-kitn:~/Documents/informant$ siege -c100 -t1m http://localhost:8000/api/v1/test
		** SIEGE 3.0.5
		** Preparing 100 concurrent users for battle.
		The server is now under siege...
		Lifting the server siege...      done.

		Transactions:                  12027 hits
		Availability:                 100.00 %
		Elapsed time:                  59.98 secs
		Data transferred:               0.30 MB
		Response time:                  0.00 secs
		Transaction rate:             200.52 trans/sec
		Throughput:                     0.00 MB/sec
		Concurrency:                    0.63
		Successful transactions:       12027
		Failed transactions:               0
		Longest transaction:            0.05
		Shortest transaction:           0.00


*Siege test for RegexRoute*

	$ siege -c100 -t1m http://localhost:8000/api/v1/testregex
		** SIEGE 3.0.5
		** Preparing 100 concurrent users for battle.
		The server is now under siege...
		Lifting the server siege...      done.

		Transactions:                  11793 hits
		Availability:                 100.00 %
		Elapsed time:                  59.47 secs
		Data transferred:               0.28 MB
		Response time:                  0.00 secs
		Transaction rate:             198.30 trans/sec
		Throughput:                     0.00 MB/sec
		Concurrency:                    0.59
		Successful transactions:       11793
		Failed transactions:               0
		Longest transaction:            0.06
		Shortest transaction:           0.00
