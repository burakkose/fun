import sys
import threading

from PyQt4 import QtGui, QtCore

from gui.mygui import Ui_MainWindow
from models.primes import PrimeController

result = None
search = True


# Eşit bölmek için bir fonksiyon
def partition(lst, n):
    division = len(lst) / float(n)
    return [lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n)]


def worker(id2, check, range_):
    '''
İşçi fonksiyonu, her thread bu fonksiyonu çalıştırıyor.
id2 = thread numarası
check = aranan sayı
range_ = arama aralığı
'''
    global result
    global search
    for i in list(range_):
        if not search:
            break
        if check % i == 0:  # mod 0 ise sayı asal değildir
            search = False
            result = (id2, i)  # asallığı bozanı global deişkene ata
            break


'''
Form ekranı için oluşturulmuş sınıf'''


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    ''' Ekranda gösterilen bilgiler
    no_prime_text = asal değil diyor ve şu thread sunu bozdu diyor
    prime_test = asal diyor
    '''
    no_prime_text = "{} is not prime number because of Thread{} and {}"
    prime_text = "{} is prime number"

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.is_run = True
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.thread_table.setColumnCount(4)
        self.ui.thread_table.setHorizontalHeaderLabels(
                ['Thread', 'Start', 'Stop', 'Durum'])
        self.ui.start_button.clicked.connect(self.start)
        self.ui.stop_button.clicked.connect(self.stop)

    def start(self):
        '''start butonuna bastıgında bu çalışıyor yani iş burada yapılıyor
        '''
        global result, search
        self.is_run = True  # çalışıyor mu
        latest = PrimeController.get_latest_prime_num() + 2  # veri tabanında kayıtlı son asal sayı + 2
        while self.is_run:
            if latest % 2 == 0:  # sayı çift ise takma
                latest += 1  # latest aranan sayı
            QtCore.QCoreApplication.processEvents()
            self.set_searching_number(latest)  # ekrana aranan sayının bilgisini gösteriyor

            sqrt = int(latest ** 0.5) + 1  # sayıın karekökünün 1 fazlası
            # veritabanında 2 ile yukarıda bulunan sonuca kadarki
            # olan asal sayılar getiriliyor
            primesdb = PrimeController.get_primes_between(2, sqrt)
            if len(primesdb) <= 10:  # eğer asal sayı sayısı 100 den küçükse
                threads = [None] * 2  # 2 tane thread yarat
            else:  # 100 den fazla ise
                # dökümanda verilen formuldeki sayı kadar thread yarat
                threads = [None] * (len(primesdb) // 10 + 1)

            limits = partition(primesdb, len(threads))
            # yukarıda hangi threadlerin hangi aralıklara bakacagı ayarlanıyor
            for i in range(len(threads)):  # threadleri yaratıyor
                threads[i] = threading.Thread(
                        target=worker, args=(i, latest, limits[i],))
                threads[i].start()  # threadleri çalıştır

            self.update_table(len(threads), limits)  # tabloda bilgi göster ekranda

            for i in threads:
                i.join()  # tüm threadler birbirini bekleyecekler yani hepsi bitene kadar program bekleyecek

            if result is None:  # veri tabanına ekleniyor. Farklı threadde
                PrimeController.add_table(latest)

            self.update_table(len(threads), limits, result)  # yine ekrandaki yerlerde bilgiler gösteriliyor
            self.set_result_information(latest, result)  # sayı hakkıda bilgi gösteriliyor asal mı değil mi diye
            result, search, latest = None, True, latest + 1  # tekrar araştırma için her şey sıfırlanıyor

    def stop(self):
        '''stop bastığında bu olacak'''
        self.is_run = False

    def set_searching_number(self, num):
        '''aranan numarayı ekranda göster'''
        self.ui.searching_number.display(num)

    def set_result_information(self, num, res):
        '''sayı hakkında bilgi göster asal mı değil mi gibi'''
        text = self.prime_text.format(num) if res is None else \
            self.no_prime_text.format(num, res[0], res[1])
        self.ui.result_label.setText(text)

    def update_table(self, thread_count, limits, arg=None):
        '''ekrandaki tabloyu güncelliyor'''
        thread_id = -1 if arg is None else arg[0]

        self.ui.thread_table.clearContents()
        self.ui.thread_table.setRowCount(thread_count)
        for i in range(thread_count):
            limits[i] = limits[i] * 2 if len(limits[i]) == 1 else limits[i]
            self.ui.thread_table.setItem(i, 0, QtGui.QTableWidgetItem(str(i)))
            self.ui.thread_table.setItem(
                    i, 1, QtGui.QTableWidgetItem(str(limits[i][0])))
            self.ui.thread_table.setItem(
                    i, 2, QtGui.QTableWidgetItem(str(limits[i][-1])))
            column4 = True if (thread_id == i) else False
            self.ui.thread_table.setItem(
                    i, 3, QtGui.QTableWidgetItem(str(column4)))


'''
Main fonksiyonu
'''
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()
    sys.exit()
