"""
Soccer Analytics — Player Comparison App

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from players_data import get_processed_data, simulate_shot_locations

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
    [
        "Radar Comparison",
        "Bar Comparison",
        "Percentile Rankings (Beeswarm)",
        "Goals vs xG (Efficiency)",
        "Shot Map (simulated)",
        "League Averages",
    ],
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

# ================= VIEW 4: EFFICIENCY (GOALS VS xG) =================
elif view == "Goals vs xG (Efficiency)":
    st.subheader("Finishing Efficiency: Goals vs. Expected Goals (xG)")
    st.caption("Points above the diagonal line are outperforming their xG (clinical finishers). Points below are underperforming.")

    max_val = max(df["goals"].max(), df["xg"].max()) + 3

    fig = px.scatter(
        df, x="xg", y="goals", color="league", size="shots",
        hover_name="player", hover_data={"team": True, "xg": True, "goals": True, "shots": True},
        labels={"xg": "Expected Goals (xG)", "goals": "Actual Goals"},
    )
    fig.add_shape(
        type="line", x0=0, y0=0, x1=max_val, y1=max_val,
        line=dict(color="gray", dash="dash"),
    )
    fig.update_layout(height=600, xaxis_range=[0, max_val], yaxis_range=[0, max_val])

    # Highlight the two selected players
    for p, color in [(player_1, "black"), (player_2, "red")]:
        prow = df[df["player"] == p].iloc[0]
        fig.add_annotation(
            x=prow["xg"], y=prow["goals"], text=p, showarrow=True,
            arrowhead=2, ax=20, ay=-30, font=dict(size=11, color=color),
        )

    st.plotly_chart(fig, use_container_width=True)

    df_diff = df.copy()
    df_diff["goals_minus_xg"] = (df_diff["goals"] - df_diff["xg"]).round(1)
    top_over = df_diff.sort_values("goals_minus_xg", ascending=False).head(5)[["player", "team", "goals", "xg", "goals_minus_xg"]]
    top_under = df_diff.sort_values("goals_minus_xg").head(5)[["player", "team", "goals", "xg", "goals_minus_xg"]]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Overperforming xG (clinical)**")
        st.dataframe(top_over, use_container_width=True, hide_index=True)
    with col2:
        st.markdown("**Underperforming xG (wasteful / unlucky)**")
        st.dataframe(top_under, use_container_width=True, hide_index=True)

# ================= VIEW 5: SHOT MAP =================
elif view == "Shot Map (simulated)":
    st.subheader(f"Shot Map — {player_1}")
    st.caption("⚠️ Simulated shot locations for demo purposes (this sample dataset only has season totals, not shot-by-shot event data). Swap in real StatsBomb/Opta event data for an accurate map.")

    row = df[df["player"] == player_1].iloc[0]
    shots_df = simulate_shot_locations(row)

    fig = go.Figure()

    # Draw a simplified pitch (attacking half only, goal at x=120)
    pitch_shapes = [
        dict(type="rect", x0=60, y0=0, x1=120, y1=80, line=dict(color="white")),
        dict(type="rect", x0=102, y0=18, x1=120, y1=62, line=dict(color="white")),  # box
        dict(type="rect", x0=114, y0=30, x1=120, y1=50, line=dict(color="white")),  # 6-yard box
        dict(type="circle", x0=99, y0=36, x1=105, y1=44, line=dict(color="white")),  # penalty spot area
    ]
    for shape in pitch_shapes:
        fig.add_shape(**shape)

    fig.add_trace(go.Scatter(
        x=shots_df[shots_df["result"] == "No Goal"]["x"],
        y=shots_df[shots_df["result"] == "No Goal"]["y"],
        mode="markers", name="No Goal",
        marker=dict(size=9, color="rgba(150,150,150,0.6)"),
    ))
    fig.add_trace(go.Scatter(
        x=shots_df[shots_df["result"] == "Goal"]["x"],
        y=shots_df[shots_df["result"] == "Goal"]["y"],
        mode="markers", name="Goal",
        marker=dict(size=13, color="#E63946", symbol="star", line=dict(width=1, color="white")),
    ))

    fig.update_layout(
        plot_bgcolor="#2d6a4f", paper_bgcolor="#2d6a4f",
        xaxis=dict(range=[58, 122], visible=False),
        yaxis=dict(range=[-2, 82], visible=False, scaleanchor="x"),
        height=500, showlegend=True,
        legend=dict(font=dict(color="white")),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"{int(row['shots'])} shots simulated → {int(row['goals'])} marked as goals, positioned closest to goal.")

# ================= VIEW 6: LEAGUE AVERAGES =================
elif view == "League Averages":
    st.subheader("League-Level Averages (per 90 minutes)")

    league_metrics = list(RADAR_METRICS.values())
    league_avg = df.groupby("league")[league_metrics].mean().round(2).reset_index()

    metric_pick = st.selectbox("Metric", list(RADAR_METRICS.keys()))
    col = RADAR_METRICS[metric_pick]

    fig = px.bar(
        league_avg.sort_values(col, ascending=False), x="league", y=col,
        color="league", text=col, title=f"Average {metric_pick} by League",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("See all league averages"):
        st.dataframe(
            league_avg.rename(columns={v: k for k, v in RADAR_METRICS.items()}),
            use_container_width=True, hide_index=True,
        )

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
