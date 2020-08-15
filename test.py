import urllib.request
import requests
resp = requests.get("https://cdn.discordapp.com/attachments/740864143522922509/744078647761174559/card.jpg")
print(resp)
output = open("temp.jpg", "wb")
output.write(resp.content)
output.close()