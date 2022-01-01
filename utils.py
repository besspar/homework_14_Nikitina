import sqlite3
DB_PATH = "netflix.db"

def get_movie_by_title(title):

    connection = sqlite3.connect(DB_PATH)

    sqlite_query = f"""
                   SELECT title, country, release_year, listed_in, description
                   FROM netflix
                   WHERE "title" = '{title}'
                   ORDER BY "release_year"
                   LIMIT 1
                   """

    cursor = connection.cursor()
    cursor.execute(sqlite_query)
    data_raw = cursor.fetchone()

    data = {
        "title": data_raw[0],
        "country": data_raw[1],
        "release_year": data_raw[2],
        "genre": data_raw[3],
        "description": data_raw[4]
    }

    return str(data)


def get_movie_list_between_dates(year1, year2):
    connection = sqlite3.connect(DB_PATH)

    sqlite_query = f"""
                   SELECT title, release_year
                   FROM netflix
                   WHERE release_year BETWEEN {year1} AND {year2}
                   LIMIT 100
                   """
    cursor = connection.cursor()
    cursor.execute(sqlite_query)
    data_raw = cursor.fetchall()

    movie_list = []
    for item in data_raw:
        movie = {"title": item[0], "release_year": item[1]}
        movie_list.append(str(movie))

    return movie_list


def get_movies_by_rating(age):
    connection = sqlite3.connect(DB_PATH)


    if age == "children":
            sqlite_query = f"""
                               SELECT title, rating, description
                               FROM netflix
                               WHERE rating IN ('G') AND rating IS NOT NULL
                               LIMIT 100
                               """
    elif age == "family":
        sqlite_query = f"""
                                       SELECT title, rating, description
                                       FROM netflix
                                       WHERE rating IN ('G', 'PG', 'PG-13') AND rating IS NOT NULL
                                       LIMIT 100
                                       """

    elif age == "adult":
        sqlite_query = f"""
                                       SELECT title, rating, description
                                       FROM netflix
                                       WHERE rating IN ('R', 'NC-17') AND rating IS NOT NULL
                                       LIMIT 100
                                       """
    cursor = connection.cursor()
    cursor.execute(sqlite_query)
    data_raw = cursor.fetchall()

    movie_list = []
    for item in data_raw:
        movie = {"title": item[0], "rating": item[1], "description": item[2]}
        movie_list.append(str(movie))

    return movie_list

def get_10_movies_by_genre(genre):
    connection = sqlite3.connect(DB_PATH)
    sqlite_query = f"""
                       SELECT title, description
                       FROM netflix
                       WHERE listed_in LIKE '%{genre}%'
                       ORDER BY "release_year" ASC
                       LIMIT 10
                       """
    cursor = connection.cursor()
    cursor.execute(sqlite_query)
    data_raw = cursor.fetchall()

    movie_list = []
    for item in data_raw:
        movie = {"title": item[0], "description": item[1]}
        movie_list.append(movie)

    return movie_list

def get_special_cast(artist1, artist2):
    connection = sqlite3.connect(DB_PATH)
    sqlite_query = f"""
                           SELECT "cast"
                           FROM netflix
                           WHERE "cast" LIKE '%{artist1}%'
                           AND "cast" LIKE '%{artist2}%'
                           """
    cursor = connection.cursor()
    cursor.execute(sqlite_query)
    data_raw = cursor.fetchall()

    cast_list = []
    for item in data_raw:
        current_name_list = list(item)
        current_name_list = current_name_list[0].split(', ')
        for name in current_name_list:
            if name not in cast_list and name != artist1 and name != artist2:
                cast_list.append(name)

    result_cast = []
    for name in cast_list:
        count = 0
        for item in data_raw:
            current_list = list(item)
            current_list = current_list[0].split(', ')
            if name in current_list:
                 count += 1
        if count > 2:
            result_cast.append(name)

    return result_cast


def get_movies_by_query(type, release_year, genre):
    connection = sqlite3.connect(DB_PATH)
    sqlite_query = f"""
                           SELECT title, description
                           FROM netflix
                           WHERE type = '{type}'
                           AND release_year = '{release_year}'
                           AND listed_in LIKE '%{genre}%'
                           """
    cursor = connection.cursor()
    cursor.execute(sqlite_query)
    data_raw = cursor.fetchall()

    matched_pictures = []
    for item in data_raw:
        movie = {"title": item[0], "description": item[1]}
        matched_pictures.append(movie)
    return matched_pictures

print(get_movie_by_title("1994"))
print(get_movie_list_between_dates(1994, 1995))
print(get_movies_by_rating("adult"))
print(get_10_movies_by_genre('comedy'))
print(get_special_cast('Jack Black', 'Dustin Hoffman'))
print(get_movies_by_query("TV Show", '2020', 'comedy'))

