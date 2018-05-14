import sys
from test import Ui_MainWindow
from func import Function
from PyQt5.QtWidgets import QApplication, QMainWindow




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = Ui_MainWindow()
    # ui = Function()
    MainWindow = Function()

    # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
