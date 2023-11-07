from typing import Optional, List, Dict, Any
import polars as pl
from IPython.display import display, Markdown
from bokeh.plotting import show
from .data_retrieval import get_cfa_and_noncfa_data, get_imf_data_df
from .presentation import generate_graph, chat_gpt_analyze_results
from .constants import CFA_FRANC_ZONE, WEST_AFRICA, MIDDLE_AFRICA


def analyze_medians(merged_df: pl.DataFrame) -> tuple:
    median_count = merged_df.select(
        (pl.col("noncfa_median") > pl.col("cfa_median"))
        .sum()
        .alias("number_of_times_non_cfa_greater"),
        (pl.col("cfa_median") > pl.col("noncfa_median"))
        .sum()
        .alias("number_of_times_cfa_greater"),
    )

    number_of_times_cfa_median_is_greater = median_count["number_of_times_cfa_greater"][
        0
    ]
    number_of_times_non_cfa_median_is_greater = median_count[
        "number_of_times_non_cfa_greater"
    ][0]
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
    return intervals_where_median_is_higher, merged_df["Year"].to_list()


def get_median_df(all_data_df: pl.DataFrame, indicator_label: str) -> pl.DataFrame:
    median_df = (
        all_data_df.group_by(["Year"], maintain_order=True)
        .agg(
            pl.col(indicator_label)
            .where(pl.col("Country").is_in(CFA_FRANC_ZONE))
            .median()
        )
        .join(
            all_data_df.group_by(["Year"], maintain_order=True).agg(
                pl.col(indicator_label)
                .where(
                    pl.col("Country").is_in(WEST_AFRICA)
                    | pl.col("Country").is_in(MIDDLE_AFRICA)
                )
                .median()
            ),
            on="Year",
        )
    )
    median_df.columns = ["Year", "cfa_median", "noncfa_median"]
    return median_df


def process_single_indicator(
    indicator_abbrv: str,
    only_these_indicators: Optional[List[str]],
    countries: Dict[str, str],
    all_countries: Dict[str, Any],
    indicators: Dict[str, Any],
) -> None:
    indicator_info = indicators[indicator_abbrv]
    indicator_label = indicator_info.get("label", "").strip("\n")
    unit = indicator_info.get("unit", "").strip("\n")
    description = indicator_info.get("description", "")
    try:
        # one approach, merge all the dict, create one df , then use exp to get cols to do groupby
        all_data_dict = get_cfa_and_noncfa_data(
            indicator_abbrv, countries, all_countries
        )
        all_data_df = get_imf_data_df(all_data_dict, indicator_label)
        median_df = get_median_df(all_data_df, indicator_label)
        p = generate_graph(median_df.to_dict(as_series=False), indicator_label, unit)
        display(
            Markdown(
                f"""## {indicator_label} comparison between CFA African Franc Zone Countries and Non CFA African Franc Zone Countries"""
            )
        )
        show(p)
        intervals_where_median_is_higher, years = analyze_medians(median_df)
        display(
            chat_gpt_analyze_results(
                indicator_label,
                years,
                intervals_where_median_is_higher,
                description,
                unit,
            )
        )
    except Exception as e:
        print(
            f"issue with indicator {indicator_label}, abbrv: {indicator_abbrv}, exception: {e}"
        )
