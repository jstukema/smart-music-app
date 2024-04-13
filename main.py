import json


from dotenv import load_dotenv
import os
import base64
from requests import post, get

load_dotenv()
client_id = os.getenv("CLIENT_ID")
secret_id = os.getenv("SECRET_ID")


def retrieve_token():
    auth_string = f"{client_id}:{secret_id}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + auth_base64, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


def search_for_id(artist_name, type, limit=20):
    url = "https://api.spotify.com/v1/search"
    query = f"?q={artist_name}&type={type}&limit={limit}"
    query_url = f"{url}{query}"

    token = retrieve_token()
    headers = {"Authorization": f"Bearer {token}"}
    result = get(query_url, headers=headers)

    json_result = json.loads(result.content)["artists"]

    if len(json_result) == 0:
        print("No artist with this name exists....")
        return None
    return json_result


search_list = search_for_id("fela", "artist")

print(search_list)
