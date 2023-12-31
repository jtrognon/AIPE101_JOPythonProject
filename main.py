import sqlite3
import sys
from PySide6 import QtWidgets
from sportChoice import SportChoiceWidget
from gameSettings import GameSettingsWidget
from gameScore import GameScoreWidget
from os.path import exists


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("JOs 2024 de Paris")

        geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.setFixedSize(geometry.width()*0.8, geometry.height()*0.7)

        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.grid = QtWidgets.QGridLayout(self.centralWidget)


    def choseSport(self, sportId: int):
        # delete sport widget and create Init for game
        try:
            self.centralWidget = QtWidgets.QWidget(self)
            self.setCentralWidget(self.centralWidget)

            self.grid = QtWidgets.QGridLayout(self.centralWidget)
        except:
            print("Ereur lors de la suppression du choix des sports")

        self.grid.addWidget(GameSettingsWidget(sportId))


    def choseSettings(self, infos):
        try:
            self.centralWidget = QtWidgets.QWidget(self)
            self.setCentralWidget(self.centralWidget)

            self.grid = QtWidgets.QGridLayout(self.centralWidget)
        except:
            print("Ereur lors de la suppression du choix des sports")

        self.grid.addWidget(GameScoreWidget(infos))


    def previousSettings(self):
        try:
            self.centralWidget = QtWidgets.QWidget(self)
            self.setCentralWidget(self.centralWidget)

            self.grid = QtWidgets.QGridLayout(self.centralWidget)
        except:
            print("Ereur lors de la suppression du choix des sports")

        self.grid.addWidget(SportChoiceWidget())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()

    sportWidget = SportChoiceWidget()
    window.grid.addWidget(sportWidget)

    geometry = window.geometry()
    window.update()

    window.show()

    sys.exit(app.exec())
