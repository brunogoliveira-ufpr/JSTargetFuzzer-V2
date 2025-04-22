import os
import streamlit as st
import pandas as pd
from data_processing.load_data import load_data
from analysis.detailed_average_analysis import run_detailed_average_analysis
from plotting.view_saved_graphs import view_saved_graphs
# from data_processing.compare_weights_analysis import compare_weights_analysis
from data_processing.files_analysis.compare_weights_analysis import compare_weights_analysis

# Defina a configuração da página para largura total
# st.set_page_config(layout="wide")

st.title("Dynamic Data Analysis")

# Sidebar for navigation
page = st.sidebar.selectbox("Select a page", ["Detailed Average Analysis", "View Saved Graphs", "Compare Weights Analysis"])

if page == "Detailed Average Analysis":
    # File uploader to select CSV files
    uploaded_files = st.sidebar.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)

    if uploaded_files:
        # Load selected files
        dataframes = [pd.read_csv(file) for file in uploaded_files]
        
        # Remove empty dataframes before concatenating
        dataframes = [df for df in dataframes if not df.empty]
        
        # Combine dataframes if multiple files are loaded
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)

            # Select type of analysis
            analysis_type = st.sidebar.selectbox("Select type of analysis", ["Detailed Average Analysis"])
            
            if analysis_type == "Detailed Average Analysis":
                file_names = [file.name for file in uploaded_files]
                resampled_data_list = run_detailed_average_analysis(dataframes, file_names)

                # Inputs for saving the analysis
                save_directory = st.text_input("Directory to save the analysis", "./saved_graphs")
                save_filename = st.text_input("Filename to save the analysis", "graph_analysis.csv")

                # Add save button
                if st.button("Save This Analysis"):
                    os.makedirs(save_directory, exist_ok=True)
                    save_path = os.path.join(save_directory, save_filename)
                    # Save the resampled data instead of the complete data
                    combined_resampled_df = pd.concat(resampled_data_list, ignore_index=True)
                    combined_resampled_df.to_csv(save_path, index=False)
                    st.success(f"Analysis saved to {save_path}")

elif page == "View Saved Graphs":
    load_directory = st.text_input("Directory to load saved analyses", "./saved_graphs")
    if os.path.isdir(load_directory):
        view_saved_graphs(load_directory)
    else:
        st.error(f"Directory '{load_directory}' does not exist.")

elif page == "Compare Weights Analysis":
    compare_weights_analysis("/home/kali/PhD/JSTargetFuzzer-Dev2/programs/files")
