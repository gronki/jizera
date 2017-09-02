# Jizera - baza danych ciemnego nieba

**Jizera** to baza danych, która zbiera pomiary ciemności nieba
od obserwatorów w całej Polsce.

## Wymagania

Aplikacja jest napisana we frameworku [**Flask**](http://flask.pocoo.org/) i używa bazy danych [**SQLite**](https://www.sqlite.org/). Front-end jest oparty jest na [**CoffeeScript**](http://coffeescript.org/) oraz [**SASS**](http://sass-lang.com/).

W systemie operacyjnym
musi być zainstalowany **Python 2.7** i **virtualenv**. W systemie Fedora/CentOS/RHEL zależności te zainstalujemy poleceniem:
```
sudo yum install -y git python python-pip python-virtualenv
```

## Instalacja

### Środowisko wirtualne (virtualenv)

Tworzymy środowisko wirtualne w katalogu projektu i aktywujemy je
w sesji basha.
```sh
cd jizera
virtualenv venv
. venv/bin/activate
```

Jeżeli wszystko przebiegnie poprawnie, adnotacja o tym, ze jesteśmy w środowisku wirtualnym zostanie umieszczone na lewo od znaku zachęty.
```
(venv) [uzytkownik@maszyna jizera]$
```

### Instalacja za pomocą dystrybucji źródłowej

Najłatwiej jest zainstalować program z dystrybucji źródłowej. Będąc w środowisku
wirtualnym, instalujemy w nim bazę poleceniem:

```bash
pip install jizera-170214.tar.gz
```

Udany proces instalacji powinien przebiegać mniej-więcej tak:

```
Processing ./jizera-170214.tar.gz
Collecting flask (from jizera==170214)
  Using cached Flask-0.12-py2.py3-none-any.whl
Collecting loremipsum (from jizera==170214)
Collecting itsdangerous>=0.21 (from flask->jizera==170214)
Collecting click>=2.0 (from flask->jizera==170214)
  Using cached click-6.7-py2.py3-none-any.whl
Collecting Jinja2>=2.4 (from flask->jizera==170214)
  Using cached Jinja2-2.9.5-py2.py3-none-any.whl
Collecting Werkzeug>=0.7 (from flask->jizera==170214)
  Using cached Werkzeug-0.11.15-py2.py3-none-any.whl
Collecting MarkupSafe>=0.23 (from Jinja2>=2.4->flask->jizera==170214)
Building wheels for collected packages: jizera
  Running setup.py bdist_wheel for jizera ... done
  Stored in directory: /home/user/.cache/pip/wheels/7c/c1/fa/87926d1c1034181042cfbee8b924e7f9293bbbe8675595d0d9
Successfully built jizera
Installing collected packages: itsdangerous, click, MarkupSafe, Jinja2, Werkzeug, flask, loremipsum, jizera
Successfully installed Jinja2-2.9.5 MarkupSafe-0.23 Werkzeug-0.11.15 click-6.7 flask-0.12 itsdangerous-0.24 jizera-170214 loremipsum-1.0.5
```

### Zmienne środowiskowe
Konieczne jest ustawienie zmiennych środowiskowych aby wskazać,
która aplikacja ma być uruchomiona przez Flask.
```sh
export FLASK_APP=jizera
export FLASK_DEBUG=1
```

### Inicjalizacja pustej bazy i usunięcie bazy
Przed pierwszym uruchomieniem należy utworzyć strukturę tabel bazy danych. W tym celu używamy polecenia
```sh
flask init
```
Po eksperymentach możemy wyczyścić z powrotem bazę poleceniem
```sh
flask drop
```
Ponieważ testowanie pustej bazy jest nudne, jest możliwość wygenerowania losowych danych za pomocą polecenia
```sh
flask dummy-init
```

### Uruchomienie serwera
Uruchamiamy serwer testowy bazy poleceniem:
```sh
flask run --port 5000
```
Powinniśmy w rezultacie dostać komunikat zawierający adres w przeglądarce pod który należy wejść by przeglądać bazę (w tym przypadku ``http://127.0.0.1:5000/``).
```
* Serving Flask app "jizera"
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Na ekranie mogą się ukazywać różne komunikaty.

## Budowanie ze źródła

Pobieramy katalog projektu na nasz dysk:

```sh
git clone https://github.com/gronki/jizera.git
```

Potrzeba nam będzie kompilatorów CoffeeScript oraz SASS aby zbudować front-end.
```sh
sudo yum install -y make rubygem-sass coffee-script
```

Po instalacji, budujemy style i skrypty poleceniem:

```sh
make -C ui
```

Instalujemy program w środowisku wirtualnym za pomocą menedżera pakietów **pip**. Zależności zostaną pobrane automatycznie.
```sh
pip install -e .
```

Aby utworzyć paczkę z dystrybucją, używamy polecenia:
```sh
python setup.py sdist
```


## Przeglądanie bazy SQLite

W celu przeglądania struktury bazy danych, można użyć narzędzia **sqlitebrowser**.
```
sudo yum install -y sqlitebrowser
sqlitebrowser /tmp/jizera.db &
```
