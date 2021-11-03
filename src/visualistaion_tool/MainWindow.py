from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SwarmUS Interlocalisation Visualisation Tool")
        # Call functions to add ui elements here
        self.label = QLabel("Ta mere", self)
        self.setGeometry(0, 0, 500, 300)
