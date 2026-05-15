import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

ipl = pd.read_csv("../data/ipl_clean.csv")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🏏 IPL Dashboard")

st.sidebar.markdown("""
Use filters below to explore IPL data interactively.
""")

# -----------------------------
# SEASON FILTER
# -----------------------------

seasons = sorted(ipl['season'].dropna().unique())

selected_season = st.sidebar.selectbox(
    "Select Season",
    ["All"] + list(seasons)
)

# -----------------------------
# TEAM FILTER
# -----------------------------

teams = sorted(ipl['batting_team'].dropna().unique())

selected_team = st.sidebar.selectbox(
    "Select Team",
    ["All"] + list(teams)
)

# -----------------------------
# PLAYER FILTER
# -----------------------------

players = sorted(ipl['batsman'].dropna().unique())

selected_player = st.sidebar.selectbox(
    "Select Player",
    ["All"] + list(players)
)

# =====================================================
# FILTER DATA
# =====================================================

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

# =====================================================
# MAIN TITLE
# =====================================================

st.title("🏏 IPL Analytics Dashboard")

st.markdown("""
### Built using Python, Streamlit & Plotly

This dashboard analyzes:
- Team performance
- Player statistics
- Venue insights
- Toss impact
- Match trends across IPL seasons

Created by Soham
""")

st.markdown("---")

# =====================================================
# KPI METRICS
# =====================================================

total_matches = filtered_df['match_id'].nunique()

total_runs = filtered_df['total_runs'].sum()

avg_score = round(
    filtered_df.groupby('match_id')['total_runs']
    .sum()
    .mean(),
    2
)

total_players = filtered_df['batsman'].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Matches", total_matches)

col2.metric("Total Runs", total_runs)

col3.metric("Average Match Score", avg_score)

col4.metric("Players", total_players)

st.markdown("---")

# =====================================================
# PAGE NAVIGATION
# =====================================================

page = st.sidebar.radio(
    "Go To",
    [
        "Overview",
        "Team Analysis",
        "Player Analysis"
    ]
)

# =====================================================
# OVERVIEW PAGE
# =====================================================

if page == "Overview":

    st.header("📊 Overview Analysis")

    # -------------------------------------------------
    # TOP TEAMS BY RUNS
    # -------------------------------------------------

    team_runs = (
        filtered_df.groupby('batting_team')['total_runs']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig1 = px.bar(
        x=team_runs.index,
        y=team_runs.values,
        labels={
            'x': 'Team',
            'y': 'Runs'
        },
        title="Top Teams by Total Runs"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # -------------------------------------------------
    # RUNS ACROSS SEASONS
    # -------------------------------------------------

    season_runs = (
        filtered_df.groupby('season')['total_runs']
        .sum()
        .reset_index()
    )

    fig2 = px.line(
        season_runs,
        x='season',
        y='total_runs',
        markers=True,
        title="Runs Across IPL Seasons"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------------------------
    # MATCH RESULTS
    # -------------------------------------------------

    st.subheader("Batting First vs Chasing Wins")

    batting_first = len(
        filtered_df[filtered_df['win_by_runs'] > 0]
    )

    chasing = len(
        filtered_df[filtered_df['win_by_wickets'] > 0]
    )

    result_df = pd.DataFrame({
        'Type': ['Batting First Wins', 'Chasing Wins'],
        'Count': [batting_first, chasing]
    })

    fig3 = px.pie(
        result_df,
        names='Type',
        values='Count',
        title="Win Type Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# TEAM ANALYSIS PAGE
# =====================================================

elif page == "Team Analysis":

    st.header("🏆 Team Analysis")

    # -------------------------------------------------
    # TOSS DECISION ANALYSIS
    # -------------------------------------------------

    toss = (
        filtered_df['toss_decision']
        .value_counts()
        .reset_index()
    )

    toss.columns = ['Decision', 'Count']

    fig4 = px.pie(
        toss,
        names='Decision',
        values='Count',
        title="Toss Decision Distribution"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # -------------------------------------------------
    # TOP HIGH SCORING VENUES
    # -------------------------------------------------

    venue_runs = (
        filtered_df.groupby('venue')['total_runs']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig5 = px.bar(
        x=venue_runs.index,
        y=venue_runs.values,
        labels={
            'x': 'Venue',
            'y': 'Average Runs'
        },
        title="Top High Scoring Venues"
    )

    st.plotly_chart(fig5, use_container_width=True)

    # -------------------------------------------------
    # MOST MATCH WINS
    # -------------------------------------------------

    st.subheader("Most Match Wins")

    wins = (
        filtered_df['winner']
        .value_counts()
        .head(10)
    )

    fig6 = px.bar(
        x=wins.index,
        y=wins.values,
        labels={
            'x': 'Team',
            'y': 'Wins'
        },
        title="Top Teams by Wins"
    )

    st.plotly_chart(fig6, use_container_width=True)

# =====================================================
# PLAYER ANALYSIS PAGE
# =====================================================

elif page == "Player Analysis":

    st.header("🏏 Player Analysis")

    # -------------------------------------------------
    # TOP BATSMEN
    # -------------------------------------------------

    batsmen = (
        filtered_df.groupby('batsman')['batsman_runs']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig7 = px.bar(
        x=batsmen.index,
        y=batsmen.values,
        labels={
            'x': 'Player',
            'y': 'Runs'
        },
        title="Top 10 Batsmen"
    )

    st.plotly_chart(fig7, use_container_width=True)

    # -------------------------------------------------
    # TOP BOWLERS
    # -------------------------------------------------

    bowlers = (
        filtered_df['bowler']
        .value_counts()
        .head(10)
    )

    fig8 = px.bar(
        x=bowlers.index,
        y=bowlers.values,
        labels={
            'x': 'Bowler',
            'y': 'Wickets'
        },
        title="Top Bowlers"
    )

    st.plotly_chart(fig8, use_container_width=True)

    # -------------------------------------------------
    # BEST DEATH OVER BATSMEN
    # -------------------------------------------------

    st.subheader("Best Death Over Batsmen")

    death_overs = filtered_df[
        filtered_df['over'] >= 17
    ]

    death_batsmen = (
        death_overs.groupby('batsman')['batsman_runs']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig9 = px.bar(
        x=death_batsmen.index,
        y=death_batsmen.values,
        labels={
            'x': 'Player',
            'y': 'Runs'
        },
        title="Top Death Over Batsmen"
    )

    st.plotly_chart(fig9, use_container_width=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    "Built with ❤️ using Streamlit | IPL Analytics Dashboard"
)