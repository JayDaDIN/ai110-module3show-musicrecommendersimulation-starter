# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

My Song Recommender design consists of  Song and UserProfile objects that perform varying functions but both contribute to tailored recommendations. In the Song profile, each Song stores its title, artist, and musical features: genre, mood, energy, tempo, valence, danceability, and acousticness. The recommender uses genre, mood, energy, and acousticness to calculate a match score. For the UserProfile object, it stores the listener’s favorite genre and mood, their target energy level from 0 to 1, and whether they like acoustic music. Conclusively, the recommended songs are calculated based on the user's preferences by matching genre and mood using a energy and acoustic calculator.

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.


Algorithim Breakdown:

The goal is to score each song based on listener's preference and stated music taste, then reutnr the highest scoring songs.

The weight of each metric/feature is as follows:

Feature	Points	Match
Genre	20	1 for a match; otherwise 0
Mood	20	1 for a match; otherwise 0
Energy	12	1 - abs(song energy - target energy)
Tempo	12	max(0, 1 - abs(song BPM - target BPM) / 80)
Valence	12	1 - abs(song valence - target valence)
Danceability	12	1 - abs(song danceability - target danceability)
Acousticness	12	1 - abs(song acousticness - target acousticness)

Total score is the sum of eatch match multiplied by its points.

Some concerns and potential biases are:
1) Weights are estimates instead of learned preferences since this is a estimated calculation algorithim instead of a live algorithim in this build phase
2) Small data catalogs limits coverage
3) Music labels are extremely subjective and there is a lot of cross bending music genres/songs that can fall into varying categories
4) other audio attributes such as lyrics, cuture, and other context are not factored
5) it's more content based instead of collaborative or interactive.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:
Top recommendations
============================================================

1. Sunrise City - Neon Echo
   Genre: pop | Mood: happy
   Match score: 98.6/100
   Recommended because:
   - genre match (100%)
   - mood match (100%)
   - energy match (98%)
   - valence match (96%)
   - danceability match (99%)
   - acousticness match (98%)
   - tempo bpm match (98%)

2. Daybreak Parade - Color Theory
   Genre: pop | Mood: happy
   Match score: 93.5/100
   Recommended because:
   - genre match (100%)
   - mood match (100%)
   - energy match (95%)
   - valence match (88%)
   - danceability match (87%)
   - acousticness match (91%)
   - tempo bpm match (85%)

3. Rooftop Lights - Indigo Parade
   Genre: indie pop | Mood: happy
   Match score: 76.8/100
   Recommended because:
   - mood match (100%)
   - energy match (96%)
   - valence match (99%)
   - danceability match (98%)
   - acousticness match (85%)
   - tempo bpm match (95%)

4. First Light Run - Atlas Avenue
   Genre: pop | Mood: focused
   Match score: 76.6/100
   Recommended because:
   - genre match (100%)
   - energy match (89%)
   - valence match (93%)
   - danceability match (95%)
   - acousticness match (100%)
   - tempo bpm match (95%)

5. Open Road Anthem - Westline
   Genre: country | Mood: happy
   Match score: 76.5/100
   Recommended because:
   - mood match (100%)
   - energy match (93%)
   - valence match (92%)
   - danceability match (97%)
   - acousticness match (96%)
   - tempo bpm match (92%)

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



