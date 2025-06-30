from dotenv import load_dotenv
import os
from openrouteservice import Client


def calculate_distance(origin: str, destination: str, profile) -> dict | None:
    """
    Calcula a distância e a duração estimada entre dois endereços
    utilizando a API do OpenRouteService.
    
    Parâmetros:
    - origin (str): Endereço de origem.
    - destination (str): Endereço de destino.
    - profile: Perfil do tipo de transporte (ex: 'driving-car', 'driving-hgv').

    Retorna:
    - dict: Um dicionário contendo a distância (em km) e a duração (em horas),
            ou None em caso de erro.
    """
    load_dotenv(dotenv_path='.env')
    api_key = os.getenv("API_KEY")

    if not api_key:
        print("[Erro] Chave de API não encontrada no .env")
        return None

    client = Client(key=api_key)
    if profile == "driving-car":
        profile = "driving-car"
    if profile == "driving-hgv":
        profile = "driving-hgv"

    def geocode(address: str):
        try:
            result = client.pelias_search(text=address)
            coords = result['features'][0]['geometry']['coordinates']
            return tuple(coords)
        except (IndexError, KeyError):
            raise ValueError(f"Endereço inválido ou não encontrado: {address}")

    try:
        coords_origin = geocode(origin)
        coords_dest = geocode(destination)

        rota = client.directions(
            coordinates=[coords_origin, coords_dest],
            profile=profile,
            format='json'
        )

        distancia_km = rota['routes'][0]['summary']['distance'] / 1000
        duracao_horas = rota['routes'][0]['summary']['duration'] / 3600

        return {
            "distancia_km": f"{distancia_km:.2f}",
            "duracao_horas": f"{duracao_horas:.1f}"
        }

    except Exception as e:
        print(f"[Erro ao calcular rota] {e}")
        return None


ponto_A = 'Rua Olivio Segatto, 1017, Tupi Paulista, SP, 17930045'
ponto_B = 'Rua Folha Dourada, 6, São Paulo, SP, 08161-060, '


print(calculate_distance(ponto_A, ponto_B, 'driving-car'))