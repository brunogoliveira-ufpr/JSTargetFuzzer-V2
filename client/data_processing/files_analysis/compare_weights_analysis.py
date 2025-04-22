import os
import streamlit as st
import pandas as pd
import plotly.express as px
from .count_operations_and_variables import count_operations_and_variables
from .cyclomatic_complexity import cyclomatic_complexity
from .categorize_operations import categorize_operations
from .count_lines_per_operation import count_lines_per_operation
from .save_unknown_operations import save_unknown_operations
from .generate_overall_summary import generate_overall_summary
from .generate_operation_statistics import generate_operation_statistics
from .generate_detailed_file_data import generate_detailed_file_data
from .latex_generator import save_latex_file
from .generate_latex_chart_content import save_latex_chart_file
from .parse_swift_code_generators import parse_swift_code_generators
from .translate_to_il import translate_to_il

def compare_weights_analysis(directory):
    swift_file_path = os.path.join(os.path.dirname(__file__), 'CodeGenerators.swift')
    
    with open(swift_file_path, 'r') as file:
        swift_code = file.read()
        
    generators = parse_swift_code_generators(swift_code)
    
    il_instructions = translate_to_il(generators)
    
    weight1_files = [f for f in os.listdir(directory) if 'weight1' in f]
    weight1000_files = [f for f in os.listdir(directory) if 'weight1000' in f]

    detailed_file_data_df = generate_detailed_file_data(
        directory, weight1_files, weight1000_files, 
        count_operations_and_variables, cyclomatic_complexity, 
        count_lines_per_operation
    )
    
    st.header("Detailed File Data")
    st.write(detailed_file_data_df)

    operation_stats_df = generate_operation_statistics(detailed_file_data_df.to_dict(orient='list'))
    
    st.header("Operation Statistics")
    st.write(operation_stats_df)

    categorized_df, unknown_operations = categorize_operations(operation_stats_df)
    
    grouped_df = categorized_df.groupby(['Category', 'Category Description']).agg(
        {'1 Count': 'sum', '1000 Count': 'sum', '1 Mean': 'mean', '1000 Mean': 'mean', '1 Lines': 'sum', '1000 Lines': 'sum'}
    ).reset_index()
    
    st.header("Grouped Operation Statistics by Category")
    st.write(grouped_df)

    if unknown_operations:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        save_unknown_operations(unknown_operations, script_directory)
        st.header("Unknown Operations")
        st.write(unknown_operations)

    overall_summary_df = generate_overall_summary(detailed_file_data_df)
    
    st.header("Overall Summary Statistics")
    st.write(overall_summary_df)

    st.header("LaTeX Example in Streamlit")
    st.latex(r'''
    \text{Average Operations Count:} \ \frac{\sum_{i=1}^{n} \text{Operations}_i}{n}
    ''')
    custom_y_labels = {'1 Mean': "Fuzzilli's Programs", '1000 Mean': "JSTargetFuzzer's Programs"}
    fig = px.bar(
        grouped_df,
        x='Category',
        y=['1 Mean', '1000 Mean'],
        barmode='group',
        title='',
        labels={'value': 'Average Values', 'Category': 'Category'}
    )

    # Atualizar os rótulos do eixo y
    fig.for_each_trace(lambda t: t.update(name=custom_y_labels[t.name]))

    st.plotly_chart(fig)
    print(grouped_df)
    plot_data = {
        'categories': grouped_df['Category'].tolist(),
        'means_1': grouped_df['1 Mean'].tolist(),
        'means_1000': grouped_df['1000 Mean'].tolist()
    }

    latex_config = {
        'report_title': 'Custom Analysis Report',
        'plot_section_title': 'Comparison of Averages by Category',
        'xlabel': 'Operation Category',
        'ylabel': 'Average Count',
        'legend_label1': "Fuzzilli's Programs",
        'legend_label2': "JSTargetFuzzer's Programs",
        'plot_width': '1.5\\textwidth',
        'plot_height': '0.8\\textheight'
    }

    if st.button('Generate Full LaTeX Report'):
        save_latex_file(grouped_df, overall_summary_df, plot_data, latex_config)
        st.success("Full LaTeX report saved successfully!")

    if st.button('Generate Chart Only LaTeX File'):
        chart_config = {
            'xlabel': 'Operation Category',
            'ylabel': 'Average Count',
            'legend_label1': "Fuzzilli's Programs",
            'legend_label2': "JSTargetFuzzer's Programs",
        }
        save_latex_chart_file(plot_data, chart_config)
        st.success("Chart-only LaTeX file saved successfully!")
