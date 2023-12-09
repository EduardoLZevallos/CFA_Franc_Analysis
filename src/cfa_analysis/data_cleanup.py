from typing import Dict, Tuple, List
import pandas as pd
import polars as pl
import numpy as np
import datetime
from .constants import UNIT_FORMATTING, LABEL_FORMATTING


def rename_from_abbr_to_full_name(abbrv_dict: Dict, all_countries: Dict) -> Dict:
    """Takes the abbreviation key and converts to label key"""
    abbrv = list(abbrv_dict.keys())
    for key in abbrv:
        abbrv_dict[all_countries["countries"][key]["label"]] = abbrv_dict.pop(key)
    return abbrv_dict


def clean_up_indicators_dict(indicators: Dict[str, Dict[str, str]]) -> Dict:
    for indict in indicators:
        if (
            indicators[indict]["unit"] is not None
            and indicators[indict]["unit"] in UNIT_FORMATTING
        ):
            indicators[indict]["unit"] = UNIT_FORMATTING[indicators[indict]["unit"]]
        if (
            indicators[indict]["label"] is not None
            and indicators[indict]["label"] in LABEL_FORMATTING
        ):
            indicators[indict]["label"] = LABEL_FORMATTING[indicators[indict]["label"]]
    return indicators


def find_duplicate_indicators(indicators: Dict[str, Dict[str, str]]) -> dict:
    label_unit_combinations: Dict[tuple, list] = {}
    for key, value in indicators.items():
        label = value.get("label")
        unit = value.get("unit")
        combination = (label, unit)

        if combination in label_unit_combinations:
            label_unit_combinations[combination].append(key)
        else:
            label_unit_combinations[combination] = [key]

    # Find duplicates with the same 'label' and 'unit'.
    return {
        comb: keys for comb, keys in label_unit_combinations.items() if len(keys) > 1
    }


def merge_duplicate_dfs(
    all_dfs: List[pl.DataFrame], indicator_label: str
) -> pl.DataFrame:
    """Merges all the duplicate dictionaries"""
    merged_df = all_dfs[0]
    for x, df in enumerate(all_dfs):
        if x == len(all_dfs) - 1:
            continue
        merged_df = merged_df.join(df, on=["Country", "Year"], how="outer").rename(
            {indicator_label: f"{indicator_label}_left"}
        )
        return (
            merged_df.with_columns(
                [
                    (
                        pl.col(f"{indicator_label}_left").is_not_null()
                        & pl.col(f"{indicator_label}_right").is_not_null()
                    )
                    .then(
                        (
                            pl.col(f"{indicator_label}_left").add(
                                pl.col(f"{indicator_label}_right")
                            )
                        ).truediv(2)
                    )
                    .when(pl.col(f"{indicator_label}_left").is_not_null())
                    .then(pl.col(f"{indicator_label}_left"))
                    .when(pl.col(f"{indicator_label}_right").is_not_null())
                    .then(pl.col(f"{indicator_label}_right"))
                    .otherwise(None)
                    .alias(indicator_label)
                ]
            )
        ).drop([f"{indicator_label}_left", f"{indicator_label}_right"])
