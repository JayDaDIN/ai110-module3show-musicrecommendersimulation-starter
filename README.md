# Music Recommender Simulation

## Project Summary

This CLI-first classroom simulation recommends fictional songs by comparing song metadata with a listener's stated music preferences. It loads a small CSV catalog, calculates a weighted content-based match score, ranks songs, and prints match reasons. It is designed to make the recommender's rules easy to inspect, not to predict real-world listening behavior.

## How the System Works

### Song data

Each song in `data/songs.csv` has:

- `id`, `title`, and `artist` for identification and display
- `genre` and `mood` for categorical matching
- `energy`, `valence`, `danceability`, and `acousticness`, represented from 0 to 1
- `tempo_bpm`, represented in beats per minute

The CLI currently scores genre, mood, energy, tempo, valence, danceability, and acousticness. The ID, title, and artist are not part of the score.

### Listener preferences

The CLI stores sample preference dictionaries in `USER_PROFILES` in `src/main.py`. A profile can specify `genre`, `mood`, and numeric targets named `target_energy`, `target_tempo_bpm`, `target_valence`, `target_danceability`, and `target_acousticness`. The recommender compares only the preferences supplied; omitted preferences are left out of the score calculation.

The `Song` and `UserProfile` dataclasses are also defined in `src/recommender.py` as an object-oriented starting point. The current CLI uses the dictionary-based functions `load_songs`, `score_song`, and `recommend_songs`; the dataclass recommender methods are starter placeholders and are not used by the CLI.

### Scoring recipe

Each preference produces a match from 0 to 1. Categorical values are stripped of surrounding whitespace and compared without regard to case. A genre or mood match scores 1; a mismatch scores 0.

| Feature | Weight | Match calculation |
|---|---:|---|
| Genre | 20 points | 1 for a match, otherwise 0 |
| Mood | 20 points | 1 for a match, otherwise 0 |
| Energy | 12 points | `max(0, 1 - abs(song energy - target energy))` |
| Tempo | 12 points | `max(0, 1 - abs(song BPM - target BPM) / 80)` |
| Valence | 12 points | `max(0, 1 - abs(song valence - target valence))` |
| Danceability | 12 points | `max(0, 1 - abs(song danceability - target danceability))` |
| Acousticness | 12 points | `max(0, 1 - abs(song acousticness - target acousticness))` |

The weighted matches are summed and divided by the total weight of the preferences provided, then multiplied by 100. This keeps scores on a 0–100 scale when profiles omit preferences. For example, when all seven features are supplied, genre and mood together contribute 40% of the possible score and the five numeric features contribute 60%. Tempo uses an 80 BPM distance scale; this is a design choice for this simulation, not a learned value.

Songs are sorted by score, highest first. Song ID breaks ties in ascending order. The CLI displays the top five results for each sample profile with scores and match reasons.

### Example profiles

The CLI runs seven profiles to demonstrate different and challenging preference combinations:

- **High-Energy Pop:** pop, happy, high energy, upbeat, danceable, and low acousticness
- **Chill Lofi:** lofi, chill, low energy, slower tempo, and high acousticness
- **Deep Intense Rock:** rock, intense, high energy, and low acousticness
- **Acoustic Folk:** folk, relaxed, moderate energy, and high acousticness
- **Conflicting Preferences:** rock and chill, but with high energy, slow tempo, low valence, high danceability, and high acousticness
- **Sparse Case-Insensitive Genre:** only `" POP "` to demonstrate case/whitespace normalization and omitted preferences
- **Unseen Genre and Mood:** `"dream pop"` and `"nostalgic"`, neither of which appears in the catalog

## Getting Started

Run commands from the repository root.

### Setup

Create and activate a virtual environment if desired:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the CLI:

```bash
python -m src.main
```

The program prints recommendations for all seven profiles. Alternatively, `python src/main.py` works from the repository root.

### Running Tests

```bash
python -m pytest -q
```

Tests check the starter dataclass behavior, CSV loading and numeric types, functional scoring/ranking, expected top tracks, all sample profiles, sparse/unseen preferences, and the empty-preferences error.

## Sample Recommendation Output

Example from the **High-Energy Pop** profile (scores and recommendations are based on the current catalog and weights):

```text
High-Energy Pop
============================================================

1. Daybreak Parade - Color Theory
   Genre: pop | Mood: happy
   Match score: 98.4/100
   Reasons: genre match (100%), mood match (100%), energy match (97%), valence match (96%), danceability match (97%), acousticness match (99%), tempo bpm match (98%)

2. Sunrise City - Neon Echo
   Genre: pop | Mood: happy
   Match score: 94.7/100
   Reasons: genre match (100%), mood match (100%), energy match (94%), valence match (96%), danceability match (89%), acousticness match (92%), tempo bpm match (85%)
```

### Stress-test summary

Top five tracks from a run of the current seven profiles:

| Profile | Recommendations, ranked (score / 100) |
|---|---|
| High-Energy Pop | Daybreak Parade (98.4), Sunrise City (94.7), Electric Bloom (78.0), Gym Hero (76.9), Open Road Anthem (74.4) |
| Chill Lofi | Library Rain (98.9), Midnight Coding (96.6), Focus Flow (78.0), Corner Table (76.6), Low Tide Letters (76.2) |
| Deep Intense Rock | Storm Runner (98.1), Static Hearts (76.3), Fast Lane Daydream (74.8), Neon Sprint (71.8), Gym Hero (70.2) |
| Acoustic Folk | Sunday Kitchen (98.9), Coffee Shop Stories (77.1), Paper Planes (76.3), Low Tide Letters (70.9), Golden Hour Drive (70.5) |
| Conflicting Preferences | Library Rain (59.5), Low Tide Letters (58.8), Midnight Coding (58.6), Spacewalk Thoughts (58.5), Corner Table (56.2) |
| Sparse Case-Insensitive Genre | Sunrise City (100.0), Gym Hero (100.0), First Light Run (100.0), Daybreak Parade (100.0), Midnight Coding (0.0) |
| Unseen Genre and Mood | After the Rain (56.8), Midnight Postcard (56.7), Golden Hour Drive (55.7), Velvet Room (53.2), Paper Planes (52.8) |

The sparse profile has only four matching pop tracks, so the top-five request includes a fifth zero-score result. The unseen-label profile gets no categorical match points, but its numeric preferences still rank songs.

## Experiments Tried

- Compared high-energy pop, chill lofi, intense rock, and acoustic folk profiles. Their top results matched the intended broad styles in this synthetic catalog.
- Used conflicting targets to see which attributes dominate when preferences point in different directions. The top result favored chill mood and acousticness, illustrating that the weights affect tradeoffs rather than enforcing every preference.
- Used an unseen genre/mood to confirm numeric feature matches can still produce rankings without categorical matches.
- Used a case- and whitespace-varied genre with no other preferences to check normalization and sparse-profile scoring.
- Added tempo, valence, and danceability to the weighted score so recommendations consider more than genre, mood, and energy.

The weights are hand-selected starting values. The simulation does not establish that they are optimal; meaningful weight tuning would require listener feedback or labeled evaluation data.

## Limitations and Risks

- The catalog has only 30 fictional, manually authored tracks. It does not represent the depth or balance of a real music catalog.
- Mood and genre labels are subjective, and exact categorical matching cannot recognize related labels such as “relaxed” and “chill.”
- Audio attributes are proxies for a musical vibe; the system does not analyze audio or understand lyrics, language, vocals, timbre, culture, listening context, or personal associations.
- Numeric weights and tempo scaling are fixed assumptions, not learned from user behavior.
- Missing profile preferences are excluded and remaining weights are renormalized. A sparse profile can therefore produce high scores based on just one feature.
- A request for more songs than there are positive matches can include zero-score recommendations.
- The system has no user histories, ratings, saves, plays, or skips. It is content-based, not collaborative, and cannot validate that high scores predict enjoyment.
- The current dataclass-based `Recommender` methods are placeholders; the working path is the functional CLI implementation.

## Reflection

This project shows how a recommender turns a preference profile and item features into a ranked list by applying explicit scoring rules. A high score is a measure of agreement with those rules, not proof that someone will like a song. Small changes to weights, feature definitions, or labels can change the ranking.

The simulation also highlights where bias can enter: the catalog may underrepresent styles, subjective labels may not fit every listener, and the scoring weights privilege the features chosen by the designer. Real user feedback, a broader catalog, clear explanations, and checks for catalog coverage and diversity would be needed before making stronger claims about recommendation quality.

## Project Files

- `src/main.py` — CLI runner and sample profiles
- `src/recommender.py` — song/profile data classes and functional scoring/ranking logic
- `data/songs.csv` — fictional song catalog
- `tests/test_recommender.py` — automated checks
- `model_card.md` — intended use, data, evaluation, limitations, and future work
