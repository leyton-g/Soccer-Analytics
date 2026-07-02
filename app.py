"""
Soccer Analytics — Player Comparison App

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from players_data import get_processed_data

st.set_page_config(page_title="Soccer Analytics", page_icon="⚽", layout="wide")

# ---------- Load data ----------
df = get_processed_data()

# Metrics used for the radar chart (per-90 stats)
RADAR_METRICS = {
    "Goals p90": "goals_p90",
    "Assists p90": "assists_p90",
    "xG p90": "xg_p90",
    "Key Passes p90": "key_passes_p90",
    "Dribbles p90": "dribbles_completed_p90",
    "Prog. Carries p90": "progressive_carries_p90",
}

st.title("⚽ Soccer Analytics — Player Comparison")
st.caption("Sample dataset of forwards across Europe's top 5 leagues (La Liga, Premier League, Serie A, Bundesliga, Ligue 1). Swap in real FBref data via `fetch_real_data.py`.")

# ---------- Sidebar controls ----------
st.sidebar.header("Controls")

leagues = ["All"] + sorted(df["league"].unique().tolist())
league_filter = st.sidebar.selectbox("League", leagues, index=0)

filtered_df = df if league_filter == "All" else df[df["league"] == league_filter]
players = filtered_df["player"].tolist()

player_1 = st.sidebar.selectbox("Player 1", players, index=0)
player_2 = st.sidebar.selectbox("Player 2", players, index=min(1, len(players) - 1))

view = st.sidebar.radio(
    "View",
    ["Radar Comparison", "Bar Comparison", "Percentile Rankings (Beeswarm)"],
)

# ---------- Helper to normalize radar values 0-1 for shape comparability ----------
def normalize_for_radar(df, metrics_cols):
    norm = df.copy()
    for col in metrics_cols:
        max_val = df[col].max()
        norm[col] = df[col] / max_val if max_val > 0 else 0
    return norm

# ================= VIEW 1: RADAR =================
if view == "Radar Comparison":
    st.subheader(f"{player_1} vs {player_2}")

    metric_cols = list(RADAR_METRICS.values())
    metric_labels = list(RADAR_METRICS.keys())
    norm_df = normalize_for_radar(df, metric_cols)

    row1 = norm_df[norm_df["player"] == player_1].iloc[0]
    row2 = norm_df[norm_df["player"] == player_2].iloc[0]

    raw1 = df[df["player"] == player_1].iloc[0]
    raw2 = df[df["player"] == player_2].iloc[0]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[row1[c] for c in metric_cols] + [row1[metric_cols[0]]],
        theta=metric_labels + [metric_labels[0]],
        fill="toself",
        name=player_1,
    ))
    fig.add_trace(go.Scatterpolar(
        r=[row2[c] for c in metric_cols] + [row2[metric_cols[0]]],
        theta=metric_labels + [metric_labels[0]],
        fill="toself",
        name=player_2,
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        height=550,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Values are scaled relative to the max in this sample dataset (1.0 = highest among these 6 players), so the shape is comparable across different stats.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**{player_1}** ({raw1['team']})")
        st.dataframe(raw1[metric_cols].rename(dict(zip(metric_cols, metric_labels))), use_container_width=True)
    with col2:
        st.markdown(f"**{player_2}** ({raw2['team']})")
        st.dataframe(raw2[metric_cols].rename(dict(zip(metric_cols, metric_labels))), use_container_width=True)

# ================= VIEW 2: BAR COMPARISON =================
elif view == "Bar Comparison":
    st.subheader(f"{player_1} vs {player_2} — Single Stat Comparison")

    stat_choice = st.selectbox(
        "Choose a stat",
        list(RADAR_METRICS.keys()) + ["Minutes", "Total Goals", "Total Assists"],
    )

    stat_map = {**RADAR_METRICS, "Minutes": "minutes", "Total Goals": "goals", "Total Assists": "assists"}
    col = stat_map[stat_choice]

    comp_df = df[df["player"].isin([player_1, player_2])][["player", col]]
    fig = px.bar(comp_df, x="player", y=col, color="player", text=col,
                 title=f"{stat_choice}: {player_1} vs {player_2}")
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("All players — same stat")
    fig_all = px.bar(filtered_df.sort_values(col, ascending=False), x="player", y=col,
                      color="player", text=col, title=f"{stat_choice} — All Players ({league_filter})")
    fig_all.update_traces(textposition="outside")
    fig_all.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_all, use_container_width=True)

# ================= VIEW 3: PERCENTILE BEESWARM =================
else:
    st.subheader("Percentile Rankings vs. Sample Group")
    st.caption("Each dot is a player. Position (0-100) shows percentile rank on that stat within this sample group.")

    pct_cols = [c for c in df.columns if c.endswith("_pct")]
    pct_labels = [c.replace("_pct", "").replace("_", " ").title() for c in pct_cols]

    melted = df.melt(id_vars=["player"], value_vars=pct_cols,
                      var_name="stat", value_name="percentile")
    melted["stat"] = melted["stat"].str.replace("_pct", "").str.replace("_", " ").str.title()

    highlight = st.multiselect("Highlight players", players, default=[player_1, player_2])
    melted["highlighted"] = melted["player"].isin(highlight)

    fig = px.strip(
        melted, x="percentile", y="stat", color="highlighted",
        hover_data=["player"], orientation="h",
        color_discrete_map={True: "#E63946", False: "#A8A8A8"},
        stripmode="overlay",
    )
    fig.update_traces(marker=dict(size=14, line=dict(width=1, color="white")))
    fig.update_layout(height=450, showlegend=False, xaxis_range=[-5, 105])
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("See raw percentile table"):
        st.dataframe(
            df[["player", "team"] + pct_cols].rename(
                columns=dict(zip(pct_cols, pct_labels))
            ),
            use_container_width=True,
        )

st.divider()
st.caption("Data: sample dataset. See fetch_real_data.py for how to pull real stats from FBref via the `soccerdata` package.")
