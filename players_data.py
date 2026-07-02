"""
Sample player data for the Soccer Analytics app.

This is realistic-looking sample data for demo purposes so the app runs
out of the box. To pull REAL data from FBref, see fetch_real_data.py.
"""

import pandas as pd

# Raw season totals for sample forwards across Europe's top 5 leagues
# (sample/illustrative data — not live stats. See fetch_real_data.py for real data.)
RAW_DATA = [
    # name, team, league, position, minutes, goals, assists, xg, xa, shots, key_passes,
    # dribbles_completed, progressive_carries, touches_in_box

    # --- La Liga ---
    {"player": "Robert Lewandowski", "team": "Barcelona", "league": "La Liga", "position": "FW",
     "minutes": 2650, "goals": 23, "assists": 6, "xg": 20.1, "xa": 5.4,
     "shots": 98, "key_passes": 34, "dribbles_completed": 18,
     "progressive_carries": 45, "touches_in_box": 210},

    {"player": "Vinicius Junior", "team": "Real Madrid", "league": "La Liga", "position": "FW",
     "minutes": 2800, "goals": 19, "assists": 11, "xg": 16.8, "xa": 9.2,
     "shots": 88, "key_passes": 52, "dribbles_completed": 95,
     "progressive_carries": 180, "touches_in_box": 195},

    {"player": "Antoine Griezmann", "team": "Atletico Madrid", "league": "La Liga", "position": "FW",
     "minutes": 2900, "goals": 14, "assists": 9, "xg": 12.5, "xa": 8.1,
     "shots": 70, "key_passes": 60, "dribbles_completed": 40,
     "progressive_carries": 110, "touches_in_box": 140},

    {"player": "Alexander Sorloth", "team": "Villarreal", "league": "La Liga", "position": "FW",
     "minutes": 2450, "goals": 20, "assists": 4, "xg": 17.9, "xa": 3.6,
     "shots": 90, "key_passes": 20, "dribbles_completed": 15,
     "progressive_carries": 40, "touches_in_box": 200},

    {"player": "Ferran Torres", "team": "Barcelona", "league": "La Liga", "position": "FW",
     "minutes": 2300, "goals": 13, "assists": 7, "xg": 11.4, "xa": 6.5,
     "shots": 60, "key_passes": 38, "dribbles_completed": 35,
     "progressive_carries": 90, "touches_in_box": 130},

    # --- Premier League ---
    {"player": "Erling Haaland", "team": "Manchester City", "league": "Premier League", "position": "FW",
     "minutes": 2600, "goals": 27, "assists": 5, "xg": 24.5, "xa": 4.2,
     "shots": 105, "key_passes": 22, "dribbles_completed": 12,
     "progressive_carries": 35, "touches_in_box": 225},

    {"player": "Mohamed Salah", "team": "Liverpool", "league": "Premier League", "position": "FW",
     "minutes": 3000, "goals": 25, "assists": 16, "xg": 21.3, "xa": 12.8,
     "shots": 100, "key_passes": 70, "dribbles_completed": 55,
     "progressive_carries": 130, "touches_in_box": 190},

    {"player": "Cole Palmer", "team": "Chelsea", "league": "Premier League", "position": "FW",
     "minutes": 2850, "goals": 18, "assists": 12, "xg": 15.2, "xa": 10.5,
     "shots": 85, "key_passes": 65, "dribbles_completed": 48,
     "progressive_carries": 120, "touches_in_box": 160},

    {"player": "Ollie Watkins", "team": "Aston Villa", "league": "Premier League", "position": "FW",
     "minutes": 2900, "goals": 16, "assists": 8, "xg": 14.8, "xa": 6.9,
     "shots": 75, "key_passes": 40, "dribbles_completed": 20,
     "progressive_carries": 55, "touches_in_box": 175},

    {"player": "Bukayo Saka", "team": "Arsenal", "league": "Premier League", "position": "FW",
     "minutes": 2750, "goals": 15, "assists": 13, "xg": 13.6, "xa": 11.2,
     "shots": 78, "key_passes": 62, "dribbles_completed": 60,
     "progressive_carries": 140, "touches_in_box": 150},

    # --- Serie A ---
    {"player": "Lautaro Martinez", "team": "Inter Milan", "league": "Serie A", "position": "FW",
     "minutes": 2700, "goals": 22, "assists": 6, "xg": 19.5, "xa": 5.1,
     "shots": 92, "key_passes": 30, "dribbles_completed": 22,
     "progressive_carries": 50, "touches_in_box": 205},

    {"player": "Dusan Vlahovic", "team": "Juventus", "league": "Serie A", "position": "FW",
     "minutes": 2500, "goals": 17, "assists": 4, "xg": 15.9, "xa": 3.8,
     "shots": 80, "key_passes": 18, "dribbles_completed": 14,
     "progressive_carries": 38, "touches_in_box": 185},

    {"player": "Victor Osimhen", "team": "Napoli", "league": "Serie A", "position": "FW",
     "minutes": 2300, "goals": 19, "assists": 3, "xg": 17.2, "xa": 2.9,
     "shots": 85, "key_passes": 15, "dribbles_completed": 25,
     "progressive_carries": 42, "touches_in_box": 195},

    {"player": "Paulo Dybala", "team": "Roma", "league": "Serie A", "position": "FW",
     "minutes": 2200, "goals": 12, "assists": 9, "xg": 10.4, "xa": 7.8,
     "shots": 62, "key_passes": 55, "dribbles_completed": 45,
     "progressive_carries": 95, "touches_in_box": 130},

    {"player": "Ademola Lookman", "team": "Atalanta", "league": "Serie A", "position": "FW",
     "minutes": 2600, "goals": 16, "assists": 7, "xg": 13.8, "xa": 6.2,
     "shots": 75, "key_passes": 42, "dribbles_completed": 50,
     "progressive_carries": 100, "touches_in_box": 145},

    # --- Bundesliga ---
    {"player": "Harry Kane", "team": "Bayern Munich", "league": "Bundesliga", "position": "FW",
     "minutes": 2900, "goals": 28, "assists": 8, "xg": 25.1, "xa": 7.2,
     "shots": 110, "key_passes": 45, "dribbles_completed": 15,
     "progressive_carries": 48, "touches_in_box": 220},

    {"player": "Serhou Guirassy", "team": "Borussia Dortmund", "league": "Bundesliga", "position": "FW",
     "minutes": 2400, "goals": 21, "assists": 3, "xg": 18.6, "xa": 2.5,
     "shots": 88, "key_passes": 12, "dribbles_completed": 10,
     "progressive_carries": 30, "touches_in_box": 200},

    {"player": "Loic Bade", "team": "Bayer Leverkusen", "league": "Bundesliga", "position": "FW",
     "minutes": 2000, "goals": 9, "assists": 4, "xg": 8.1, "xa": 3.6,
     "shots": 45, "key_passes": 20, "dribbles_completed": 8,
     "progressive_carries": 25, "touches_in_box": 100},

    {"player": "Omar Marmoush", "team": "Eintracht Frankfurt", "league": "Bundesliga", "position": "FW",
     "minutes": 2500, "goals": 19, "assists": 10, "xg": 16.4, "xa": 8.7,
     "shots": 80, "key_passes": 50, "dribbles_completed": 38,
     "progressive_carries": 105, "touches_in_box": 165},

    {"player": "Michael Olise", "team": "Bayern Munich", "league": "Bundesliga", "position": "FW",
     "minutes": 2600, "goals": 14, "assists": 12, "xg": 12.1, "xa": 10.8,
     "shots": 70, "key_passes": 68, "dribbles_completed": 58,
     "progressive_carries": 125, "touches_in_box": 140},

    # --- Ligue 1 ---
    {"player": "Ousmane Dembele", "team": "Paris Saint-Germain", "league": "Ligue 1", "position": "FW",
     "minutes": 2450, "goals": 20, "assists": 10, "xg": 17.5, "xa": 8.9,
     "shots": 82, "key_passes": 48, "dribbles_completed": 65,
     "progressive_carries": 150, "touches_in_box": 170},

    {"player": "Bradley Barcola", "team": "Paris Saint-Germain", "league": "Ligue 1", "position": "FW",
     "minutes": 2350, "goals": 13, "assists": 8, "xg": 11.6, "xa": 6.8,
     "shots": 65, "key_passes": 40, "dribbles_completed": 52,
     "progressive_carries": 115, "touches_in_box": 135},

    {"player": "Alexandre Lacazette", "team": "Lyon", "league": "Ligue 1", "position": "FW",
     "minutes": 2600, "goals": 15, "assists": 6, "xg": 13.2, "xa": 5.4,
     "shots": 68, "key_passes": 35, "dribbles_completed": 20,
     "progressive_carries": 50, "touches_in_box": 150},

    {"player": "Jonathan David", "team": "Lille", "league": "Ligue 1", "position": "FW",
     "minutes": 2700, "goals": 18, "assists": 5, "xg": 15.8, "xa": 4.3,
     "shots": 78, "key_passes": 25, "dribbles_completed": 18,
     "progressive_carries": 45, "touches_in_box": 175},

    {"player": "Folarin Balogun", "team": "Monaco", "league": "Ligue 1", "position": "FW",
     "minutes": 2100, "goals": 11, "assists": 3, "xg": 9.8, "xa": 2.7,
     "shots": 55, "key_passes": 15, "dribbles_completed": 12,
     "progressive_carries": 30, "touches_in_box": 120},
]


def load_raw_dataframe() -> pd.DataFrame:
    """Return the raw season-totals DataFrame."""
    return pd.DataFrame(RAW_DATA)


def add_per90_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Add per-90-minute normalized versions of the counting stats."""
    df = df.copy()
    per90_factor = 90 / df["minutes"]

    counting_stats = [
        "goals", "assists", "xg", "xa", "shots", "key_passes",
        "dribbles_completed", "progressive_carries", "touches_in_box",
    ]
    for stat in counting_stats:
        df[f"{stat}_p90"] = (df[stat] * per90_factor).round(2)

    return df


def add_percentile_ranks(df: pd.DataFrame, stats: list[str]) -> pd.DataFrame:
    """Add percentile rank columns (0-100) for the given per-90 stats,
    relative to the players currently in the DataFrame (i.e. their position group)."""
    df = df.copy()
    for stat in stats:
        col = f"{stat}_p90"
        if col in df.columns:
            df[f"{stat}_pct"] = (df[col].rank(pct=True) * 100).round(0)
    return df


def get_processed_data() -> pd.DataFrame:
    """Full pipeline: raw data -> per-90 -> percentile ranks."""
    df = load_raw_dataframe()
    df = add_per90_stats(df)
    percentile_stats = [
        "goals", "assists", "xg", "xa", "key_passes",
        "dribbles_completed", "progressive_carries",
    ]
    df = add_percentile_ranks(df, percentile_stats)
    return df
