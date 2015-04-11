'''
The MIT License

Copyright (c) 2015 burak köse

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.'''

__author__ = 'burakks'
__version__= '0.1.1'

import cmd
import getpass

import requests
from termcolor import colored
from bs4 import BeautifulSoup
from prettytable import PrettyTable

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
        self.is_Login = False
        self.request = {}
        self.response = {}
        self.session = requests.session()

    def do_login(self, ln):
        if not self.is_Login:
            username = input('{} Okul No : '.format(colored('>>>', 'red')))
            pasword = getpass.getpass('{}Parola : '.format(colored(">>> ", "red")))
            try:
                self.request['Sicil'] = username
                self.request['Sifre'] = pasword
                self.request['LoggingOn'] = '1'
                self.response['login_page'] = self.session.post(BASE_URL, data = self.request,verify=False)
                if username in str(self.response['login_page'].text):
                    self.is_Login = True
                    print(colored("Giriş başarılı", 'green'))
                else:
                    self.is_Login = False
                    print(colored(">>>> Giriş başarısız", 'red'))
            except requests.ConnectionError:
                self.is_Login = False
                print(colored(">>>> Bağlantı hatası", 'red'))

    def do_grades(self, ln):
        if self.is_Login:
            try:
                self.response['grades_page'] = self.session.get(GRADE_URL)
                current_term = BeautifulSoup(self.response['grades_page'].text).find('option', selected = True)['value']
                self.request['Donem'] = current_term
                self.request['Ara'] = 'Listele'
                self.response['grades_page'] = self.session.post(GRADE_URL, data = self.request)
                table = BeautifulSoup(self.response['grades_page'].text).find_all('table',
                                                                                  'table table-bordered '
                                                                                  'table-condensed')[0]
                parsed_table = table.findChildren(['th', 'tr'])
                out_table = PrettyTable(['DERS ADI', 'AKTS', 'VIZE', 'FINAL', 'BN'])
                for i in range(1, len(parsed_table)):
                    a = [str(n.text).strip() for n in parsed_table[i].findChildren('td')]
                    a = [a[2].split('(')[0]] + a[3:6] + [a[7]]
                    out_table.add_row(a)
                print(out_table)
            except:
                print(colored(">>>> Notlar işlenirken hata oluştu", 'red'))
        else:
            self.do_login(ln)
            self.do_grades(ln)

    def do_status(self, ln):
        if self.is_Login:
            try:
                self.response['bgrades_page'] = self.session.get(BGRADE_URL)
                info = BeautifulSoup(self.response['bgrades_page'].text).find_all('tr', 'menu_td')
                for i, j in zip(info, range(len(info) - 1, 0, -1)):
                    print("""
                        {} : {}
                        {} : {}
                    ########################################
                    """.format(
                        *[str(n).strip() for n in i.text.strip().replace(':', '\n').split('\n')
                          if str(n).strip() != '']), sep = "\n")
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
                                                               """, 'blue'))

    def do_exit(self, ln):
        return -1

    def do_quit(self, ln):
        return self.do_exit(ln)

    def do_EOF(self, ln):
        return self.do_exit(ln)


if __name__ == '__main__':
    KOUCMD().cmdloop()
			
