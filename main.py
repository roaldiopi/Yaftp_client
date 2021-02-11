import sys
import signal
from ftplib import FTP, error_perm, error_reply
from progressbar import ProgressBar, Percentage, Bar, ETA, FileTransferSpeed

signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
ftp = FTP()


def ftp_command(ftp_cmd):
    split_cmd = ftp_cmd.split()
    if split_cmd[0] == "ls" or split_cmd[0] == "LS":
        ftp.dir()
    if split_cmd[0] == "cd" or split_cmd[0] == "CD":
        ftp.cwd(split_cmd[1])
    if split_cmd[0] == "download" or split_cmd[0] == "DOWNLOAD":
        widgets = ['Downloading: ', Percentage(), ' ',
                   Bar(marker='#', left='[', right=']'),
                   ' ', ETA(), ' ', FileTransferSpeed(), '\n']
        file = open(split_cmd[1], 'wb')
        size = ftp.size(split_cmd[1])
        pbar = ProgressBar(widgets=widgets, maxval=size)
        pbar.start()

        def file_write(data, proggresbar=pbar):
            file.write(data)
            proggresbar += len(data)

        ftp.retrbinary("RETR " + split_cmd[1], file_write)
        file.close()
    if split_cmd[0] == "read" or split_cmd[0] == "read":
        # ftp.retrlines(cmd, callback=None)
        # По умолчанию callback выводит строчки в sys.stdout
        ftp.retrlines("RETR " + split_cmd[1])
    if split_cmd[0] == "load" or split_cmd[0] == "LOAD":
        ftp.storbinary("STOR " + split_cmd[1], open(split_cmd[1], 'rb'))
    if split_cmd[0] == "help" or split_cmd[0] == "HELP":
        print("""Доступные команды:
1)ls        6)delete
2)cd        7)rmd
3)download  8)mkd
4)load      9)quit
5)rename    10)help""")
    if split_cmd[0] == "rename" or split_cmd[0] == "RENAME":
        ftp.rename(split_cmd[1], split_cmd[2])
    if split_cmd[0] == "delete" or split_cmd[0] == "DELETE":
        ftp.delete(split_cmd[1])
    if split_cmd[0] == "rmd" or split_cmd[0] == "RMD":
        ftp.rmd(split_cmd[1])
    if split_cmd[0] == "mkd" or split_cmd[0] == "MKD":
        ftp.mkd(split_cmd[1])
    if split_cmd[0] == "quit" or split_cmd[0] == "QUIT":
        ftp.quit()


if len(sys.argv) > 1:
    if len(sys.argv) == 3:
        port = sys.argv[2]
    else:
        port = 21
    ftp.connect(sys.argv[1], int(port))
    print(ftp.getwelcome())
    if len(sys.argv) >= 4:
        login = sys.argv[3]
        password = sys.argv[4]
    else:
        login = "anonymous"
        password = ""
    print(login, password)
    ftp.login()
    ftp.dir()
    while True:
        try:
            cmd = input("cmd>")
            ftp_command(cmd)
            if cmd == "quit" or cmd == "QUIT":
                print("Выходим с сервера")
                break
        except error_perm:
            print("Ошибка доступа")
        except UnicodeEncodeError:
            print("Ошибка кодировки!Пажалуйста используйте латиницу")
        except error_reply:
            print("Неожиданный ответ получен от сервера")
else:
    print("Приветствуем вас в YAFTP клиенте версии 0.1")
    while True:
        user_input = input(">").split()
        if user_input[0] == "connect" or user_input[0] == "CONNECT":
            if len(user_input) == 1:
                address = input("Введите адрес ftp сервера:")
            else:
                address = user_input[1]
            if len(user_input) == 3:
                port = user_input[2]
            else:
                port = 21
            ftp.connect(address, int(port))
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
                    cmd = input("cmd>")
                    ftp_command(cmd)
                    if cmd == "quit" or cmd == "QUIT":
                        print("Выходим с сервера")
                        break
                except UnicodeEncodeError:
                    print("Ошибка кодировки!Пажалуйста используйте латиницу")
                except error_perm:
                    print("Ошибка доступа")
                except error_reply:
                    print("Неожиданный ответ получен от сервера")
        elif user_input[0] == "help" or user_input[0] == "HELP":
            print("""Доступные команды:
1)connect
2)exit
3)debug
4)help""")
        elif user_input[0] == "debug" or user_input[0] == "DEBUG":
            ftp.set_debuglevel(int(user_input[1]))
            print("Текущий уровень debug=" + user_input[1])
        elif user_input[0] == "exit" or user_input[0] == "Exit":
            print("Завершаем работу прогграмы")
            break
        else:
            print("Неизвестная команда")
