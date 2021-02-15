import requests
from bs4 import BeautifulSoup
import random
import string
import time


class Color:
    """
    Класс с цветами
    """
    purple = '\033[95m'
    cyan = '\033[96m'
    dark_cyan = '\033[36m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'


class Date:
    def __init__(self):
        self.seconds = time.time()
        self.date = time.localtime(self.seconds)

    def get_date(self):
        # Преоброзуем в стандартный вариант
        now = time.strftime("%d/%m/%Y %H:%M", self.date)
        return now

    def get_seconds(self):
        return int(self.seconds)

    def get_date_by_code(self, date_code):
        # Преоброзуем в вариант который запросили
        now = time.strftime(date_code, self.date)
        return now


def generate_string(length):
    """
    Функция генерирует строку с цифрами
    """
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string


class Update:
    """
    Класс обновления прогграмы на входе берёт названия репозитория,имя пользователя,
    также можно указать ветвь(по умолчанию ветвь=main) и сайт.
    """
    def __init__(self, repository, user, site=None, branch="main"):
        self.rp = repository
        if site is None:
            self.username = user
            self.url = f"https://raw.githubusercontent.com/{self.username}/{self.rp}/{branch}/"
            self.xml = requests.get(self.url + "releases.xml")
        else:
            self.url = site
            self.xml = requests.get(site + "releases.xml")
        self.response = self.xml.content

    def get_json(self, delete=-1):
        """
        Этот метод класс Update выдаёт json с обнолвениями.
        """
        parser = BeautifulSoup(self.response, "lxml")
        releases = []
        for release in parser.select("release"):
            exists_dirs = release.update.find("create_directory")
            if exists_dirs is not None:
                dirs = release.update.create_directory.text
            else:
                dirs = "None"
            files = release.update.files.text
            exists_commit = release.update.find("commit")
            if exists_commit is not None:
                commit = release.update.commit.text
            else:
                commit = "None"
            releases.append({
                "version": release['version'],
                "date": release['date'],
                "description": release.description.text,
                "dirs": dirs,
                "files": files,
                "commit": commit
            })
        if delete != -1:
            for i in range(delete):
                releases.pop(0)
        return releases

    def get_update(self):
        """
        Этот метод смотрит если в локальным releases.xml и releases.xml которые
        на гитхабе есть различия тоесть в версиях то он обновляет прогграму.
        Возращает True если прогграма обновилась,False если нет обновлений
        """
        release = self.get_json()
        try:
            f = open("releases.xml", "r")
            bs = BeautifulSoup(f.read(), "lxml")
            version = bs.current.text
            f.close()
            if version != release[-1]['version']:
                exec(f"""import os
            if {release[-1]['dirs']} != None:
                for dir in {release[-1]['dirs']}:
                    os.mkdir(dir)
            for file in {release[-1]['files']}:
                r = requests.get(self.url + file)
                file_content = r.content
                f = open(file,'w')
                f.write(file_content.decode())
                f.close()
            """)
                print(f"Версия прогграмы обновленна до {release[-1]['version']}")
                return True
            else:
                return False
        except FileNotFoundError:
            print("releases.xml не найден!\nСкачиваем releases.xml")
            rq = requests.get(self.url + "releases.xml")
            xml_content = rq.content
            releases_file = open("releases.xml", 'w')
            releases_file.write(xml_content.decode())
            releases_file.close()
            return False


def write_log(log, literals_in_console=False, path="logs.txt"):
    """
    Функция может писать логи в консоль,и записавать их в указанную директорию
    """
    # Если нужны литералы то выводим лог вместе с ними
    if literals_in_console:
        print(log)
    # Если не нужны литералы убираем их
    else:
        console_log = log.replace("\n", "")
        print(console_log)
    with open(path, "a", encoding="utf-8") as f:
        f.write(log)


def binary_search(array, item):
    # В переменных low и high хранятся границы той части списка, в которой выполняется поиск
    low = 0
    high = len(array) - 1

    # Пока эта часть не сократится до одного элемента...
    while low <= high:
        # ... проверяем средний элемент
        mid = (low + high) // 2
        guess = array[mid]
        # Значение найдено
        if guess == item:
            return mid
        # Много
        if guess > item:
            high = mid - 1
        # Мало
        else:
            low = mid + 1

    # Значение не существует
    return None


def search(arr, key):
    for i in arr:
        if i == key:
            return i
    return None


def search_in_array_json(arr, index, key):
    for el in arr:
        if el[index] == key:
            return arr.index(el)
    return None
