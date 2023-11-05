import pandas as pd


def generate_median_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a DataFrame with the median values of each column in the input DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with the median values, sorted by year.
    """
    median_df = df.median().to_frame(name="median")
    median_df.index.name = "year"
    median_df.reset_index(inplace=True)
    median_df.sort_values(by="year", inplace=True)
    median_df["year"] = median_df["year"].astype(
        int
    )  # had an issue where some of the data was returning as string
    median_df["median"] = median_df["median"].astype(
        float
    )  # had an issue where some of the data was returning as string
    return median_df


def analyze_medians(merge_df: pd.DataFrame) -> tuple:
    merge_df["cfa_median_greater"] = merge_df["median_cfa"] > merge_df["median_non_cfa"]
    number_of_times_cfa_median_is_greater = merge_df["cfa_median_greater"].sum()
    number_of_times_non_cfa_median_is_greater = (
        len(merge_df) - number_of_times_cfa_median_is_greater
    )
    if (
        abs(
            number_of_times_cfa_median_is_greater
            - number_of_times_non_cfa_median_is_greater
        )
        <= 2
    ):
        intervals_where_median_is_higher = "CFA and Non CFA were equal"
    elif (
        number_of_times_cfa_median_is_greater
        > number_of_times_non_cfa_median_is_greater
    ):
        intervals_where_median_is_higher = "Cfa African Franc Zone Countries"
    else:
        intervals_where_median_is_higher = "Non Cfa African Franc Zone Countries"
    return intervals_where_median_is_higher, merge_df["year"].to_list()
