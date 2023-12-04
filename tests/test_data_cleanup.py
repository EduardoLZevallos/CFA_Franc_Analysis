import datetime
import pandas as pd
import numpy as np
from  cfa_analysis.data_cleanup import find_outliers_IQR, rename_from_abbr_to_full_name


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
    
def test_find_outliers_IQR_no_outliers_found():
    # GIVEN
    data = {'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'B': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]}
    df = pd.DataFrame(data)
    
    # WHEN
    outliers = find_outliers_IQR(df)

    # THEN
    expected_result = pd.DataFrame({'A': [float('nan')] * 10, 'B': [float('nan')] * 10})
    pd.testing.assert_frame_equal(outliers,expected_result)
    
def test_find_outliers_IQR_outliers_found():
    # GIVEN
    data = {'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 100],  # Outlier: 100
            'B': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]}
    df = pd.DataFrame(data)
    
    # WHEN
    outliers = find_outliers_IQR(df)
    
    # THEN
    expected_result = pd.DataFrame({'A': [np.nan] * 9 + [100.0], 'B': [np.nan] * 10})
    pd.testing.assert_frame_equal(outliers, expected_result)
    
    
    pd.testing.assert_frame_equal(cleaned_df, expected_result)
