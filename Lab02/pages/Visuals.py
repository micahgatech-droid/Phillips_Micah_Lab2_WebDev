# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import altair as alt
import os
import statistics

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data.csv"
)

DATA_JSON = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.json")

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="🏀",
)

# PAGE TITLE
st.title("40+ Point Games Data Visualizations 📈")

# LOAD DATA
DATA_JSON = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.json")

with open(DATA_JSON, "r") as file:
    data = json.load(file)

# Convert JSON data into a table for the graph
df = pd.DataFrame(data["data_points"])
    

# PART 1: GRAPHS FROM data.json

# BAR GRAPH
st.subheader("40+ Point Games by Player")
st.bar_chart(df, x="Player", y="40+ Point Games")

# INTERACTIVE GRAPH
st.subheader("40+ Point Games by Player")

if "selected_player" not in st.session_state:
    st.session_state.selected_player = df["Player"].iloc[0]

selected_player = st.selectbox(
    "Choose a player:",
    df["Player"],
    key="selected_player"
)

player_value = df[df["Player"] == selected_player]["40+ Point Games"].iloc[0]
other_value = df[df["Player"] != selected_player]["40+ Point Games"].sum()

pie_data = pd.DataFrame({
    "Category": [selected_player, "Other Players"],
    "Games": [player_value, other_value]
})

chart = alt.Chart(pie_data).mark_arc().encode(
    theta=alt.Theta(field="Games", type="quantitative"),
    color=alt.Color(
        field="Category",
        type="nominal",
        scale=alt.Scale(
            domain=[selected_player, "Other Players"],
            range=["#80C4FF", "#0066CC"]
        )
    ),
    tooltip=["Category", "Games"]
).properties(
    title="Selected Player vs. Other Players"
)

st.altair_chart(chart, use_container_width=True)
# PART 2: GRAPHS FROM data.csv
st.title("NBA Fan Survey Results")

if os.path.exists(DATA_FILE):
    csv_data = pd.read_csv(DATA_FILE)

    # COUNT VOTES
    player_counts = csv_data["Player"].value_counts().reset_index()
    player_counts.columns = ["Player", "Votes"]

    # STATIC BAR CHART
    st.subheader("Favorite NBA Players")

    st.bar_chart(
        player_counts,
        x="Player",
        y="Votes"
    )

    # DYNAMIC PIE CHART
    st.subheader("Explore Player Votes")

    if "survey_selected_player" not in st.session_state:
        st.session_state.survey_selected_player = player_counts["Player"].iloc[0]

    selected_player = st.selectbox(
        "Choose a player:",
        player_counts["Player"],
        key="survey_selected_player"
        )

    selected_votes = player_counts[
        player_counts["Player"] == selected_player
    ]["Votes"].iloc[0]

    other_votes = player_counts[
        player_counts["Player"] != selected_player
    ]["Votes"].sum()

    other_player_votes = player_counts[
    player_counts["Player"] != selected_player
    ]["Votes"].tolist()

    current_mean = statistics.mean(other_player_votes)
    current_median = statistics.median(other_player_votes)

    st.subheader("Survey Statistics")

    if "previous_mean" not in st.session_state:
        st.session_state.previous_mean = current_mean
        st.session_state.previous_median = current_median

    mean_change = current_mean - st.session_state.previous_mean
    median_change = current_median - st.session_state.previous_median

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Mean Votes (Other Players)",
            round(current_mean, 2),
            delta=round(mean_change, 2)
        )

    with col2:
        st.metric(
            "Median Votes (Other Players)",
            round(current_median, 2),
            delta=round(median_change, 2)
        )

    st.session_state.previous_mean = current_mean
    st.session_state.previous_median = current_median

    pie_data = pd.DataFrame({
        "Category": [selected_player, "Other Players"],
        "Votes": [selected_votes, other_votes]
    })

    pie_chart = alt.Chart(pie_data).mark_arc().encode(
        theta=alt.Theta(field="Votes", type="quantitative"),
        color=alt.Color(
            field="Category",
            type="nominal",
            scale=alt.Scale(
                domain=[selected_player, "Other Players"],
                range=["#0066CC", "#80C4FF"]
            )
        ),
        tooltip=["Category", "Votes"]
    ).properties(
        title="Selected Player vs. Other Players"
    )

    st.altair_chart(pie_chart, use_container_width=True)

else:
    st.info("No survey responses have been submitted yet.")
