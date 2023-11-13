import requests
from typing import Optional, Dict, Any, List, Tuple, Set
import math
import logging

import polars as pl
import polars.selectors as cs
from .constants import CFA_FRANC_ZONE, WEST_AFRICA, MIDDLE_AFRICA
from .data_cleanup import rename_from_abbr_to_full_name


def get_all_duplicate_dfs(duplicate_combinations: Dict[Tuple[str, str], List[str]], indicator_label: str, unit: str, skip_indicators: Set, countries: Dict[str,str], all_countries: Dict[str,str]):
    """ Returns a list of dataframes of all indicators that are duplicates """
    all_dfs = []
    for indicator_abbrv in duplicate_combinations[(indicator_label,unit)]:
        all_dfs.append(get_imf_data_df(get_cfa_and_noncfa_data(
            indicator_abbrv, countries, all_countries
        ), indicator_label))
        skip_indicators.add(indicator_abbrv)
    return all_dfs
    
def get_data_from_imf(url: str) -> Optional[dict]:
    """ Queries imf api for data """
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        # Do something with the data
        return data
    else:
        print("Error: Could not retrieve data from the API endpoint")


def get_all_metric_data(country_list: list, metric_abbr: str, countries: dict) -> dict:
    """ Generates url link necessary for imf query """
    try:
        abbr = [countries[x] for x in country_list]
        url = f"https://www.imf.org/external/datamapper/api/v1/{metric_abbr}"
        for country in abbr:
            url += f"/{country}"
        response = get_data_from_imf(url)["values"][metric_abbr]
        if len(response) < math.ceil(len(country_list) * .8) : # not enough data returned
            raise Exception("Response returned country data for less than 80% of provided countries") 
        return get_data_from_imf(url)["values"][metric_abbr]
    except Exception as e:
        logging.debug(
                f"issue with indicator abbrv: {metric_abbr}, for zone {country_list} exception: {e} no data returned"
        )


def get_cfa_and_noncfa_data(
    indicator_abbrv: str, countries: dict, all_countries: dict
) -> dict:
    
    chunk_1_data_non_cfa = rename_from_abbr_to_full_name(
        get_all_metric_data(MIDDLE_AFRICA, indicator_abbrv, countries),
        all_countries,
    )  # believe theres a limit to api payload
    chunk_2_data_non_cfa = rename_from_abbr_to_full_name(
        get_all_metric_data(WEST_AFRICA, indicator_abbrv, countries),
        all_countries,
    )
    cfa_data = rename_from_abbr_to_full_name(
        get_all_metric_data(CFA_FRANC_ZONE, indicator_abbrv, countries),
        all_countries,
    )
    cfa_data.update(chunk_1_data_non_cfa)
    cfa_data.update(chunk_2_data_non_cfa)
    return cfa_data


def get_country_mapping() -> Dict[str, str]:
    all_countries = get_data_from_imf(
        "https://www.imf.org/external/datamapper/api/v1/countries"
    )
    return all_countries, {v["label"]: k for k, v in all_countries["countries"].items()}


def get_indicators_data() -> Dict[str, Dict[str, Any]]:
    indicators_imf_dict = get_data_from_imf(
        "https://www.imf.org/external/datamapper/api/v1/indicators"
    )
    return indicators_imf_dict["indicators"]


def get_imf_data_df(imf_data: dict, indicator: str) -> pl.DataFrame:
    return pl.from_dicts(
        data=[{"Country": country, **imf_data[country]} for country in imf_data],
        schema=[
            "Country",
            "1980",
            "1981",
            "1982",
            "1983",
            "1984",
            "1985",
            "1986",
            "1987",
            "1988",
            "1989",
            "1990",
            "1991",
            "1992",
            "1993",
            "1994",
            "1995",
            "1996",
            "1997",
            "1998",
            "1999",
            "2000",
            "2001",
            "2002",
            "2003",
            "2004",
            "2005",
            "2006",
            "2007",
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
            "2023",
        ],
    ).melt(
        id_vars="Country",
        value_vars=cs.numeric(),
        variable_name="Year",
        value_name=indicator,
    ).cast({
        indicator: pl.Float32
    }).with_columns(pl.col("Year").str.strptime(pl.Date, "%Y").dt.year())
