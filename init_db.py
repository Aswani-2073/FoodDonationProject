import sqlite3
import pandas as pd

# Connect (creates db if not exists)
conn = sqlite3.connect("food_donation.db")

# Load CSVs
providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")
food_listings = pd.read_csv("food_listings_data.csv")
claims = pd.read_csv("claims_data.csv")

# Save to SQLite tables
providers.to_sql("Providers", conn, if_exists="replace", index=False)
receivers.to_sql("Receivers", conn, if_exists="replace", index=False)
food_listings.to_sql("Food_Listings", conn, if_exists="replace", index=False)
claims.to_sql("Claims", conn, if_exists="replace", index=False)

print("✅ Database initialized with all tables!")
conn.close()
