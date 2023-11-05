import pandas as pd
from  cfa_analysis.median_analysis import generate_median_df, analyze_medians

def test_generate_median_df_multiple_columns():
    # GIVEN
    df = pd.DataFrame({'2026': {'Benin': 15.957120583638,
      'Burkina Faso': 21.751984021882,
      'Cameroon': 15.276436727498,
      'Central African Republic': 17.813262271024,
      'Chad': 18.122023046887,
      'Congo, Republic of ': 24.767128503001,
      "Côte d'Ivoire": 17.964340458605,
      'Equatorial Guinea': 16.816999590326,
      'Gabon': 17.833734415904,
      'Guinea-Bissau': 16.611017092856,
      'Mali': 22.483689583185,
      'Niger': 19.70280766226,
      'Senegal': 23.281517749846,
      'Togo': 18.326945016511},
     '2027': {'Benin': 16.457120583638,
      'Burkina Faso': 22.232385243724,
      'Cameroon': 15.281385158321,
      'Central African Republic': 17.730243113895,
      'Chad': 18.738886780455,
      'Congo, Republic of ': 24.549433383639,
      "Côte d'Ivoire": 17.937017341522,
      'Equatorial Guinea': 16.25586719744,
      'Gabon': 17.732059808203,
      'Guinea-Bissau': 16.928003342113,
      'Mali': 22.707552862806,
      'Niger': 19.752482712501,
      'Senegal': 23.532366053973,
      'Togo': 18.826570848518},
     '2028': {'Benin': 16.857120583638,
      'Burkina Faso': 22.596274439084,
      'Cameroon': 15.346160903338,
      'Central African Republic': 17.681195940774,
      'Chad': 17.729688314162,
      'Congo, Republic of ': 24.052521335298,
      "Côte d'Ivoire": 17.956271531288,
      'Equatorial Guinea': 15.636264329902,
      'Gabon': 17.623441793848,
      'Guinea-Bissau': 17.045901243232,
      'Mali': 22.964548671718,
      'Niger': 19.757142068433,
      'Senegal': 23.343598955458,
      'Togo': 19.283118666619}})

    # WHEN
    median_df = generate_median_df(df)

    # THEN
    expected_result = pd.DataFrame({'year': {0: 2026, 1: 2027, 2: 2028},
     'median': {0: 18.043181752746, 1: 18.3379520609885, 2: 17.842979922725}}
    )
    pd.testing.assert_frame_equal(median_df, expected_result)
    
def test_analyze_medians_non_cfa_higher_medians():
    # GIVEN
    merge_df = pd.DataFrame( {'year': [2019, 2020, 2021],
            'median_cfa': [10, 20, 30],
            'median_non_cfa': [15, 25, 35]})

    # WHEN
    result = analyze_medians(merge_df)

    # THEN
    expected_result = ("Non Cfa African Franc Zone Countries", [2019, 2020, 2021])
    assert result == expected_result
 
def test_analyze_medians_cfa_higher_medians():
    # GIVEN
    merge_df = pd.DataFrame( {'year': [2019, 2020, 2021],
            'median_cfa': [20, 26, 36],
            'median_non_cfa': [15, 25, 35]})

    # WHEN
    result = analyze_medians(merge_df)

    # THEN
    expected_result = ("Cfa African Franc Zone Countries", [2019, 2020, 2021])
    assert result == expected_result

 
def test_analyze_medians_difference_within_two_so_consider_it_equal():
    # GIVEN
    merge_df = pd.DataFrame( {'year': [2019, 2020, 2021],
            'median_cfa': [14, 26, 36],
            'median_non_cfa': [15, 25, 35]})

    # WHEN
    result = analyze_medians(merge_df)

    # THEN
    expected_result = ("CFA and Non CFA were equal", [2019, 2020, 2021])
    assert result == expected_result
 