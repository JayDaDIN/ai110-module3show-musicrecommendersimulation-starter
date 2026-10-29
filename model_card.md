# Model Card: VibeFinder CLI Simulation

## 1. Model Name

**VibeFinder CLI Simulation** — a small, explainable content-based music recommender used for classroom exploration.

## 2. Intended Use

VibeFinder ranks songs in a small fictional catalog according to a listener's stated genre, mood, and audio-feature targets. It is intended for learning how hand-designed recommender rules convert data into scores and rankings.

The system assumes that a listener can express some of their taste through these fields and that the catalog's metadata is accurate enough for a demonstration. It is not intended for real-world deployment, commercial recommendations, or claims about a person's actual enjoyment.

## 3. How the Model Works

Each song is described by genre, mood, energy, tempo, valence, danceability, and acousticness. A profile can specify a preferred genre and mood and target values for each numeric feature.

Genre and mood each receive 20 possible points when they match exactly after case and whitespace normalization. Energy, tempo, valence, danceability, and acousticness each receive 12 possible points based on closeness to the listener's target. For 0–1 features, match is `max(0, 1 - absolute difference)`. Tempo match is `max(0, 1 - absolute BPM difference / 80)`. The weighted matches are normalized by the weights of the preferences actually provided to produce a score from 0 to 100. Results are ordered by score, with song ID used to break ties.

The scoring function can also accept `likes_acoustic` when `target_acousticness` is not supplied; it uses the song's acousticness as the match for a listener who likes acoustic music and its inverse otherwise. The CLI sample profiles use the numeric acousticness target.

Compared with the starter, the functional CLI path now reads typed values from CSV, scores tracks across all seven preference dimensions, ranks them, and prints reasons. `Song` and `UserProfile` dataclasses are present as an object-oriented design, but the dataclass `Recommender` methods remain placeholders and are not used by the CLI.

## 4. Data

The catalog contains **30 fictional songs** stored in `data/songs.csv`. It has 12 genre labels: pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, electronic, country, hip hop, and r&b. It has six mood labels: happy, chill, intense, relaxed, moody, and focused.

Twenty fictional rows were added to the original ten-song starter catalog. The catalog has numeric energy, valence, danceability, and acousticness values between 0 and 1 and tempo values in BPM. These values are illustrative metadata; they were not measured from audio. The data contains no listener identities, play counts, ratings, saves, skips, or other interaction history.

The catalog cannot represent every genre, subgenre, culture, language, lyrical theme, performance style, or interpretation of mood. Since this is a small synthetic dataset, its scores should not be treated as evidence about real music preferences.

## 5. Strengths

- The rules and weights are simple enough to inspect, explain, and modify.
- Recommendations can reflect combinations such as intense rock or chill lofi instead of matching a single feature alone.
- Numeric closeness allows near matches rather than requiring exact equality.
- The CLI provides a score and match reasons, making it easier to understand why songs rank highly.
- Contrasting sample profiles produced intuitive top results for this catalog: Daybreak Parade for High-Energy Pop, Library Rain for Chill Lofi, and Storm Runner for Deep Intense Rock.
- Preferences can be omitted, allowing sparse and numeric-only profiles to be explored.

## 6. Limitations and Bias

- **Small, synthetic catalog:** Styles absent or underrepresented in the 30 rows cannot be surfaced fairly or reliably. How many songs represent a genre can affect the range of available recommendations.
- **Subjective labels:** Genre and mood depend on labeling choices. Exact matching treats “chill” and “relaxed” as different, even if a listener considers them similar.
- **Hand-selected weights:** Genre and mood together contribute 40% when all preferences are supplied; the five numeric features contribute 60%. These weights have not been learned or validated with listeners and may privilege some dimensions over others.
- **Sparse-profile inflation:** The denominator includes only supplied preferences. A profile specifying only genre can give all songs in that genre 100 points and all other songs zero, making a score appear more comprehensive than it is.
- **Zero-score fallback:** The CLI requests five tracks for each profile. If fewer than five songs match, it can still show zero-score songs to fill the list.
- **Incomplete view of musical taste:** The model does not analyze the audio and has no lyrics, language, vocals, timbre, artist context, culture, listening situation, or personal memory features.
- **No collaborative evidence:** The model does not use other listeners' behavior, so it cannot discover tracks through similar users or learn from actual responses.
- **No validated outcome metric:** A score measures similarity to the encoded profile, not satisfaction or likelihood of listening.

The profile named “Conflicting Preferences” intentionally combines preferences that rarely occur together in the catalog. Its results demonstrate tradeoffs in the weighted score; they are not a judgment about the listener.

## 7. Evaluation

The recommender was tested using these seven CLI profiles:

1. High-Energy Pop
2. Chill Lofi
3. Deep Intense Rock
4. Acoustic Folk
5. Conflicting Preferences
6. Sparse Case-Insensitive Genre
7. Unseen Genre and Mood

Automated tests check that recommendations are sorted, scores stay between 0 and 100, the first three profiles produce expected top tracks, sparse and unseen labels work, and an empty preference dictionary raises a clear error. CSV loading and the starter dataclass behavior are also tested. The test suite has **8 passing tests**.

In the observed run, the expected top songs appeared for High-Energy Pop, Chill Lofi, and Deep Intense Rock. The conflicting profile ranked acoustic chill tracks highly because mood and acousticness aligned despite the rock preference not matching. The unseen-label profile still produced rankings using its numeric preferences. The genre-only profile scored all matching pop songs at 100 and showed a zero-score fifth result because the CLI asks for five tracks while only four catalog tracks have that genre.

This evaluation verifies implementation behavior against examples; it does not measure real user satisfaction, catalog fairness, or predictive accuracy.

## 8. Future Work

- Gather listener ratings or implicit feedback (plays, skips, saves, replays) and evaluate rankings against held-out feedback.
- Tune weights using a documented validation method rather than intuition alone.
- Add related-label or multi-label genre/mood matching to handle overlapping styles.
- Add results diversity controls, such as limiting repeated artists or avoiding nearly identical top tracks.
- Make the requested result count configurable and consider excluding zero-score recommendations.
- Track how much of each score comes from provided preferences so sparse-profile scores are not misinterpreted.
- Expand the catalog with more representative and carefully documented metadata.
- Implement the dataclass-based `Recommender` and explanations consistently with the functional scoring path.
- Add richer content signals such as lyrics or audio embeddings only with appropriate data provenance, evaluation, and safeguards.

## 9. Personal Reflection

I learned that a recommender can be built from understandable rules: represent a listener's preferences, compare them with item features, and rank the results. I also learned that the score reflects the assumptions and weights chosen by the designer, not a guarantee that someone will enjoy a song. Testing different profiles showed how missing data, subjective labels, and conflicting preferences can change the results. A larger catalog and real listener feedback would be needed to tell whether the recommendations are genuinely useful.
