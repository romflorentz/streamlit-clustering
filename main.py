import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Customer Clusters", initial_sidebar_state="auto")

data = pd.read_csv("mock_data.csv")

st.title("Customer Cluster Insights – March 2025")
st.markdown("""
This dashboard presents consumer segments derived from behavioral and transactional data for a watch and accessories brand.
""")

st.subheader("Cluster Size Overview")
counts = data["CLUSTER"].value_counts().reset_index()
counts.columns = ["Cluster", "Count"]
st.dataframe(counts)
st.caption("This table shows the number of users in each identified cluster.")

spend_features = [
    "TOTAL_SPEND_WATCHES", "TOTAL_SPEND_ACCESSORIES", "TOTAL_SPEND_BAGS", "TOTAL_SPEND_WALLETS", "TOTAL_SPEND_JEWELRY"
]

data["TOTAL_SPEND"] = data[spend_features].sum(axis=1)

spend_data = data.groupby("CLUSTER")[spend_features].mean().reset_index()
spend_data = spend_data.melt(id_vars="CLUSTER", var_name="Category", value_name="Spend")
spend_data["Category"] = spend_data["Category"].str.replace("TOTAL_SPEND_", "").str.capitalize()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Spend per Category by Cluster")
    st.plotly_chart(px.bar(spend_data, x="Category", y="Spend", color="CLUSTER", barmode="group"), use_container_width=True)
    st.caption("This bar chart illustrates the average amount spent on each product category across clusters.")

with col2:
    st.subheader("Total Spend Distribution by Cluster")
    st.plotly_chart(px.bar(data, x="CLUSTER", y="TOTAL_SPEND", color="CLUSTER", barmode="group"), use_container_width=True)
    st.caption("This chart compares the total spend of customers in each cluster, summing all product categories.")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Email Click Rate by Cluster")
    st.plotly_chart(px.bar(data, x="CLUSTER", y="EMAIL_CLICK_RATE", color="CLUSTER", barmode="group"), use_container_width=True)
    st.caption("This chart shows average email engagement levels, based on click rates, across different clusters.")

with col4:
    device_df = data.melt(id_vars="CLUSTER", value_vars=["MOBILE_SESSION_SHARE", "DESKTOP_SESSION_SHARE"], var_name="Device", value_name="Share")
    st.subheader("Device Preference by Cluster")
    st.plotly_chart(px.bar(device_df, x="Device", y="Share", color="CLUSTER", barmode="group"), use_container_width=True)
    st.caption("Device usage distribution shows which clusters prefer mobile or desktop sessions.")

col5, col6 = st.columns(2)

occasions = ["SPENT_ON_BLACK_FRIDAY", "SPENT_IN_HOLIDAY_SEASON", "SPENT_AROUND_VALENTINE"]
occasion_df = data.melt(id_vars="CLUSTER", value_vars=occasions, var_name="Occasion", value_name="Amount")
occasion_df["Occasion"] = occasion_df["Occasion"].str.replace("SPENT_ON_", "").str.replace("SPENT_IN_", "").str.replace("SPENT_AROUND_", "").str.replace("_", " ").str.title()

with col5:
    st.subheader("Seasonal Spending by Cluster")
    st.plotly_chart(px.bar(occasion_df, x="Occasion", y="Amount", color="CLUSTER", barmode="group"), use_container_width=True)
    st.caption("This chart shows how much each cluster spends during specific seasons like Black Friday or Valentine's Day.")

with col6:
    st.subheader("Spend Distribution by Region")
    st.plotly_chart(px.box(data, x="REGION", y="TOTAL_SPEND", color="REGION"), use_container_width=True)
    st.caption("This box plot shows the distribution of total spend across different global regions.")

gender_df = data.melt(id_vars="CLUSTER", value_vars=["IS_MALE", "IS_FEMALE"], var_name="Gender", value_name="Presence")
gender_df = gender_df[gender_df["Presence"] == 1]
gender_df["Gender"] = gender_df["Gender"].str.replace("IS_", "").str.title()
st.subheader("Gender Distribution by Cluster")
st.plotly_chart(px.bar(gender_df, x="CLUSTER", color="Gender", barmode="group"), use_container_width=True)
st.caption("This bar chart provides a breakdown of gender representation across each cluster.")

# Additional Insights
col7, col8 = st.columns(2)

with col7:
    st.subheader("Average Total Spend by Region")
    avg_spend_region = data.groupby("REGION")["TOTAL_SPEND"].mean().reset_index()
    st.plotly_chart(px.bar(avg_spend_region, x="REGION", y="TOTAL_SPEND", color="REGION"), use_container_width=True)
    st.caption("This chart highlights which regions have the highest average spend.")

with col8:
    st.subheader("Region vs Cluster Distribution")
    region_cluster = data.groupby(["REGION", "CLUSTER"]).size().reset_index(name="Count")
    st.plotly_chart(px.bar(region_cluster, x="REGION", y="Count", color="CLUSTER", barmode="group"), use_container_width=True)
    st.caption("This bar chart shows how clusters are distributed across regions.")
