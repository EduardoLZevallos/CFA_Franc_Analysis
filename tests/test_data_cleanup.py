import numpy as np
import polars as pl
from polars.testing import assert_frame_equal
from cfa_analysis.data_cleanup import (
    rename_from_abbr_to_full_name,
    clean_up_indicators_dict,
    find_duplicate_indicators,
    merge_duplicate_dfs,
)
from cfa_analysis.constants import UNIT_FORMATTING, LABEL_FORMATTING


def test_rename_from_abbr_to_full_name():
    # GIVEN
    inflation_dict = {"USA": 2.3, "CAN": 1.9, "AUS": 1.8}
    all_countries = {
        "countries": {
            "USA": {"label": "United States"},
            "CAN": {"label": "Canada"},
            "AUS": {"label": "Australia"},
        }
    }

    # WHEN
    result = rename_from_abbr_to_full_name(inflation_dict, all_countries)

    # THEN
    assert result == {"United States": 2.3, "Canada": 1.9, "Australia": 1.8}


def test_clean_up_indicators_dict_no_label_or_unit_appears():
    # GIVEN
    original_indicators = {
        "NGDP_RPCH": {
            "label": "No Change",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at constant prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "No Change",
            "dataset": "WEO",
        },
        "NGDPD": {
            "label": "No Change",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at current prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "No Change",
            "dataset": "WEO",
        },
    }
    # WHEN
    formatted_indicators = clean_up_indicators_dict(original_indicators)

    # THEN
    assert formatted_indicators == original_indicators


def test_clean_up_indicators_dict_unit_formatted():
    # GIVEN
    original_indicators = {
        "NGDP_RPCH": {
            "label": "No Change",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at constant prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "Annual percent change",
            "dataset": "WEO",
        },
        "NGDPD": {
            "label": "No Change",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at current prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "No Change",
            "dataset": "WEO",
        },
    }
    # WHEN
    formatted_indicators = clean_up_indicators_dict(original_indicators)

    # THEN
    assert formatted_indicators == {
        "NGDP_RPCH": {
            "label": "No Change",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at constant prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "% change",
            "dataset": "WEO",
        },
        "NGDPD": {
            "label": "No Change",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at current prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "No Change",
            "dataset": "WEO",
        },
    }


def test_clean_up_indicators_dict_label_formatted():
    # GIVEN
    original_indicators = {
        "NGDP_RPCH": {
            "label": "Real GDP growth",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at constant prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "No Change",
            "dataset": "WEO",
        },
        "NGDPD": {
            "label": "No Change",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at current prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "No Change",
            "dataset": "WEO",
        },
    }
    # WHEN
    formatted_indicators = clean_up_indicators_dict(original_indicators)

    # THEN
    assert formatted_indicators == {
        "NGDP_RPCH": {
            "label": "Real GDP Growth Rate",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at constant prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "No Change",
            "dataset": "WEO",
        },
        "NGDPD": {
            "label": "No Change",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at current prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "No Change",
            "dataset": "WEO",
        },
    }


def test_find_duplicate_indicators_two_sets_of_duplicates_found():
    # GIVEN
    indicators = {
        "NGDP_RPCH": {"label": "Real GDP Growth Rate", "unit": "% change"},
        "NGDP_R_PCH": {"label": "Real GDP Growth Rate", "unit": "% change"},
        "rev": {"label": "Government Revenue", "unit": "% of GDP"},
        "GGR_G01_GDP_PT": {"label": "Government Revenue", "unit": "% of GDP"},
    }
    # WHEN
    result = find_duplicate_indicators(indicators)

    # THEN
    result == {
        ("Real GDP Growth Rate", "% change"): ["NGDP_RPCH", "NGDP_R_PCH"],
        ("Government Revenue", "% of GDP"): ["rev", "GGR_G01_GDP_PT"],
    }


def test_find_duplicate_indicators_no_duplicates_found():
    # GIVEN
    indicators = {
        "NGDP_RPCH": {"label": "A", "unit": "1"},
        "NGDP_R_PCH": {"label": "B", "unit": "2"},
        "rev": {"label": "C", "unit": "3"},
        "GGR_G01_GDP_PT": {"label": "D", "unit": "4"},
    }
    # WHEN
    result = find_duplicate_indicators(indicators)

    # THEN
    result == {}


def test_merge_duplicate_dfs_no_null_values():
    # GIVEN
    df = pl.from_dict(
        {
            "Country": [
                "Benin",
                "Burkina Faso",
                "Angola",
                "Congo, Dem. Rep. of the",
                "Cabo Verde",
            ],
            "Year": [
                1980,
                1980,
                1980,
                1980,
                1980,
            ],
            "NGDP_RPCH": [
                9,
                4,
                2,
                2,
                5,
            ],
        },
        schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
    )
    all_dfs = [df, df]

    # WHEN
    result = merge_duplicate_dfs(all_dfs, "NGDP_RPCH")

    # THEN
    assert_frame_equal(
        result,
        pl.from_dict(
            {
                "Country": [
                    "Benin",
                    "Burkina Faso",
                    "Angola",
                    "Congo, Dem. Rep. of the",
                    "Cabo Verde",
                ],
                "Year": [1980, 1980, 1980, 1980, 1980],
                "NGDP_RPCH": [9.0, 4.0, 2.0, 2.0, 5.0],
            },
            schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
        ),
    )


def test_merge_duplicate_dfs_right_has_nulls():
    # GIVEN
    df_1 = pl.from_dict(
        {
            "Country": [
                "Benin",
                "Burkina Faso",
                "Angola",
                "Congo, Dem. Rep. of the",
                "Cabo Verde",
            ],
            "Year": [
                1980,
                1980,
                1980,
                1980,
                1980,
            ],
            "NGDP_RPCH": [
                9,
                4,
                2,
                2,
                5,
            ],
        },
        schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
    )
    df_2 = pl.from_dict(
        {
            "Country": [
                "Benin",
                "Burkina Faso",
                "Angola",
                "Congo, Dem. Rep. of the",
                "Cabo Verde",
            ],
            "Year": [
                1980,
                1980,
                1980,
                1980,
                1980,
            ],
            "NGDP_RPCH": [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                5,
            ],
        },
        schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
    )
    all_dfs = [df_1, df_2]

    # WHEN
    result = merge_duplicate_dfs(all_dfs, "NGDP_RPCH")

    # THEN
    assert_frame_equal(
        result,
        pl.from_dict(
            {
                "Country": [
                    "Benin",
                    "Burkina Faso",
                    "Angola",
                    "Congo, Dem. Rep. of the",
                    "Cabo Verde",
                ],
                "Year": [1980, 1980, 1980, 1980, 1980],
                "NGDP_RPCH": [9.0, 4.0, 2.0, 2.0, 5.0],
            },
            schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
        ),
    )


def test_merge_duplicate_dfs_left_has_nulls():
    # GIVEN
    df_1 = pl.from_dict(
        {
            "Country": [
                "Benin",
                "Burkina Faso",
                "Angola",
                "Congo, Dem. Rep. of the",
                "Cabo Verde",
            ],
            "Year": [
                1980,
                1980,
                1980,
                1980,
                1980,
            ],
            "NGDP_RPCH": [
                9,
                4,
                2,
                2,
                5,
            ],
        },
        schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
    )
    df_2 = pl.from_dict(
        {
            "Country": [
                "Benin",
                "Burkina Faso",
                "Angola",
                "Congo, Dem. Rep. of the",
                "Cabo Verde",
            ],
            "Year": [
                1980,
                1980,
                1980,
                1980,
                1980,
            ],
            "NGDP_RPCH": [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                5,
            ],
        },
        schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
    )
    all_dfs = [df_2, df_1]

    # WHEN
    result = merge_duplicate_dfs(all_dfs, "NGDP_RPCH")

    # THEN
    assert_frame_equal(
        result,
        pl.from_dict(
            {
                "Country": [
                    "Benin",
                    "Burkina Faso",
                    "Angola",
                    "Congo, Dem. Rep. of the",
                    "Cabo Verde",
                ],
                "Year": [1980, 1980, 1980, 1980, 1980],
                "NGDP_RPCH": [9.0, 4.0, 2.0, 2.0, 5.0],
            },
            schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
        ),
    )


def test_merge_duplicate_dfs_left_has_nulls():
    # GIVEN
    df = pl.from_dict(
        {
            "Country": [
                "Benin",
                "Burkina Faso",
                "Angola",
                "Congo, Dem. Rep. of the",
                "Cabo Verde",
            ],
            "Year": [
                1980,
                1980,
                1980,
                1980,
                1980,
            ],
            "NGDP_RPCH": [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                5,
            ],
        },
        schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
    )
    all_dfs = [df, df]

    # WHEN
    result = merge_duplicate_dfs(all_dfs, "NGDP_RPCH")

    # THEN
    assert_frame_equal(result, df)
