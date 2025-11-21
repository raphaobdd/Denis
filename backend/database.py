from supabase import create_client
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')


def fetch_asteroids(pages=3):
    url = API_URL
    params = {"api_key": API_KEY}
    results = []

    for _ in range(pages):
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()

        data = response.json()
        neos = data.get("near_earth_objects", [])

        for neo in neos:
            item = {
                "id": neo["id"],
                "name": neo["name"],
                "absolute_magnitude": neo["absolute_magnitude_h"],
                "is_potentially_hazardous_asteroid": neo["is_potentially_hazardous_asteroid"],
                "diameter_km_min": neo["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                "diameter_km_max": neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
            }

            cad = neo.get("close_approach_data", [])
            if cad:
                approach = cad[0]
                item["close_approach_date"] = approach.get("close_approach_date")
                item["rel_km_s"] = float(approach["relative_velocity"]["kilometers_per_second"])
                item["miss_km"] = float(approach["miss_distance"]["kilometers"])
            else:
                item["close_approach_date"] = None
                item["rel_km_s"] = None
                item["miss_km"] = None

            results.append(item)

        url = data.get("links", {}).get("next")
        if not url:
            break

    return results


def salvar_asteroides_supabase(lista_dados):
    for item in lista_dados:
        supabase.table("asteroids").upsert(item).execute()


# Executando todo o fluxo
dados = fetch_asteroids(pages=3)
salvar_asteroides_supabase(dados)
print(f"{len(dados)} asteroides inseridos/atualizados!")
