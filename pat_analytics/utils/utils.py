import pandas as pd
import numpy as np

def add_column_multiidx(df : pd.DataFrame, column_name : str, vals):
    """
    To the top level of the multitindex df, add a new column
    column_name and fill it with vals
    """
    field = df.columns.levels[1]
    new_cols = pd.MultiIndex.from_product([[column_name], field])
    df[new_cols] = vals
    return df