import pandas as pd
import os
from langchain.tools import tool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "destinations.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError("destinations.csv not found")

df = pd.read_csv(DATA_PATH)
df.fillna("", inplace=True)


def clean_list(text):
    return [x.strip() for x in str(text).split(",") if x.strip()]


@tool
def search_destinations(query: str) -> str:
    """Search Sri Lanka destinations by keyword/category."""
    query = query.lower()
    results = []

    for _, row in df.iterrows():
        searchable = " ".join(str(v).lower() for v in row.values)

        score = 0
        for word in query.split():
            if word in searchable:
                score += 1

        if score > 0:
            results.append((score, row))

    if not results:
        return "No destinations found."

    results.sort(reverse=True, key=lambda x: x[0])

    output = ""
    for i, (_, row) in enumerate(results[:5], 1):
        output += f"""
{i}. {row['name']} ({row['category']})
Region: {row['region']}
Best Time: {row['best_time']}
Budget: {row['budget_level']}
Highlights: {row['highlights']}

"""

    return output


@tool
def get_attractions(city: str) -> str:
    """Get attractions of a destination."""
    match = df[df["name"].str.lower() == city.lower()]

    if match.empty:
        return "Destination not found."

    row = match.iloc[0]

    return f"""
{row['name']} Attractions:

{row['description']}

Top Attractions:
{row['attractions']}

Highlights:
{row['highlights']}
"""


@tool
def get_travel_tips(city: str) -> str:
    """Get travel tips for a destination."""
    match = df[df["name"].str.lower() == city.lower()]

    if match.empty:
        return "Destination not found."

    row = match.iloc[0]

    return f"""
Travel Tips for {row['name']}:

Best Time: {row['best_time']}
Budget: {row['budget_level']}
Distance: {row['distance_from_colombo_km']} km

Tips:
{row['travel_tips']}
"""


@tool
def compare_destinations(cities: str) -> str:
    """Compare destinations separated by comma or vs."""
    if "vs" in cities.lower():
        names = [x.strip() for x in cities.lower().split("vs")]
    else:
        names = [x.strip() for x in cities.split(",")]

    rows = []

    for name in names:
        match = df[df["name"].str.lower() == name.lower()]
        if not match.empty:
            rows.append(match.iloc[0])

    if len(rows) < 2:
        return "Need at least 2 valid destinations."

    output = "Comparison:\n\n"

    for row in rows:
        output += f"""
{row['name']}
Category: {row['category']}
Region: {row['region']}
Budget: {row['budget_level']}
Best Time: {row['best_time']}

"""

    return output


@tool
def list_all_categories(_: str = "") -> str:
    """List all categories."""
    groups = df.groupby("category")["name"].apply(list)

    output = ""

    for cat, names in groups.items():
        output += f"{cat}: {', '.join(names)}\n\n"

    return output