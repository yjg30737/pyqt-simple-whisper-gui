from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QPushButton


class Thread(QThread):
    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        try:
            pass
        except Exception as e:
            raise Exception(e)


class TextToSpeechWidget(QWidget):
    activated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__textEdit = QTextEdit()
        self.__textEdit.setPlaceholderText('Write something to get audio file 🙂')
        self.__textEdit.textChanged.connect(self.__textChanged)

        self.__runBtn = QPushButton('Run')
        self.__runBtn.clicked.connect(self.__run)
        lay = QVBoxLayout()
        lay.addWidget(self.__textEdit)
        lay.addWidget(self.__runBtn)
        self.setLayout(lay)

        self.__runBtn.setEnabled(False)

    def __textChanged(self):
        text = self.__textEdit.toPlainText()
        self.__runBtn.setEnabled(text.strip() != '')

    def __run(self):
        self.activated.emit(self.__textEdit.toPlainText())

    def started(self):
        self.__runBtn.setEnabled(False)

    def finished(self):
        self.__runBtn.setEnabled(True)
