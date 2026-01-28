import pandas as pd
import re

# Load dataset
df = pd.read_csv("customers_raw.csv")

# Remove duplicates
df = df.drop_duplicates()

# Remove rows with missing email or phone
df = df.dropna(subset=["Email", "Phone"])

# Validate email
pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
df = df[df["Email"].str.match(pattern)]

# Clean phone numbers
df["Phone"] = df["Phone"].astype(str).str.replace(r"\D", "", regex=True)

# Save cleaned file
df.to_csv("customers_cleaned.csv", index=False)

print("Cleaning complete")