import datetime
import pandas as pd
import numpy as np
from  cfa_analysis.data_cleanup import find_outliers_IQR, remove_outliers, remove_future_years

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
    
def test_remove_outliers_no_outliers():
    # GIVEN
    original_data = {'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'B': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]}
    outlier_data = {'A': [float('nan')] * 10, 'B': [float('nan')] * 10}
    original_df = pd.DataFrame(original_data)
    outlier_df = pd.DataFrame(outlier_data)

    # WHEN
    cleaned_df = remove_outliers(original_df, outlier_df)

    # THEN
    expected_result = pd.DataFrame({'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                    'B': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]})
    
    pd.testing.assert_frame_equal(cleaned_df, expected_result)

def test_remove_outliers_mixed_outliers():
    # GIVEN
    original_data = {'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'B': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]}
    outlier_data = {'A': [float('nan'), 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Outlier: 2
                    'B': [float('nan'), 10, 15, 20, 25, 30, 35, 40, 45, 50]}
    original_df = pd.DataFrame(original_data)
    outlier_df = pd.DataFrame(outlier_data)

    # WHEN
    cleaned_df = remove_outliers(original_df, outlier_df)

    # THEN
    expected_result = pd.DataFrame({'A': [1, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                                    'B': [5, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]})
    pd.testing.assert_frame_equal(cleaned_df, expected_result)

def test_remove_future_years():
    # GIVEN
    current_year = datetime.datetime.now().year
    data = {'year': [current_year - 2, current_year - 1, current_year, current_year + 1],
            'value': [10, 20, 30, 40]}
    median_df = pd.DataFrame(data)

    # WHEN
    filtered_df = remove_future_years(median_df)

    # THEN
    expected_result = pd.DataFrame({'year': [current_year - 2, current_year - 1, current_year],
                                    'value': [10, 20, 30]})
    pd.testing.assert_frame_equal(filtered_df, expected_result)