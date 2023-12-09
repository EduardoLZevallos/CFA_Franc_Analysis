from unittest.mock import patch, call

from polars.testing import assert_frame_equal
import polars as pl
import pandas as pd
import pytest
from cfa_analysis.data_retrieval import (
    get_all_metric_data,
    InsufficientDataError,
    get_country_mapping,
    get_indicators_data,
    get_cfa_and_noncfa_data,
    get_imf_data_df,
    get_all_duplicate_dfs,
)


class MockResponse:
    def __init__(self, response_dict):
        self.response_dict = response_dict

    def json(self):
        return self.response_dict


# @patch("cfa_analysis.data_retrieval.requests.get")
# def test_get_data_from_imf_valid_url(mock_requests_get):
#     # GIVEN
#     mock_requests_get.return_value = MockResponse(200)

#     # WHEN
#     data = get_data_from_imf("valid_url")

#     # THEN
#     assert data == {"some": "data"}


# @patch("cfa_analysis.data_retrieval.requests.get")
# def test_get_data_from_imf_invalid_url(mock_requests_get):
#     # GIVEN
#     mock_requests_get.return_value = MockResponse(404)
#     url = "invalid_url"

#     # WHEN
#     data = get_data_from_imf(url)

#     # THEN
#     assert data is None


@patch("cfa_analysis.data_retrieval.requests.get")
def test_get_all_metric_data_sucessfully(mock_requests_get):
    # GIVENresponse = requests.get("https://www.imf.org/external/datamapper/api/v1/=--/NNNN")
    country_list = ["Nicaragua", "Cuba", "Venezuela"]
    metric_abbr = "GDP"
    countries = {"Nicaragua": "NIC", "Cuba": "CUB", "Venezuela": "VEN"}
    mock_requests_get.return_value = MockResponse(
        {
            "values": {
                "GDP": {
                    "NIC": {
                        "2001": 0.5,
                        "2002": 3.8,
                    },
                    "CUB": {
                        "2001": 0.5,
                        "2002": 3.8,
                    },
                    "VEN": {
                        "2001": 0.5,
                        "2002": 3.8,
                    },
                }
            },
            "api": {"version": "1", "output-method": "json"},
        }
    )

    # WHEN
    result = get_all_metric_data(country_list, metric_abbr, countries)

    # THEN
    assert result == {
        "NIC": {
            "2001": 0.5,
            "2002": 3.8,
        },
        "CUB": {
            "2001": 0.5,
            "2002": 3.8,
        },
        "VEN": {
            "2001": 0.5,
            "2002": 3.8,
        },
    }
    mock_requests_get.assert_called_once_with(
        "https://www.imf.org/external/datamapper/api/v1/GDP/NIC/CUB/VEN"
    )


@patch("cfa_analysis.data_retrieval.requests.get")
def test_get_all_metric_data_response_less_than_80_percent_of_countries(
    mock_requests_get,
):
    # GIVEN
    country_list = ["United_States", "Canada", "Nicaragua", "Cuba", "Venezuela"]
    metric_abbr = "GDP"
    countries = {
        "United_States": "USA",
        "Canada": "CAN",
        "Nicaragua": "NIC",
        "Cuba": "CUB",
        "Venezuela": "VEN",
    }
    mock_requests_get.return_value = MockResponse(
        {
            "values": {
                "GDP": {
                    "NIC": {
                        "2001": 0.5,
                        "2002": 3.8,
                    },
                    "CUB": {
                        "2001": 0.5,
                        "2002": 3.8,
                    },
                    "VEN": {
                        "2001": 0.5,
                        "2002": 3.8,
                    },
                }
            },
            "api": {"version": "1", "output-method": "json"},
        }
    )

    # WHEN
    with pytest.raises(
        InsufficientDataError,
        match="Response returned country data for less than 80% of provided countries",
    ) as e_info:
        result = get_all_metric_data(country_list, metric_abbr, countries)

    # THEN
    mock_requests_get.assert_called_once_with(
        "https://www.imf.org/external/datamapper/api/v1/GDP/USA/CAN/NIC/CUB/VEN"
    )


@patch("cfa_analysis.data_retrieval.requests.get")
def test_get_country_mapping(mock_request_get):
    # GIVEN
    mock_request_get.return_value = MockResponse(
        {
            "countries": {
                "ABW": {"label": "Aruba"},
                "AFG": {"label": "Afghanistan"},
                "AGO": {"label": "Angola"},
                "AIA": {"label": "Anguilla"},
                "ALB": {"label": "Albania"},
                "ARE": {"label": "United Arab Emirates"},
            }
        }
    )
    # WHEN
    result_abbreviation_key, result_label_key = get_country_mapping()

    # THEN
    assert result_abbreviation_key == {
        "countries": {
            "ABW": {"label": "Aruba"},
            "AFG": {"label": "Afghanistan"},
            "AGO": {"label": "Angola"},
            "AIA": {"label": "Anguilla"},
            "ALB": {"label": "Albania"},
            "ARE": {"label": "United Arab Emirates"},
        }
    }
    assert result_label_key == {
        "Aruba": "ABW",
        "Afghanistan": "AFG",
        "Angola": "AGO",
        "Anguilla": "AIA",
        "Albania": "ALB",
        "United Arab Emirates": "ARE",
    }


@patch("cfa_analysis.data_retrieval.requests.get")
def test_get_indicators_data(mock_request_get):
    # GIVEN
    mock_request_get.return_value = MockResponse(
        {
            "indicators": {
                "NGDP_RPCH": {
                    "label": "Real GDP growth",
                    "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at constant prices of final goods and services produced within a country during a specified time period, such as one year.",
                    "source": "World Economic Outlook (October 2023)",
                    "unit": "Annual percent change",
                    "dataset": "WEO",
                },
                "NGDPD": {
                    "label": "GDP, current prices",
                    "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at current prices of final goods and services produced within a country during a specified time period, such as one year.",
                    "source": "World Economic Outlook (October 2023)",
                    "unit": "Billions of U.S. dollars",
                    "dataset": "WEO",
                },
            }
        }
    )
    # WHEN
    result = get_indicators_data()

    # THEN
    assert result == {
        "NGDP_RPCH": {
            "label": "Real GDP growth",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at constant prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "Annual percent change",
            "dataset": "WEO",
        },
        "NGDPD": {
            "label": "GDP, current prices",
            "description": "Gross domestic product is the most commonly used single measure of a country's overall economic activity. It represents the total value at current prices of final goods and services produced within a country during a specified time period, such as one year.",
            "source": "World Economic Outlook (October 2023)",
            "unit": "Billions of U.S. dollars",
            "dataset": "WEO",
        },
    }


@patch("cfa_analysis.data_retrieval.get_all_metric_data")
def test_get_cfa_and_noncfa_data_success(mock_get_all_metric_data):
    # GIVEN
    mock_get_all_metric_data.side_effect = [
        {
            "AGO": {
                "1980": 2.4,
                "1981": -4.4,
                "1982": 0,
                "1983": 4.2,
            },
            "COD": {
                "1980": 2.4,
                "1981": 0.9,
                "1982": -0.5,
                "1983": 1.4,
            },
        },
        {
            "CPV": {
                "1980": 5.3,
                "1981": 8.5,
                "1982": 2.8,
                "1983": 9.5,
            },
            "GHA": {
                "1980": 0.5,
                "1981": -3.8,
                "1982": -8.3,
                "1983": -6.2,
            },
        },
        {
            "BEN": {
                "1980": 9.3,
                "1981": 1.9,
                "1982": 1.7,
                "1983": -2,
            },
            "BFA": {
                "1980": 4,
                "1981": 2.7,
                "1982": 1.4,
                "1983": -1.2,
            },
        },
    ]
    all_countries = {
        "countries": {
            "AGO": {"label": "Angola"},
            "BEN": {"label": "Benin"},
            "BFA": {"label": "Burkina Faso"},
            "COD": {"label": "Congo, Dem. Rep. of the"},
            "CPV": {"label": "Cabo Verde"},
            "GHA": {"label": "Ghana"},
        },
        "api": {"version": "1", "output-method": "json"},
    }

    countries = {
        "Angola": "AGO",
        "Benin": "BEN",
        "Burkina Faso": "BFA",
        "Congo, Dem. Rep. of the": "COD",
        "Cabo Verde": "CPV",
        "Ghana": "GHA",
    }
    indicator_abbrv = "NGDP_RPCH"

    # WHEN
    result = get_cfa_and_noncfa_data(indicator_abbrv, countries, all_countries)

    # THEN
    assert result == {
        "Benin": {
            "1980": 9.3,
            "1981": 1.9,
            "1982": 1.7,
            "1983": -2,
        },
        "Burkina Faso": {
            "1980": 4,
            "1981": 2.7,
            "1982": 1.4,
            "1983": -1.2,
        },
        "Angola": {
            "1980": 2.4,
            "1981": -4.4,
            "1982": 0,
            "1983": 4.2,
        },
        "Congo, Dem. Rep. of the": {
            "1980": 2.4,
            "1981": 0.9,
            "1982": -0.5,
            "1983": 1.4,
        },
        "Cabo Verde": {
            "1980": 5.3,
            "1981": 8.5,
            "1982": 2.8,
            "1983": 9.5,
        },
        "Ghana": {
            "1980": 0.5,
            "1981": -3.8,
            "1982": -8.3,
            "1983": -6.2,
        },
    }


def test_get_imf_data_df():
    # GIVEN
    sample_imf_data = {
        "Benin": {
            "1980": 9.3,
            "1981": 1.9,
            "1982": 1.7,
            "1983": -2,
        },
        "Burkina Faso": {
            "1980": 4,
            "1981": 2.7,
            "1982": 1.4,
            "1983": -1.2,
        },
        "Angola": {
            "1980": 2.4,
            "1981": -4.4,
            "1982": 0,
            "1983": 4.2,
        },
        "Congo, Dem. Rep. of the": {
            "1980": 2.4,
            "1981": 0.9,
            "1982": -0.5,
            "1983": 1.4,
        },
        "Cabo Verde": {
            "1980": 5.3,
            "1981": 8.5,
            "1982": 2.8,
            "1983": 9.5,
        },
        "Ghana": {
            "1980": 0.5,
            "1981": -3.8,
            "1982": -8.3,
            "1983": -6.2,
        },
    }
    indicator_abbrv = "NGDP_RPCH"
    # WHEN
    df = get_imf_data_df(sample_imf_data, indicator_abbrv)

    # THEN
    assert_frame_equal(
        df,
        pl.from_dict(
            {
                "Country": [
                    "Benin",
                    "Burkina Faso",
                    "Angola",
                    "Congo, Dem. Rep. of the",
                    "Cabo Verde",
                    "Ghana",
                    "Benin",
                    "Burkina Faso",
                    "Angola",
                    "Congo, Dem. Rep. of the",
                    "Cabo Verde",
                    "Ghana",
                    "Benin",
                    "Burkina Faso",
                    "Angola",
                    "Congo, Dem. Rep. of the",
                    "Cabo Verde",
                    "Ghana",
                    "Benin",
                    "Burkina Faso",
                    "Angola",
                    "Congo, Dem. Rep. of the",
                    "Cabo Verde",
                    "Ghana",
                ],
                "Year": [
                    1980,
                    1980,
                    1980,
                    1980,
                    1980,
                    1980,
                    1981,
                    1981,
                    1981,
                    1981,
                    1981,
                    1981,
                    1982,
                    1982,
                    1982,
                    1982,
                    1982,
                    1982,
                    1983,
                    1983,
                    1983,
                    1983,
                    1983,
                    1983,
                ],
                "NGDP_RPCH": [
                    9.300000190734863,
                    4.0,
                    2.4000000953674316,
                    2.4000000953674316,
                    5.300000190734863,
                    0.5,
                    1.899999976158142,
                    2.700000047683716,
                    -4.400000095367432,
                    0.8999999761581421,
                    8.5,
                    -3.799999952316284,
                    1.7000000476837158,
                    1.399999976158142,
                    0.0,
                    -0.5,
                    2.799999952316284,
                    -8.300000190734863,
                    -2.0,
                    -1.2000000476837158,
                    4.199999809265137,
                    1.399999976158142,
                    9.5,
                    -6.199999809265137,
                ],
            },
            schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
        ),
    )


@patch("cfa_analysis.data_retrieval.get_cfa_and_noncfa_data")
@patch("cfa_analysis.data_retrieval.get_imf_data_df")
def test_get_all_duplicate_dfs(mock_get_imf_data_df, mock_get_cfa_and_noncfa_data):
    # GIVEN
    imf_data_df = pl.from_dict(
        {
            "Country": [
                "Benin",
                "Burkina Faso",
                "Angola",
                "Congo, Dem. Rep. of the",
                "Cabo Verde",
                "Ghana",
                "Benin",
                "Burkina Faso",
                "Angola",
                "Congo, Dem. Rep. of the",
                "Cabo Verde",
                "Ghana",
                "Benin",
                "Burkina Faso",
                "Angola",
                "Congo, Dem. Rep. of the",
                "Cabo Verde",
                "Ghana",
                "Benin",
                "Burkina Faso",
                "Angola",
                "Congo, Dem. Rep. of the",
                "Cabo Verde",
                "Ghana",
            ],
            "Year": [
                1980,
                1980,
                1980,
                1980,
                1980,
                1980,
                1981,
                1981,
                1981,
                1981,
                1981,
                1981,
                1982,
                1982,
                1982,
                1982,
                1982,
                1982,
                1983,
                1983,
                1983,
                1983,
                1983,
                1983,
            ],
            "NGDP_RPCH": [
                9.300000190734863,
                4.0,
                2.4000000953674316,
                2.4000000953674316,
                5.300000190734863,
                0.5,
                1.899999976158142,
                2.700000047683716,
                -4.400000095367432,
                0.8999999761581421,
                8.5,
                -3.799999952316284,
                1.7000000476837158,
                1.399999976158142,
                0.0,
                -0.5,
                2.799999952316284,
                -8.300000190734863,
                -2.0,
                -1.2000000476837158,
                4.199999809265137,
                1.399999976158142,
                9.5,
                -6.199999809265137,
            ],
        },
        schema={"Country": pl.Utf8, "Year": pl.Int32, "NGDP_RPCH": pl.Float32},
    )
    cfa_noncfa_data = {
        "Benin": {
            "1980": 9.3,
            "1981": 1.9,
            "1982": 1.7,
            "1983": -2,
        },
        "Burkina Faso": {
            "1980": 4,
            "1981": 2.7,
            "1982": 1.4,
            "1983": -1.2,
        },
        "Angola": {
            "1980": 2.4,
            "1981": -4.4,
            "1982": 0,
            "1983": 4.2,
        },
        "Congo, Dem. Rep. of the": {
            "1980": 2.4,
            "1981": 0.9,
            "1982": -0.5,
            "1983": 1.4,
        },
        "Cabo Verde": {
            "1980": 5.3,
            "1981": 8.5,
            "1982": 2.8,
            "1983": 9.5,
        },
        "Ghana": {
            "1980": 0.5,
            "1981": -3.8,
            "1982": -8.3,
            "1983": -6.2,
        },
    }
    # prob can just pass the list not the entire dict
    duplicate_combinations = {
        ("Real GDP Growth Rate", "% change"): ["NGDP_RPCH", "NGDP_R_PCH"],
        ("Government Revenue", "% of GDP"): ["rev", "GGR_G01_GDP_PT"],
        ("Government Expenditure", "% of GDP"): ["exp", "GGX_GDP"],
    }
    indicator_label = "Government Revenue"
    unit = "% of GDP"
    skip_indicators = set()
    mock_get_imf_data_df.side_effect = [imf_data_df, imf_data_df]
    mock_get_cfa_and_noncfa_data.side_effect = [cfa_noncfa_data, cfa_noncfa_data]

    all_countries = {
        "countries": {
            "AGO": {"label": "Angola"},
            "BEN": {"label": "Benin"},
            "BFA": {"label": "Burkina Faso"},
            "COD": {"label": "Congo, Dem. Rep. of the"},
            "CPV": {"label": "Cabo Verde"},
            "GHA": {"label": "Ghana"},
        },
        "api": {"version": "1", "output-method": "json"},
    }

    countries = {
        "Angola": "AGO",
        "Benin": "BEN",
        "Burkina Faso": "BFA",
        "Congo, Dem. Rep. of the": "COD",
        "Cabo Verde": "CPV",
        "Ghana": "GHA",
    }

    # WHEN
    result = get_all_duplicate_dfs(
        duplicate_combinations,
        indicator_label,
        unit,
        skip_indicators,
        countries,
        all_countries,
    )

    # THEN
    assert mock_get_cfa_and_noncfa_data.call_count == 2
    mock_get_cfa_and_noncfa_data.assert_has_calls(
        [
            call("rev", countries, all_countries),
            call("GGR_G01_GDP_PT", countries, all_countries),
        ]
    )

    assert mock_get_imf_data_df.call_count == 2
    mock_get_imf_data_df.assert_has_calls(
        [call(cfa_noncfa_data, indicator_label), call(cfa_noncfa_data, indicator_label)]
    )
    assert skip_indicators == {"rev", "GGR_G01_GDP_PT"}
