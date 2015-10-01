from informant import Engine, StringRoute, RegexRoute

app = Engine()

@app.register(StringRoute('/test'))
class TestHandler(object):
	def do_GET(self, request):
		"""API endpoint example route"""
		return {'status': 'String Match'}

@app.register(RegexRoute('test\w+'))
class TestHandler(object):
	def do_GET(self, request):
		"""API endpoint example route"""
		return {'status': 'Regex Match'}


@app.register('test2')
class TestHandler(object):
	def do_GET(self, request):
		"""API endpoint example route"""
		return {'status': 'Presumed String Match'}