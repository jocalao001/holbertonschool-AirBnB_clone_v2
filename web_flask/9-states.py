#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.city import City
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def task10a():
    return render_template("9-states.html",
                           data1=storage.all(State),
                           data3=None)


@app.route("/states/<id>", strict_slashes=False)
def task10b(id):
    return render_template("9-states.html",
                           data1=storage.all(State),
                           data2=storage.all(City),
                           data3=id)


@app.teardown_appcontext
def close(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
