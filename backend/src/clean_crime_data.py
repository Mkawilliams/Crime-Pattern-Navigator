import pandas as pd
import os

base_dir = os.path.dirname(__file__)  # points code to go up one level
C_Data_DIR = os.path.join(
    base_dir, "..", "data", "processed_data"
)  # directory containing processed CSV files
C_Data_DIR = os.path.abspath(C_Data_DIR)  # directory containing PDF files

# Read the CSV file into a DataFrame
df = pd.read_csv(os.path.join(C_Data_DIR, "np_crime_data.csv"))

# Reset the index of the DataFrame
df.reset_index(drop=True, inplace=True)

# Remove rows where 'Offence' is 'Total' and 'Sub Total'
df = df[df["Offence"] != "Sub Total"]
df = df[df["Offence"] != "Total"]
df = df[df["Offence"] != "TOTAL"]

# Fix blank offences
mask = df["Offence"].isna() | (df["Offence"] == "")

# If Offence is blank, fill it with the previous offence + "From Vehicle"
for i in df[mask].index:
    previous_offence = df.loc[i - 1, "Offence"]

    if previous_offence == "Stealing" or (previous_offence == "Stealing"):
        df["Offence"] = df["Offence"].replace({"Vehicle": "Stealing from Vehicle"})
        df.loc[i, "Offence"] = "Stealing from Vehicle"

    elif previous_offence == "Robbery":
        df.loc[i, "Offence"] = "Attempted Robbery"

# Fix the "Shop breaking" offence to "Shopbreaking"
df["Offence"] = df["Offence"].replace({"Shop breaking": "Shopbreaking"})

# Save the cleaned data to a new CSV file
df.to_csv(os.path.join(C_Data_DIR, "cleaned_np_crime_data.csv"), index=False)
