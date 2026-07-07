"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    # Define multiple diverse user profiles for stress testing
    profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.2, "target_acousticness": 0.8},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95},
    }

    # Run the recommender for each profile and print the top-5 results
    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        profile_str = ", ".join(f"{key}={value}" for key, value in user_prefs.items())

        header = f"Top {len(recommendations)} Recommendations for profile: {profile_name} ({profile_str})"
        print()
        print(header)
        print("=" * len(header))
        print()

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} — {song['artist']}")
            print(f"   Score: {score:.2f} / 8.5")
            print(f"   Reasons: {explanation}")
            print()


if __name__ == "__main__":
    main()
