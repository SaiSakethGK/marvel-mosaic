import hashlib
import time
import requests

PUBLIC_KEY = 'fbe37c4860e8046b563a216c91a085f5'
PRIVATE_KEY = '11e9068fd09399fe432c4da4040b25bfb4491039'
LIMIT = 100


def generate_hash(time_stamp):
    hash_input = time_stamp + PRIVATE_KEY + PUBLIC_KEY
    return hashlib.md5(hash_input.encode()).hexdigest()


def get_marvel_characters(max_characters=1000):
    characters = []
    time_stamp = str(time.time())
    hash_value = generate_hash(time_stamp)
    offset = 0

    while len(characters) < max_characters:
        params = {
            'apikey': PUBLIC_KEY,
            'ts': time_stamp,
            'hash': hash_value,
            'limit': LIMIT,
            'offset': offset
        }

        response = requests.get('http://gateway.marvel.com/v1/public/characters', params=params, timeout=10)
        data = response.json()

        if 'data' in data and 'results' in data['data']:
            characters.extend(data['data']['results'])
            offset += LIMIT
        else:
            break

    return characters[:max_characters]

def get_character_by_id(character_id):
    ts = str(time.time())
    hash_value = hashlib.md5((ts + PRIVATE_KEY + PUBLIC_KEY).encode('utf-8')).hexdigest()

    url = f"http://gateway.marvel.com/v1/public/characters/{character_id}"
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts,
        'hash': hash_value
    }

    response = requests.get(url, params=params)
    return response.json()['data']['results'][0]