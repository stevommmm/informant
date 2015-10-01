from informant import engine
import json

app = engine()

@app.route('^/test$')
class TestHandler(object):
	def do_GET(self, request):
		"""API endpoint example route"""
		request.headers = [('content-type', 'application/json')]
		return json.dumps({
			'status': 'okay',
		})
