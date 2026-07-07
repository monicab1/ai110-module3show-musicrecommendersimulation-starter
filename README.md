# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project builds a simple music recommender. It looks at each song's
mood, genre, and a few other traits like energy and acousticness. Then it
compares those traits to what a listener likes, using a made-up "taste
profile." Songs that match the listener's taste best get ranked highest
and recommended first. The system also makes sure the list isn't filled
with songs from just one artist.

---

## How The System Works

Explain your design in plain language.

Major streaming platforms predict your next favorite song using two types of filtering: collaborative and content-based. Collaborative filtering analyzes user behavior patterns — if two users have similar listening histories, the system recommends each user's unique favorites to the other. Content-based filtering looks at the specific properties of a song and recommends other songs with similar properties. Core data inputs include implicit feedback (skips, completions, repeats, total listening time) and explicit feedback (likes, follows, thumbs up, adding a song to a library). Most real platforms use a hybrid of both. This version is content-based only, since it works from song features and a single user profile rather than multi-user behavior data. It prioritizes mood as the primary matching signal, since mood better captures situational listening intent — like working out, focusing, or relaxing — regardless of genre. Genre serves as a secondary signal, while energy and acousticness reinforce the mood match using a distance-to-target scoring approach that rewards songs close to the user's preference rather than simply higher or lower values.

Some prompts to answer:

- What features does each `Song` use in your system

Each Song uses genre, mood, energy, acousticness, valence, danceability, and tempo (tempo is stored but not weighted in the initial scoring version).

- What information does your `UserProfile` store

Each UserProfile stores a preferred mood, a preferred genre, and target values for energy, acousticness, valence, and danceability, representing the ideal song profile for that user.

- How does your `Recommender` compute a score for each song

The Recommender combines a weighted mix of categorical matches and numeric closeness. Mood and genre are scored as matches (exact match, partial/adjacent match, or no match), while energy, acousticness, valence, and danceability are scored using a distance-to-target formula that rewards songs closer to the user's preferred value rather than simply higher or lower values. These are combined into a single weighted score, with mood weighted highest, followed by genre, energy, acousticness, and valence/danceability.

- How do you choose which songs to recommend

Songs are ranked by their total weighted score from highest to lowest, and the top results are selected for the recommendation list, with a diversity rule applied so the top recommendations aren't dominated by a single artist.

You can include a simple diagram or bullet list if helpful.

**Scoring weights:**

- Mood match: 35%
- Genre match: 20%
- Energy closeness: 20%
- Acousticness closeness: 15%
- Valence / danceability closeness: 10%

---
## Algorithm Recipe

**Step 1 — Score each song on 5 components**

| Component | Rule | Max Points |
|---|---|---|
| Genre match | Exact match = full points. Adjacent genre = half points. No match = 0. | 2.0 |
| Mood match | Exact match = full points. Adjacent mood = half points. No match = 0. | 2.0 |
| Energy closeness | `1 - abs(song.energy - target_energy)`, scaled to max 2.0 | 2.0 |
| Acousticness closeness | `1 - abs(song.acousticness - target_acousticness)`, scaled to max 1.5 | 1.5 |
| Valence / danceability closeness | Average of valence-closeness and danceability-closeness, scaled to max 1.0 | 1.0 |

**Step 2 — Define "adjacent" categories**

- Genre adjacency: `rock ↔ punk ↔ metal` (hard/guitar cluster), `lofi ↔ ambient ↔ jazz ↔ classical` (calm cluster), `pop ↔ indie pop ↔ synthwave` (upbeat/produced cluster)
- Mood adjacency: `intense ↔ rebellious`, `chill ↔ relaxed ↔ focused`

**Step 3 — Total score**

score = genre_points + mood_points + energy_points + acousticness_points + valence_dance_points


Max possible score = 2.0 + 2.0 + 2.0 + 1.5 + 1.0 = **8.5 points**

**Step 4 — Rank and select**

Sort all songs by total score, highest to lowest. Walk down the ranked list and apply a diversity rule: skip or demote a song if its artist already appears in the current top-N recommendations, so one artist can't dominate the list (e.g. `Neon Echo` and `LoRoom` each appear twice in the catalog).

**Sample walk-through (using the sample `user_taste_profile`: rock/intense, energy=0.85, acousticness=0.10):**

| Song | Genre | Mood | Notes |
|---|---|---|---|
| Storm Runner | rock (exact) | intense (exact) | Top candidate — exact-exact match, energy 0.91 and acousticness 0.10 are very close to target |
| Iron Verdict | metal (adjacent) | intense (exact) | Strong runner-up — half genre points, full mood points, energy 0.97 is even higher than target |
| Riot Static | punk (adjacent) | rebellious (adjacent) | Lower — half points on both categorical scores, though energy/acousticness are close |

## Potential Biases to Watch For

- **Genre lock-in:** Because genre adjacency is hand-picked (e.g. rock/punk/metal cluster), the system may never surface a genuinely good match from outside that cluster — for example, a high-energy, low-acousticness song in a genre I didn't think to group (like `edm`'s Pulse Overdrive, energy=0.95, acousticness=0.04) could be a strong content match but get 0 genre points simply because it wasn't manually placed in the "hard/guitar" cluster.
- **Mood over-narrowing:** The adjacency map only covers moods present in my own reasoning about the sample profile. Moods like `euphoric`, `nostalgic`, or `romantic` aren't mapped to anything, so songs with those moods always score 0 on the mood component even if their numeric features are a near-perfect fit.
- **Cold-start / small-catalog bias:** With only ~18 songs and a handful of artists, the diversity rule can end up promoting a weaker match just to avoid repeating an artist, which wouldn't reflect a real recommender working with a much larger catalog.
- **Popularity/first-mover bias in ties:** If two songs tie on score, whichever comes first in the CSV will be recommended first — an artifact of data ordering rather than genuine preference.

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

```
Loaded songs: 18

Top 5 Recommendations for profile: genre=pop, mood=happy, energy=0.8
====================================================================

1. Sunrise City — Neon Echo
   Score: 5.96 / 8.5
   Reasons: genre match (+2.0), mood match (+2.0), energy closeness (+2.0)

2. Rooftop Lights — Indigo Parade
   Score: 4.92 / 8.5
   Reasons: adjacent genre match (+1.0), mood match (+2.0), energy closeness (+1.9)

3. Gym Hero — Max Pulse
   Score: 3.74 / 8.5
   Reasons: genre match (+2.0), energy closeness (+1.7)

4. Riot Static — Cass Rivers
   Score: 1.84 / 8.5
   Reasons: energy closeness (+1.8)

5. Storm Runner — Voltline
   Score: 1.78 / 8.5
   Reasons: energy closeness (+1.8)
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
