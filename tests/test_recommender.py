from pathlib import Path

import pytest

from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_songs,
)
from src.main import USER_PROFILES

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


def test_all_sample_profiles_return_ranked_recommendations():
    songs = load_songs(str(Path(__file__).parents[1] / "data" / "songs.csv"))

    for preferences in USER_PROFILES.values():
        recommendations = recommend_songs(preferences, songs, k=5)

        assert len(recommendations) == 5
        scores = [score for _, score, _ in recommendations]
        assert scores == sorted(scores, reverse=True)
        assert all(0.0 <= score <= 100.0 for score in scores)


def test_distinct_profiles_surface_expected_top_tracks():
    songs = load_songs(str(Path(__file__).parents[1] / "data" / "songs.csv"))
    expected_top_tracks = {
        "High-Energy Pop": "Daybreak Parade",
        "Chill Lofi": "Library Rain",
        "Deep Intense Rock": "Storm Runner",
    }

    for profile_name, expected_title in expected_top_tracks.items():
        recommendations = recommend_songs(USER_PROFILES[profile_name], songs, k=5)

        assert recommendations[0][0]["title"] == expected_title


def test_sparse_and_unseen_profile_preferences_are_supported():
    songs = load_songs(str(Path(__file__).parents[1] / "data" / "songs.csv"))

    sparse_results = recommend_songs(
        USER_PROFILES["Sparse Case-Insensitive Genre"], songs, k=3
    )
    unseen_results = recommend_songs(
        USER_PROFILES["Unseen Genre and Mood"], songs, k=3
    )

    assert all(song["genre"] == "pop" for song, _, _ in sparse_results)
    assert unseen_results[0][1] > 0
    assert all(
        "genre match" not in reasons and "mood match" not in reasons
        for _, _, reasons in unseen_results
    )


def test_recommender_rejects_profile_without_supported_preferences():
    songs = load_songs(str(Path(__file__).parents[1] / "data" / "songs.csv"))

    with pytest.raises(ValueError, match="at least one supported feature"):
        recommend_songs({}, songs)
