import streamlit as st
import pandas as pd
import plotly.express as px

st.title("A Cut Above Historical Standings (2022–2025)")

# -----------------------------
# Raw placement table
# -----------------------------
data = {
    "Place": [18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1],
    "2022": ["", "", "", "","Jimmy", "Brandon L", "Ian", "mell2real", "Leo", "Kevin", "Jeff", "Jon", "CJ", "Brandon", "Harry", "Jonathan", "Hoffman", "Mat"],
    "2023": ["Harry", "Harry G", "Myles", "Ed", "Shea", "Jon", "Jimmy", "Mat", "Kevin", "Brandon", "Ian", "Nick", "CJ", "Kyle", "Jonathan", "Hunter", "Jeff", "Leo"],
    "2024": ["Ed", "CJ", "Harry", "Brandon", "Jimmy", "Hunter", "Jon", "Shea", "Jonathan", "Leo", "Myles", "Jordan", "Ian", "Kyle", "Kevin", "Nick", "Mat", "Jeff"],
    "2025": ["Ian", "Jimmy", "Shea", "Hunter", "Harry", "Jordan", "Leo", "Jon", "Kyle", "CJ", "Ed", "Jeff", "Kevin", "Myles", "Nick", "Brandon", "Jonathan", "Mat"]
}

managers_2025 = {
    "Ian", "Jimmy", "Shea", "Hunter", "Harry", "Jordan", "Leo", "Jon",
    "Kyle", "CJ", "Ed", "Jeff", "Kevin", "Myles", "Nick", "Brandon",
    "Jonathan", "Mat"
}

df = pd.DataFrame(data)

# -----------------------------
# Reshape into long format
# -----------------------------
long_df = df.melt(id_vars="Place", var_name="Year", value_name="Manager")

# Restrict to only managers who appear in 2025
long_df = long_df[long_df["Manager"].isin(managers_2025)]

# Force Year to be discrete by converting to string
long_df["Year"] = long_df["Year"].astype(str)

# -----------------------------
# Plotly figure (legend controls highlighting)
# -----------------------------
fig = px.line(
    long_df,
    x="Year",
    y="Place",
    color="Manager",
    markers=True,
    hover_data=["Manager", "Year", "Place"],
    category_orders={"Year": ["2022", "2023", "2024", "2025"]}  # <-- force discrete axis
)

# Reverse y-axis (1 = best)
fig.update_yaxes(autorange="reversed")

# Force categorical x-axis (prevents 2,023.5)
fig.update_xaxes(type="category")


fig.update_layout(
    height=600,
    legend_title_text="Click to show/hide managers",
    title="Standings by Season",
)

st.plotly_chart(fig, use_container_width=True)


# -----------------------------
# Build summary table
# -----------------------------

def is_bottom4(place, year):
    # 2022: bottom 4 = 11–14
    if year == "2022":
        return 11 <= place <= 14
    # 2023–2025: bottom 4 = 15–18
    return place >= 15

summary = (
    long_df.groupby("Manager")
           .agg(
               seasons_played=("Year", "count"),

               top4_finishes=("Place", lambda x: sum(x <= 4)),

               first_place=("Place", lambda x: sum(x == 1)),

               bottom4_finishes=("Place", lambda x: sum(
                   is_bottom4(place, year)
                   for place, year in zip(x, long_df.loc[x.index, "Year"])
               ))
           )
           .reset_index()
)

# Sort by top‑4 finishes (descending)
summary = summary.sort_values(
    by=["top4_finishes", "first_place", "seasons_played"],
    ascending=[False, False, False]
)

st.subheader("Manager Summary")
st.dataframe(summary, hide_index=True, use_container_width=True)