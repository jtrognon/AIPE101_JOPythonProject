import sqlite3, sys
from PySide6 import QtCore, QtWidgets

class GameSettingsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Connect to DB
        self.co = sqlite3.connect("JOs.db")

        # primary layout
        self.primaryLayout = QtWidgets.QVBoxLayout(self)

        # sport Label (title)
        self.sportLabel = QtWidgets.QLabel("")
        self.primaryLayout.addWidget(self.sportLabel)

        # Team choice
        self.getTeams()


    def setSport(self):



    def getTeams(self):
        # get teams
        teams = self.co.execute("SELECT Name FROM Teams")

        print(teams.fetchall()[0][0])



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GameSettingsWidget()

    window.update()

    window.show()

    sys.exit(app.exec())
