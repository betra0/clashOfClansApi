import os
import requests
from flask import Flask, request, jsonify
from config import Config
from flask_cors import CORS

from routes import RaizBlueprint

class CustomFlask(Flask):
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        options.setdefault('strict_slashes', False)
        super().add_url_rule(rule, endpoint, view_func, **options)

app = CustomFlask(__name__)
CORS(app, supports_credentials=True)


app.register_blueprint(RaizBlueprint, url_prefix='/')



    


if __name__ == '__main__':
    app.run(debug=True, port=5000)