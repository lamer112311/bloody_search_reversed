from faker import Faker
import requests
import phonenumbers as p
from phonenumbers import carrier, geocoder, timezone
from helper import printer
import curses
import time
import os
import msvcrt
import win32gui
import random
import ctypes
# Получение дескриптора процесса
kernel32 = ctypes.WinDLL('kernel32')
pid = kernel32.GetCurrentProcess()

# Игнорирование CTRL+C
kernel32.SetConsoleCtrlHandler(None, 1)


banner = """ 

888888b.   888       .d88888b.   .d88888b.  8888888b.  Y88b   d88P        .d8888b.  8888888888        d8888 8888888b.   .d8888b.  888    888 
888  "88b  888       d88P" "Y88b d88P" "Y88b 888  "Y88b  Y88b d88P        d88P  Y88b 888              d88888 888   Y88b d88P  Y88b 888    888 
888  .88P  888      888     888 888     888 888    888   Y88o88P         Y88b.      888             d88P888 888    888 888    888 888    888 
8888888K.  888      888     888 888     888 888    888    Y888P           "Y888b.   8888888        d88P 888 888   d88P 888        8888888888 
888  "Y88b 888      888     888 888     888 888    888     888               "Y88b. 888           d88P  888 8888888P"  888        888    888 
888    888 888      888     888 888     888 888    888     888                 "888 888          d88P   888 888 T88b   888    888 888    888 
888   d88P 888      Y88b. .d88P Y88b. .d88P 888  .d88P     888           Y88b  d88P 888         d8888888888 888  T88b  Y88b  d88P 888    888 
8888888P"  88888888  "Y88888P"   "Y88888P"  8888888P"      888            "Y8888P"  8888888888 d88P     888 888   T88b  "Y8888P"  888    888

                                                    РАЗРАБОТЧИК - https://t.me/pr0xit
                                                                                                                                            
"""
def getch():
    try:
        return msvcrt.getch()
    except KeyboardInterrupt:
        return b''

def set_console_window_size(width, height):
    hwnd = win32gui.GetForegroundWindow()
    win32gui.MoveWindow(hwnd, 0, 0, width, height, True)


def rain(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    curses.halfdelay(5)

    max_y, max_x = stdscr.getmaxyx()

    raindrops = []
    for _ in range(50):
        y = random.randint(0, max_y-1)
        x = random.randint(0, max_x-1)
        speed = random.uniform(3, 8)
        symbol = random.choice(["/", "+", "-"])
        raindrops.append({'y': y, 'x': x, 'speed': speed, 'symbol': symbol})

    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        stdscr.clear()

        text = """
        
                            
            ██████╗ ██████╗ ███████╗███████╗███████╗     █████╗ ███╗   ██╗██╗   ██╗    ██╗  ██╗███████╗██╗   ██╗
            ██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝    ██╔══██╗████╗  ██║╚██╗ ██╔╝    ██║ ██╔╝██╔════╝╚██╗ ██╔╝
            ██████╔╝██████╔╝█████╗  ███████╗███████╗    ███████║██╔██╗ ██║ ╚████╔╝     █████╔╝ █████╗   ╚████╔╝ 
            ██╔═══╝ ██╔══██╗██╔══╝  ╚════██║╚════██║    ██╔══██║██║╚██╗██║  ╚██╔╝      ██╔═██╗ ██╔══╝    ╚██╔╝  
            ██║     ██║  ██║███████╗███████║███████║    ██║  ██║██║ ╚████║   ██║       ██║  ██╗███████╗   ██║   
            ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝       ╚═╝  ╚═╝╚══════╝   ╚═╝   
                                                                                                    
        """

        if len(text.split('\n')) > max_y or max_x < 80:
            stdscr.addstr(0, 0, "Ошибка: Текст слишком большой, разверните окно на весь экран")
            stdscr.refresh()
            time.sleep(1)
            break

        stdscr.addstr(0, 0, text)

        for drop in raindrops:
            try:
                stdscr.addstr(int(drop['y']), int(drop['x']), drop['symbol'], curses.color_pair(1))
            except curses.error as e:
                print("Error:", e)
            drop['y'] += drop['speed']
            if drop['y'] >= max_y:
                drop['y'] = 0
                drop['x'] = random.randint(0, max_x-1)

        stdscr.refresh()
        time.sleep(0.05)

        ch = stdscr.getch()
        if ch != -1:
            break


def function_1():
    phone_number = ""
    try:
        while not phone_number:
            print("Введите номер телефона с кодом страны:", end='', flush=True)
            c = ord(getch())
            while c != 13:  # Enter key
                if c == 3:  # Ctrl+C
                    raise KeyboardInterrupt
                if c == 8:  # Backspace key
                    if phone_number:
                        print("\b \b", end='', flush=True)
                        phone_number = phone_number[:-1]
                else:
                    print(chr(c), end='', flush=True)
                    phone_number += chr(c)
                c = ord(getch())
        print("\n")
        ph_no = p.parse(phone_number)
        country = p.region_code_for_country_code(ph_no.country_code)
        no_carrier = carrier.name_for_number(ph_no, "ru")
        no_valid = p.is_valid_number(ph_no)
        no_possible = p.is_possible_number(ph_no)
        time_zone = timezone.time_zones_for_number(ph_no)
        region = geocoder.description_for_number(ph_no, "ru")

        printer.info(f"Ищем информацию на '{phone_number}'...")
        time.sleep(1)
        printer.success("Номер телефона:", phone_number)
        printer.success(f"Валидный:", no_valid)
        printer.success(f"Правильность набора:", no_possible)
        printer.success(f"Оператор:", no_carrier)
        printer.success(f"Страна:", country)
        printer.success(f"Город:", region)
        printer.success(f"Часовые пояса:", time_zone)
        input("Нажмите Enter, чтобы вернуться в главное меню...")
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")

def function_2():
    try:
        ip_address = input("Введите айпи:")
        if not ip_address:
            raise KeyboardInterrupt
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()

        printer.success("IP: ", data["ip"])
        printer.success("Местоположение: ", data["city"], ",", data["region"], ",", data["country"])
        printer.success("Провайдер: ", data["org"])
        printer.success("Часовой пояс: ", data["timezone"])
        printer.success("Почтовый индекс: ", data["postal"])
        printer.success("Координаты: ", data["loc"])

        input("Нажмите Enter, чтобы вернуться в главное меню...")
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
    except EOFError:
        # Если пользователь просто нажал Enter, игнорируем и возвращаемся в главное меню
        print("\nВозвращаемся в главное меню...")


def Generate():
    try:
        fake = Faker()
        printer.info("Генерация информации...")
        time.sleep(1)
        printer.success(f"Имя : {fake.name()}")
        printer.success(f"Адресс : {fake.address()}")
        printer.success(f"Почта: {fake.email()}")
        printer.success(f"Номер телефона : {fake.phone_number()}")
        printer.success(f"Работа : {fake.job()}")
        printer.success(f"Компания : {fake.company()}")
        printer.success(f"Кредитная карта : {fake.credit_card_number()}")
        printer.success(f"СВС Карты : {fake.credit_card_security_code()}")
        printer.success(f"Срок годности карты : {fake.credit_card_expire()}")
        printer.success(f"Тип карты : {fake.credit_card_provider()}")
        printer.success(f"IBAN : {fake.iban()}")
        printer.success(f"BIC : {fake.bban()}")
        printer.success(f"Страна : {fake.country()}")
        printer.success(f"Город : {fake.city()}")
        input("Нажмите Enter, чтобы вернуться в главное меню...")
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")
    except EOFError:
        # Если пользователь просто нажал Enter, игнорируем и возвращаемся в главное меню
        print("\nВозвращаемся в главное меню...")


def main_menu(options):
    os.system('cls' if os.name == 'nt' else 'clear')
    for line in banner.splitlines():
        print(line.center(80))
        time.sleep(0.4)
    time.sleep(1)

    selected_option = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner.center(80))

        for i, option in enumerate(options):
            if i == selected_option:
                print("\033[41m\033[37m  " + option.center(130) + "\033[0m")
            else:
                print("  " + option.center(130))

        key = ord(getch())  # Здесь используем нашу функцию getch()

        if key == 72:
            selected_option = (selected_option - 1) % len(options)
        elif key == 80:
            selected_option = (selected_option + 1) % len(options)
        elif key == 13:
            if selected_option == 0:
                function_1()
            elif selected_option == 1:
                function_2()
            elif selected_option == 2:
                Generate()
            elif selected_option == 3:
                exit()

if __name__ == "__main__":
    kernel32.SetConsoleCtrlHandler(None, 1)
    options = ["Поиск по номеру", "Поиск по IP", "Генерация фейковой информации", "Выход"]
    set_console_window_size(1920, 1080)
    time.sleep(1)
    curses.wrapper(rain)
    main_menu(options)
