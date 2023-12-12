import pytest
import polars as pl
from polars.testing import assert_frame_equal
from cfa_analysis.analysis import get_median_df, analyze_medians


def test_get_median_df():
    # GIVEN
    df = pl.from_dict(
        {
            "Country": [
                "Benin",
                "Burkina Faso",
                "Central African Republic",
                "Côte d'Ivoire",
                "Cameroon",
                "Congo, Republic of ",
                "Gabon",
                "Guinea-Bissau",
                "Equatorial Guinea",
                "Mali",
                "Niger",
                "Senegal",
                "Chad",
                "Togo",
                "Angola",
                "Congo, Dem. Rep. of the",
                "São Tomé and Príncipe",
                "Cabo Verde",
                "Ghana",
                "Guinea",
                "Gambia, The",
                "Liberia",
                "Mauritania",
                "Nigeria",
                "Sierra Leone",
            ],
            "Year": [
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
            ],
            "Real GDP Growth Rate": [
                9.300000190734863,
                4.0,
                -3.0,
                5.199999809265137,
                9.899999618530273,
                12.699999809265137,
                0.0,
                None,
                4.800000190734863,
                3.299999952316284,
                4.900000095367432,
                -0.800000011920929,
                -6.0,
                -2.299999952316284,
                2.4000000953674316,
                2.4000000953674316,
                -1.100000023841858,
                5.300000190734863,
                0.5,
                2.5999999046325684,
                0.699999988079071,
                None,
                None,
                None,
                -0.6000000238418579,
            ],
        },
        schema={
            "Country": pl.Utf8,
            "Year": pl.Int32,
            "Real GDP Growth Rate": pl.Float32,
        },
    )
    # WHEN
    result = get_median_df(df, "Real GDP Growth Rate")

    # THEN
    assert_frame_equal(
        result,
        pl.from_dict(
            {
                "Year": [1980],
                "cfa_median": [4.0],
                "noncfa_median": [2.4000000953674316],
                "abs_cfa_median": [4.0],
                "abs_noncfa_median": [2.4000000953674316],
            },
            schema={
                "Year": pl.Int32,
                "cfa_median": pl.Float32,
                "noncfa_median": pl.Float32,
                "abs_cfa_median": pl.Float32,
                "abs_noncfa_median": pl.Float32,
            },
        ),
    )


def test_analyze_medians_CFA_has_more_intervals_where_median_is_higher():
    # GIVEN
    median_df = pl.from_dict(
        {
            "Year": [1980, 1981, 1982, 1983],
            "cfa_median": [4.0, 5.0, 6.0, 7.0],
            "noncfa_median": [2.0, 3.0, 4.0, 5.0],
            "abs_cfa_median": [4.0, 5.0, 6.0, 7.0],
            "abs_noncfa_median": [2.0, 3.0, 4.0, 5.0],
        },
        schema={
            "Year": pl.Int32,
            "cfa_median": pl.Float32,
            "noncfa_median": pl.Float32,
            "abs_cfa_median": pl.Float32,
            "abs_noncfa_median": pl.Float32,
        },
    )
    # WHEN
    result = analyze_medians(median_df)

    # THEN
    assert result == ("African CFA Countries", [1980, 1981, 1982, 1983])


def test_analyze_medians_Non_CFA_has_more_intervals_where_median_is_higher():
    # GIVEN
    median_df = pl.from_dict(
        {
            "Year": [1980, 1981, 1982, 1983],
            "noncfa_median": [4.0, 5.0, 6.0, 7.0],
            "cfa_median": [2.0, 3.0, 4.0, 5.0],
            "abs_noncfa_median": [4.0, 5.0, 6.0, 7.0],
            "abs_cfa_median": [2.0, 3.0, 4.0, 5.0],
        },
        schema={
            "Year": pl.Int32,
            "cfa_median": pl.Float32,
            "noncfa_median": pl.Float32,
            "abs_cfa_median": pl.Float32,
            "abs_noncfa_median": pl.Float32,
        },
    )
    # WHEN
    result = analyze_medians(median_df)

    # THEN
    assert result == (
        "Non-CFA Middle Africa and Western Africa Countries",
        [1980, 1981, 1982, 1983],
    )


def test_analyze_medians_where_count_is_within_two_so_considered_equal():
    #
    median_df = pl.from_dict(
        {
            "Year": [1980, 1981, 1982, 1983],
            "noncfa_median": [10.0, 5.0, 6.0, 7.0],
            "cfa_median": [4.0, 5.0, 6.0, 7.0],
            "abs_noncfa_median": [4.0, 5.0, 6.0, 7.0],
            "abs_cfa_median": [4.0, 5.0, 6.0, 7.0],
        },
        schema={
            "Year": pl.Int32,
            "cfa_median": pl.Float32,
            "noncfa_median": pl.Float32,
            "abs_cfa_median": pl.Float32,
            "abs_noncfa_median": pl.Float32,
        },
    )
    # WHEN
    result = analyze_medians(median_df)

    # THEN
    assert result == (
        "CFA and Non CFA countries have roughly an equal amount of intervals where their respective medians was higher",
        [1980, 1981, 1982, 1983],
    )