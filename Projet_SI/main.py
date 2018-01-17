import sys
from Fen_principale import Fen_principale
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Fen_principale()
    MainWindow.show()

    try:
        sys.exit(app.exec_())
    except:
        sys.exit(0)


