
import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# reading the data from excel
df = pd.read_csv('C://Users//kwaku//Desktop//POWER BI//DataDNA-Dataset-Challenge-Animal-Shelter-Operations-December-2025//python//animal.csv')
st.set_page_config(layout="wide") # creating a page layout
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
#insecting an image
image = Image.open(r'C:\Users\kwaku\Desktop\POWER BI\DataDNA-Dataset-Challenge-Animal-Shelter-Operations-December-2025\python\animal shelter.jpg')

col1, col2 = st.columns([0.5,1.0])
with col1:
    st.image(image,width=400)

html_title = """ 
    cd<style>
    .title-test {
    font-weight:bold;
    padding:5px
    border-radius:6px
    }
    </style>
    <center><h1 class="title-test">Animal Shelter Operations Analytics</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1,0.45,0.45]) #insecting a date
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n{box_date}")

# first chart which is bar chart
with col4:
    fig = px.bar(
        df.groupby("Intake Type")["Animal ID"].count().reset_index(),
        x="Intake Type",
        y="Animal ID",
        labels={"Animal ID": "Count of Animals"},
        title="Intake Type Count",
        template="gridon",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# Convert Outcome Date column to datetime
df["Outcome Date"] = pd.to_datetime(df["Outcome Date"], errors="coerce")
# Create Month column
df["Month"] = df["Outcome Date"].dt.strftime("%b")

# Calculate Live Release Rate per Month
result = (
    df.groupby("Month")["outcome_is_alive"]
    .mean()
    .reset_index()
)

# Line Chart
with col5:
    fig1 = px.line(
        result,
        x="Month",
        y="outcome_is_alive",
        title="Live Release Rate Trend",
        markers=True,
        template="gridon",
        height=500
    )
    st.plotly_chart(fig1, use_container_width=True)

# line to divide to chart up
st.divider()

# Treemap needs a numeric column (Animal Count)
treemap = (
    df.groupby("Animal Type")["Animal ID"]
      .count()
      .reset_index()
      .rename(columns={"Animal ID": "Animal Count"})
)

# Layout: second column holds the treemap
_, col7 = st.columns([0.1, 1])

# Create Treemap
fig4 = px.treemap(
    treemap,
    path=["Animal Type"],
    values="Animal Count",
    color="Animal Type",
    hover_data={"Animal Count": True},
    height=700
)

fig4.update_traces(textinfo="label+value")

with col7:
    st.subheader(":point_right: Species Breakdown")
    st.plotly_chart(fig4, use_container_width=True)

# Prepare data
pie_data = (
    df.groupby("Outcome Type")["Animal ID"]
      .count()
      .reset_index()
      .rename(columns={"Animal ID": "Animal Count"})
)

# Sort and keep Top 5
pie_data = pie_data.sort_values("Animal Count", ascending=False).head(5)

# Layout (optional)
_, col8 = st.columns([0.1, 1])

# Create Pie Chart
fig5 = px.pie(
    pie_data,
    names="Outcome Type",
    values="Animal Count",
    title="Top 5 Outcome Types",
    hole=0.4   # donut style (optional)
)

fig5.update_traces(textinfo="label+percent")

with col8:
    st.subheader(":point_right: Top 5 Outcome Types")
    st.plotly_chart(fig5, use_container_width=True)

