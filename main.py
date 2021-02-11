import sys
import signal
from ftplib import FTP, error_perm, error_reply

signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
ftp = FTP()
ftp.set_pasv(True)
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
            mode = input("mode>")
            cmd = input("cmd>")
            if mode == "ASCII" or mode == "ascii":
                print(ftp.retrlines(cmd))
            elif mode == "DOWNLOAD" or mode == "download":
                print("Скачиваем файл")
                ftp.retrbinary("RETR " + cmd, open(cmd, 'wb').write)
            elif mode == "LOAD" or mode == "load":
                print("Закачиваем файл")
                ftp.storbinary("STOR " + cmd, open(cmd, 'rb'))
            else:
                print(ftp.sendcmd(cmd))
            if cmd == "quit" or cmd == "QUIT":
                print("Выходим с сервера")
                break
        except error_perm:
            print("Неизвестная команда")
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
                    mode = input("mode>")
                    cmd = input("cmd>")
                    if mode == "ASCII" or mode == "ascii":
                        print(ftp.retrlines(cmd))
                    elif mode == "DOWNLOAD" or mode == "download":
                        print("Скачиваем файл")
                        ftp.retrbinary("RETR "+cmd, open(cmd, 'wb').write)
                    elif mode == "LOAD" or mode == "load":
                        print("Закачиваем файл")
                        ftp.storbinary("STOR " + cmd, open(cmd, 'rb'))
                    else:
                        print(ftp.sendcmd(cmd))
                    if cmd == "quit" or cmd == "QUIT":
                        print("Выходим с сервера")
                        break
                except UnicodeEncodeError:
                    print("Ошибка кодировки!Пажалуйста используйте латиницу")
                except error_perm:
                    print("Ошибка команды")
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
            print("Текущий уровень debug="+user_input[1])
        elif user_input[0] == "exit" or user_input[0] == "Exit":
            print("Завершаем работу прогграмы")
            break
        else:
            print("Неизвестная команда")
