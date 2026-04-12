import sqlite3
import pandas as pd

# This script reads the cleaned crime data from a CSV file, transforms it into a long format suitable for SQL storage, and then loads it into a SQLite database.
df = pd.read_csv("backend/data/processed_data/cleaned_np_crime_data.csv")

# The columns representing the divisions are specified in a list.
division_columns = [
    "A",
    "CB",
    "C",
    "E",
    "FH",
    "NE",
    "NW",
    "PI",
    "SC",
    "SE",
    "S",
    "SW",
    "W",
]

# The DataFrame is transformed from a wide format to a long format using the melt function, which creates a row for each division's crime count.
long_df = df.melt(
    id_vars=["Offence", "Year"],
    value_vars=division_columns,
    var_name="division_code",
    value_name="crime_count",
)

long_df = long_df[long_df["crime_count"] > 0]

# Connect to the SQLite database (or create it if it doesn't exist) and load the long format DataFrame into a table named "crime_data". If the table already exists, the new data will be appended to it.
conn = sqlite3.connect("crime.db")

long_df.to_sql("crime_data", conn, if_exists="append", index=False)

conn.close()

print("Crime data loaded into SQL")
