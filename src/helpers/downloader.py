import requests
from pathlib import Path

def download_to_local(url:str, destination:Path, parent_mkdir:bool = True):
    if not isinstance(destination, Path):
        raise ValueError(f'{destination} should be the pathlib')
    if parent_mkdir:
        destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(url)
        response.raise_for_status()
        destination.write_bytes(response.content)
        print('Everything written!')
        return True
    except requests.RequestException as e:
        print(f'Failed to download {url}: {e}')
        return False