import streamlit as st
import plotly.express as px
import pandas as pd

def plot_detailed_average(df, y_column, additional_columns, group_columns, file_name, plot_type):
    st.write(f"Detailed Average Analysis for {file_name}")
    st.write(f"Comparing {y_column} and additional columns grouped by {', '.join(group_columns)}")

    if plot_type == "line":
        fig = px.line(df, x='ElapsedTime', y=y_column, color=group_columns[0] if group_columns else None, title=f'{y_column} Analysis for {file_name}')
    elif plot_type == "histogram":
        fig = px.histogram(df, x=y_column, color=group_columns[0] if group_columns else None, title=f'{y_column} Distribution for {file_name}')

    fig.update_layout(width=800, height=400)
    st.plotly_chart(fig, use_container_width=True)

    for col in additional_columns:
        if plot_type == "line":
            fig = px.line(df, x='ElapsedTime', y=col, color=group_columns[0] if group_columns else None, title=f'{col} Analysis for {file_name}')
        elif plot_type == "histogram":
            fig = px.histogram(df, x=col, color=group_columns[0] if group_columns else None, title=f'{col} Distribution for {file_name}')

        fig.update_layout(width=800, height=400)
        st.plotly_chart(fig, use_container_width=True)
