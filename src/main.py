"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

if __package__:
    from .recommender import load_songs, recommend_songs
else:
    from recommender import load_songs, recommend_songs


USER_PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "target_energy": 0.88,
        "target_tempo_bpm": 130,
        "target_valence": 0.88,
        "target_danceability": 0.90,
        "target_acousticness": 0.10,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "target_energy": 0.38,
        "target_tempo_bpm": 76,
        "target_valence": 0.60,
        "target_danceability": 0.58,
        "target_acousticness": 0.85,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "target_energy": 0.90,
        "target_tempo_bpm": 145,
        "target_valence": 0.45,
        "target_danceability": 0.65,
        "target_acousticness": 0.12,
    },
    "Acoustic Folk": {
        "genre": "folk",
        "mood": "relaxed",
        "target_energy": 0.45,
        "target_tempo_bpm": 92,
        "target_valence": 0.78,
        "target_danceability": 0.60,
        "target_acousticness": 0.88,
    },
    "Conflicting Preferences": {
        "genre": "rock",
        "mood": "chill",
        "target_energy": 0.95,
        "target_tempo_bpm": 60,
        "target_valence": 0.10,
        "target_danceability": 0.95,
        "target_acousticness": 0.95,
    },
    "Sparse Case-Insensitive Genre": {
        "genre": " POP ",
    },
    "Unseen Genre and Mood": {
        "genre": "dream pop",
        "mood": "nostalgic",
        "target_energy": 0.55,
        "target_tempo_bpm": 105,
        "target_valence": 0.65,
        "target_danceability": 0.60,
        "target_acousticness": 0.50,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in USER_PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n{profile_name}")
        print("=" * 60)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']} - {song['artist']}")
            print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
            print(f"   Match score: {score:.1f}/100")
            print(f"   Reasons: {explanation}")


if __name__ == "__main__":
    main()
