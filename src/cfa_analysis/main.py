"""Main function"""
from typing import Optional
import logging

from .data_retrieval import (
    get_country_mapping,
    get_indicators_data,
    get_all_duplicate_dfs,
    get_imf_data_df,
    get_cfa_and_noncfa_data,
)
from .data_cleanup import (
    clean_up_indicators_dict,
    find_duplicate_indicators,
    merge_duplicate_dfs,
)
from .analysis import process_single_indicator
from .data_classes import Indicator
from .constants import SKIP_INDICATORS


def generate_metric_graphs(only_these_indicators: Optional[list[str]] = None) -> None:
    """Main function"""
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    (
        all_countries,
        countries,
    ) = get_country_mapping()
    indicators = clean_up_indicators_dict(get_indicators_data())
    duplicate_indicators = find_duplicate_indicators(indicators)
    processed_dupes = set()
    for indicator_abbrv in indicators:
        if (
            (indicator_abbrv in SKIP_INDICATORS)
            or (indicator_abbrv in processed_dupes)
            or (only_these_indicators and indicator_abbrv not in only_these_indicators)
            or (
                indicators[indicator_abbrv]["source"]
                in ["Wang-Jahan Index", "Capital Flows in Developing Economies"]
                # Wang Jahan ends in 2015 and its an index, requires more research to see if useful
                # ommitting Capital Flows because data appears very incomplete
            )
        ):
            continue
        indicator_info = indicators.get(indicator_abbrv, {})
        indicator_label = indicator_info.get("label", "")
        indicator_label = (
            indicator_label.strip("\n") if indicator_label is not None else None
        )
        indicator_unit = indicator_info.get("unit", "")
        indicator_unit = (
            indicator_unit.strip("\n") if indicator_unit is not None else None
        )
        indicator = Indicator(
            indicator_abbrv,
            indicator_info.get("description", ""),
            indicator_label,
            indicator_unit,
        )
        try:
            if (indicator.label, indicator.unit) in duplicate_indicators:
                all_data_df = merge_duplicate_dfs(
                    get_all_duplicate_dfs(
                        duplicate_indicators,
                        indicator,
                        processed_dupes,
                        countries,
                        all_countries,
                    ),
                    indicator.label,
                )
            else:
                all_data_df = get_imf_data_df(
                    get_cfa_and_noncfa_data(indicator.abbrv, countries, all_countries),
                    indicator.label,
                )
        except Exception as e:
            logging.debug(
                f"issue with indicator {indicator.label}, abbrv: {indicator.abbrv}, exception: {e}"
            )
        try:
            process_single_indicator(all_data_df, indicator)

        except Exception as e:
            logging.debug(
                f"issue with indicator {indicator.label}, abbrv: {indicator.abbrv}, exception: {e}"
            )
