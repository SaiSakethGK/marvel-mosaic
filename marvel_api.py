import hashlib
import time
import requests

PUBLIC_KEY = 'fde588ec5df0f1e04985e5211581029c'
PRIVATE_KEY = '72cf8b450b4d360126b186906ec81b769d66ecfb'
LIMIT = 100


def generate_hash(ts):
    to_hash = ts + PRIVATE_KEY + PUBLIC_KEY
    return hashlib.md5(to_hash.encode()).hexdigest()


def get_marvel_characters(max_characters=80):
    characters = []
    offset = 0

    while len(characters) < max_characters:
        ts = str(time.time())
        hash_value = generate_hash(ts)

        params = {
            'apikey': PUBLIC_KEY,
            'ts': ts,
            'hash': hash_value,
            'limit': LIMIT,
            'offset': offset
        }

        url = 'https://gateway.marvel.com/v1/public/characters'
        print(f"Fetching: {url} with {params}")

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"Error fetching Marvel characters: {e}")
            break

        if 'data' in data and 'results' in data['data']:
            characters.extend(data['data']['results'])
            offset += LIMIT
        else:
            break

    return characters[:max_characters]



def get_character_by_id(character_id):
    ts = str(time.time())
    hash_value = hashlib.md5((ts + PRIVATE_KEY + PUBLIC_KEY).encode('utf-8')).hexdigest()
    print("Hash value: "+hash_value)

    url = f"https://gateway.marvel.com/v1/public/characters/{character_id}"
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts,
        'hash': hash_value
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json().get('data', {})
        results = data.get('results', [])
        return results[0] if results else None
    except Exception as e:
        print(f"Marvel API error for character ID {character_id}: {e}")
        return None
