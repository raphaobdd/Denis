import requests

def get_all_data(url, params=None):
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()   # retorna lista ou dict

