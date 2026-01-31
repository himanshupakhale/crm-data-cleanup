import pandas as pd
import re


print("Starting CRM data cleaning...")


# Step 1: Load file
try:
    df = pd.read_csv("customers_raw.csv")
    print("File loaded successfully")
except Exception as e:
    print("Error loading file:", e)
    exit()


print("Total rows before cleaning:", len(df))
print("Columns:", list(df.columns))


# Step 2: Remove duplicate rows
print("Checking duplicates...")

before_dup = len(df)
df = df.drop_duplicates()
after_dup = len(df)

print("Duplicates removed:", before_dup - after_dup)
print("Rows after duplicate removal:", after_dup)


# Step 3: Check missing values
print("Checking missing values...")

missing_email = df["Email"].isnull().sum()
missing_phone = df["Phone"].isnull().sum()

print("Missing emails:", missing_email)
print("Missing phones:", missing_phone)


print("Removing rows with missing email or phone...")

df = df.dropna(subset=["Email", "Phone"])

print("Rows after removing missing values:", len(df))


# Step 4: Email validation
print("Validating email format...")

email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

valid_email = []
invalid_count = 0


for email in df["Email"]:

    if re.match(email_pattern, str(email)):
        valid_email.append(True)
    else:
        valid_email.append(False)
        invalid_count += 1


df = df[valid_email]

print("Invalid emails removed:", invalid_count)
print("Rows after email validation:", len(df))


# Step 5: Phone number cleaning
print("Cleaning phone numbers...")


def clean_phone(phone):

    phone = str(phone)

    phone = re.sub(r"\D", "", phone)

    if len(phone) < 10:
        return None

    return phone


cleaned_phone = []
invalid_phone = 0


for p in df["Phone"]:

    new_phone = clean_phone(p)

    if new_phone is None:
        cleaned_phone.append(None)
        invalid_phone += 1
    else:
        cleaned_phone.append(new_phone)


df["Phone"] = cleaned_phone


print("Invalid phone numbers:", invalid_phone)


print("Removing rows with invalid phone numbers...")

df = df.dropna(subset=["Phone"])

print("Rows after phone cleaning:", len(df))


# Step 6: Standardize text fields
print("Standardizing name and city columns...")

df["Name"] = df["Name"].str.strip().str.title()
df["City"] = df["City"].str.strip().str.title()


# Step 7: Final check
print("Final dataset info:")
print(df.info())


# Step 8: Save cleaned file
try:
    df.to_csv("customers_cleaned.csv", index=False)
    print("Cleaned file saved as customers_cleaned.csv")
except Exception as e:
    print("Error saving file:", e)


print("CRM data cleaning completed.")