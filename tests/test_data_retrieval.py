from unittest.mock import patch

import pandas as pd
import pytest
from  cfa_analysis.data_retrieval import rename_from_abbr_to_full_name, get_data_from_imf, get_all_metric_data

def test_rename_from_abbr_to_full_name():
    # GIVEN
    inflation_dict = {
        "USA": 2.3,
        "CAN": 1.9,
        "AUS": 1.8
    }
    all_countries = {
        "countries": {
            "USA": {"label": "United States"},
            "CAN": {"label": "Canada"},
            "AUS": {"label": "Australia"}
        }
    }

    # WHEN
    result = rename_from_abbr_to_full_name(inflation_dict, all_countries)

    # THEN
    assert result == {
        "United States": 2.3,
        "Canada": 1.9,
        "Australia": 1.8
    }
    
class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        return {"some": "data"}

@patch('cfa_analysis.data_retrieval.requests.get')
def test_get_data_from_imf_valid_url(mock_requests_get):
    # GIVEN
    mock_requests_get.return_value = MockResponse(200) 

    # WHEN
    data = get_data_from_imf("valid_url")

    # THEN
    assert data == {
        'some' : 'data'
    }
    
@patch('cfa_analysis.data_retrieval.requests.get')
def test_get_data_from_imf_invalid_url(mock_requests_get):
    # GIVEN
    mock_requests_get.return_value = MockResponse(404)
    url = "invalid_url"

    # WHEN
    data = get_data_from_imf(url)

    # THEN
    assert data is None

@patch('cfa_analysis.data_retrieval.get_data_from_imf')
def test_get_all_metric_data(mock_get_data_from_imf):
    # GIVEN
    country_list = ["Nicaragua", "Cuba", "Venezuela"]
    metric_abbr = "GDP"
    countries = {"Nicaragua": "NIC", "Cuba": "CUB", "Venezuela": "VEN"}
    mock_get_data_from_imf.return_value = {
            "values": {
                "GDP": {
                    "2021": 100,
                    "2022": 110,
                    "2023": 120
                }
            }
        }
    
    # WHEN
    result = get_all_metric_data(country_list, metric_abbr, countries)

    # THEN
    assert result == {
        "2021": 100,
        "2022": 110,
        "2023": 120
    }
    mock_get_data_from_imf.assert_called_once_with(
        "https://www.imf.org/external/datamapper/api/v1/GDP/NIC/CUB/VEN")