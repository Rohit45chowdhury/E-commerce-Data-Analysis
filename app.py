import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.title("E-commerce Data Analysis Web App")

df = None
csv_path = os.path.join(os.path.dirname(__file__), "Amazon Sale Report copy.csv")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully")
elif os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.success("CSV loaded from local file")
else:
    st.warning("CSV not found. Please upload your dataset")

if df is not None:
    df.columns = df.columns.str.strip()

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Information")
    st.write("Shape:", df.shape)

    if 'Amount' in df.columns:
        total_revenue = df['Amount'].sum()
        st.metric(label="Total Revenue Generated", value=f"₹{total_revenue:,.2f}")

    if 'Date' in df.columns and 'Amount' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Month'] = df['Date'].dt.to_period('M').astype(str)
        monthly_revenue = df.groupby('Month')['Amount'].sum().reset_index()

        st.subheader("Monthly Revenue Trend")
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        sns.lineplot(x='Month', y='Amount', data=monthly_revenue, marker='o', color='green', ax=ax1)
        ax1.set_title("Monthly Revenue Trend")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

    if 'Category' in df.columns and 'Amount' in df.columns:
        st.subheader("Revenue by Product Category")
        category_revenue = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).reset_index()
        st.dataframe(category_revenue)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        sns.barplot(x='Amount', y='Category', data=category_revenue, color='green', ax=ax2)
        for i, (value, category) in enumerate(zip(category_revenue['Amount'], category_revenue['Category'])):
            ax2.text(value, i, f"₹{value:,.0f}", va='center', ha='left', fontsize=9)
        ax2.set_title("Revenue by Product Category")
        ax2.set_xlabel("Revenue (₹)")
        ax2.set_ylabel("Category")
        st.pyplot(fig2)

    if 'Order ID' in df.columns and 'Amount' in df.columns:
        st.subheader("Average Order Value (AOV)")
        monthly_orders = df.groupby('Month')['Order ID'].nunique().reset_index().sort_values(by='Month')
        total_orders = df['Order ID'].nunique()
        average_order_value = total_revenue / total_orders if total_orders > 0 else 0

        st.write("Total Orders:", total_orders)
        st.write("Average Order Value (₹):", round(average_order_value, 2))

        st.subheader("Monthly Orders")
        st.dataframe(monthly_orders)
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        sns.barplot(x='Month', y='Order ID', data=monthly_orders, color='skyblue', ax=ax3)
        ax3.set_title("Monthly Orders Count")
        ax3.set_xlabel("Month")
        ax3.set_ylabel("Number of Orders")
        plt.xticks(rotation=45)
        st.pyplot(fig3)

    if 'SKU' in df.columns and 'Amount' in df.columns:
        st.subheader("Top 5 Products by Revenue")
        top_products = df.groupby('SKU')['Amount'].sum().sort_values(ascending=False).head(5)
        st.dataframe(top_products)
        fig4, ax4 = plt.subplots(figsize=(8, 4))
        sns.barplot(x=top_products.values, y=top_products.index, color='purple', ax=ax4)
        ax4.set_title("Top 5 Products by Revenue")
        st.pyplot(fig4)

    if 'Order ID' in df.columns and 'Amount' in df.columns:
        st.subheader("Top 5 Most Valuable Customers")
        customer_value = df.groupby('Order ID')['Amount'].sum().sort_values(ascending=False).head(5)
        st.dataframe(customer_value)
        fig5, ax5 = plt.subplots(figsize=(8, 4))
        sns.barplot(x=customer_value.values, y=customer_value.index, color='green', ax=ax5)
        ax5.set_title("Top 5 Customers by Total Spend")
        ax5.set_xlabel("Revenue")
        ax5.set_ylabel("Order ID")
        st.pyplot(fig5)

    if 'ship-city' in df.columns and 'ship-state' in df.columns and 'Amount' in df.columns:
        st.subheader("Top Cities and States by Revenue")
        col1, col2 = st.columns(2)

        with col1:
            city_revenue = df.groupby("ship-city")["Amount"].sum().reset_index().sort_values(by="Amount", ascending=False).head(5)
            st.write("Top 5 Cities by Revenue")
            st.dataframe(city_revenue)
            fig6, ax6 = plt.subplots(figsize=(6, 4))
            sns.barplot(x="Amount", y="ship-city", data=city_revenue, color='green', ax=ax6)
            st.pyplot(fig6)

        with col2:
            state_revenue = df.groupby("ship-state")["Amount"].sum().reset_index().sort_values(by="Amount", ascending=False).head(5)
            st.write("Top 5 States by Revenue")
            st.dataframe(state_revenue)
            fig7, ax7 = plt.subplots(figsize=(6, 4))
            sns.barplot(x="Amount", y="ship-state", data=state_revenue, color='purple', ax=ax7)
            st.pyplot(fig7)

    if 'Order ID' in df.columns and 'Amount' in df.columns:
        st.subheader("Customer Summary by Order ID")
        order_id_input = st.text_input("Enter Order ID")
        search_button = st.button("Search Customer")
        if search_button and order_id_input:
            order_data = df[df["Order ID"].astype(str) == order_id_input]
            if order_data.empty:
                st.warning("No record found for this Order ID")
            else:
                total_orders_customer = order_data.shape[0]
                total_revenue_customer = order_data["Amount"].sum()
                city = order_data["ship-city"].values[0] if 'ship-city' in order_data.columns else "N/A"
                state = order_data["ship-state"].values[0] if 'ship-state' in order_data.columns else "N/A"
                sales_channel = order_data["Sales Channel"].values[0] if 'Sales Channel' in order_data.columns else "N/A"
                st.write("Total Orders:", total_orders_customer)
                st.write("Total Revenue: ₹{:,.2f}".format(total_revenue_customer))
                st.write("City:", city)
                st.write("State:", state)
                st.write("Sales Channel:", sales_channel)
