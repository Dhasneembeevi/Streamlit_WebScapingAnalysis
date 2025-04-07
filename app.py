import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Price Analytics Dashboard", layout="wide")
st.title("📊 Price Analytics Dashboard")


uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
import pandas as pd

import streamlit as st
import pandas as pd

df = pd.read_csv("product_data.csv")
specs_df = df[df['SECTION'].fillna(method='ffill') == 'Specifications']
specs_df = specs_df[specs_df['KEY'].notna()]

st.subheader("📋 Specifications")

for index, row in specs_df.iterrows():
    st.markdown(f"**{row['KEY']}**: {row['VALUE']}")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    df['datetime'] = pd.to_datetime(df['datetime'], dayfirst=True)
    df['date'] = df['datetime'].dt.date
    df['month'] = df['datetime'].dt.to_period('M')
    df['year'] = df['datetime'].dt.year

    st.sidebar.header("📅 Filter Options")
    date_range = st.sidebar.date_input("Select Date Range", [df['date'].min(), df['date'].max()])
    if len(date_range) == 2:
        df = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔽 Min Price", f"₹{df['price'].min():,.0f}")
    with col2:
        st.metric("🔼 Max Price", f"₹{df['price'].max():,.0f}")
    with col3:
        st.metric("📉 Average Price", f"₹{df['price'].mean():,.0f}")

    st.markdown("---")

    st.subheader("📈 Price Over Time")
    st.line_chart(df.set_index('datetime')['price'])

    st.subheader("🗓️ Monthly Average Prices")
    monthly_avg = df.groupby(df['datetime'].dt.to_period('M')).mean(numeric_only=True).reset_index()
    monthly_avg['datetime'] = monthly_avg['datetime'].astype(str)
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=monthly_avg, x='datetime', y='price', marker='o', ax=ax)
    plt.xticks(rotation=45)
    plt.title("Monthly Average Price")
    st.pyplot(fig)

    st.subheader("📊 Price Distribution")
    fig2, ax2 = plt.subplots()
    sns.histplot(df['price'], kde=True, ax=ax2)
    st.pyplot(fig2)

    st.subheader("📋 Recent Price Entries")
    st.dataframe(df.sort_values(by='datetime', ascending=False).head(20))

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Download Filtered Data",
        data=csv,
        file_name='filtered_price_data.csv',
        mime='text/csv'
    )

else:
    st.info("👆 Please upload a CSV file to begin analysis.")
