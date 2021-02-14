import sys
import signal
from lib import Update
from socket import gaierror
from ftplib import FTP, error_perm, error_reply, error_temp

signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
ftp = FTP()
update = Update("Yaftp_client", "roaldiopi")
update.get_update()
updates = update.get_json()
def ftp_command(ftp_cmd):
    split_cmd = ftp_cmd.split()
    if split_cmd[0] == "ls" or split_cmd[0] == "LS":
        ftp.dir()
    elif split_cmd[0] == "cd" or split_cmd[0] == "CD":
        ftp.cwd(split_cmd[1])
    elif split_cmd[0] == "download" or split_cmd[0] == "DOWNLOAD":
        print(">Скачиваем файл")
        if "--in" in split_cmd:
            directory = split_cmd[3]+split_cmd[1]
        else:
            directory = split_cmd[1]
        ftp.retrbinary("RETR "+split_cmd[1], open(directory, 'wb').write)
        print(">Скачано")
    elif split_cmd[0] == "read" or split_cmd[0] == "read":
        # ftp.retrlines(cmd, callback=None)
        # По умолчанию callback выводит строчки в sys.stdout
        ftp.retrlines("RETR " + split_cmd[1])
    elif split_cmd[0] == "load" or split_cmd[0] == "LOAD":
        ftp.storbinary("STOR " + split_cmd[1], open(split_cmd[1], 'rb'))
    elif split_cmd[0] == "help" or split_cmd[0] == "HELP":
        print(""">Доступные команды:
1)ls        6)delete
2)cd        7)rmd
3)download  8)mkd
4)load      9)quit
5)rename    10)help""")
    elif split_cmd[0] == "rename" or split_cmd[0] == "RENAME":
        ftp.rename(split_cmd[1], split_cmd[2])
    elif split_cmd[0] == "delete" or split_cmd[0] == "DELETE":
        ftp.delete(split_cmd[1])
    elif split_cmd[0] == "rmd" or split_cmd[0] == "RMD":
        ftp.rmd(split_cmd[1])
    elif split_cmd[0] == "mkd" or split_cmd[0] == "MKD":
        ftp.mkd(split_cmd[1])
    elif split_cmd[0] == "quit" or split_cmd[0] == "QUIT":
        ftp.quit()
    else:
        print(">Неизвестная команда")


if len(sys.argv) > 1:
    if "--get_last_update":
        print(f"""Версия:{updates[-1]['version']}
Дата обновления:{updates[-1]['date']}
Описание:{updates[-1]['description']}
""")
        exit(0)
    if "-p" in sys.argv:
        i = sys.argv.index("-p")
        port = sys.argv[i+1]
    else:
        port = 21
    ftp.connect(sys.argv[1], int(port))
    print(ftp.getwelcome())
    if "--account" in sys.argv:
        i = sys.argv.index("--account")
        login = sys.argv[i+1]
        password = sys.argv[i+2]
    else:
        login = "anonymous"
        password = ""
    ftp.login(login, password)
    ftp.dir()
    while True:
        try:
            cmd = input(">")
            ftp_command(cmd)
            if cmd == "quit" or cmd == "QUIT":
                print(">Выходим с сервера")
                break
        except error_perm:
            print(">Ошибка доступа")
        except UnicodeEncodeError:
            print(">Ошибка кодировки!Пажалуйста используйте латиницу")
        except error_reply:
            print(">Неожиданный ответ получен от сервера")
else:
    print(f"Приветствуем вас в YAFTP клиенте версии {updates[-1]['version']}")
    while True:
        user_input = input(">").split()
        if user_input[0] == "connect" or user_input[0] == "CONNECT":
            if len(user_input) == 1:
                address = input(">Введите адрес ftp сервера:")
            else:
                address = user_input[1]
            if len(user_input) == 3:
                port = user_input[2]
            else:
                port = 21
            try:
                ftp.connect(address, int(port))
            except gaierror:
                print(">С именем хоста не связан адрес")
                break
            print(ftp.getwelcome())
            if len(user_input) >= 4:
                login = user_input[3]
                password = user_input[4]
            else:
                login = "anonymous"
                password = ""
            ftp.login(login, password)
            ftp.dir()
            while True:
                try:
                    cmd = input(">")
                    ftp_command(cmd)
                    if cmd == "quit" or cmd == "QUIT":
                        print(">Выходим с сервера")
                        break
                except UnicodeEncodeError:
                    print(">Ошибка кодировки!Пажалуйста используйте латиницу")
                except error_perm:
                    print(">Ошибка доступа")
                except error_temp:
                    print(">Временная ошибка")
                except error_reply:
                    print(">Неожиданный ответ получен от сервера")
        elif user_input[0] == "help" or user_input[0] == "HELP":
            print("""Доступные команды:
1)connect   3)debug          
2)exit      4)help""")
        elif user_input[0] == "debug" or user_input[0] == "DEBUG":
            ftp.set_debuglevel(int(user_input[1]))
            print(">Текущий уровень debug=" + user_input[1])
        elif user_input[0] == "exit" or user_input[0] == "Exit":
            print(">Завершаем работу прогграмы")
            break
        else:
            print(">Неизвестная команда")
