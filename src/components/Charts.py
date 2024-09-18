import streamlit as st
import plotly.express as px

def render_chart(data):
    fig = px.line(data, x="Date", y="Value")
    st.plotly_chart(fig)
