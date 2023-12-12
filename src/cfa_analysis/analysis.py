""" Generates median df, and counts of when frequencies are generator, 
and have a process single indicator function"""

import polars as pl
from .data_classes import Indicator
from .presentation import generate_graph, display_indicator_report
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
        who_is_higher = """CFA and Non CFA countries have roughly an equal amount of intervals where their respective medians was higher"""
    elif cfa_media_count_higher > non_cfa_media_count_higher:
        who_is_higher = "African CFA Countries"
    else:
        who_is_higher = "Non-CFA Middle Africa and Western Africa Countries"
    return who_is_higher, merged_df["Year"].to_list()

    
def chat_gpt_analyze_results(
    indicator: type[Indicator],
    years: list[int],
    intervals_where_median_is_higher: str,
):  # pragma: no cover
    """Makes chatgpt call to get definition of indicator and
    simple based on frequency of when medians are larger"""
    get_ipython().run_cell_magic(
        "ai", "openai-chat:gpt-3.5-turbo -r", "reset the chat history"
    )  # reset the model else we run out of tokens
    return (
        get_ipython().run_cell_magic(
            "ai",
            "openai-chat:gpt-3.5-turbo -f markdown",
            f"""
            In a professional tone resembling that of a Keynesian economist, the response must be only be one paragraph and must not mention Keynesian economics. 
            Explain the concept of {indicator.label} measured in {indicator.unit} and its significance as an indicator of a country's economic growth and development. Use this definition from the imf: {indicator.description}.
        """,
        ),
        get_ipython().run_cell_magic(
            "ai",
            "openai-chat:gpt-3.5-turbo -f markdown",
            f"""
            In a professional tone resembling that of a Keynesian economist, the response should only be one paragraph and must not mention Keynesian economics.
            This analysis challenges the claim that the CFA franc zone promotes growth and development. 
            step 1 - Does a higher {indicator.label} promote economic growth and development?  In assessing the impact of the CFA franc zone on economic growth and development,it is crucial to consider the relationship between {indicator.label} and overall progress.
            step 2 - Examing the data, it is evident for {indicator.label} {intervals_where_median_is_higher} had more yearly intervals with a higher median from {years[0]} to {years[-1]}. 
            Based on your answer to step 1 and step 2, draw a concise conclusion comparing economic growth and development of African CFA franc zone countries to non-CFA Middle Africa and Western Africa countries. This conclusion must unequivocally address whether the CFA franc zone promotes growth and development. Do not reference the words step 1 and step 2 in your response.
        """,
        )
    )

def process_single_indicator(
    all_data_df: pl.DataFrame,
    indicator: type[Indicator],
) -> None:  # pragma: no cover
    """helps generate report, calls median function
    generates the report, calls chatgpt and formats"""
    median_df = get_median_df(all_data_df, indicator.label)
    p = generate_graph(
        median_df.to_dict(as_series=False), indicator.label, indicator.unit
    )
    intervals_where_median_is_higher, years = analyze_medians(median_df)
    definition, conclusion = chat_gpt_analyze_results(
        indicator, years, intervals_where_median_is_higher
    )
