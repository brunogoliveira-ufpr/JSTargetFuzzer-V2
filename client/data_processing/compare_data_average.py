import pandas as pd

def compare_data_average(dfs, columns, group_columns, aggregation_methods, aggregate):
    """Compares data from multiple dataframes based on the total time interval and aggregation methods."""
    resampled_dfs = []

    for df in dfs:
        df = df.copy()
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['ElapsedTime'] = (df['Timestamp'] - df['Timestamp'].min()).apply(lambda x: x.total_seconds() / 60)  # Tempo decorrido em minutos
        df.set_index('Timestamp', inplace=True)
        resampled_data = {}

        for col in columns:
            agg_method = aggregation_methods[col]
            group_by_columns = ['ElapsedTime'] + group_columns if aggregate else ['ElapsedTime']

            if agg_method == "mean":
                resampled = df[[col] + group_columns + ['ElapsedTime']].groupby(group_by_columns).mean().reset_index()
            elif agg_method == "max":
                resampled = df[[col] + group_columns + ['ElapsedTime']].groupby(group_by_columns).max().reset_index()
            elif agg_method == "last":
                resampled = df[[col] + group_columns + ['ElapsedTime']].groupby(group_by_columns).last().reset_index()
            elif agg_method == "count":
                resampled = df[[col] + group_columns + ['ElapsedTime']].groupby(group_by_columns).count().reset_index()
            elif agg_method == "min":
                resampled = df[[col] + group_columns + ['ElapsedTime']].groupby(group_by_columns).min().reset_index()
            elif agg_method == "std":
                resampled = df[[col] + group_columns + ['ElapsedTime']].groupby(group_by_columns).std().reset_index()
            elif agg_method == "sum":
                resampled = df[[col] + group_columns + ['ElapsedTime']].groupby(group_by_columns).sum().reset_index()
            else:
                raise ValueError(f"Invalid aggregation method for column {col}")

            resampled_data[col] = resampled.set_index(group_by_columns)[col]

        combined_resampled_df = pd.concat(resampled_data.values(), axis=1).reset_index()
        resampled_dfs.append(combined_resampled_df)

    return resampled_dfs
