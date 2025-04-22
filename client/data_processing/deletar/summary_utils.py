import pandas as pd
import streamlit as st
from .operation_categories import *
import streamlit as st


def create_summary_table(metrics):
    summary_data = {
        "Metric": [
            "Number of Variables", "Number of Operations", "Control Flow Operations", "Class Operations",
            "Function Operations", "Variable and Assignment Operations", "Exception Operations",
            "Expression and Operator Operations", "Loop Operations", "Higher Order Function Operations",
            "Object and Property Operations", "Scope Operations", "Module Operations", "Event Handling Operations",
            "Program Flow Operations", "User Interaction Operations", "Cyclomatic Complexity"
        ],
        "Weight 1 Total": [
            metrics["total_variables_defined"][1], sum(metrics["total_operation_counts"][1].values()), metrics["total_control_flow_ops"][1],
            metrics["total_class_ops"][1], metrics["total_function_ops"][1], metrics["total_variables_assignment_ops"][1],
            metrics["total_exception_ops"][1], metrics["total_expression_operator_ops"][1], metrics["total_loop_ops"][1],
            metrics["total_higher_order_function_ops"][1], metrics["total_object_property_ops"][1], metrics["total_scope_ops"][1],
            metrics["total_module_ops"][1], metrics["total_event_handling_ops"][1], metrics["total_program_flow_ops"][1],
            metrics["total_user_interaction_ops"][1], metrics["average_complexity_by_weight"].get(1, 0)
        ],
        "Weight 500 Total": [
            metrics["total_variables_defined"][500], sum(metrics["total_operation_counts"][500].values()), metrics["total_control_flow_ops"][500],
            metrics["total_class_ops"][500], metrics["total_function_ops"][500], metrics["total_variables_assignment_ops"][500],
            metrics["total_exception_ops"][500], metrics["total_expression_operator_ops"][500], metrics["total_loop_ops"][500],
            metrics["total_higher_order_function_ops"][500], metrics["total_object_property_ops"][500], metrics["total_scope_ops"][500],
            metrics["total_module_ops"][500], metrics["total_event_handling_ops"][500], metrics["total_program_flow_ops"][500],
            metrics["total_user_interaction_ops"][500], metrics["average_complexity_by_weight"].get(500, 0)
        ],
        "Weight 1 Average": [
            metrics["total_variables_defined"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            sum(metrics["total_operation_counts"][1].values()) / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_control_flow_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_class_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_function_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_variables_assignment_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_exception_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_expression_operator_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_loop_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_higher_order_function_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_object_property_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_scope_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_module_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_event_handling_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_program_flow_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["total_user_interaction_ops"][1] / metrics["file_count_by_weight"][1] if metrics["file_count_by_weight"][1] else 0,
            metrics["average_complexity_by_weight"].get(1, 0)
        ],
        "Weight 500 Average": [
            metrics["total_variables_defined"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            sum(metrics["total_operation_counts"][500].values()) / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_control_flow_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_class_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_function_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_variables_assignment_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_exception_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_expression_operator_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_loop_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_higher_order_function_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_object_property_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_scope_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_module_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_event_handling_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_program_flow_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["total_user_interaction_ops"][500] / metrics["file_count_by_weight"][500] if metrics["file_count_by_weight"][500] else 0,
            metrics["average_complexity_by_weight"].get(500, 0)
        ]
    }

    df = pd.DataFrame(summary_data)
    st.table(df)

    # Add option to download the table as CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='summary_table.csv',
        mime='text/csv'
    )

def add_complexity_to_summary(metrics, avg_complexity):
    metrics["average_complexity_by_weight"] = avg_complexity

