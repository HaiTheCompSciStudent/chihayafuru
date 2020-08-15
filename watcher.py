from discord.ext import commands, tasks

import pytesseract
import requests
import numpy
import json
import cv2

POINTS = [(50, 220), (325, 495), (600, 770), (875, 1045)]
EMOJIS = {
    0: "1\ufe0f\u20e3",
    1: "2\ufe0f\u20e3",
    2: "3\ufe0f\u20e3",
    3: "4\ufe0f\u20e3"
}

CHANNEL_ID = 648044573536550922
KARUTA_ID = 646937666251915264

with open("characters.json", "r") as f:
    CHARACTERS = json.load(f)


class Karuta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.karuta_watcher.start()

    @tasks.loop(minutes=30)
    async def karuta_watcher(self):

        print("Started watching for SSR Cards...")

        def event_check(m):
            return all((m.author.id == KARUTA_ID, m.channel.id == CHANNEL_ID))

        while True:
            try:
                message = await self.bot.wait_for("message", check=event_check)
                if message.attachments:
                    attachments = message.attachments.pop()
                    r = requests.get(attachments.url)
                    with open("temp.jpg", "wb") as f:
                        f.write(r.content)
                    cards = cv2.imread("temp.jpg")
                    characters = []
                    for i, name in enumerate(self._ocr_name(cards)):
                        try:
                            rank = CHARACTERS[name]
                        except KeyError:
                            pass
                        else:
                            print("Found %s [RANK%s] in the selection!" % (name, rank))
                            characters.append((i, name, rank))
                    if characters:
                        i, name, rank = min(characters, key=lambda p: p[2])
                        print("Attempting to pick %s [RANK%s]..." % (name, rank))
                        await message.add_reaction(EMOJIS[i])
            except Exception:
                continue

    @karuta_watcher.before_loop
    async def prep_karuta_watcher(self):
        print("Preparing Karuta Watcher... ")
        await self.bot.wait_until_ready()

    def _ocr_name(self, image):
        h, w, c = image.shape
        n = 4 if w > 836 else 3
        for i in range(n):
            start_x, end_x = POINTS[i]
            name_box = image[60: 105, start_x: end_x]
            name_box = cv2.cvtColor(name_box, cv2.COLOR_RGB2GRAY)
            name = pytesseract.image_to_string(name_box).rstrip()
            yield name


def setup(bot):
    bot.add_cog(Karuta(bot))
