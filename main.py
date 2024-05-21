import sys
# from PyQt5 import QtGui
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QTableWidget,
                             QTableWidgetItem,
                             QMenu,
                             QFileDialog)

from icecream.icecream import ic

from hex_file_io import HEXFileIO


class Editor(QMainWindow):
    hexdigits: set = set("0123456789abcdefABCDEF")

    def __init__(self) -> None:
        super(Editor, self).__init__(None)
        self.setGeometry(20, 60, 1300, 600)
        # self.showMaximized()
        self.__file = HEXFileIO(".txt")
        self.__init_hex_table()
        self.__init_menu_bar()

        self.setCentralWidget(self.__hex_table)

    def __init_menu_bar(self) -> None:
        menu_bar = self.menuBar()
        file_menu = QMenu("&File", self)
        file_menu.addAction("Open", self.__open, shortcut="ctrl+o")
        file_menu.addAction("Save", self.__save, shortcut="ctrl+s")
        menu_bar.addMenu(file_menu)

    def __init_hex_table(self) -> None:
        self.__hex_table = QTableWidget(self)
        size = len(self.__file)
        ic(size)
        self.__len_of_strings = 1 + (size >> 4)
        self.__hex_table.setColumnCount(16 + 1 + 1)
        self.__hex_table.setRowCount(self.__len_of_strings)
        self.__hex_table.setHorizontalHeaderLabels([
            "00", "01", "02", "03",
            "04", "05", "06", "07",
            "08", "09", "0A", "0B",
            "0C", "0D", "0E", "0F",
            "", "Decoded Text"])
        for i in range(16):
            self.__hex_table.setColumnWidth(i, 1)
        self.__hex_table.setColumnWidth(16, 1)

        labels = ["" for _ in range(self.__len_of_strings)]
        for i in range(self.__len_of_strings):
            s = self.__file.read(16 * i, 16).split(":")
            # ic(s)
            self.__hex_table.setItem(
                i, 17,
                QTableWidgetItem(self.__from_hex_to_string("".join(s))))
            labels[i] = f"{i:07X}0"
            j = 0
            for j in range(len(s)):
                cell = QTableWidgetItem(s[j].upper())
                self.__hex_table.setItem(i, j, cell)
            while j != 15:
                j += 1
                cell = QTableWidgetItem()
                self.__hex_table.setItem(i, j, cell)
        self.__hex_table.setVerticalHeaderLabels(labels)
        self.__hex_table.itemChanged.connect(self.__cell_changed)
        self.__hex_table.itemEntered.connect(self.__cell_entered)
        self.__hex_table.itemActivated.connect(self.__cell_entered)

    def __from_hex_to_string(self, hex_string: str) -> str:
        return bytes.fromhex(hex_string).decode("utf-8", errors="replace")

    def __cell_entered(self, cell: QTableWidget) -> None:
        ic("entered", cell.row(), cell.column())
        ...

    def __cell_changed(self, cell: QTableWidgetItem) -> None:
        ic("changed", cell.row(), cell.column())
        text = cell.text()
        if 2 != len(text):
            self.__cell_undo(cell)
            return
        a, b = text
        if a not in Editor.hexdigits or b not in Editor.hexdigits:
            self.__cell_undo(cell)
            return
        y, x = cell.row(), cell.column()
        ic(y * 16 + x)
        ic(self.__file.read(0, 16))
        self.__file.overwrite(y * 16 + x, text)
        ic("changed")

    def __cell_undo(self, cell: QTableWidgetItem) -> None:
        y, x = cell.row(), cell.column()
        cell.setText(self.__file.read(y * 16 + x, 1))

    def __open(self) -> None:
        ic("openmenu")
        filename, _ = QFileDialog.getOpenFileName(self, "Select file")
        ic(filename, _)
        if "" == filename:  # файл не был выбран
            return
        self.__file.delete()
        self.__file = HEXFileIO(filename)
        self.__init_hex_table()
        self.setCentralWidget(self.__hex_table)

    def __save(self) -> None:
        ic("savemenu")
        filename = self.__file.original
        self.__file.save()
        self.__file = HEXFileIO(filename)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = Editor()
    editor.show()
    sys.exit(app.exec_())
