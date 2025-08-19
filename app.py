import streamlit as st
import sqlite3
import pandas as pd

# ---- DB Connection ----
conn = sqlite3.connect("food_donation.db")

def run_query(query):
    return pd.read_sql(query, conn)

# ---- Page Config ----
st.set_page_config(
    page_title="🍴 Food Donation Dashboard",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 Food Donation Analytics Dashboard")
st.markdown("Gain insights into **providers, receivers, food types, and claims** in one place.")

# ---- Top Metric Cards ----
col1, col2, col3 = st.columns(3)
col1.metric("🌆 Cities", "320+")
col2.metric("👨‍🍳 Providers", "600+")
col3.metric("🤝 Receivers", "1000+")

st.markdown("---")

# ---- Sidebar Navigation ----
st.sidebar.header("🔎 Navigation")
section = st.sidebar.radio(
    "Go to:",
    ["📊 Providers & Receivers", "🥘 Food Listings", "📦 Claims & Distribution", "📈 Insights", "ℹ️ About"]
)

# ---- Providers & Receivers ----
if section == "📊 Providers & Receivers":
    st.subheader("👨‍🍳 Providers & Receivers by City")
    q1 = """
    SELECT 'Providers' AS Entity, City, COUNT(*) AS Count FROM Providers GROUP BY City
    UNION ALL
    SELECT 'Receivers' AS Entity, City, COUNT(*) AS Count FROM Receivers GROUP BY City
    ORDER BY Entity, Count DESC;
    """
    df1 = run_query(q1)
    st.dataframe(df1, use_container_width=True)
    st.bar_chart(df1.pivot_table(index="City", columns="Entity", values="Count", fill_value=0))

    st.subheader("🏢 Provider Type Contribution")
    q2 = """
    SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
    FROM Food_Listings
    GROUP BY Provider_Type
    ORDER BY Total_Quantity DESC;
    """
    df2 = run_query(q2)
    st.dataframe(df2, use_container_width=True)
    st.bar_chart(df2.set_index("Provider_Type"))

    st.subheader("📇 Contact Information (Example: Mumbai)")
    city = st.text_input("Enter city name:", "Mumbai")
    q3 = f"SELECT Name, Contact, City FROM Providers WHERE City = '{city}';"
    df3 = run_query(q3)
    st.dataframe(df3, use_container_width=True)

# ---- Food Listings ----
elif section == "🥘 Food Listings":
    st.subheader("🤝 Top Receivers by Claims")
    q4 = """
    SELECT r.Receiver_ID, r.Name, COUNT(*) AS Total_Claims
    FROM Claims c
    JOIN Receivers r ON r.Receiver_ID = c.Receiver_ID
    GROUP BY r.Receiver_ID, r.Name
    ORDER BY Total_Claims DESC;
    """
    st.dataframe(run_query(q4), use_container_width=True)

    st.subheader("📦 Total Food Available")
    q5 = "SELECT SUM(Quantity) AS Total_Available_Quantity FROM Food_Listings;"
    st.dataframe(run_query(q5), use_container_width=True)

    st.subheader("🌆 Cities with Most Food Listings")
    q6 = """
    SELECT Location AS City, COUNT(*) AS Listings
    FROM Food_Listings
    GROUP BY Location
    ORDER BY Listings DESC;
    """
    df6 = run_query(q6)
    st.dataframe(df6, use_container_width=True)
    st.bar_chart(df6.set_index("City").head(10))

    st.subheader("🥗 Most Common Food Types")
    q7 = """
    SELECT Food_Type, COUNT(*) AS Items
    FROM Food_Listings
    GROUP BY Food_Type
    ORDER BY Items DESC;
    """
    st.dataframe(run_query(q7), use_container_width=True)

# ---- Claims & Distribution ----
elif section == "📦 Claims & Distribution":
    st.subheader("🍛 Claims per Food Item")
    q8 = """
    SELECT fl.Food_ID, fl.Food_Name, COUNT(c.Claim_ID) AS Total_Claims
    FROM Food_Listings fl
    LEFT JOIN Claims c ON c.Food_ID = fl.Food_ID
    GROUP BY fl.Food_ID, fl.Food_Name
    ORDER BY Total_Claims DESC;
    """
    st.dataframe(run_query(q8), use_container_width=True)

    st.subheader("🏅 Provider with Most Completed Claims")
    q9 = """
    SELECT p.Provider_ID, p.Name, COUNT(*) AS Completed_Claims
    FROM Claims c
    JOIN Food_Listings fl ON fl.Food_ID = c.Food_ID
    JOIN Providers p ON p.Provider_ID = fl.Provider_ID
    WHERE c.Status = 'Completed'
    GROUP BY p.Provider_ID, p.Name
    ORDER BY Completed_Claims DESC
    LIMIT 1;
    """
    st.dataframe(run_query(q9))

    st.subheader("📊 Claims Status Distribution")
    q10 = """
    WITH t AS (SELECT COUNT(*) AS all_rows FROM Claims)
    SELECT Status,
           ROUND(100.0 * COUNT(*) / (SELECT all_rows FROM t), 1) AS Percentage
    FROM Claims
    GROUP BY Status
    ORDER BY Percentage DESC;
    """
    df10 = run_query(q10)
    st.dataframe(df10, use_container_width=True)
    st.bar_chart(df10.set_index("Status"))

# ---- Insights ----
elif section == "📈 Insights":
    st.subheader("📐 Average Quantity Claimed per Receiver")
    q11 = """
    SELECT r.Receiver_ID, r.Name,
           AVG(fl.Quantity) AS Avg_Quantity_Claimed
    FROM Claims c
    JOIN Receivers r ON r.Receiver_ID = c.Receiver_ID
    JOIN Food_Listings fl ON fl.Food_ID = c.Food_ID
    GROUP BY r.Receiver_ID, r.Name
    ORDER BY Avg_Quantity_Claimed DESC;
    """
    st.dataframe(run_query(q11), use_container_width=True)

    st.subheader("🍽️ Most Claimed Meal Type")
    q12 = """
    SELECT fl.Meal_Type, COUNT(*) AS Claims
    FROM Claims c
    JOIN Food_Listings fl ON fl.Food_ID = c.Food_ID
    GROUP BY fl.Meal_Type
    ORDER BY Claims DESC;
    """
    st.dataframe(run_query(q12))

    st.subheader("📦 Total Quantity Donated by Provider")
    q13 = """
    SELECT p.Provider_ID, p.Name, SUM(fl.Quantity) AS Total_Donated
    FROM Food_Listings fl
    JOIN Providers p ON p.Provider_ID = fl.Provider_ID
    GROUP BY p.Provider_ID, p.Name
    ORDER BY Total_Donated DESC;
    """
    st.dataframe(run_query(q13), use_container_width=True)

    st.subheader("📅 Monthly Claim Trends")
    q14 = """
    SELECT strftime('%Y-%m', Timestamp) AS Month, COUNT(*) AS Claims
    FROM Claims
    GROUP BY strftime('%Y-%m', Timestamp)
    ORDER BY Month;
    """
    df14 = run_query(q14)
    st.line_chart(df14.set_index("Month"))

    st.subheader("🌍 Top Cities by Completed Claims")
    q15 = """
    SELECT r.City, COUNT(*) AS Completed_Claims
    FROM Claims c
    JOIN Receivers r ON r.Receiver_ID = c.Receiver_ID
    WHERE c.Status = 'Completed'
    GROUP BY r.City
    ORDER BY Completed_Claims DESC;
    """
    df15 = run_query(q15)
    st.dataframe(df15, use_container_width=True)
    st.bar_chart(df15.set_index("City").head(10))

# ---- About ----
elif section == "ℹ️ About":
    st.subheader("ℹ️ About This Dashboard")
    st.info("""
    This project analyzes **food donations, providers, receivers, food availability, and claims**.
    Built with:
    - SQL (SQLite)
    - Python (Pandas)
    - Streamlit (Interactive Dashboard)
    """)
