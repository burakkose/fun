import cmd
import getpass
import requests

from termcolor import colored
from bs4 import BeautifulSoup as bs4
from prettytable import PrettyTable

__author__ = 'burakks'
__version__ = '0.1.1'

requests.packages.urllib3.disable_warnings()

BASE_URL = 'https://ogr.kocaeli.edu.tr/KOUBS/ogrenci/index.cfm'
GRADE_URL = 'https://ogr.kocaeli.edu.tr/KOUBS/ogrenci/bologna_transkript.cfm'
BGRADE_URL = 'https://ogr.kocaeli.edu.tr/KOUBS/ogrenci/bologna_Tumnotlar.cfm'


class KOUCMD(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = colored("""
                __    __   ______   __    __
                /  |  /  | /      \ /  |  /  |
                $$ | /$$/ /$$$$$$  |$$ |  $$ |
                $$ |/$$/  $$ |  $$ |$$ |  $$ |
                $$  $$<   $$ |  $$ |$$ |  $$ |
                $$$$$  \  $$ |  $$ |$$ |  $$ |
                $$ |$$  \ $$ \__$$ |$$ \__$$ |
                $$ | $$  |$$    $$/ $$    $$/
                $$/   $$/  $$$$$$/   $$$$$$/
                    KOCAELI UNIVERSITESI
                        Vers {}\n""".format(__version__), 'green')
        self.prompt = colored('>>', 'red')
        self.is_login = False
        self.request = {}
        self.response = {}
        self.session = requests.session()

    def do_login(self, ln):
        if not self.is_login:
            username = input('{} Okul No : '.format(colored('>>>', 'red')))
            password = getpass.getpass(
                '{}Parola : '.format(colored(">>> ", "red")))
            try:
                self.request['Sicil'] = username
                self.request['Sifre'] = password
                self.request['LoggingOn'] = '1'
                self.response['login_page'] = self.session.post(
                    BASE_URL, data=self.request, verify=False)
                if username in str(self.response['login_page'].text):
                    self.is_login = True
                    print(colored("Giriş başarılı", 'green'))
                else:
                    self.is_login = False
                    print(colored(">>>> Giriş başarısız", 'red'))
            except requests.ConnectionError:
                self.is_login = False
                print(colored(">>>> Bağlantı hatası", 'red'))
        else:
            text = "Giriş yapılmış, yeni giriş için 'e' : "
            if input(colored(text, 'yellow')).upper() == 'E':
                self.is_login = False
                self.do_login(ln)

    def do_grades(self, ln):
        if self.is_login:
            try:
                self.response['grades'] = self.session.get(GRADE_URL)
                current_term = bs4(self.response['grades'].text, 'lxml') \
                    .find('option', selected=True)['value']

                self.request['Donem'] = current_term
                self.request['Ara'] = 'Listele'
                self.response['grades'] = self.session.post(GRADE_URL,
                                                            data=self.request)

                table = bs4(self.response['grades'].text, 'lxml') \
                    .find_all('table',
                              'table table-bordered '
                              'table-condensed')[0]

                parsed_table = table.findChildren(['th', 'tr'])
                out_table = PrettyTable(
                    ['DERS', 'AKTS', 'VIZE', 'FIN', 'BÜT', 'BN'])

                for i in range(1, len(parsed_table)):
                    a = [str(n.text).strip()
                         for n in parsed_table[i].findChildren('td')]
                    a = [a[2].split('(')[0]] + a[3:8]
                    out_table.add_row(a)
                print(out_table)
            except:
                print(colored(">>>> Notlar işlenirken hata oluştu", 'red'))
        else:
            self.do_login(ln)
            self.do_grades(ln)

    def do_status(self, ln):
        if self.is_login:
            try:
                self.response['bgrades'] = self.session.get(BGRADE_URL)
                info = bs4(self.response['bgrades'].text, 'lxml') \
                    .find_all('tr', 'menu_td')

                for i, j in zip(info, range(len(info) - 1, 0, -1)):
                    print("""
                        {} : {}
                        {} : {}
                    ########################################
                    """.format(*[str(n).strip() for n in i.text.strip()
                                 .replace(':', '\n').split('\n')
                                 if str(n).strip() != '']), sep="\n")
                print(info[-1].text)
            except:
                print(colored(">>>> Notlar işlenirken hata oluştu", 'red'))

    def do_info(self, ln):
        print(colored("""
             ____   _    _ _____            _  __  _  ___   _ _____ ______
             |  _ \| |  | |  __ \     /\   | |/ / | |/ (_)_(_) ____|  ____|
             | |_) | |  | | |__) |   /  \  | ' /  | ' / / _ \ (___ | |__
             |  _ <| |  | |  _  /   / /\ \ |  <   |  < | | | \___ \|  __|
             | |_) | |__| | | \ \  / ____ \| . \  | . \| |_| |___) | |____
             |____/ \____/|_|  \_\/_/    \_\_|\_\ |_|\_\\___/_____/|______|
                                  www.koseburak.net
                                                               """, 'blue'))

    def do_exit(self, ln):
        return -1

    def do_EOF(self, ln):
        return self.do_exit(ln)


if __name__ == '__main__':
    KOUCMD().cmdloop()
