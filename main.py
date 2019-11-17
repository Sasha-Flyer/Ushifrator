from flask import Flask, render_template, request
from shifer import *

app = Flask(__name__)



@app.route('/')
def hello_world():
    z = zip(emotions_pegasus + emotions_unicorns + emotions_earth, names_pegasus + names_unicorns + names_earth)
    return render_template("ponychooser.html", pegasus=names_pegasus, emotions_pegasus=z, unicorns=names_unicorns,
                           emotions_unicorns=zip(emotions_unicorns, names_unicorns),
                           earth=names_earth, emotions_earth=zip(emotions_earth, names_earth))


@app.route('/decrypt')
def test():
    return render_template("ушифратор.html")


@app.route('/decrypt', methods=['POST'])
def testt():
    if "textarea" in request.form.keys() and len(request.form['textarea']) > 0:
        area = request.form['textarea']
        if "storage" in area and area[-1] == 'g':
            area = area[area.index("storage") + 8:-4]
            with open("messeges.json") as file:
                jsn = json.load(file)
            if area in jsn.keys():
                text = jsn[area]
                print("\n" in text)
                if "secret" in request.form.keys():
                    return render_template("ушифратор.html", search=text,
                                           save=request.form['secret'])
                return render_template("ушифратор.html", search=text)
            else:
                if "secret" in request.form.keys():
                    return render_template("ушифратор.html",
                                           search_error="Расшифровать не удалось. Вероятно, этот шифр - подделка.",
                                           save=request.form['secret'])
                return render_template("ушифратор.html",
                                       search_error="Расшифровать не удалось. Вероятно, этот шифр - подделка.")
        else:
            if "secret" in request.form.keys():
                return render_template("ушифратор.html",
                                       search_error="Не удалось распознать шифр. Просто перетащите картинку сюда.",
                                       save=request.form['secret'])
            return render_template("ушифратор.html",
                                   search_error="Не удалось распознать шифр. Просто перетащите картинку сюда.")
    else: render_template("ушифратор.html")


@app.route('/', methods=['POST'])
def processing():
    data = request.form
    id = data['emotion']
    text = data['secret'].lower()
    pony = data['pony']
    wing = ("wings" in data.keys())
    magic = ("magic" in data.keys())
    z = zip(emotions_pegasus+emotions_unicorns+emotions_earth, names_pegasus+names_unicorns+names_earth)
    for char in text:
        if char not in keys.keys():
            return render_template("ponychooser.html", pegasus=names_pegasus, emotions_pegasus=z,
                                   unicorns=names_unicorns,
                                   emotions_unicorns=zip(emotions_unicorns, names_unicorns),
                                   earth=names_earth, emotions_earth=zip(emotions_earth, names_earth),
                                   error="Неподдерживаемый символ: {0}".format(char), save = text.replace(char, ""))
    if len(text) > 1000:
        return render_template("ponychooser.html", pegasus=names_pegasus, emotions_pegasus=z,
                               unicorns=names_unicorns,
                               emotions_unicorns=zip(emotions_unicorns, names_unicorns),
                               earth=names_earth, emotions_earth=zip(emotions_earth, names_earth),
                               error="Максимальный размер шифра - 1000. Сейчас у вас {0} символов".format(len(text)),
                               save=text)
    elif len(text) == 0:
        return render_template("ponychooser.html", pegasus=names_pegasus, emotions_pegasus=z,
                               unicorns=names_unicorns,
                               emotions_unicorns=zip(emotions_unicorns, names_unicorns),
                               earth=names_earth, emotions_earth=zip(emotions_earth, names_earth),
                               error="Введите текст")
    return render_template("ponychooser.html", message=ponies[pony].make_svg(id, text, wing, magic),
                           pegasus=names_pegasus, emotions_pegasus=z, unicorns=names_unicorns,
                           emotions_unicorns=zip(emotions_unicorns, names_unicorns),
                           earth=names_earth, emotions_earth=zip(emotions_earth, names_earth))


if __name__ == '__main__':
    with open("config.json") as file:
        jsn = json.load(file)
        local = jsn["local"]
    if local:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=80, debug=False)