from os import mkdir, remove
from PIL import Image
import tabun_api
import json
import base64

with open("C:\config.json") as file:
    jsn = json.load(file)
login = jsn["login"]
password = jsn["password"]
me = tabun_api.User(login=login, passwd=password)
p = "C:/Users/User/PycharmProjects/site/"
available = []
available_chars = []
keys = {
    "а": "1",
    "б": "93",
    "в": "95",
    "г": "96",
    "д": "97",
    "е": "4",
    "ё": "99",
    "ж": "62",
    "з": "22",
    "и": "23",
    "к": "29",
    "л": "25",
    "м": "26",
    "н": "27",
    "о": "0",
    "п": "28",
    "р": "63",
    "с": "65",
    "т": "32",
    "у": "33",
    "ф": "35",
    "х": "36",
    "ц": "37",
    "ч": "38",
    "ш": "39",
    "щ": "66",
    "ъ": "52",
    "ы": "53",
    "ь": "56",
    "э": "57",
    "ю": "58",
    "я": "59",
    "й": "61",
    " ": "67",
    ",": "68",
    ".": "69",
    "!": "72",
    "?": "73",
    ":": "75",
    "(": "76",
    ")": "77",
    "1": "78",
    "2": "79",
    "3": "82",
    "4": "83",
    "5": "85",
    "6": "86",
    "7": "87",
    "8": "88",
    "9": "89",
    "+": "92",
    "-": "93",
    "=": "95",
    "\r": "97",
    "\n": "98",
    "0": "96"
}

svg_template = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" height="80" width="80" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 80 80">{0}</svg>'''
h = 'hidden;'
v = 'visible;'
svg_elemet = '''<image class="p" xlink:href="{0}" width="80" height="80" transform="translate(0 0) scale(1) "> <animate id="pony" attributeName="visibility" fill = "freeze"  from="hidden" values = "{1}" to="hidden" dur="{2}" calcMode="discrete" repeatCount="indefinite"
/></image>'''
svg_simple = """
<image class="s" xlink:href="{0}" width="80" height="80" transform="translate(0 0) scale(1)"></image>"""

class Pony():
    def __init__(self, my_name, bot = True, bot_wing = False, ears = True, emotes = True, blink = True, top_name = True, magic = False):
        self.name = my_name
        self.bot = bot
        self.emotes = emotes
        if bot:

            file = "new\{0}\{1}.png".format(self.name, self.name + "_" + "BOT")
            self.botimg, self.bot64 = self.get_img_64(file)
        self.bot_wing = bot_wing
        if bot_wing:
            file = "new\{0}\{1}.png".format(self.name, self.name + "_" + "BOT_WING")
            self.bot_wingimg, self.bot_wing64 = self.get_img_64(file)
        if ears:
            self.ears = []
            for i in range(10):
                file = "new\{0}\{1}.png".format(self.name, "test" + self.name + "_" + "EARS" + str(i) + "_opt")
                self.ears.append(self.base_64(file))
            file = "new\{0}\{1}.png".format(self.name, "test" + self.name + "_" + "EARS" + str(0) + "_opt")
            self.earsimg = self.get_first_frame(file)
        if emotes:

            self.emotesimg = []
            self.emotes64 = []
            start_file = "new\{0}\{1}".format(self.name, self.name + "_" + "EMOTES")
            for i in range(1, 29):
                file = "{0}\q{1:04d}.png".format(start_file, i)
                img, b64 = self.get_img_64(file)
                self.emotesimg.append(img)
                self.emotes64.append(b64)
        if blink:
            self.blink = True
            file = "new\{0}\{1}.png".format(self.name, "test" + self.name + "_" + "BLINK" + str(81) + "_opt")
            self.blinkimg = self.get_first_frame(file)
            self.blink64 = self.base_64(file)
        self.mane = top_name
        if top_name:
            self.top_name = []
            for i in range(10):
                file = "new\{0}\{1}.png".format(self.name, "test" + self.name + "_" + "TOP_MANE" + str(i) + "_opt")
                self.top_name.append(self.base_64(file))
            file = "new\{0}\{1}.png".format(self.name, "test" + self.name + "_" + "TOP_MANE" + str(0) + "_opt")
            self.top_maneimg = self.get_first_frame(file)
        self.magic = magic
        if magic:
            file = "new\{0}\{1}.png".format(self.name, self.name + "_" + "MAGIC")
            self.magicimg = self.get_first_frame(file)
            self.magic64 = self.base_64(file)
      #  self.make_preview()
    # разкомментить когда добавятся новые персонажи
    def make_svg(self, id, text, wing = False, magic = False):
        code = ""

        for char in text:
            code += keys[char]

        duration = len(code)
        data = ['', '', '', '', '', '', '', '', '', '']
        for c in code:
            for i, d in enumerate(data):
                if int(c) == i:
                    data[i] += v
                else: data[i] += h
        example = ""
        if wing and self.bot_wing:
            example += svg_simple.format(self.bot_wing64)
        elif self.bot:
            example += svg_simple.format(self.bot64)
        if self.ears:
            for i, ear in enumerate(self.ears):
                if ("visible" in data[i]):
                    example += svg_elemet.format(ear, data[i], duration)
        if self.emotes:
            example+=svg_simple.format(self.emotes64[int(id)])
        if self.blink:
            example+=svg_simple.format(self.blink64)
        if self.mane:
            for i, mane in enumerate(self.top_name):
                if ("visible" in data[i]):
                    example += svg_elemet.format(mane, data[i], duration)
        if self.magic and magic:
            example+=svg_simple.format(self.magic64)

        with open("dellme.svg", "w") as svg:
            svg.write(svg_template.format(example))

        link = me.upload_image_file("dellme.svg",title=text)
        remove("dellme.svg")
        key = link[link.index("storage") + 8:link.index(".svg")]
        with open("messeges.json") as file:
            jsn = json.load(file)
        jsn[key] = text
        with open("messeges.json", "w") as file:
            file.write(json.dumps(jsn, sort_keys=True, indent=4, separators=(',', ': ')))
        return link

    def make_preview(self):
        folder = "{0}\{1}".format("static", self.name)
        try:
            mkdir(folder)
        except:
            pass
        for i, emote in enumerate(self.emotesimg):
            pr = Image.new("RGBA", (80, 80))
            if self.bot: pr = Image.alpha_composite(pr, self.botimg.convert('RGBA'))
            pr = Image.alpha_composite(pr, self.earsimg.convert('RGBA'))
            pr = Image.alpha_composite(pr, emote.convert('RGBA'))
            pr = Image.alpha_composite(pr, self.blinkimg.convert('RGBA'))
            if self.mane: pr = Image.alpha_composite(pr, self.top_maneimg.convert('RGBA'))
            pr.save("{0}\{1}.png".format(folder, i))
        if False and self.bot_wing: # крылья теперь только в SVG, этот блок не нужен.
            folder = "{0}\{1}".format("static", self.name + "_" + "WING")
            mkdir(folder)
            for i, emote in enumerate(self.emotesimg):
                pr = Image.new("RGBA", (80, 80))
                pr = Image.alpha_composite(pr, self.bot_wingimg.convert('RGBA'))
                pr = Image.alpha_composite(pr, self.earsimg.convert('RGBA'))
                pr = Image.alpha_composite(pr, emote.convert('RGBA'))
                pr = Image.alpha_composite(pr, self.blinkimg.convert('RGBA'))
                if self.top_name: pr = Image.alpha_composite(pr, self.top_maneimg.convert('RGBA'))
                pr.save("{0}\{1}.png".format(folder, i))


    def get_img_64(self, file):
        image = Image.open(file)
        with open(file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        bas64 = encoded_string.decode("utf-8")
        return image, "data:image/png;base64," + bas64

    def base_64(self, file):
        with open(file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        bas64 = encoded_string.decode("utf-8")
        return "data:image/png;base64," + bas64

    def get_first_frame(self, file):
        im = Image.open(file)
        left, upper, width, lower = 0, 0, 80, 80
        bbox = (left, upper, width, lower)
        working_slice = im.crop(bbox)
        return working_slice


names_pegasus = ["TS", "FS", "RD"]
names_unicorns = ["SG"]
names_earth = ["BG"]
ponies = dict()
for name in names_pegasus:
    ponies[name] = Pony(name, bot_wing=True)
for name in names_unicorns:
    ponies[name] = Pony(name, magic=True)
for name in names_earth:
    ponies[name] = Pony(name, bot=False, top_name=False)
emotions_pegasus = []
emotions_unicorns = []
emotions_earth = []
for pegas in names_pegasus:
    emotion = []
    for i in range(28):
        emotion.append(i)
    emotions_pegasus.append(emotion)
for unicorn in names_unicorns:
    emotion = []
    for i in range(28):
        emotion.append(i)
    emotions_unicorns.append(emotion)
for earth in names_earth:
    emotion = []
    for i in range(28):
        emotion.append(i)
    emotions_earth.append(emotion)
