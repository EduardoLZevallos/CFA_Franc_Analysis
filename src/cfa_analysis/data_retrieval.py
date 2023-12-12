""" Retrieves data from imf, country list, indicator list, and metrics for indicator per country """
import math
import requests
from typing import Any

import polars as pl
import polars.selectors as cs
from .constants import CFA_FRANC_ZONE, WEST_AFRICA, MIDDLE_AFRICA
from .data_cleanup import rename_from_abbr_to_full_name
from .data_classes import Indicator


class InsufficientDataError(Exception):
    """Exception raised if query returns datas for fewer than 80% of requested countries"""


def get_all_metric_data(country_list: list, metric_abbr: str, countries: dict) -> dict:
    """Generates url link necessary for imf query"""
    try:
        abbr = [countries[x] for x in country_list]
        url = f"https://www.imf.org/external/datamapper/api/v1/{metric_abbr}"
        for country in abbr:
            url += f"/{country}"
        response = requests.get(url).json()["values"][metric_abbr]
        if len(response) < math.ceil(len(country_list) * 0.8):
            raise InsufficientDataError(
                "Response returned country data for less than 80% of provided countries"
            )
        return response
    except InsufficientDataError:
        raise  # Re-raise the exception

    return None


def get_cfa_and_noncfa_data(
    indicator_abbrv: str, countries: dict, all_countries: dict
) -> dict:
    """Returns a dict of all data for middle africa,
    west africa, and cfa franc zone for a given indicator"""
    middle_africa_data = rename_from_abbr_to_full_name(
        get_all_metric_data(MIDDLE_AFRICA, indicator_abbrv, countries),
        all_countries,
    )  # believe theres a limit to api payload
    west_africa_data = rename_from_abbr_to_full_name(
        get_all_metric_data(WEST_AFRICA, indicator_abbrv, countries),
        all_countries,
    )
    cfa_data = rename_from_abbr_to_full_name(
        get_all_metric_data(CFA_FRANC_ZONE, indicator_abbrv, countries),
        all_countries,
    )
    cfa_data.update(middle_africa_data)
    cfa_data.update(west_africa_data)
    return cfa_data


def get_country_mapping() -> dict[str, str]:
    """Returns all countires from imf in two dicts,
    one where country name is the key, one where abbreviation is the key"""
    all_countries = requests.get(
        "https://www.imf.org/external/datamapper/api/v1/countries"
    ).json()
    return all_countries, {v["label"]: k for k, v in all_countries["countries"].items()}


def get_indicators_data() -> dict[str, dict[str, Any]]:
    """Returns all economic indicators you can query for from imf"""
    return requests.get(
        "https://www.imf.org/external/datamapper/api/v1/indicators"
    ).json()["indicators"]


def get_imf_data_df(imf_data: dict, indicator: str) -> pl.DataFrame:
    """returns dataframe of imf data for a given metric for all african zones"""
    return (
        pl.from_dicts(
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
        )
        .melt(
            id_vars="Country",
            value_vars=cs.numeric(),
            variable_name="Year",
            value_name=indicator,
        )
        .cast({indicator: pl.Float32})
        .with_columns(pl.col("Year").str.strptime(pl.Date, "%Y").dt.year())
    )


def get_all_duplicate_dfs(
    duplicate_combinations: dict[tuple[str, str], list[str]],
    indicator: type[Indicator],
    skip_indicators: set,
    countries: dict[str, str],
    all_countries: dict[str, str],
) -> list[pl.DataFrame]:
    """Returns a list of dataframes of all indicators that are duplicates"""
    all_dfs = []
    for indicator_abbrv in duplicate_combinations[(indicator.label, indicator.unit)]:
        all_dfs.append(
            get_imf_data_df(
                get_cfa_and_noncfa_data(indicator_abbrv, countries, all_countries),
                indicator.label,
            )
        )
        skip_indicators.add(indicator_abbrv)
    return all_dfs
