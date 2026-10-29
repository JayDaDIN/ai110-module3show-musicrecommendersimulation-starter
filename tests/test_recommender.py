from pathlib import Path

from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_songs,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_reads_csv_data():
    csv_path = Path(__file__).parents[1] / "data" / "songs.csv"

    songs = load_songs(str(csv_path))

    assert songs
    assert isinstance(songs[0]["id"], int)
    assert isinstance(songs[0]["energy"], float)


def test_functional_recommender_ranks_matching_song_first():
    songs = load_songs(str(Path(__file__).parents[1] / "data" / "songs.csv"))
    preferences = {
        "genre": "rock",
        "mood": "intense",
        "target_energy": 0.9,
        "target_tempo_bpm": 150,
        "target_valence": 0.5,
        "target_danceability": 0.65,
        "target_acousticness": 0.1,
    }

    recommendations = recommend_songs(preferences, songs, k=3)

    assert len(recommendations) == 3
    assert recommendations[0][0]["title"] == "Storm Runner"
    assert recommendations[0][1] > recommendations[1][1]
