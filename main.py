from flask import Flask, render_template, request
app = Flask(__name__)
from shifer import *
from django import template
register = template.Library()

@register.simple_tag
def include_anything(file_name):
    return open(file_name).read()
@app.route('/')
def hello_world():
    print(request.host)
    if request.host == "http://127.0.0.1:5000/" or request.host ==  "xn--80aptgckdj8a.xn--p1ai"  or request.host ==  "ушифратор.рф":
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
                    return render_template("ушифратор.html", available_chars=available_chars, search=text,
                                           save=request.form['secret'])
                return render_template("ушифратор.html", available_chars=available_chars, search=text)
            else:
                if "secret" in request.form.keys():
                    return render_template("ушифратор.html", available_chars=available_chars,
                                           search_error="Расшифровать не удалось. Вероятно, этот шифр - подделка.",
                                           save=request.form['secret'])
                return render_template("ушифратор.html", available_chars=available_chars,
                                       search_error="Расшифровать не удалось. Вероятно, этот шифр - подделка.")
        else:
            if "secret" in request.form.keys():
                return render_template("ушифратор.html", available_chars=available_chars,
                                       search_error="Не удалось распознать шифр. Просто перетащите картинку сюда.",
                                       save=request.form['secret'])
            return render_template("ушифратор.html", available_chars=available_chars,
                                   search_error="Не удалось распознать шифр. Просто перетащите картинку сюда.")
    else: render_template("ушифратор.html")

@app.route('/', methods=['POST'])
def processing():
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
                    return render_template("ушифратор.html", available_chars=available_chars, search=text, save=request.form['secret'])
                return render_template("ушифратор.html", available_chars=available_chars, search=text)
            else:
                if "secret" in request.form.keys():
                    return render_template("ушифратор.html", available_chars=available_chars,
                                           search_error="Расшифровать не удалось. Вероятно, этот шифр - подделка.",
                                           save=request.form['secret'])
                return render_template("ушифратор.html", available_chars=available_chars, search_error="Расшифровать не удалось. Вероятно, этот шифр - подделка.")
        else:
            if  "secret"  in request.form.keys():
                return render_template("ушифратор.html", available_chars=available_chars,
                                       search_error="Не удалось распознать шифр. Просто перетащите картинку сюда.", save = request.form['secret'])
            return render_template("ушифратор.html", available_chars=available_chars,
                                   search_error="Не удалось распознать шифр. Просто перетащите картинку сюда.")

    data = request.form
    print(data)
    id = data['emotion']
    text = data['secret'].lower()
    pony = data['pony']
    wing = ("wings" in data.keys())
    magic = ("magic" in data.keys())

    z = zip(emotions_pegasus+emotions_unicorns+emotions_earth, names_pegasus+names_unicorns+names_earth)

    for char in text:
        if char not in keys.keys():
            if request.host == "127.0.0.1:5000" or True:
                return render_template("ponychooser.html", pegasus=names_pegasus, emotions_pegasus=z,
                                       unicorns=names_unicorns,
                                       emotions_unicorns=zip(emotions_unicorns, names_unicorns),
                                       earth=names_earth, emotions_earth=zip(emotions_earth, names_earth), error = "Неподдерживаемый символ: {0}".format(char), save = text.replace(char, ""))
    if len(text) > 1000:
        return render_template("ponychooser.html", pegasus=names_pegasus, emotions_pegasus=z,
                               unicorns=names_unicorns,
                               emotions_unicorns=zip(emotions_unicorns, names_unicorns),
                               earth=names_earth, emotions_earth=zip(emotions_earth, names_earth),
                               error="Максимальный размер шифра - 1000. Сейчас у вас {0} символов".format(len(text)), save=text)
    elif len(text) == 0:
        return render_template("ponychooser.html", pegasus=names_pegasus, emotions_pegasus=z,
                               unicorns=names_unicorns,
                               emotions_unicorns=zip(emotions_unicorns, names_unicorns),
                               earth=names_earth, emotions_earth=zip(emotions_earth, names_earth),
                               error="Введите текст")
    if request.host == "127.0.0.1:5000" or request.host == "xn--80aptgckdj8a.xn--p1ai" or request.host ==  "ушифратор.рф":
        return render_template("ponychooser.html", message=ponies[pony].make_svg(id, text, wing, magic),
                               pegasus=names_pegasus, emotions_pegasus=z, unicorns=names_unicorns,
                               emotions_unicorns=zip(emotions_unicorns, names_unicorns),
                               earth=names_earth, emotions_earth=zip(emotions_earth, names_earth))

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80, debug=False)
  # app.run(debug=True)

