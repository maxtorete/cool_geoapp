from flask import Flask
from flask_caching import Cache
from flask_jwt_extended import JWTManager

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

app = Flask(__name__)
cache.init_app(app)

app.config['JWT_SECRET_KEY'] = '5^h2%Vk8B^v#ix7k4AmyYs6'
jwt = JWTManager(app)

# Circular Imports
# Every Python programmer hates them, and yet we just added some: circular imports
# (That’s when two modules depend on each other. In this case views.py depends on __init__.py).
# Be advised that this is a bad idea in general but here it is actually fine.
# The reason for this is that we are not actually using the views in __init__.py and just ensuring the module is
# imported and we are doing that at the bottom of the file.
#
# There are still some problems with that approach but if you want to use decorators there is no way around that.
# Check out the Becoming Big section for some inspiration how to deal with that.
# From: https://flask.palletsprojects.com/en/2.1.x/patterns/packages/

import resource.PostalCodeResource
import resource.PaystatMonthlyReportResource
import resource.TokenResource
