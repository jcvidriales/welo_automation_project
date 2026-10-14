from main import classify_duration, classify_type


def test_short_movie():
    movie = {"duration_minutes": "81", "type": "Movie"}
    assert classify_duration(movie) == "Short"


def test_long_movie():
    movie = {"duration_minutes": "152", "type": "Movie"}
    assert classify_duration(movie) == "Long"


def test_medium_tv_show():
    show = {"duration_minutes": "50", "type": "TV Show"}
    assert classify_duration(show) == "Medium"


def test_type_is_case_insensitive():
    movie = {"type": " MOVIE "}
    assert classify_type(movie) == "Movie"


def test_unknown_type():
    item = {"type": "Documentary"}
    assert classify_type(item) == "Other"