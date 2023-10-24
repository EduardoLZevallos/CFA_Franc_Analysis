import pandas as pd
import numpy as np
import datetime


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
    """40 countries per year in the noncfa, so i think its fine to remove outliers"""
    original_df[outlier_df.notna()] = np.nan
    return original_df


def remove_future_years(median_df: pd.DataFrame) -> pd.DataFrame:
    current_year = datetime.datetime.now().year  # drop years that dont exist yet
    return median_df[median_df["year"] <= current_year]
