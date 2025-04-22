import streamlit as st
import plotly.express as px
import os
import pandas as pd

def view_saved_graphs(base_save_path):
    saved_files = [f for f in os.listdir(base_save_path) if f.endswith('.csv')]
    
    if not saved_files:
        st.write("No saved data available.")
        return
    
    uploaded_files = st.sidebar.file_uploader("Upload saved CSV files", type="csv", accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            save_path = os.path.join(base_save_path, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.experimental_rerun()

    selected_file = st.sidebar.selectbox("Select a file to view", saved_files)
    if selected_file:
        df = pd.read_csv(os.path.join(base_save_path, selected_file))
        graph_title = st.sidebar.text_input("Graph Title", selected_file)

        # Check if ElapsedTime column exists, otherwise use another valid column
        x_column = 'ElapsedTime' if 'ElapsedTime' in df.columns else df.columns[0]

        y_column = df.columns[1]  # Always use the second column for y_column
        plot_type = "line"  # Always use "line" for plot_type

        # Display the graph
        fig = px.line(df, x=x_column, y=y_column, color='Source', title=graph_title, markers=True) if plot_type == "line" else px.histogram(df, x=y_column, color='Source', title=graph_title)
        fig.update_layout(width=400, height=400, autosize=True, xaxis_range=[0, 120])  # Limiting x-axis to 120 minutes
        st.plotly_chart(fig, use_container_width=True)

        if st.sidebar.button(f"Delete {selected_file}"):
            os.remove(os.path.join(base_save_path, selected_file))
            st.experimental_rerun()

        if st.sidebar.button("Apply Changes"):
            st.experimental_rerun()
