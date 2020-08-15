import bs4
import requests
import json

CHARACTERS = {}


for index in range(10):
    limit = index * 50
    response = requests.get("https://myanimelist.net/character.php", params={"limit": limit})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    for i, elem in enumerate(soup.find_all("a", {"class": "fs14 fw-b"})):
        name = " ".join(elem.text.split(", ")[::-1])
        CHARACTERS[name] = limit + i

with open("characters.json", "w") as f:
    json.dump(CHARACTERS, f, indent=4)