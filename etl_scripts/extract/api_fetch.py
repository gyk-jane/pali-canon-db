import requests
import pandas as pd
from prefect import flow, task

@task(log_prints=True)
def get_menu_data(uid: str) -> dict:
    """
    Retrieves menu data from SuttaCentral API based on the provided uid.
    This menu data will provide children information of the provided uid.
    Args:
        uid (str): The unique identifier for the menu.
    Returns:
        dict: The menu data retrieved from the API.
    Raises:
        requests.exceptions.RequestException: If there is an error in making the API request.
    """
    url = f'https://suttacentral.net/api/menu/{uid}'
    response = requests.get(url)
    try:
        response.raise_for_status()
        menu_data = response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error retrieving menu data: {uid} - {err}\n")
        menu_data = None
    return menu_data

@task(log_prints=True)
def get_suttaplex(basket: str) -> None:
    """
    Retrieves suttaplex data from the SuttaCentral API for given basket.
    Args:
        basket (str): The basket identifier (sutta, vinaya, or abhidhamma)
    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    suttaplex_url = f'https://suttacentral.net/api/suttaplex/{basket}'
    response = requests.get(suttaplex_url, timeout=30)
    response.raise_for_status()
    data = response.json()
        
    return data
