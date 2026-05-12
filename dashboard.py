import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📚 Books Price Analytics Dashboard")

df = pd.read_csv("books.csv")

# -------------------------
# 📊 SUMMARY METRICS
# -------------------------
st.subheader("Key Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Average Price", f"£{df['price'].mean():.2f}")
col2.metric("Min Price", f"£{df['price'].min():.2f}")
col3.metric("Max Price", f"£{df['price'].max():.2f}")

# -------------------------
# 📈 HISTOGRAM
# -------------------------
st.subheader("Price Distribution")

fig, ax = plt.subplots()
ax.hist(df["price"], bins=20)
ax.set_xlabel("Price (£)")
ax.set_ylabel("Number of Books")

st.pyplot(fig)

# -------------------------
# 📄 RAW DATA
# -------------------------
st.subheader("Dataset Preview")
st.dataframe(df)