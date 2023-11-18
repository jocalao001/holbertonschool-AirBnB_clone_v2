#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def task10b():
    return render_template(
        "10-hbnb_filters.html",
        data1=storage.all(State),
        data2=storage.all(City),
        data3=storage.all(Amenity),
    )


@app.teardown_appcontext
def close(exception=None):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
