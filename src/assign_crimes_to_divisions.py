import sqlite3
import pandas as pd

df = pd.read_csv("data/processed_data/cleaned_np_crime_data.csv")

division_columns = [
    "A","CB","C","E","FH","NE","NW","PI","SC","SE","S","SW","W"
]

long_df = df.melt(
    id_vars=["Offence", "Year"],
    value_vars=division_columns,
    var_name="division_code",
    value_name="crime_count"
)

long_df = long_df[long_df["crime_count"] > 0]

conn = sqlite3.connect("crime.db")

long_df.to_sql("crime_data", conn, if_exists="append", index=False)

conn.close()

print("Crime data loaded into SQL")