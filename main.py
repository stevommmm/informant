#!/usr/bin/env python

from informant import engine

# Import all our modules from /getters/
from modules import *

# Get a new instance of our application framework
app = engine()

if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8000)