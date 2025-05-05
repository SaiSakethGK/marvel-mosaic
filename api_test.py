import hashlib
import time
import requests

# Your new keys
public_key = "fde588ec5df0f1e04985e5211581029c"
private_key = "72cf8b450b4d360126b186906ec81b769d66ecfb"

# Step 1: Generate timestamp
ts = str(int(time.time()))  # Use int here

# Step 2: Generate hash
to_hash = ts + private_key + public_key
hash_ = hashlib.md5(to_hash.encode()).hexdigest()

# Step 3: Call the Marvel API
url = "https://gateway.marvel.com/v1/public/characters"
params = {
    "ts": ts,
    "apikey": public_key,
    "hash": hash_,
    "limit": 1
}

print(f"Fetching: {url} with {params}")
response = requests.get(url, params=params)
print("Status:", response.status_code)
print("Response:", response.json())
