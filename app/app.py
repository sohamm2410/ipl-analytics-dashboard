import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
ipl = pd.read_csv("../data/ipl_clean.csv")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("IPL Dashboard Filters")

# Season Filter
seasons = sorted(ipl['season'].dropna().unique())
selected_season = st.sidebar.selectbox(
    "Select Season",
    ["All"] + list(seasons)
)

# Team Filter
teams = sorted(ipl['batting_team'].dropna().unique())
selected_team = st.sidebar.selectbox(
    "Select Team",
    ["All"] + list(teams)
)

# Player Filter
players = sorted(ipl['batsman'].dropna().unique())
selected_player = st.sidebar.selectbox(
    "Select Player",
    ["All"] + list(players)
)

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = ipl.copy()

if selected_season != "All":
    filtered_df = filtered_df[
        filtered_df['season'] == selected_season
    ]

if selected_team != "All":
    filtered_df = filtered_df[
        filtered_df['batting_team'] == selected_team
    ]

if selected_player != "All":
    filtered_df = filtered_df[
        filtered_df['batsman'] == selected_player
    ]

# -----------------------------
# TITLE
# -----------------------------
st.title("🏏 IPL Analytics Dashboard")

st.markdown("---")

# -----------------------------
# METRICS
# -----------------------------
total_matches = filtered_df['match_id'].nunique()
total_runs = filtered_df['total_runs'].sum()
avg_score = round(
    filtered_df.groupby('match_id')['total_runs']
    .sum()
    .mean(),
    2
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Matches", total_matches)
col2.metric("Total Runs", total_runs)
col3.metric("Average Match Score", avg_score)

st.markdown("---")

# -----------------------------
# PAGE SELECT
# -----------------------------
page = st.sidebar.radio(
    "Go To",
    [
        "Overview",
        "Team Analysis",
        "Player Analysis"
    ]
)

# ======================================================
# OVERVIEW PAGE
# ======================================================
if page == "Overview":

    st.header("Overview Analysis")

    # Top Teams
    team_runs = (
        filtered_df.groupby('batting_team')['total_runs']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig = px.bar(
        x=team_runs.index,
        y=team_runs.values,
        labels={
            'x': 'Team',
            'y': 'Runs'
        },
        title="Top Teams by Runs"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Season Runs
    season_runs = (
        filtered_df.groupby('season')['total_runs']
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        season_runs,
        x='season',
        y='total_runs',
        title="Runs Across Seasons"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ======================================================
# TEAM ANALYSIS
# ======================================================
elif page == "Team Analysis":

    st.header("Team Analysis")

    # Toss Decision
    toss = (
        filtered_df['toss_decision']
        .value_counts()
        .reset_index()
    )

    toss.columns = ['Decision', 'Count']

    fig3 = px.pie(
        toss,
        names='Decision',
        values='Count',
        title="Toss Decisions"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Venue Analysis
    venue_runs = (
        filtered_df.groupby('venue')['total_runs']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig4 = px.bar(
        x=venue_runs.index,
        y=venue_runs.values,
        labels={
            'x': 'Venue',
            'y': 'Average Runs'
        },
        title="Top High Scoring Venues"
    )

    st.plotly_chart(fig4, use_container_width=True)

# ======================================================
# PLAYER ANALYSIS
# ======================================================
elif page == "Player Analysis":

    st.header("Player Analysis")

    # Top Batsmen
    batsmen = (
        filtered_df.groupby('batsman')['batsman_runs']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig5 = px.bar(
        x=batsmen.index,
        y=batsmen.values,
        labels={
            'x': 'Player',
            'y': 'Runs'
        },
        title="Top Batsmen"
    )

    st.plotly_chart(fig5, use_container_width=True)

    # Top Bowlers
    bowlers = (
        filtered_df['bowler']
        .value_counts()
        .head(10)
    )

    fig6 = px.bar(
        x=bowlers.index,
        y=bowlers.values,
        labels={
            'x': 'Bowler',
            'y': 'Wickets'
        },
        title="Top Bowlers"
    )

    st.plotly_chart(fig6, use_container_width=True)