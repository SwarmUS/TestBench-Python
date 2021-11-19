from src.visualisation_tool.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication, QLabel


def main():
    app = QApplication([])
    main_window = MainWindow()
    main_window.showMaximized()
    app.exec_()



if __name__ == "__main__":
    main()
