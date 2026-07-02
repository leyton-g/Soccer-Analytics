"""
Template for pulling REAL player stats from FBref using the `soccerdata` package.

This won't run in a sandboxed environment without internet access, but it
will work on your own machine.

Install first:
    pip install soccerdata

Usage:
    python fetch_real_data.py
    -> writes real_player_stats.csv, which you can load in players_data.py
       instead of the RAW_DATA sample list.
"""

import soccerdata as sd
import pandas as pd

# FBref league IDs used by soccerdata (big-5 leagues combined call is supported)
LEAGUES = [
    "ESP-La Liga",
    "ENG-Premier League",
    "ITA-Serie A",
    "GER-Bundesliga",
    "FRA-Ligue 1",
]

SEASON = "2425"  # 2024-2025 season, adjust as needed


def fetch_forward_stats():
    fbref = sd.FBref(leagues=LEAGUES, seasons=SEASON)

    # Standard stats (goals, assists, minutes, etc.)
    standard = fbref.read_player_season_stats(stat_type="standard")

    # Shooting stats (xG, shots)
    shooting = fbref.read_player_season_stats(stat_type="shooting")

    # Passing stats (key passes, xA)
    passing = fbref.read_player_season_stats(stat_type="passing")

    # Possession stats (dribbles, progressive carries, touches)
    possession = fbref.read_player_season_stats(stat_type="possession")

    # Merge them all on player/team/league
    merged = standard.join(shooting, lsuffix="", rsuffix="_shooting")
    merged = merged.join(passing, lsuffix="", rsuffix="_passing")
    merged = merged.join(possession, lsuffix="", rsuffix="_possession")

    merged = merged.reset_index()

    # Filter down to forwards only
    forwards = merged[merged["pos"].str.contains("FW", na=False)]

    return forwards


if __name__ == "__main__":
    df = fetch_forward_stats()
    df.to_csv("real_player_stats.csv", index=False)
    print(f"Saved {len(df)} forward records to real_player_stats.csv")
    print(df.head())
