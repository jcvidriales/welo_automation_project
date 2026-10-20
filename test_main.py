from unittest.mock import MagicMock

from main import ai_classify_genre, classify_duration, classify_type


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


def test_ai_genre_cleans_response():
    fake_client = MagicMock()
    fake_client.responses.create.return_value.output_text = "Action."
    result = ai_classify_genre("A hero fights villains in a big city.", fake_client)
    assert result == "Action"


def test_ai_genre_not_in_list_returns_unknown():
    fake_client = MagicMock()
    fake_client.responses.create.return_value.output_text = "Sci-Fi"
    result = ai_classify_genre("Astronauts explore a distant planet.", fake_client)
    assert result == "Unknown"


def test_ai_error_returns_unknown():
    fake_client = MagicMock()
    fake_client.responses.create.side_effect = Exception("No internet")
    result = ai_classify_genre("A group of friends goes on a road trip.", fake_client)
    assert result == "Unknown"