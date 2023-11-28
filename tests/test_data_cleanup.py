import datetime
import pandas as pd
import numpy as np
from  cfa_analysis.data_cleanup import find_outliers_IQR

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
