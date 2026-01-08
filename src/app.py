import streamlit as st
import plotly.express as px
from queries import SalesAnalytics

st.set_page_config(page_title="SalesPulse", layout="wide")
st.markdown("<style>.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

st.title("🔹 SalesPulse Analytics")
st.markdown("---")

region = st.sidebar.selectbox("Filter by Region", ["All Regions", "North", "South", "East", "West"])

kpis = SalesAnalytics.get_kpis(region)
trend = SalesAnalytics.get_trend(region)
prods = SalesAnalytics.get_top_products(region)

if not kpis.empty and kpis.iloc[0]['revenue'] is not None:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"${kpis.iloc[0]['revenue']:,.0f}")
    c2.metric("Total Orders", f"{kpis.iloc[0]['orders']}")
    c3.metric("Active Customers", f"{kpis.iloc[0]['active_customers']}")
else:
    st.info("No data found. Please run setup_db.py first.")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Revenue Trend")
    if not trend.empty:
        fig = px.line(trend, x='month', y='revenue', markers=True, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Products")
    if not prods.empty:
        fig = px.bar(prods, x='revenue', y='product_name', orientation='h', template="plotly_white")
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)