import streamlit as st
import plotly.express as px
import pandas as pd

def plot_combined_average(df, y_column, additional_columns, group_columns, plot_type):
    st.write(f"Combined Detailed Average Analysis")
    st.write(f"Comparing {y_column} and additional columns grouped by {', '.join(group_columns)} and Source")

    # Create a new column for a clearer legend dynamically based on group_columns
    df['Source'] = df.apply(lambda row: f"{row['Source']} ({', '.join([str(row[col]) for col in group_columns])})", axis=1)

    if plot_type == "line":
        fig = px.line(df, x='ElapsedTime', y=y_column, color='Source', title=f'Combined {y_column} Analysis', markers=True)
    elif plot_type == "histogram":
        fig = px.histogram(df, x=y_column, color='Source', title=f'Combined {y_column} Distribution')

    fig.update_layout(width=800, height=400)
    st.plotly_chart(fig, use_container_width=True)

    for col in additional_columns:
        if plot_type == "line":
            fig = px.line(df, x='ElapsedTime', y=col, color='Source', title=f'Combined {col} Analysis', markers=True)
        elif plot_type == "histogram":
            fig = px.histogram(df, x=col, color='Source', title=f'Combined {col} Distribution')

        fig.update_layout(width=800, height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Option to save the data
    if st.button("Save this combined data"):
        if 'saved_data' not in st.session_state:
            st.session_state['saved_data'] = []
        st.session_state['saved_data'].append(df)
        st.success("Data saved successfully!")
