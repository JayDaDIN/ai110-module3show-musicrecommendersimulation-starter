import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Create a recommender for the supplied song catalog."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return up to k songs for the user."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a song matches the user's preferences."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load song records from a CSV file."""
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        songs = []
        for row in csv.DictReader(csv_file):
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return matching reasons."""
    weights = {
        "genre": 20,
        "mood": 20,
        "energy": 12,
        "tempo_bpm": 12,
        "valence": 12,
        "danceability": 12,
        "acousticness": 12,
    }
    matches = {}

    for feature in ("genre", "mood"):
        preference = user_prefs.get(feature)
        if preference is not None:
            matches[feature] = float(
                str(song[feature]).strip().casefold()
                == str(preference).strip().casefold()
            )

    for feature in ("energy", "valence", "danceability", "acousticness"):
        target = user_prefs.get(f"target_{feature}")
        if target is not None:
            matches[feature] = max(0.0, 1.0 - abs(song[feature] - float(target)))

    tempo_target = user_prefs.get("target_tempo_bpm")
    if tempo_target is not None:
        matches["tempo_bpm"] = max(
            0.0, 1.0 - abs(song["tempo_bpm"] - float(tempo_target)) / 80.0
        )

    if "acousticness" not in matches and "likes_acoustic" in user_prefs:
        acousticness = song["acousticness"]
        matches["acousticness"] = (
            acousticness if user_prefs["likes_acoustic"] else 1.0 - acousticness
        )

    total_weight = sum(weights[feature] for feature in matches)
    if total_weight == 0:
        raise ValueError("User preferences must include at least one supported feature.")

    score = 100.0 * sum(
        weights[feature] * match for feature, match in matches.items()
    ) / total_weight
    reasons = [
        f"{feature.replace('_', ' ')} match ({match:.0%})"
        for feature, match in matches.items()
        if match > 0
    ]
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k scored songs with explanations."""
    if k <= 0:
        return []

    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) or "No matching preferences."
        scored_songs.append((song, score, explanation))
    scored_songs.sort(key=lambda result: (-result[1], result[0]["id"]))
    return scored_songs[:k]
