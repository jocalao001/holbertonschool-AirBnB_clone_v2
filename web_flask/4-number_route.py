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

# https://juncotic.com/manejo-de-rutas-en-flask/


@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def py_route(text="is cool"):
    """This method recieves a text and parses
    it if a '_' char is present also the default
    value of the text is 'is cool'"""
    parsed_text = text.replace('_', ' ')
    format_to_display = f"Python {parsed_text}"
    return format_to_display

# https://stackoverflow.com/questions/14350920/
# how to handle integers in route Flask


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """This method will display n is a number
    only if n is an integer"""
    parsed_number = n
    format_to_display = f"{parsed_number} is a number"
    return format_to_display


if __name__ == "__main__":
    app.run(host="0.0.0.0")
