# Сайт доставки еды Star Burger

Это сайт сети ресторанов [Star Burger](https://inftechntransport.ru/). Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Как запустить dev-версию сайта

Для запуска сайта нужно запустить **одновременно** бэкенд и фронтенд, в двух терминалах.

### Быстрый запуск на сервере (деплой)
После скачивания кода с гитхаба и занесения в файл .env необходимых переменных окружения.
Перейдите в скаченную папку с проектом на сервере и запустите скрипт:
```pycon
. deploy_star_burger.sh
```
Данный скрипт установит папку виртуального окружения, установит в нее
все зависимости из requirements.txt и необходимые библиотеки JS, соберет фронтенд
соберет всю статику в одну папку и перезапустит команды Systemd

### Как собрать бэкенд

Скачайте код:
```sh
git clone https://github.com/devmanorg/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии. 

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Определите переменную окружения `SECRET_KEY`. Создать файл `.env` в каталоге `star_burger/` и положите туда такой код:
```sh
SECRET_KEY=django-insecure-0if40nf4nf93n4
```

Создайте файл базы данных SQLite и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Если вы увидели пустую белую страницу, то не пугайтесь, выдохните. Просто фронтенд пока ещё не собран. Переходите к следующему разделу README.

### Собрать фронтенд

**Откройте новый терминал**. Для работы сайта в dev-режиме необходима одновременная работа сразу двух программ `runserver` и `parcel`. Каждая требует себе отдельного терминала. Чтобы не выключать `runserver` откройте для фронтенда новый терминал и все нижеследующие инструкции выполняйте там.

[Установите Node.js](https://nodejs.org/en/), если у вас его ещё нет.

Проверьте, что Node.js и его пакетный менеджер корректно установлены. Если всё исправно, то терминал выведет их версии:

```sh
nodejs --version
# v16.16.0
# Если ошибка, попробуйте node:
node --version
# v16.16.0

npm --version
# 8.11.0
```

Версия `nodejs` должна быть не младше `10.0` и не старше `16.16`. Лучше ставьте `16.16.0`, её мы тестировали. Версия `npm` не важна. Как обновить Node.js читайте в статье: [How to Update Node.js](https://phoenixnap.com/kb/update-node-js-version).

Перейдите в каталог проекта и установите пакеты Node.js:

```sh
cd star-burger
npm ci --dev
```

Команда `npm ci` создаст каталог `node_modules` и установит туда пакеты Node.js. Получится аналог виртуального окружения как для Python, но для Node.js.

Помимо прочего будет установлен [Parcel](https://parceljs.org/) — это упаковщик веб-приложений, похожий на [Webpack](https://webpack.js.org/). В отличии от Webpack он прост в использовании и совсем не требует настроек.

Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:

```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Если вы на Windows, то вам нужна та же команда, только с другими слешами в путях:

```sh
.\node_modules\.bin\parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Дождитесь завершения первичной сборки. Это вполне может занять 10 и более секунд. О готовности вы узнаете по сообщению в консоли:

```
✨  Built in 10.89s
```

Parcel будет следить за файлами в каталоге `bundles-src`. Сначала он прочитает содержимое `index.js` и узнает какие другие файлы он импортирует. Затем Parcel перейдёт в каждый из этих подключенных файлов и узнает что импортируют они. И так далее, пока не закончатся файлы. В итоге Parcel получит полный список зависимостей. Дальше он соберёт все эти сотни мелких файлов в большие бандлы `bundles/index.js` и `bundles/index.css`. Они полностью самодостаточны, и потому пригодны для запуска в браузере. Именно эти бандлы сервер отправит клиенту.

Теперь если зайти на страницу  [http://127.0.0.1:8000/](http://127.0.0.1:8000/), то вместо пустой страницы вы увидите:

![](https://dvmn.org/filer/canonical/1594651900/687/)

Каталог `bundles` в репозитории особенный — туда Parcel складывает результаты своей работы. Эта директория предназначена исключительно для результатов сборки фронтенда и потому исключёна из репозитория с помощью `.gitignore`.

**Сбросьте кэш браузера <kbd>Ctrl-F5</kbd>.** Браузер при любой возможности старается кэшировать файлы статики: CSS, картинки и js-код. Порой это приводит к странному поведению сайта, когда код уже давно изменился, но браузер этого не замечает и продолжает использовать старую закэшированную версию. В норме Parcel решает эту проблему самостоятельно. Он следит за пересборкой фронтенда и предупреждает JS-код в браузере о необходимости подтянуть свежий код. Но если вдруг что-то у вас идёт не так, то начните ремонт со сброса браузерного кэша, жмите <kbd>Ctrl-F5</kbd>.


## Как запустить prod-версию сайта

Собрать фронтенд:

```sh
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
```

Настроить бэкенд: создать файл `.env` в каталоге `star_burger/` со следующими настройками:

- `DEBUG` — дебаг-режим. Поставьте `False`.
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `YANDEX_API_KEY` - ключ API разработчика Яндекса
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)

Для просмотра и фиксации ошибок при работе сайта - необходимо зарегестрироваться на сайте [rollbar](https://rollbar.com/)
Создать проект и записать в файле `.env` project_access_token. Вы можете этого не делать,
если вам не нужно получать информацию об ошибках в роллбаре.
Тогда укажите в .env `ROLLBAR=False`. Если же нужны записи ошибок, то в .env необходимо
прописать `ROLLBAR=True` и указать следующие 3 переменные окружения:
```sh
ROLLBAR_ACCESS_TOKEN='521c.....'
```

Создайте базу данных в [PostgreSQL](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)
и получите данные `USER`, `PASSWORD`, имя базы данных `NAME` и внесите эти данные
в виде URL в `.env`
```pycon
POSTGRES_URL='postgres://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]'
```

### Запуск через Докер
Скачайте код:
```
git clone https://github.com/Arkady-Bikhd/star-burger-masteк.git

```

Перейдите в каталог проекта:
```
cd star-burger
```
Откройте файл `docker-compose.yml` и заполните переменные окружения

Для вычисления расстояний между клиентом и различными ресторанами потребуется
`YANDEX_API_KEY`. Его можно получить на сайте [яндекс разработчика](https://developer.tech.yandex.ru/services/), а это
[инструкция по получению ключа](https://dvmn.org/encyclopedia/api-docs/yandex-geocoder-api/). Полученный ключ необходимо записать в .env
```
YANDEX_API_KEY=ваш ключ
```
Если вы запускаете проект не на локальном компьютере, а на арендованном сервере,
то необходимо прописать ip сервера
```
ALLOWED_HOSTS=45.8....
```
Для просмотра и фиксации ошибок при работе сайта - необходимо зарегестрироваться на сайте [rollbar](https://rollbar.com/)
Создать проект и записать project_access_token. Вы можете этого не делать,
если вам не нужно получать информацию об ошибках в роллбаре.
Тогда укажите `ROLLBAR=False`. Если же нужны записи ошибок, то необходимо
прописать `ROLLBAR=True` и указать следующие 3 переменные окружения:
```
ROLLBAR_ACCESS_TOKEN='521c.....'
```
В зависимости от того запустили вы сервер в "боевом" режиме или в режиме
"отладки" необходимо указать
```
DEV=True - для отладки
DEV=False - для боевого
```
и ваше имя
```
USER='capark'
```

Создайте базу данных в [PostgreSQL](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)
и получите данные `USER`, `PASSWORD`, имя базы данных `NAME` и внесите эти данные
в виде URL
```
POSTGRES_URL='postgres://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]'
```

так должен выглядеть полностью заполненный файл с переменными:
```
environment:
      SECRET_KEY: 'replace_me'
      DJANGO_SUPERUSER_USERNAME: admin
      DJANGO_SUPERUSER_PASSWORD: admin
      DJANGO_SUPERUSER_EMAIL: admin@example.com
      YANDEX_API_KEY: 485691e3-.....
      ALLOWED_HOSTS: 40.8.....,127.0.0.1:8080,127.0.0.1,localhost,starburger
      DEBUG: 'False'
      ROLLBAR: 'False'
      DEV: 'False'
      USER: 'max'
      ROLLBAR_ACCESS_TOKEN: 521c8a98a37348669908...........
      POSTGRES_URL: postgres://capark:197408@pgdb:5432/starburger
```
А потом запустите `docker-compose.yml` в каталоге где он находится:
```
docker-compose up
```
Данный скрипт создаст 3 докер контейнера `backend`, `pgdb`, `nginx`, установит в них
все зависимости из requirements.txt и необходимые библиотеки JS, соберет фронтенд,
соберет всю статику в одну папку, сделает миграции и запустит сайт.
Сайт будет доступен на локале http://127.0.0.1/ или на вашем сервере

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного курса Django](https://dvmn.org/modules/django/)
