from dotenv import load_dotenv
import os
from openai import OpenAI
import csv
load_dotenv()
ALLOWED_GENRES = [
    "Action",
    "Comedy",
    "Drama",
    "Horror",
    "Romance",
    "Animation",
    "Superhero",
    "Supernatural",
]

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("No se encontró la API key")
    exit()
client = OpenAI(api_key=api_key)
def classify_duration(movie):
    duration = int(movie["duration_minutes"])

    if duration < 90:
        return "Short"

    elif duration <= 120:
        return "Medium"

    else:
        return "Long"
         
def classify_type(movie):
    content_type = movie["type"].strip().lower()
    
    if content_type == "movie":
        return "Movie"
    elif content_type == "tv show":
        return "TV Show"
    else:
        return "Other"

def classify_movie(movie):
    return {
        "title": movie["title"],
        "genre": "",
        "duration_category": classify_duration(movie),
        "type": classify_type(movie)
    }

def ai_classify_genre(description):
    if not description or len(description.strip()) < 10:
        return "Unknown"
    try:
            genre_options = ", ".join(ALLOWED_GENRES)
            response = client.responses.create(
            model="gpt-5",
            input=f"""
    Classify the genre of this movie or TV show.
    Choose the genre from this list: {genre_options}.
    Description:
    {description}

    Return only one genre.
    """
        )

            genre = response.output_text.strip().rstrip(".").title()
            allowed_genres = ALLOWED_GENRES
            genre = genre.replace('"', "").replace("'", "")
            if genre not in allowed_genres:
                return "Unknown"
            return genre
    except Exception as e:
        print("AI classification failed:", e)
        return "Unknown"
def main():
    movies = []
    try:

        with open("input_movies.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required_fields = {"title", "description", "duration_minutes", "type"}
            if not required_fields.issubset(reader.fieldnames or []):
                print("Error: input_movies.csv is missing required columns.")
                return
            movies = list(reader)
            if not movies:
                print("Warning: input_movies.csv is empty.")
    except FileNotFoundError:
                print("Error: input_movies.csv not found.")
                return
    classified_movies = []
    for item in movies:
        try:
            if not all(item.get(field, "").strip() for field in required_fields):
                print("Warning: skipping row with missing data.")
                continue
            if not item["duration_minutes"].isdigit() or int(item["duration_minutes"]) <= 0:
                print("Warning: skipping row with invalid duration.")
                continue
            item["type"] = classify_type(item)
            if item["type"] == "Other":
                print("Warning: skipping row with invalid type.")
                continue
            classification = classify_movie(item)
            ai_genre = ai_classify_genre(item["description"])
            print(item["title"], "->", ai_genre)
            classification["genre"] = ai_genre
            classified_movies.append(classification)
        except Exception as e:
            print("Error en:", item["title"], "-", e)
            classification = {
                "title": item.get("title", "Unknown"),
                "genre": "Unknown",
                "duration_category": "Unknown",
                "type": item.get("type", "Unknown")
            }
            classified_movies.append(classification)
    with open("classified_movies.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "genre", "duration_category", "type"])
        writer.writeheader()
        writer.writerows(classified_movies)

if __name__ == "__main__":
    main()