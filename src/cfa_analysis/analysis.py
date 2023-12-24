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
        who_is_higher = """CFA franc zone and non-CFA middle/west Africa countries have roughly an equal amount of intervals where their respective medians was higher"""
    elif cfa_media_count_higher > non_cfa_media_count_higher:
        who_is_higher = "CFA franc zone countries"
    else:
        who_is_higher = "non-CFA middle/west Africa countries"
    return who_is_higher, merged_df["Year"].to_list()


def chat_gpt_analyze_results(
    median_df: pl.DataFrame,
    indicator: type[Indicator],
    years: list[int],
    intervals_where_median_is_higher: str,
):  # pragma: no cover
    """Makes chatgpt call to get definition of indicator and
    simple based on frequency of when medians are larger"""
    
    cfa_franc_zone_background = """The CFA franc, originally the French African Colonial franc, was created in 1945 and imposed on France's colonies. The CFA franc zone of today is an area of monetary cooperation, comprised of two African economic zones: the West Africa Economic and Monetary Union (WAEMU) and the Central African Economic and Monetary Union (CEMAC), along with Comoros. It should be noted that since 1993, the two CFA francs and the Comorian franc cannot be exchanged for one another. To exchange one currency for the other, it must first be converted to euros. This additional step in conversion creates additional demand for euros, which consequently acts as a privileged intermediary in trade between the African countries. Overall, more than 162 million people use the two CFA francs.<br>
    
    Key decisions concerning the CFA franc zone are made in Paris. The central actor in this system is the French Treasury. All foreign exchange transactions (the purchase or sale of CFA francs) of the 15 countries in the franc zone must go through the French Treasury due to the French guarantee of unlimited convertibility of CFA francs into euros. This makes France the only country in the world that directly manages a set of currencies distinct from its own.<br>
    
    The CFA franc zone is based on four interrelated principles: the fixed exchange rate, the free movement of capital, the free convertibility of the currency, and the centralization of foreign exchange reserves.<br>
    
    Supporters of the CFA franc system suggest that it provides monetary stability, economic attractiveness, investment inflows, and an increase in the growth rate.<br>
    
    The idea that the CFA franc promotes growth and development has been widely touted by the Bank of France. In 2015, the Bank of France stated, "For over forty years, the franc zone has been an instrument of solidarity and development aimed at consolidating growth, reducing poverty, and deepening regional integration." Additionally, in 2012, Christian Noyer, the governor of the Bank of France, remarked, "The last fifty years have shown that the franc zone is a favorable factor for development."<br> 
    
    However, the CFA franc zone has four major downsides for the countries that are part of it: an excessively rigid exchange rate regime, a problematic pegging to the euro, the underfinancing of African economies, and a free movement of capital that generates a massive financial bleed-out.<br> """
    
    get_ipython().run_cell_magic(
        "ai", "openai-chat:gpt-3.5-turbo -r", "reset the chat history"
    )  # reset the model else we run out of tokens
    return ( 
        get_ipython().run_cell_magic(
            "ai",
            "openai-chat:gpt-3.5-turbo -f markdown",
            f"""
                In a professional tone resembling that of a Keynesian economist, the response must be only be one paragraph and must not mention Keynesian economics. 
                Explain the concept of {indicator.label} measured in {indicator.unit} and its significance as an indicator of a country's economic growth and development. For additional context consider this definition from the imf: {indicator.description}.
            """,
        ), 
        get_ipython().run_cell_magic(
            "ai",
            "openai-chat:gpt-3.5-turbo -f markdown",
           f"""
                In a professional tone, thinking like a keynesian economist. 
                Do not mention keynesian economist in your response.
                Non-CFA middle/west Africa countries are countries that are not in the cfa franc zone. 
                Here is additional context about the CFA franc zone: {cfa_franc_zone_background}
                Here is additional context, a dataframe with the median {indicator.label} from {years[0]} to {years[-1]} for CFA franc zone and non-CFA franc:{median_df}
                step 1 - Does a higher {indicator.label} promote economic growth and development?  
        
                step 2 - Based on your response to step 1,
                for {indicator.label} {intervals_where_median_is_higher} had more yearly intervals with a higher median from
                {years[0]} to {years[-1]}.Please provide a concise compariative insight between cfa franc zone countries and
                non-CFA middle/west Africa countries related to {indicator.label}. 
                
                Do not include the word step 2 in your response.
                Please make your response is only one paragraph
                """
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
         median_df.drop(['abs_cfa_median', 'abs_noncfa_median']), indicator, years, intervals_where_median_is_higher
    )
    display_indicator_report(p, definition, conclusion, indicator)
