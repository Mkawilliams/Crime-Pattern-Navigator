import pdfplumber
import pandas as pd
import re
import os

columns = [
    "Offence",
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
    "Total",
]

all_rows = []

base_dir = os.path.dirname(__file__)  # points code to go up one level
PDF_DIR = os.path.join(base_dir, "..", "data", "raw_pdfs")
PDF_DIR = os.path.abspath(PDF_DIR)  # directory containing PDF files

output_dir = os.path.join(
    base_dir, "..", "data", "processed_data"
)  # directory to save the output CSV
os.makedirs(output_dir, exist_ok=True)

all_tables = []  # list to hold all extracted tables

print("Scanning PDFs in:", PDF_DIR)

for filename in os.listdir(PDF_DIR):
    if filename.endswith(".pdf"):
        year = re.search(r"\d{4}", filename).group()
        path = os.path.join(PDF_DIR, filename)
        print("Opening:", filename)

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                text = page.extract_text()
                if (
                    (
                        text
                        and "New Providence District" in text
                        and "Divisional Breakdown" in text
                    )
                    or (text and "New Providence District Breakdown" in text)
                    or (
                        text
                        and "New Providence District" in text
                        and "Divisional Breakdown 2021" in text
                    )
                ):
                    print(f"  ✅ Match on page {page.page_number}")

                lines = text.split("\n")
                previous_text = ""

                for line in lines:
                    # Remove commas
                    clean_line = line.replace(",", "")

                    if not clean_line:
                        continue  # Skip empty lines

                    # Skip known headers
                    if any(
                        header in clean_line
                        for header in [
                            "A CB C E FH NE NW PI SC SE S SW W Total",
                            "Divisional Breakdown",
                            "New Providence District",
                            "Person",
                            "Property",
                        ]
                    ):
                        previous_text = ""  # Reset previous text when hitting a header
                        continue

                    # Find all numbers in line
                    numbers = re.findall(r"\d+", clean_line)

                    # Valid crime row must have 14 numbers
                    if len(numbers) == 14:
                        offence_part = re.split(r"\d", clean_line)[
                            0
                        ].strip()  # Get text before first number

                        # Merg only if previous text exists and is short
                        if previous_text and not len(previous_text.split()) <= 3:
                            offence = previous_text + " " + offence_part
                        else:
                            # Extract offence name (text before first number)
                            offence = offence_part  # Remove leading/trailing whitespace

                        offence = offence.strip()  # Final clean offence name

                        row = [offence] + numbers  # Create row with offence and numbers
                        row.append(filename)  # Add source file name
                        row.append(year)  # Add year extracted from file name

                        all_rows.append(row)

                        previous_text = ""  # Reset previous text after using it

                    else:
                        # Store possible split offence name for next line if it does not contain numbers
                        if len(clean_line.split()) <= 3:
                            previous_text = clean_line  # Store current line as previous text for next iteration
                        else:
                            previous_text = ""  # Reset if line is not short enough to be part of offence name

final_columns = columns + ["Source_File", "Year"]

df = pd.DataFrame(
    all_rows, columns=final_columns
)  # Create DataFrame from extracted rows with defined columns
output_path = os.path.join(
    output_dir, "np_crime_data.csv"
)  # Define output path for CSV
df.to_csv(output_path, index=False)  # Save DataFrame to CSV without index

print("✅ CSV saved to:", os.path.join(output_dir, "np_crime_data.csv"))

print("Extraction Complete")
