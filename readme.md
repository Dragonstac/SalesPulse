# 🔹 SalesPulse Analytics

**A Modern Business Intelligence Dashboard for Sales & Operations Planning.**

SalesPulse is a full-stack analytics application designed to simulate real-world business intelligence workflows. It ingests raw transactional data into a normalized PostgreSQL database, processes it using Python (SQLAlchemy/Pandas), and visualizes key performance indicators (KPIs) via an interactive Streamlit dashboard.

---

## 🏗️ Architecture & Tech Stack

This project follows industry-standard data engineering practices:

* **Database:** PostgreSQL (Relational Data Warehousing)
* **Backend Logic:** Python, SQLAlchemy, Pandas (ETL & Analysis)
* **Frontend:** Streamlit (Interactive Dashboard)
* **Visualization:** Plotly (Dynamic Charts)
* **Infrastructure:** Docker-ready, Environment Variable Configuration

---

## ⚡ Key Features

* **Automated Data Seeding:** Instantly generates thousands of mock transactions (Orders, Customers, Products, Regions) for testing.
* **Advanced SQL Analytics:** Uses Complex SQL (Joins, Aggregations, Window Functions) to calculate Month-over-Month growth and retention.
* **Interactive Filtering:** Real-time data slicing by Region (North, South, East, West).
* **Business KPIs:** Tracks Total Revenue, Active Customers, AOV (Average Order Value), and Top Selling Products.

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.10+
* PostgreSQL installed locally (or via Docker)

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/salespulse-analytics.git](https://github.com/yourusername/salespulse-analytics.git)
cd salespulse-analytics