from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication, QLabel


def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()



if __name__ == "__main__":
    main()
