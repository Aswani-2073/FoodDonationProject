🍲 Food Donation Project
📌 Overview

The Food Donation Project is a data-driven application that manages food providers, receivers, donations, and claims.
It combines SQL queries, Python (Pandas, SQLite), and a Streamlit web app to deliver insights and visualizations that help in tracking contributions, monitoring food availability, and analyzing distribution trends.

This project was built to simulate a real-world food management system that promotes efficient distribution and reduces food waste.

🚀 Features

✅ SQL-based analysis of providers, receivers, food listings, and claims
✅ Interactive Streamlit dashboard with buttons to view query results
✅ Visual insights using Plotly charts
✅ Organized query outputs for 15+ business questions
✅ Modular structure – ready to expand with ML or advanced analytics

🛠️ Tech Stack

Python (Pandas, SQLite, Streamlit)

SQL (SQLite database with queries)

Plotly for data visualization

VS Code / Jupyter / Colab for development

📊 Example Insights

Which providers contribute the most food?

Which cities have the highest food donations?

Status breakdown of claims (Completed, Pending, Cancelled)

Most demanded meal types (Breakfast, Lunch, Dinner, Snacks)

Monthly trends in claims and donations

📂 Project Structure
FoodDonationProject/
│── app.py              # Streamlit app
│── init_db.py          # Script to create and load database
│── database.db         # SQLite database (after init)
│── requirements.txt    # Project dependencies
│── README.md           # Documentation

⚡ How to Run
1️⃣ Clone the Repository
git clone https://github.com/your-username/FoodDonationProject.git
cd FoodDonationProject

2️⃣ Create Virtual Environment & Install Dependencies
python -m venv .venv
source .venv/bin/activate   # macOS/Linux  
.venv\Scripts\activate      # Windows  

pip install -r requirements.txt

3️⃣ Initialize Database
python init_db.py

4️⃣ Run the Streamlit App
streamlit run app.py

🌍 Real-Life Use Cases

NGOs can monitor food donations & distribution in real time

Restaurants & grocery stores can track excess food contribution

Governments & charities can optimize food waste management

Communities can ensure fair food allocation to those in need

📌 Conclusion

This project demonstrates how data + technology can solve a crucial real-world problem — food wastage.
By connecting providers with receivers and tracking food claims, the system promotes sustainability, transparency, and efficiency in food distribution.
