from bs4 import BeautifulSoup
import requests
import os
from os.path import getsize
from pprint import  pprint

class Update:
    """
    Класс обновления прогграмы на входе берёт названия репозитория,имя пользователя,
    также можно указать ветвь(по умолчанию ветвь=main) и сайт.
    """

    def __init__(self, repository, user=None, site=None, branch="main", file="repository.xml"):
        self.rp = repository
        self.repository_file = file
        if site is None:
            self.username = user
            self.url = f"https://raw.githubusercontent.com/{self.username}/{self.rp}/{branch}/"
            self.xml = requests.get(self.url + file)
        else:
            self.url = site + "/"+self.rp+"/"
            self.xml = requests.get(self.url+self.repository_file)
        self.response = self.xml.content
        self.parser = BeautifulSoup(self.response, "lxml")

    def get_json(self, delete=-1):
        """
        Этот метод класс Update выдаёт json с обнолвениями.
        """
        releases_array = []
        releases = self.parser.find_all("release")
        for release in releases:
            exists_dirs = release.find("create_directory")
            if exists_dirs is not None:
                dirs = release.find("create_directory").text
            else:
                dirs = "None"
            files = release.find("files").text
            exists_commit = release.find("commit")
            if exists_commit is not None:
                commit = release.find("commit").text
            else:
                commit = "None"
            releases_array.append({
                "version": release['version'],
                "date": release['date'],
                "description": release.description.text,
                "dirs": dirs,
                "files": files,
                "commit": commit
            })
        if delete != -1:
            for i in range(delete):
                releases_array.pop(0)
        return releases_array

    def get_update(self):
        """
        Этот метод смотрит если в локальным repository.xml и repository.xml которые
        на гитхабе есть различия тоесть в версиях то он обновляет прогграму.
        Возращает True если прогграма обновилась,False если нет обновлений
        """
        release = self.get_json()
        try:
            f = open(self.repository_file, "r")
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
    f.close()""")
                print(f"Версия прогграмы обновленна до {release[-1]['version']}")
                return True
            else:
                return False
        except FileNotFoundError:
            print("repository.xml не найден!\nСкачиваем repository.xml")
            rq = requests.get(self.url + "repository.xml")
            xml_content = rq.content
            releases_file = open(self.repository_file, 'w')
            releases_file.write(xml_content.decode())
            releases_file.close()
            return False

    @staticmethod
    def get_elements_folder(exclude=("./venv", "./.git", "./.idea", "__pycache__")):
        # Создаём список в который будет входить незапрёщенные папки
        elements = []
        # Получаем данные о всех элементах в этой папки
        tree = os.walk(".", topdown=True)
        # Создаём список какой должна быть папка чтобы её записали
        not_found = []
        # Генерируем список
        for i in range(len(exclude)):
            not_found.append(-1)
        # ----
        # Начинаем обход по элментам
        for root, dirs, files in tree:
            check_dir = []
            if root == ".":
                elements.append([root, files])
            for el in exclude:
                check_dir.append(root.find(el))
            if check_dir == not_found:
                if root != ".":
                    elements.append([root, files])
        elements_folder = []
        # Добавляем размер к файлам
        for el in elements:
            file_size = []
            for file in el[1]:
                file_size.append((file, getsize(el[0]+"/"+file)))
            elements_folder.append([el[0], file_size])
        return elements_folder

    def smart_update(self):
        # Получаем локальный список элментов
        elements = self.get_elements_folder()
        # Получаем списко элментов в репозиторие
        directory = self.parser.program.directory.text
        exec(f"""from itertools import zip_longest
for local,destination in zip_longest({elements},{directory}):
    if local is None:
        os.mkdir(destination[0])
        for files in destination[1]:
            path = destination[0]+"/"+files[0]
            rq = requests.get(self.url+destination[0]+"/"+files[0])
            file = open(path,'w')
            file_content = rq.content
            file.write(file_content.decode())
            file.close()
    else:
        if local[1] != destination[1]:
            for files in zip_longest(local[1],destination[1]):
                if files[0] is None and files[1] is not None:
                    if destination[0] != ".":
                        path = destination[0]+"/"+files[1][0]
                        rq = requests.get(self.url+destination[0]+"/"+files[1][0])
                    else:
                        path = files[1][0]
                        rq = requests.get(self.url+files[1][0])
                    file = open(path,'w')
                    file_content = rq.content
                    file.write(file_content.decode())
                    file.close()
                else:
                    if files[0][1] != files[1][1] and files[1] is not None:
                        if destination[0] != ".":
                            path = destination[0]+"/"+files[1][0]
                            rq = requests.get(self.url+destination[0]+"/"+files[1][0])
                        else:
                            path = files[1][0]
                            rq = requests.get(self.url+files[1][0])
                        print(path)
                        print(self.url+files[1][0])
                        
""")


if __name__ == '__main__':
    update = Update("Yaftp_client", "roaldiopi")
    update.smart_update()
    print(123)
