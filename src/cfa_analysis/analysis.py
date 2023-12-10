""" Generates median df, and counts of when frequencies are generator, 
and have a process single indicator function"""

from IPython.display import display, Markdown
import polars as pl
from bokeh.plotting import show
from .presentation import generate_graph, chat_gpt_analyze_results
from .constants import CFA_FRANC_ZONE, WEST_AFRICA, MIDDLE_AFRICA


def get_median_df(all_data_df: pl.DataFrame, indicator_label: str) -> pl.DataFrame:
    """Returns the medians for cfa and noncfa african countries as a
    new dataframe, drops nulls and renames columns
    Handles casees of when countries joined the cfa zone
    Guinea-Bissau joined cfa zone in 1997
    Mali joined cfa zone in 1984
    Equatorial Guinea joined cfa zone in 1985
    """
    return (
        all_data_df.group_by(["Year"], maintain_order=True)
        .agg(
            pl.col(indicator_label)
            .where(
                ((pl.col("Year") >= 1997) & (pl.col("Country") == "Guinea-Bissau"))
                | ((pl.col("Year") >= 1984) & (pl.col("Country") == "Mali"))
                | (
                    (pl.col("Year") >= 1985)
                    & (pl.col("Country") == "Equatorial Guinea")
                )
                | (
                    pl.col("Country").is_in(CFA_FRANC_ZONE)
                    & ~pl.col("Country").is_in(
                        ["Guinea-Bissau", "Mali", "Equatorial Guinea"]
                    )
                )
            )
            .median()
        )
        .join(
            all_data_df.group_by(["Year"], maintain_order=True).agg(
                pl.col(indicator_label)
                .where(
                    pl.col("Country").is_in(WEST_AFRICA)
                    | pl.col("Country").is_in(MIDDLE_AFRICA)
                    | ((pl.col("Year") < 1997) & (pl.col("Country") == "Guinea-Bissau"))
                    | ((pl.col("Year") < 1984) & (pl.col("Country") == "Mali"))
                    | (
                        (pl.col("Year") < 1985)
                        & (pl.col("Country") == "Equatorial Guinea")
                    )
                )
                .median()
            ),
            on="Year",
        )
        .drop_nulls()
        .rename(
            {indicator_label: "cfa_median", f"{indicator_label}_right": "noncfa_median"}
        )
        .with_columns(
            pl.col("cfa_median").abs().alias("abs_cfa_median"),
            pl.col("noncfa_median").abs().alias("abs_noncfa_median"),
        )
    )


def analyze_medians(merged_df: pl.DataFrame) -> tuple:
    """Calculates the number of times the median is higher,
    if the difference in median counts is less than or
    equal to two then considers the count the same
    """
    median_count = merged_df.select(
        (pl.col("noncfa_median") > pl.col("cfa_median"))
        .sum()
        .alias("number_of_times_non_cfa_greater"),
        (pl.col("cfa_median") > pl.col("noncfa_median"))
        .sum()
        .alias("number_of_times_cfa_greater"),
    )

    cfa_media_count_higher = median_count["number_of_times_cfa_greater"][0]
    non_cfa_media_count_higher = median_count["number_of_times_non_cfa_greater"][0]
    if abs(cfa_media_count_higher - non_cfa_media_count_higher) <= 2:
        who_is_higher = """CFA and Non CFA countries have roughly an
        equal amount of intervals where their respective medians was higher"""
    elif cfa_media_count_higher > non_cfa_media_count_higher:
        who_is_higher = "African CFA Countries"
    else:
        who_is_higher = "Non-CFA Middle Africa and Western Africa Countries"
    return who_is_higher, merged_df["Year"].to_list()


def process_single_indicator(
    all_data_df: pl.DataFrame,
    indicator_label: str,
    indicator_unit: str,
    indicator_description: str,
) -> None:  # pragma: no cover
    """helps generate report, calls median function
    generates the report, calls chatgpt and formats"""
    median_df = get_median_df(all_data_df, indicator_label)
    p = generate_graph(
        median_df.to_dict(as_series=False), indicator_label, indicator_unit
    )
    display(
        Markdown(
            f"""## {indicator_label} comparison between African CFA Zone Countries to 
            Non-CFA Middle Africa and Western Africa Countries"""
        )
    )
    show(p)
    # intervals_where_median_is_higher, years = analyze_medians(median_df)
    # display(
    #     chat_gpt_analyze_results(
    #         indicator_label,
    #         years,
    #         intervals_where_median_is_higher,
    #         indicator_description,
    #         indicator_unit,
    #     )
    # )
