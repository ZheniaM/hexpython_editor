import sys
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QMenu,
                             QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from dialogs.save_dialog import SaveDialog

from icecream.icecream import ic

# from hex_routines.utf8_converter import convert
from hex_routines.hex_file_io import HEXFileIO
from widgets.hex_table import HexTable


class Editor(QMainWindow):
    hexdigits: set = set("0123456789abcdefABCDEF")

    def __init__(self) -> None:
        super(Editor, self).__init__(None)
        self.setGeometry(20, 60, 1300, 600)
        # self.showMaximized()
        self.__file = HEXFileIO(".txt")
        self.__hex_table = HexTable(self, self.__file)
        self.__init_menu_bar()

        self.setCentralWidget(self.__hex_table)
        self.__update_status_bar()

    def __update_status_bar(self) -> None:
        insert = self.__hex_table.is_insert_mode
        self.statusBar().showMessage(("--REPLACE--", "--INSERT--")[insert])

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Insert:
            ic("'insert' is pressed")
            insert = not self.__hex_table.is_insert_mode
            self.__hex_table.is_insert_mode = insert
            self.__update_status_bar()

    def __init_menu_bar(self) -> None:
        menu_bar = self.menuBar()
        file_menu = QMenu("&File", self)
        file_menu.addAction("Open", self.__open, shortcut="ctrl+o")
        file_menu.addAction("Save", self.__save, shortcut="ctrl+s")
        menu_bar.addMenu(file_menu)

    def __open(self) -> None:
        ic("openmenu")
        filename, _ = QFileDialog.getOpenFileName(self, "Select file")
        ic(filename, _)
        if "" == filename:  # файл не был выбран
            return
        self.__delete()
        self.__file = HEXFileIO(filename)
        self.__hex_table = HexTable(self, self.__file)
        self.setCentralWidget(self.__hex_table)

    def __alarm_save(self) -> bool:
        if not self.__file.is_chaged:
            return False
        filename = self.__file.original
        dlg = SaveDialog(filename)
        return dlg.exec()

    def __delete(self) -> None:
        ic("delete file")
        if self.__alarm_save():
            self.__file.save()
            ic("file is saved")
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = Editor()
    app.aboutToQuit.connect(editor.exit)
    editor.show()
    sys.exit(app.exec_())
