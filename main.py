import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QTableWidget,
                             QTableWidgetItem,
                             QMenu,
                             QFileDialog)

from icecream.icecream import ic

from hex_file_io import HEXFileIO


class Editor(QMainWindow):
    def __init__(self) -> None:
        super(Editor, self).__init__(None)
        self.setGeometry(500, 100, 0, 0)
        self.showMaximized()
        self.__table = QTableWidget()
        self.__file = HEXFileIO("")
        self.__init_table()
        self.__init_menu_bar()

        self.setCentralWidget(self.__table)

        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__main)
        self.__timer.start(100)

    def __init_menu_bar(self) -> None:
        menu_bar = self.menuBar()
        file_menu = QMenu("&File", self)
        file_menu.addAction("Open", self.__open)
        file_menu.addAction("Save", self.__save)
        menu_bar.addMenu(file_menu)

    def __init_table(self) -> None:
        size = len(self.__file)
        self.__len_of_strings = 1 + (size >> 4)
        self.__table.setColumnCount(16)
        self.__table.setRowCount(self.__len_of_strings)
        self.__table.setHorizontalHeaderLabels([
            "00", "01", "02", "03",
            "04", "05", "06", "07",
            "08", "09", "0A", "0B",
            "0C", "0D", "0E", "0F",])
        for i in range(16):
            self.__table.setColumnWidth(i, 1)

        labels = ["" for _ in range(self.__len_of_strings)]
        for i in range(self.__len_of_strings):
            s = self.__file.read(16 * i, 16).split(":")
            # ic(s)
            labels[i] = f"{i:07X}0"
            for j in range(len(s)):
                self.__table.setItem(i, j, QTableWidgetItem(s[j].upper()))

        self.__table.setVerticalHeaderLabels(labels)

    def __open(self) -> None:
        self.__file.delete()
        ic("openmenu")
        filename, _ = QFileDialog.getOpenFileName(self, "Select file")
        ic(filename)
        self.__file = HEXFileIO(filename)
        self.__init_table()

    def __save(self) -> None:
        ic("savemenu")

    def update_table(self) -> None:
        # self.__table.setRowCount(self.__len_of_strings)
        ...

    def __main(self) -> None:
        self.update_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
