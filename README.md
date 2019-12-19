# Ushifrator

В папке с проектом должен быть `config.json` в следующем формате:
```
{
"login": "ВашЛогинТабуна",<br>
"password": "Пароль",<br>
"local": true если вы хотите запустить сервер локально<br>
}
```

Требуется Python 3 (если стоят одновременно Python 2.x и Python 3.x, то нужно
конфигурировать проект так, чтобы он запускался с помощью Python 3.x).

Установка зависимостей:
```
pip install pillow
pip install flask
pip install git+https://github.com/andreymal/tabun_api.git#egg=tabun_api[full]
```

## Конфигурация для mod_wsgi

В корневом каталоге веб-сервера (или виртуального хоста) надо
создать файл `Ushifrator.wsgi` примерно такого содержания: 
```
# -*- encoding: utf-8 -*-
import os, sys
sys.path.insert(0, '/usr/share/htdocs/Ushifrator')
os.chdir('/usr/share/htdocs/Ushifrator')
from main import app as application
```

В `httpd.conf` или включаемый из него конфиг, в секцию,
относящуюся к серверу или виртуальному хосту (на тот же уровень,
где находится соответствующая директива `DocumentRoot`),
нужно добавить следующую строку:
```
WSGIScriptAlias / /usr/share/htdocs/Ushifrator.wsgi
```

В обоих местах `/usr/share/htdocs` надо заменить на путь к корню веб-сервера
(где в подкаталоге `Ushifrator` лежит код из git-репозитория).

