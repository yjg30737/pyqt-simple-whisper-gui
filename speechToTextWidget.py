from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextBrowser

from findPathWidget import FindPathWidget


class SpeechToTextWidget(QWidget):
    activated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__findPathWidget = FindPathWidget()
        self.__findPathWidget.getLineEdit().setPlaceholderText('Select the MP3 file...')
        self.__findPathWidget.setExtOfFiles('Audio Files (*.mp3)')
        self.__findPathWidget.added.connect(self.__added)

        self.__runBtn = QPushButton('Run!')
        self.__runBtn.clicked.connect(self.__activated)

        self.__textBrowser = QTextBrowser()
        self.__textBrowser.setPlaceholderText('Speech To Text Result')

        lay = QVBoxLayout()
        lay.addWidget(self.__findPathWidget)
        lay.addWidget(self.__runBtn)
        lay.addWidget(self.__textBrowser)

        self.setLayout(lay)

        self.__runBtn.setEnabled(False)

    def __added(self):
        self.__runBtn.setEnabled(True)

    def __activated(self):
        filename = self.__findPathWidget.getLineEdit().text()
        self.activated.emit(filename)

    def setResultText(self, text):
        self.__textBrowser.setText(text)