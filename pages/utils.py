import requests


def get_dog_image():
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    if response.json()["status"] == "success":
        image = response.json()["message"]
        return image
    else:
        return None
