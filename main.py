import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QTableWidget,
                             QTableWidgetItem,
                             QMenu,
                             QFileDialog)
# from PyQt5 import Qt
from dialogs.save_dialog import SaveDialog
from hex_routines.utf8_converter import convert

from icecream.icecream import ic

from hex_routines.hex_file_io import HEXFileIO


class Editor(QMainWindow):
    hexdigits: set = set("0123456789abcdefABCDEF")

    def __init__(self) -> None:
        super(Editor, self).__init__(None)
        self.__file_is_chaged = False
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
            labels[i] = f"{i:07X}0"
            self.__init_hex_table_row(i)

        self.__hex_table.setVerticalHeaderLabels(labels)
        self.__hex_table.itemChanged.connect(self.__cell_changed)

    def __init_hex_table_row(self, row: int) -> None:
        ic(row)
        s = self.__file.read(16 * row, 16).split(":")
        decoded = QTableWidgetItem(self.__from_hex_to_string("".join(s)))
        # ic("before")
        decoded.setFlags(Qt.ItemFlag.ItemIsEnabled)
        # ic("after")
        self.__hex_table.setItem(row, 17, decoded)
        j = 0
        for j in range(len(s)):
            ic(j)
            cell = QTableWidgetItem(s[j].upper())
            # ic("before j")
            self.__hex_table.setItem(row, j, cell)
            # ic("after j")
        while j != 15:
            j += 1
            cell = QTableWidgetItem()
            self.__hex_table.setItem(row, j, cell)

    def __from_hex_to_string(self, hex_string: str) -> str:
        h = hex_string.upper()
        r = "".join([convert[h[i:i+2]] for i in range(0, len(h), 2)])
        ic(r)
        return r

    def __cell_changed(self, cell: QTableWidgetItem) -> None:
        try:
            self.__hex_table.itemChanged.disconnect()
            if 17 == cell.column():
                return
            # ic("changed", cell.row(), cell.column())
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
            self.__file_is_chaged = True
            self.__file.overwrite(y * 16 + x, text)
            self.__init_hex_table_row(y)
            ic("changed")
        finally:
            self.__hex_table.itemChanged.connect(self.__cell_changed)

    def __cell_undo(self, cell: QTableWidgetItem) -> None:
        y, x = cell.row(), cell.column()
        cell.setText(self.__file.read(y * 16 + x, 1))

    def __open(self) -> None:
        ic("openmenu")
        filename, _ = QFileDialog.getOpenFileName(self, "Select file")
        ic(filename, _)
        if "" == filename:  # файл не был выбран
            return
        self.__delete()
        self.__file = HEXFileIO(filename)
        self.__init_hex_table()
        self.setCentralWidget(self.__hex_table)

    def __alarm_save(self) -> bool:
        if not self.__file_is_chaged:
            return False
        filename = self.__file.original
        dlg = SaveDialog(filename)
        return dlg.exec()

    def __delete(self) -> None:
        ic("delete file")
        if self.__alarm_save():
            self.__file.save()
            ic("file is saved")
            self.__file_is_chaged = False
        else:
            self.__file.delete()
            ic("file is deleted")

    def __save(self) -> None:
        ic("savemenu")
        filename = self.__file.original
        self.__file.save()
        self.__file = HEXFileIO(filename)

    def exit(self) -> None:
        # ic(event)
        self.__delete()
        print("exit")
        exit()

        ...


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = Editor()
    app.aboutToQuit.connect(editor.exit)
    editor.show()
    sys.exit(app.exec_())
