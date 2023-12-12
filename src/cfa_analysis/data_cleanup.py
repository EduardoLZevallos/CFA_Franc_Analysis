"""Clean up data functions, find and merge duplicates, format names of units and labels"""
import polars as pl
from .constants import UNIT_FORMATTING, LABEL_FORMATTING


def rename_from_abbr_to_full_name(abbrv_dict: dict, all_countries: dict) -> dict:
    """Takes the abbreviation key and converts to label key"""
    abbrv = list(abbrv_dict.keys())
    for key in abbrv:
        abbrv_dict[all_countries["countries"][key]["label"]] = abbrv_dict.pop(key)
    return abbrv_dict


def clean_up_indicators_dict(indicators: dict[str, dict[str, str]]) -> dict:
    """Apply formatting to the unit and label of indicators"""
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


def find_duplicate_indicators(indicators: dict[str, dict[str, str]]) -> dict:
    """Find all duplicate indicators"""
    label_unit_combinations: dict[tuple, list] = {}
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
    all_dfs: list[pl.DataFrame], indicator_label: str
) -> pl.DataFrame:
    """Merges all the duplicate dictionaries"""
    merged_df = all_dfs[0]
    for x, df in enumerate(all_dfs):
        if x == len(all_dfs) - 1:
            continue
        merged_df = merged_df.join(df, on=["Country", "Year"], how="outer").rename(
            {indicator_label: f"{indicator_label}_left"}
        )
        merged_df = (
            merged_df.with_columns(
                [
                    pl.when(
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
    return merged_df

    # TODO: add logic that raises exception if not enough data
    # null_cfa = len(all_data_df.select(pl.col('Country', indicator.label)).filter((pl.col("Country").is_in(CFA_FRANC_ZONE)) & (pl.col(indicator.label).is_null())))
    # null_west_africa = len(all_data_df.select(pl.col('Country', indicator.label)).filter((pl.col("Country").is_in(WEST_AFRICA)) & (pl.col(indicator.label).is_null())))
    # null_middle_africa = len(all_data_df.select(pl.col('Country', indicator.label)).filter((pl.col("Country").is_in(MIDDLE_AFRICA)) & (pl.col(indicator.label).is_null())))
    # # logging.debug(
    # #     f"""Number of null values for CFA FRANC: {null_cfa} \n
    # #     Number of null values for WEST AFRICA: {null_west_africa} \n
    # #     Number of null values in MIDDLE AFRICA: {null_middle_africa}"""
    # # )
    # print(f"""Number of null values for CFA FRANC: {null_cfa} \n
    #     Number of null values for WEST AFRICA: {null_west_africa} \n
    #     Number of null values in MIDDLE AFRICA: {null_middle_africa}""")
