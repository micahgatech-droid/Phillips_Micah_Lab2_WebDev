# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data.csv"
    )

# PAGE CONFIGURATION
st.set_page_config(
    page_title="NBA Survey",
    page_icon="🏀"
)

# PAGE TITLE AND USER DIRECTIONS
st.title("NBA Fan Survey 🏀")
st.write("Tell us about your favorite NBA player!")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("Who is your favorite featured player?"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.write("Enter a Player:")
    favorite_player = st.text_input("Who is your favorite featured NBA player?")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        new_data = pd.DataFrame({
            "Player": [favorite_player]
        })

        if os.path.exists(DATA_FILE):
            csv_data = pd.read_csv(DATA_FILE)

            if "Player" in csv_data.columns:
                new_data.to_csv(DATA_FILE, mode="a", header=False, index=False)
            else:
                new_data.to_csv(DATA_FILE, index=False)
        else:
            new_data.to_csv(DATA_FILE, index=False)

    st.success("Your response has been submitted!")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider()
st.header("Current Survey Results")

if os.path.exists(DATA_FILE):
    csv_data = pd.read_csv(DATA_FILE)

    if "Player" in csv_data.columns:
        player_counts = csv_data["Player"].value_counts().reset_index()
        player_counts.columns = ["Player", "Votes"]
        st.dataframe(player_counts)
    else:
        st.error("CSV columns found: " + str(list(csv_data.columns)))
else:
    st.info("No survey responses yet.")
