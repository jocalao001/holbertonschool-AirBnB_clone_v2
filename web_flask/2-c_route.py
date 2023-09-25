#!/usr/bin/python3
"""script that starts a Flask web application
routes: / and /hbnb"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """This method displays 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """This method displays 'HBNB'"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """This method recieves a text and parses
    it if a '_' char is present"""
    parsed_text = text.replace('_', ' ')
    format_to_display = f"C {parsed_text}"
    return format_to_display


if __name__ == "__main__":
    app.run(host="0.0.0.0")
