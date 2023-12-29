#C:\Users\lucan\PycharmProjects\dashboard_1\data

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df_top100_books = pd.read_csv("data/Amazon_top100_bestselling_books_2009to2021.csv")


price_max = df_top100_books["price"].max()
price_min = df_top100_books["price"].min()


max_price = st.sidebar.slider("Price Range", price_min, price_max, price_max)

df_books = df_top100_books[df_top100_books["price"] <= max_price]

fig_year = px.bar(df_books["year"].value_counts())
fig_price = px.histogram(df_books["price"])

df_books

col1, col2 = st.columns(2)

col1.plotly_chart(fig_year)
col2.plotly_chart(fig_price)