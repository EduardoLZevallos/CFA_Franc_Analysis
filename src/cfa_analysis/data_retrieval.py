import requests
from typing import Optional


def rename_from_abbr_to_full_name(inflation_dict: dict, all_countries: dict) -> dict:
    abbrv = list(inflation_dict.keys())
    for key in abbrv:
        inflation_dict[all_countries["countries"][key]["label"]] = inflation_dict.pop(
            key
        )
    return inflation_dict


def get_data_from_imf(url: str) -> Optional[dict]:
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
    abbr = [countries[x] for x in country_list]
    url = f"https://www.imf.org/external/datamapper/api/v1/{metric_abbr}"
    for country in abbr:
        url += f"/{country}"
    return get_data_from_imf(url)["values"][metric_abbr]
