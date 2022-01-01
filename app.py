from flask import Flask, render_template, request, jsonify
from utils import *
import json

app = Flask(__name__)

@app.route("/movie/<title>")
def search_for_movie(title):
    result = get_movie_by_title(title)
    return jsonify(result)


@app.route("/movie/<int:year>")
def search_by_year(year):
    result = get_movie_list_between_dates(year-1, year)
    return jsonify(result)


@app.route("/rating/<rating>")
def search_by_rating(rating):
    result = get_movies_by_rating(rating)
    return jsonify(result)



if __name__ == "__main__":
    app.run()

