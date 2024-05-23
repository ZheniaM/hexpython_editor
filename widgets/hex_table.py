from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from hex_routines.hex_file_io import HEXFileIO
from hex_routines.utf8_converter import convert
# from icecream.icecream import ic


class HexTable(QTableWidget):
    hexdigits: set = set("0123456789abcdefABCDEF")

    def __init__(self, parrent, file: HEXFileIO) -> None:
        super().__init__(parrent)
        self.file = file
        size = len(self.file)
        # ic(size)
        self.__len_of_strings = 1 + (size >> 4)
        self.setColumnCount(16 + 1 + 1)
        self.setRowCount(self.__len_of_strings)
        self.setHorizontalHeaderLabels([
            "00", "01", "02", "03",
            "04", "05", "06", "07",
            "08", "09", "0A", "0B",
            "0C", "0D", "0E", "0F",
            "", "Decoded Text"])
        for i in range(16):
            self.setColumnWidth(i, 1)
        self.setColumnWidth(16, 1)

        labels = ["" for _ in range(self.__len_of_strings)]
        for i in range(self.__len_of_strings):
            labels[i] = f"{i:07X}0"
            self.__init_hex_table_row(i)

        self.setVerticalHeaderLabels(labels)
        self.itemChanged.connect(self.__cell_changed)

    def __init_hex_table_row(self, row: int) -> None:
        # ic(row)
        s = self.file.read(16 * row, 16).split(":")
        decoded = QTableWidgetItem(self.__from_hex_to_string("".join(s)))
        decoded.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.setItem(row, 17, decoded)
        j = 0
        for j in range(len(s)):
            cell = QTableWidgetItem(s[j].upper())
            self.setItem(row, j, cell)
        while j != 15:
            j += 1
            cell = QTableWidgetItem()
            self.setItem(row, j, cell)

    def __from_hex_to_string(self, hex_string: str) -> str:
        h = hex_string.upper()
        return "".join([convert[h[i:i+2]] for i in range(0, len(h), 2)])

    def __cell_changed(self, cell: QTableWidgetItem) -> None:
        try:
            self.itemChanged.disconnect()
            if 17 == cell.column():
                return
            # ic("changed", cell.row(), cell.column())
            text = cell.text()
            if 2 != len(text):
                self.__cell_undo(cell)
                return
            a, b = text
            if a not in HexTable.hexdigits or b not in HexTable.hexdigits:
                self.__cell_undo(cell)
                return
            y, x = cell.row(), cell.column()
            # ic(y * 16 + x)
            self.file.overwrite(y * 16 + x, text)
            self.__init_hex_table_row(y)
            # ic("changed")
        finally:
            self.itemChanged.connect(self.__cell_changed)

    def insert_empty_cell_and_shift(self, row: int, column: int) -> None:
        start_byte = row * 16 + column
        self.file.insert_empty_cell(start_byte)
        self.__init_hex_table_row(row)
        self.__init_hex_table_row(row + 1)
        self.setCurrentCell(row + 1, 0)

        if row < self.rowCount() - 1:
            for r in range(self.rowCount() - 1, row + 1, -1):
                for c in range(16, 0, -1):
                    item = self.item(r - 1, c - 1)
                    if item:
                        text = item.text()
                        item = QTableWidgetItem(text)
                        self.setItem(r, c, item)

    def __cell_undo(self, cell: QTableWidgetItem) -> None:
        y, x = cell.row(), cell.column()
        cell.setText(self.file.read(y * 16 + x, 1))
