import sys
import threading
from PyQt4 import QtGui, QtCore

from gui.mygui import Ui_MainWindow
from models.primes import PrimeController

result = None
search = True


def partition(lst, n):
    division = len(lst) / float(n)
    return [lst[int(round(division * i)): int(round(division * (i + 1)))] for i in range(n)]


def worker(id2, check, range_):
    global result
    global search
    for i in list(range_):
        if not search:
            break
        if check % i == 0:
            search = False
            result = (id2, i)
            break


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
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
        global result, search
        self.is_run = True
        latest = PrimeController.get_latest_prime_num() + 2
        while self.is_run:
            if latest % 2 == 0:
                latest += 1
            QtCore.QCoreApplication.processEvents()
            self.set_searching_number(latest)

            sqrt = int(latest ** 0.5) + 1
            primesdb = PrimeController.get_primes_between(2, sqrt)
            if len(primesdb) <= 10:
                threads = [None] * 2
            else:

                threads = [None] * (len(primesdb) // 10 + 1)

            limits = partition(primesdb, len(threads))

            for i in range(len(threads)):
                threads[i] = threading.Thread(
                    target=worker, args=(i, latest, limits[i],))
                threads[i].start()

            self.update_table(len(threads), limits)

            for i in threads:
                i.join()
            if result is None:
                PrimeController.add_table(latest)

            self.update_table(len(threads), limits, result)
            self.set_result_information(latest, result)
            result, search, latest = None, True, latest + 1

    def stop(self):
        self.is_run = False

    def set_searching_number(self, num):
        self.ui.searching_number.display(num)

    def set_result_information(self, num, res):
        text = self.prime_text.format(num) if res is None else \
            self.no_prime_text.format(num, res[0], res[1])
        self.ui.result_label.setText(text)

    def update_table(self, thread_count, limits, arg=None):
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


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()
    sys.exit()
