#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.city import City
from models.state import State

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def task9():
    return render_template(
        "8-cities_by_states.html", data1=storage.all(State),
        data2=storage.all(City)
    )


@app.teardown_appcontext
def close(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
