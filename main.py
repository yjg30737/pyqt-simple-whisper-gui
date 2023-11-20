import os
import sys

from apiWidget import ApiWidget
from loadingLbl import LoadingLabel
from script import load_client, get_tts, get_stt
from speechToTextWidget import SpeechToTextWidget
from textToSpeechWidget import TextToSpeechWidget

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QTabWidget, \
    QVBoxLayout
from PyQt5.QtCore import Qt, QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QFont

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    sttFinished = pyqtSignal(str)

    def __init__(self, f, text=''):
        super(Thread, self).__init__()
        self.__f = f
        self.__text = text

    def run(self):
        try:
            if self.__f == 0:
                get_tts(self.__text)
            else:
                self.sttFinished.emit(get_stt(self.__text))
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('PyQt Simple Whisper GUI')
        apiWidget = ApiWidget()
        apiWidget.apiKeyAccepted.connect(self.__showApi)
        apiWidget.setApi()

        self.__textToSpeechWidget = TextToSpeechWidget()
        self.__textToSpeechWidget.activated.connect(self.__ttsRun)

        self.__speechToTextWidget = SpeechToTextWidget()
        self.__speechToTextWidget.activated.connect(self.__sttRun)

        tabWidget = QTabWidget()
        tabWidget.addTab(self.__textToSpeechWidget, 'Text-to-Speech')
        tabWidget.addTab(self.__speechToTextWidget, 'Speech-to-Text')

        self.__loadingLbl = LoadingLabel()
        self.__loadingLbl.setEnabled(False)

        lay = QVBoxLayout()
        lay.addWidget(apiWidget)
        lay.addWidget(tabWidget)
        lay.addWidget(self.__loadingLbl)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

    def __showApi(self, api_key):
        self.__api_key = api_key
        load_client(self.__api_key)

    def __ttsRun(self, text):
        f = 0
        self.__run(f, text)

    def __sttRun(self, filename):
        f = 1
        self.__run(f, filename)

    def __run(self, f, text):
        self.__t = Thread(f, text)
        self.__t.started.connect(self.__started)
        self.__t.sttFinished.connect(self.__speechToTextWidget.setResultText)
        self.__t.finished.connect(self.__finished)
        self.__t.start()

    def __started(self):
        self.__textToSpeechWidget.started()
        self.__loadingLbl.setVisible(True)
        self.__loadingLbl.start()

    def __finished(self):
        self.__textToSpeechWidget.finished()
        self.__loadingLbl.setVisible(False)
        self.__loadingLbl.stop()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())