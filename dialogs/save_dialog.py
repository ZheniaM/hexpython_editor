from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class SaveDialog(QDialog):
    def __init__(self, filename: str) -> None:
        super().__init__()
        self.setWindowTitle("Saving...")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.__buttonBox = QDialogButtonBox(QBtn)
        self.__buttonBox.accepted.connect(self.accept)
        self.__buttonBox.rejected.connect(self.reject)

        self.__filename = filename.split("/")[-1]

        self.layout = QVBoxLayout()
        message = QLabel(f"Do you want to save file '{self.__filename}'")
        self.layout.addWidget(message)
        self.layout.addWidget(self.__buttonBox)
        self.setLayout(self.layout)
