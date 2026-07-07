# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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

4. Night Drive Loop — Neon Echo
   Score: 2.70 / 8.5
   Reasons: adjacent genre match (+1.0), energy closeness (+1.7)

5. Storm Runner — Voltline
   Score: 1.98 / 8.5
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

4. Focus Flow — LoRoom
   Score: 6.07 / 8.5
   Reasons: genre match (+2.0), adjacent mood match (+1.0), energy closeness (+1.6), acousticness closeness (+1.5)

5. Moonlit Sonata Dreams — Elena Frost
   Score: 5.08 / 8.5
   Reasons: adjacent genre match (+1.0), adjacent mood match (+1.0), energy closeness (+1.8), acousticness closeness (+1.3)
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
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
