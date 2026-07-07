import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


def _song_to_dict(song: "Song") -> Dict:
    """Convert a Song dataclass into the dictionary shape used by the scoring helpers."""
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


def _user_to_prefs(user: "UserProfile") -> Dict:
    """Convert a UserProfile dataclass into the preference dictionary expected by scoring."""
    return {
        "favorite_genre": user.favorite_genre,
        "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy,
    }

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
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append({
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            })

    print(f"Loaded songs: {len(songs)}")
    return songs


# Genre adjacency clusters (Algorithm Recipe, Step 2)
GENRE_ADJACENCY = {
    "rock": {"punk", "metal"},
    "punk": {"rock", "metal"},
    "metal": {"rock", "punk"},
    "lofi": {"ambient", "jazz", "classical"},
    "ambient": {"lofi", "jazz", "classical"},
    "jazz": {"lofi", "ambient", "classical"},
    "classical": {"lofi", "ambient", "jazz"},
    "pop": {"indie pop", "synthwave"},
    "indie pop": {"pop", "synthwave"},
    "synthwave": {"pop", "indie pop"},
}

# Mood adjacency clusters (Algorithm Recipe, Step 2)
MOOD_ADJACENCY = {
    "intense": {"rebellious"},
    "rebellious": {"intense"},
    "chill": {"relaxed", "focused"},
    "relaxed": {"chill", "focused"},
    "focused": {"chill", "relaxed"},
}


def _category_score(target: str, actual: str, adjacency: Dict[str, set], max_points: float) -> Tuple[float, Optional[str]]:
    """
    Shared helper for genre/mood scoring.
    Exact match = full points, adjacent = half points, no match = 0.
    Returns (points, reason_label) where reason_label is one of
    'exact', 'adjacent', or None (no match).
    """
    if not target:
        return 0.0, None

    target = target.lower().strip()
    actual = (actual or "").lower().strip()

    if actual == target:
        return max_points, "exact"
    if actual in adjacency.get(target, set()):
        return max_points / 2, "adjacent"
    return 0.0, None


def _closeness_score(song_value: float, target_value: Optional[float], max_points: float) -> float:
    """
    Distance-to-target scoring: 1 - abs(song_value - target_value), scaled to max_points.
    If no target is provided, contributes 0 (feature not used in scoring).
    """
    if target_value is None:
        return 0.0
    closeness = 1 - abs(song_value - target_value)
    closeness = max(0.0, closeness)  # guard against negative closeness
    return closeness * max_points


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the Algorithm Recipe:

      - Genre match:              max 2.0 (exact / adjacent / none)
      - Mood match:                max 2.0 (exact / adjacent / none)
      - Energy closeness:          max 2.0
      - Acousticness closeness:    max 1.5
      - Valence/danceability:      max 1.0 (average of the two closeness scores)

    Total max score = 8.5

    Accepts either the simple `main.py` style prefs
    ({"genre", "mood", "energy"}) or the fuller UserProfile-style dict
    ({"favorite_genre", "favorite_mood", "target_energy",
      "target_acousticness", "target_valence", "target_danceability"}).

    Returns (score, reasons) where reasons is a list of human-readable
    strings like "genre match (+2.0)".
    """
    reasons: List[str] = []

    target_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    target_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))
    target_acousticness = user_prefs.get("target_acousticness")
    target_valence = user_prefs.get("target_valence")
    target_danceability = user_prefs.get("target_danceability")

    # --- Genre match (max 2.0) ---
    genre_points, genre_match_type = _category_score(
        target_genre, song.get("genre"), GENRE_ADJACENCY, 2.0
    )
    if genre_match_type == "exact":
        reasons.append(f"genre match (+{genre_points:.1f})")
    elif genre_match_type == "adjacent":
        reasons.append(f"adjacent genre match (+{genre_points:.1f})")

    # --- Mood match (max 2.0) ---
    mood_points, mood_match_type = _category_score(
        target_mood, song.get("mood"), MOOD_ADJACENCY, 2.0
    )
    if mood_match_type == "exact":
        reasons.append(f"mood match (+{mood_points:.1f})")
    elif mood_match_type == "adjacent":
        reasons.append(f"adjacent mood match (+{mood_points:.1f})")

    # --- Energy closeness (max 2.0) ---
    energy_points = _closeness_score(song.get("energy", 0.0), target_energy, 2.0)
    if target_energy is not None:
        reasons.append(f"energy closeness (+{energy_points:.1f})")

    # --- Acousticness closeness (max 1.5) ---
    acousticness_points = _closeness_score(
        song.get("acousticness", 0.0), target_acousticness, 1.5
    )
    if target_acousticness is not None:
        reasons.append(f"acousticness closeness (+{acousticness_points:.1f})")

    # --- Valence / danceability closeness (max 1.0, averaged) ---
    valence_dance_points = 0.0
    if target_valence is not None or target_danceability is not None:
        valence_closeness = _closeness_score(song.get("valence", 0.0), target_valence, 1.0)
        dance_closeness = _closeness_score(song.get("danceability", 0.0), target_danceability, 1.0)

        # Average only over the components that actually have a target set,
        # so a missing target doesn't unfairly drag the average to 0.
        parts = [p for p, t in ((valence_closeness, target_valence), (dance_closeness, target_danceability)) if t is not None]
        valence_dance_points = sum(parts) / len(parts) if parts else 0.0

        if valence_dance_points > 0:
            reasons.append(f"valence/danceability closeness (+{valence_dance_points:.1f})")

    total_score = (
        genre_points
        + mood_points
        + energy_points
        + acousticness_points
        + valence_dance_points
    )

    return total_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Steps:
      1. Score every song in the catalog using score_song().
      2. Sort all scored songs from highest to lowest score.
      3. Walk down the sorted list applying a diversity rule: skip a
         song if its artist already has a recommendation in the
         current results, so one artist can't dominate the top-k.
      4. Return the top k as (song_dict, score, explanation) tuples,
         where explanation is a human-readable string built from the
         reasons list.
    """
    # Step 1: score every song, pairing each with its (score, reasons).
    # A list comprehension is the Pythonic way to apply score_song to
    # the whole catalog in one pass.
    scored_songs = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]

    # Step 2: sort highest to lowest score. sorted() with a key and
    # reverse=True avoids mutating the input list and keeps ties in
    # their original (CSV) order, since Python's sort is stable.
    scored_songs.sort(key=lambda entry: entry[1], reverse=True)

    # Step 3 + 4: walk the ranked list, keeping the best-scoring songs
    # Enforce diversity: prefer at most one recommendation per artist.
    # First pass: collect up to k recommendations, skipping songs whose
    # artist already appears in the current results.
    recommendations: List[Tuple[Dict, float, str]] = []
    seen_artists = set()

    for song, score, reasons in scored_songs:
        if len(recommendations) >= k:
            break

        artist = (song.get("artist") or "").strip()
        if artist in seen_artists:
            # skip duplicate-artist entries in the primary pass
            continue

        explanation = ", ".join(reasons) if reasons else "no strong matches"
        recommendations.append((song, score, explanation))
        seen_artists.add(artist)

    # If we didn't reach k unique-artist recommendations (catalog too small),
    # fill the remaining slots with the highest-scoring songs regardless of artist.
    if len(recommendations) < k:
        for song, score, reasons in scored_songs:
            if len(recommendations) >= k:
                break

            # skip songs already included
            if any(s[0]["id"] == song.get("id") for s in recommendations):
                continue

            explanation = ", ".join(reasons) if reasons else "no strong matches"
            recommendations.append((song, score, explanation))

    return recommendations
