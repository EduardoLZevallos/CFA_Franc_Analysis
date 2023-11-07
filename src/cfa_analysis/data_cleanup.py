import pandas as pd
import numpy as np
import datetime


def rename_from_abbr_to_full_name(inflation_dict: dict, all_countries: dict) -> dict:
    abbrv = list(inflation_dict.keys())
    for key in abbrv:
        inflation_dict[all_countries["countries"][key]["label"]] = inflation_dict.pop(
            key
        )
    return inflation_dict


def find_outliers_IQR(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate the first quartile (Q1) and third quartile (Q3)
    q1 = df.quantile(0.25, interpolation="midpoint", numeric_only=True)
    q3 = df.quantile(0.75, interpolation="midpoint", numeric_only=True)

    # Calculate the interquartile range (IQR)
    IQR = q3 - q1

    # Calculate the lower and upper bounds for outliers
    outliers = df[((df < (q1 - 1.5 * IQR)) | (df > (q3 + 1.5 * IQR)))]
    return outliers


def remove_outliers(
    original_df: pd.DataFrame, outlier_df: pd.DataFrame
) -> pd.DataFrame:
    original_df[outlier_df.notna()] = np.nan
    return original_df
