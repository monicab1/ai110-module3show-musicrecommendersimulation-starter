# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
**That's My Song! 1.0**

##### description: It captures that exact moment of joy when a track comes on and someone exclaims, "That’s my song!"
---

## 2. Intended Use  

**Describe what your recommender is designed to do and who it is for.** 

**That's My Song! 1.0**, is a small, rule-based demo that scores songs against one user's stated preferences and returns a ranked top-k list; it's built for learning/classroom purposes, not as a product.

**Prompts:**  

- What kind of recommendations does it generate?

**That's My Song! 1.0**, generates content-based matches — songs whose genre, mood, energy, acousticness, valence, and danceability numerically resemble what the user says they want.


- What assumptions does it make about the user?

The Recommender assumes the user can articulate their taste as a single fixed profile (one favorite genre, one favorite mood, a few target numbers) rather than taste being varied, contextual, or evolving.


- Is this for real users or classroom exploration?

**That's My Song! 1.0** is intended for **Classroom exploration** use — The catalog is only (18 songs) and the logic is simplified for teaching how recommenders work, not for production use.

---

## 3. How the Model Works  

Songs are ranked by their total weighted score from highest to lowest, and the top results are selected for the recommendation list, with a diversity rule applied so the top recommendations aren't dominated by a single artist.

**Prompts:**  

- What features of each song are used (genre, energy, mood, etc.)

Each Song uses genre, mood, energy, acousticness, valence, danceability, and tempo (tempo is stored but not weighted in the initial scoring version).

- What user preferences are considered

Each UserProfile stores a preferred mood, a preferred genre, and target values for energy, acousticness, valence, and danceability, representing the ideal song profile for that user.

- How does the model turn those into a score

**That's My Song! 1.0**, combines a weighted mix of categorical matches and numeric closeness. Mood and genre are scored as matches (exact match, partial/adjacent match, or no match), while energy, acousticness, valence, and danceability are scored using a distance-to-target formula that rewards songs closer to the user's preferred value rather than simply higher or lower values. These are combined into a single weighted score, with mood weighted highest, followed by genre, energy, acousticness, and valence/danceability.
    
- What changes did you make from the starter logic

Applied the diversity rule — walk the sorted list, tracking seen_artists in a set. Skip any song whose artist is already represented in the results, so one artist can't take multiple top-k slots.

Build explanations — join the reasons list into a readable string.

Another change is that the logic also selects songs more thoughtfully and displays simple reasons for each song choice.

---

## 4. Data  

**Describe the dataset the model uses.**

The dataset has 18 songs across 12 genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, punk, metal, r&b, edm, country) and 12 moods (happy, chill, intense, relaxed, focused, moody, sad, rebellious, romantic, euphoric, nostalgic), performed by 13 distinct artists — two artists (Neon Echo, LoRoom) and (Mara Vance, Cass Rivers) each appear twice, which is what makes the diversity rule matter. Each song also carries five numeric features — energy, tempo_bpm, valence, danceability, and acousticness — all on roughly a 0–1 scale except tempo, which is in raw BPM.

Prompts:  

- How many songs are in the catalog

There are 18 songs in the dataset/catalog


- What genres or moods are represented

**12 genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, punk, metal, r&b, edm, country

**12 moods:** happy, chill, intense, relaxed, focused, moody, sad, rebellious, romantic, euphoric, nostalgic


- Did you add or remove data

**Yes, data was added** to the song dataset. The original set had 10 songs. **8 more** songs were added to give the Recommender more choices.

Resulting genres and moods added:
**genres added**: hip-hop, classical, punk, metal, r&b, edm, country
**moods added**: sad, rebellious, intense, romantic, euphoric

**No data was removed.** One planned field was intentionally *not* added:
`target_tempo` on `user_taste_profile`. Every song carries a `tempo_bpm`
value, but the user profile has no corresponding target, so tempo is
collected but currently unused by the recommender.


- Are there parts of musical taste missing in the dataset 
Yes, several:

- Lyrics/language/theme — nothing about lyrical content, explicitness, language, or subject matter, so two songs with identical numeric features but opposite messages score the same.
- Cultural/regional context — no data on language of origin, regional scenes, or cultural context (e.g., K-pop and Afrobeats genres aren't represented at all).
- Vocal characteristics — no vocalist gender, vocal style (rap vs. sung vs. instrumental), or presence/absence of vocals.
- Instrumentation/production texture — acousticness is a proxy, but there's nothing capturing specific instruments (guitar-driven vs. synth-driven vs. orchestral) beyond genre labels.
- Behavioral/social signals — no skip rate, replay count, likes, or "songs liked by similar users," which is why the README correctly notes this is content-based only, not collaborative.
- Release era/popularity — no release year or chart popularity, so nostalgia-driven or era-specific taste can't be modeled.

---

## 5. Strengths  

**Where does your system seem to work well**

**That's My Song! 1.0**, performs well for users whose taste sits inside one of the three hand-built adjacency clusters (hard/guitar, calm, upbeat/produced) and who have at least an energy target set — exactly the profiles your main.py test cases use.

Prompts:  

- User types for which it gives reasonable results

**That's My Song! 1.0**, works best for users whose favorite mood and genre fall inside a defined cluster and who have a clear energy target, for example:

"Deep Intense Rock" (rock/intense, energy≈0.95) — rock, punk, and metal are explicitly linked in GENRE_ADJACENCY, and intense/rebellious are linked in MOOD_ADJACENCY, so Storm Runner, Iron Verdict, and Riot Static all score well even when the exact genre doesn't match.
"High-Energy Pop" (pop/happy, energy≈0.9) — pop, indie pop, and synthwave are clustered, so Sunrise City, Rooftop Lights, and Night Drive Loop all surface reasonably, and Gym Hero picks up strong energy closeness even without a mood match.
"Chill Lofi" (lofi/chill, energy≈0.2, acousticness≈0.8) — the lofi/ambient/jazz/classical cluster plus the chill/relaxed/focused mood cluster means Library Rain, Spacewalk Thoughts, Coffee Shop Stories, and Focus Flow all cross-pollinate well, giving a coherent chill-catalog result.

- Any patterns you think your scoring captures correctly

**That's My Song! 1.0**, picks songs that closely match the mood and energy a listener asks for. It also avoids showing the same artist over and over. This mirrors how real music apps try to match your vibe, not just your favorite genre

- Cases where the recommendations matched your intuition

Sample taste profile (rock/intense) → top 3 matches the README's expected order exactly: 
Storm Runner (8.37) > Iron Verdict (7.03) > Riot Static (6.27).

Diversity rule check (pop/happy profile) → only one Neon Echo track appears in the top 5, even though both of their songs score well — confirming the rule prevents artist domination.

---

## 6. Limitations and Bias 

**Where the system struggles or behaves unfairly.**

One clear weakness is in how the mood-matching system handles moods outside its adjacency map. Genres like hip-hop, r&b, edm, and country, and moods like euphoric, romantic, nostalgic, and moody were never grouped with anything else in the code, so songs like Pulse Overdrive (edm, euphoric) or Slow Burn (r&b, romantic) can only earn points through an exact string match — there's no "adjacent" fallback for them the way rock and punk get. In practice, this means a user whose taste happens to fall into an unmapped genre or mood gets a much narrower path to a high score than a user who likes pop, rock, or lofi, even if their song's numeric features (energy, acousticness, etc.) are just as close a fit. This isn't a bug in the math — it's a byproduct of which clusters happened to get defined, and it shows how easily a hand-built taxonomy can quietly disadvantage whole categories of taste.

Prompts:  

- Features it does not consider

**That's My Song! 1.0**, does not consider the following features: Lyrics, cultural/language context, listening history, implicit feedback (skips/repeats), explicit feedback (likes/saves), and multi-user collaborative signals.

- Genres or moods that are underrepresented

Genres like hip-hop, r&b, edm, country, and classical(outside its one cluster) have no adjacency partners; moods like euphoric, romantic, nostalgic, moody, and sad aren't mapped to anything either.

- Cases where the system overfits to one preference

**Yes**, the system can overfit to one preference, because mood and genre are weighted heaviest, a user who nails an exact mood/genre match can rank highly even if their energy or acousticness is a poor fit, overemphasizing category labels over overall similarity.

- Ways the scoring might unintentionally favor some users

**Yes**, the scoring can unintentionally favor some users whose taste falls inside a defined adjacency cluster (rock/punk/metal, lofi/ambient/jazz/classical, pop/indie pop/synthwave) get partial credit for near-misses, while users who like anything outside those clusters only ever get all-or-nothing scoring.
 
**Simple notes about limitations and bias:**

- The model does not use listening history or context like time of day.
- Some genres or moods may be underrepresented in the song list.
- If a user only sets one preference (for example only `genre`), the results may ignore other tastes.
- Users who set `energy` or other numeric targets have more influence on scoring.

---

## 7. Evaluation  

**How you checked whether the recommender behaved as expected.** 

**Prompts:**  

- Which user profiles you tested

I tested three profiles: a high-energy pop user, a chill lofi user, and a deep intense rock user. These profiles helped me check whether the recommendations matched different kinds of taste.

- What you looked for in the recommendations

I looked for songs that matched the user's genre, mood, and energy preferences in a sensible way. I also checked whether the top results felt more like a good fit than random matches.  

- What surprised you

I was surprised that removing mood from the scoring changed the rankings a lot. The system still picked songs that fit genre and energy, but it became less sensitive to the vibe the user seemed to want.  

- Any simple tests or comparisons you ran

I ran the main script to inspect the recommendations and also compared the normal scoring run with a temporary version that skipped mood. The comparison showed that mood has a meaningful effect on the results.


### Stress test profiles

I tested the recommender with three diverse preference profiles:

- **High-Energy Pop**: `genre=pop`, `mood=happy`, `energy=0.9`
- **Chill Lofi**: `genre=lofi`, `mood=chill`, `energy=0.2`, `target_acousticness=0.8`
- **Deep Intense Rock**: `genre=rock`, `mood=intense`, `energy=0.95`

### Terminal outputs

**High-Energy Pop**

```text
Loaded songs: 18

Top 5 Recommendations for profile: High-Energy Pop (genre=pop, mood=happy, energy=0.9)
======================================================================================

1. Sunrise City — Neon Echo
   Score: 5.84 / 8.5
   Reasons: genre match (+2.0), mood match (+2.0), energy closeness (+1.8)

2. Rooftop Lights — Indigo Parade
   Score: 4.72 / 8.5
   Reasons: adjacent genre match (+1.0), mood match (+2.0), energy closeness (+1.7)

3. Gym Hero — Max Pulse
   Score: 3.94 / 8.5
   Reasons: genre match (+2.0), energy closeness (+1.9)

4. Storm Runner — Voltline
   Score: 1.98 / 8.5
   Reasons: energy closeness (+2.0)

5. Riot Static — Cass Rivers
   Score: 1.96 / 8.5
   Reasons: energy closeness (+2.0)
```

**Chill Lofi**

```text
Top 5 Recommendations for profile: Chill Lofi (genre=lofi, mood=chill, energy=0.2, target_acousticness=0.8)
===========================================================================================================

1. Library Rain — Paper Lanterns
   Score: 7.11 / 8.5
   Reasons: genre match (+2.0), mood match (+2.0), energy closeness (+1.7), acousticness closeness (+1.4)

2. Midnight Coding — LoRoom
   Score: 6.93 / 8.5
   Reasons: genre match (+2.0), mood match (+2.0), energy closeness (+1.6), acousticness closeness (+1.4)

3. Spacewalk Thoughts — Orbit Bloom
   Score: 6.16 / 8.5
   Reasons: adjacent genre match (+1.0), mood match (+2.0), energy closeness (+1.8), acousticness closeness (+1.3)

4. Moonlit Sonata Dreams — Elena Frost
   Score: 5.08 / 8.5
   Reasons: adjacent genre match (+1.0), adjacent mood match (+1.0), energy closeness (+1.8), acousticness closeness (+1.3)

5. Coffee Shop Stories — Slow Stereo
   Score: 5.03 / 8.5
   Reasons: adjacent genre match (+1.0), adjacent mood match (+1.0), energy closeness (+1.7), acousticness closeness (+1.4)
```

**Deep Intense Rock**

```text
Top 5 Recommendations for profile: Deep Intense Rock (genre=rock, mood=intense, energy=0.95)
============================================================================================

1. Storm Runner — Voltline
   Score: 5.92 / 8.5
   Reasons: genre match (+2.0), mood match (+2.0), energy closeness (+1.9)

2. Iron Verdict — Grim Anthem
   Score: 4.96 / 8.5
   Reasons: adjacent genre match (+1.0), mood match (+2.0), energy closeness (+2.0)

3. Gym Hero — Max Pulse
   Score: 3.96 / 8.5
   Reasons: mood match (+2.0), energy closeness (+2.0)

4. Riot Static — Cass Rivers
   Score: 3.86 / 8.5
   Reasons: adjacent genre match (+1.0), adjacent mood match (+1.0), energy closeness (+1.9)

5. Pulse Overdrive — DJ Kairos
   Score: 2.00 / 8.5
   Reasons: energy closeness (+2.0)
```

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences

Right now, moods like "sad" or "romantic" get ignored completely, even if the song fits well. Adding those missing moods would let more good songs get picked. We could also use song speed (tempo), since that affects how a song feels just as much as energy does.

- Better ways to explain recommendations

The reasons given for a song are short and use technical scoring language. Simpler wording, like "this song matches your happy mood," would help users understand why a song was picked. Clearer reasons would also help users adjust their preferences to get better results next time.

- Improving diversity among the top results

Currently, the system only makes sure artists aren't repeated too much. It doesn't do the same for genres or moods, so results can still feel repetitive. Adding variety across genres and moods would make the recommendations feel richer.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
