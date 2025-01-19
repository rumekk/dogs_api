import json
import webbrowser
import requests
from pprint import pprint
import credentials


def get_json_from_request(request):
    try:
        content = request.json()
    except json.decoder.JSONDecodeError:
        pprint('Niepoprawny format')
    else:
        return content


def get_favourites(userId):
    params = {
        'sub_id': userId,
    }
    req = requests.get("https://api.thedogapi.com/v1/favourites",
                       params, headers=credentials.headers)
    return get_json_from_request(req)


def get_random_doggo():
    req = requests.get(
        "https://api.thedogapi.com/v1/images/search", headers=credentials.headers)
    return get_json_from_request(req)[0]
# ?breed_ids=8,121,226


def add_to_favourites(imageId, userId):
    imageData = {
        'image_id': imageId,
        'sub_id': userId
    }
    req = requests.post("https://api.thedogapi.com/v1/favourites",
                        json=imageData, headers=credentials.headers)
    return get_json_from_request(req)


def remove_from_favourites(userId, idFromFavourites):
    req = requests.delete("https://api.thedogapi.com/v1/favourites/" +
                          idFromFavourites, headers=credentials.headers)
    return get_json_from_request(req)


# def get_image_by_id(imageId):
#     req = requests.get(f"https://api.thedogapi.com/v1/images/{imageId}", headers=credentials.headers)
#     return get_json_from_request(req)
