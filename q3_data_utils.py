#!/usr/bin/env python3
# Assignment 5, Question 3: Data Utilities Library

import pandas as pd
import numpy as np

def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


def clean_data(df: pd.DataFrame, remove_duplicates: bool = True,
               sentinel_value: float = -999) -> pd.DataFrame:
    df = df.replace(sentinel_value, np.nan)
    if remove_duplicates:
        df = df.drop_duplicates()
    return df


def detect_missing(df: pd.DataFrame) -> pd.Series:
    return df.isna().sum()


def fill_missing(df: pd.DataFrame, column: str, strategy: str = 'mean') -> pd.DataFrame:
    if strategy == 'mean':
        value = df[column].mean()
        df[column] = df[column].fillna(value)
    elif strategy == 'median':
        value = df[column].median()
        df[column] = df[column].fillna(value)
    elif strategy == 'ffill':
        df[column] = df[column].fillna(method='ffill')
    else:
        raise ValueError("Strategy must be: 'mean', 'median', or 'ffill'")
    return df


def filter_data(df: pd.DataFrame, filters: list) -> pd.DataFrame:
    for f in filters:
        col = f['column']
        cond = f['condition']
        val = f['value']

        if cond == 'equals':
            df = df[df[col] == val]
        elif cond == 'greater_than':
            df = df[df[col] > val]
        elif cond == 'less_than':
            df = df[df[col] < val]
        elif cond == 'in_range':
            df = df[(df[col] >= val[0]) & (df[col] <= val[1])]
        elif cond == 'in_list':
            df = df[df[col].isin(val)]
        else:
            raise ValueError(f"Unsupported condition: {cond}")

    return df


def transform_types(df: pd.DataFrame, type_map: dict) -> pd.DataFrame:
    for col, typ in type_map.items():
        if typ == 'datetime':
            df[col] = pd.to_datetime(df[col], errors='coerce')
        elif typ == 'numeric':
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif typ == 'category':
            df[col] = df[col].astype('category')
        elif typ == 'string':
            df[col] = df[col].astype(str)
        else:
            raise ValueError(f"Unsupported type: {typ}")

    return df


def create_bins(df: pd.DataFrame, column: str, bins: list,
                labels: list, new_column: str = None) -> pd.DataFrame:
    if new_column is None:
        new_column = f"{column}_binned"
    df[new_column] = pd.cut(df[column], bins=bins, labels=labels, include_lowest=True)
    return df


def summarize_by_group(df: pd.DataFrame, group_col: str,
                       agg_dict: dict = None) -> pd.DataFrame:
    grouped = df.groupby(group_col)
    
    if agg_dict:
        result = grouped.agg(agg_dict)
    else:
        result = grouped.describe()

    return result.reset_index()


if __name__ == '__main__':
    print("✅ Data utilities loaded successfully!")
