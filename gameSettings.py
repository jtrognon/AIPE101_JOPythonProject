import sqlite3, sys
from PySide6 import QtCore, QtWidgets, QtGui

class GameSettingsWidget(QtWidgets.QWidget):
    def __init__(self, sportId):
        super().__init__()

        # Properties
        self.width = 600
        self.height = 400
        self.setFixedSize(self.width, self.height)

        # Connect to DB
        self.co = sqlite3.connect("JOs.db")

        # Primary layout
        self.primaryLayout = QtWidgets.QVBoxLayout(self)
        # self.primaryLayout.addStretch()
        # self.primaryLayout.setDirection(QtWidgets.QBoxLayout.Direction.TopToBottom)

        # Sport Label and layout (title)
        # Layout
        self.sportLayout = QtWidgets.QVBoxLayout(self)
        self.primaryLayout.addLayout(self.sportLayout)

        # Sport label
        self.sportLabel = QtWidgets.QLabel("")
        self.sportId = sportId
        self.setSport()
        self.sportLabel.setFont(QtGui.QFont("Arial", 20))
        self.sportLayout.addWidget(self.sportLabel, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # ---- Teams layouts ----
        # Primary teams layout
        self.primaryTeamsLayout = QtWidgets.QVBoxLayout(self)
        self.primaryLayout.addLayout(self.primaryTeamsLayout)

        # TeamsLabel
        self.teamsLabel = QtWidgets.QLabel("Choisissez votre équipe : ")
        self.primaryTeamsLayout.addWidget(self.teamsLabel, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.teamsLabel.setFixedSize(450, 60)
        self.teamsLabel.setFont(QtGui.QFont("Arial", 30))

        # TeamsBottomSpace
        self.teamsBottomSpace = QtWidgets.QWidget()
        self.primaryTeamsLayout.addWidget(self.teamsBottomSpace)
        self.teamsBottomSpace.setFixedSize(50, 25)

        # Secondary teams layout
        self.secondaryTeamsLayout = QtWidgets.QVBoxLayout(self)
        self.primaryTeamsLayout.addLayout(self.secondaryTeamsLayout)

        # ---- Team 1 ----
        # Team 1 layout
        self.team1Layout = QtWidgets.QHBoxLayout()
        self.secondaryTeamsLayout.addLayout(self.team1Layout)


        # Team 1 label
        self.team1Label = QtWidgets.QLabel("Équipe 1 : ")
        self.team1Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.team1Layout.addWidget(self.team1Label)
        self.team1Label.setFixedSize(200, 40)
        self.team1Label.setFont(QtGui.QFont("Arial", 20))

        # Team1 DropDown
        self.team1DropDown = QtWidgets.QComboBox()
        self.team1DropDown.setFixedWidth(150)
        self.team1Layout.addWidget(self.team1DropDown)
        self.team1DropDown.setFixedSize(200, 40)
        self.team1DropDown.setFont(QtGui.QFont("Arial", 20))

        # ---- Team 2 ----
        # Team 2 layout
        self.team2Layout = QtWidgets.QHBoxLayout()
        self.secondaryTeamsLayout.addLayout(self.team2Layout)

        # Team 2 label
        self.team2Label = QtWidgets.QLabel("Équipe 2 : ")
        self.team2Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.team2Layout.addWidget(self.team2Label)
        self.team2Label.setFixedSize(200, 40)
        self.team2Label.setFont(QtGui.QFont("Arial", 20))

        # Team2 DropDown
        self.team2DropDown = QtWidgets.QComboBox()
        self.team2DropDown.setFixedWidth(150)
        self.team2Layout.addWidget(self.team2DropDown)
        self.team2DropDown.setFixedSize(200, 40)
        self.team2DropDown.setFont(QtGui.QFont("Arial", 20))

        # Team choice
        self.getTeams()

        # Next and Back Buttons and Layout
        # Layout
        self.buttonsLayout = QtWidgets.QHBoxLayout(self)
        self.primaryLayout.addLayout(self.buttonsLayout)
        self.buttonsLayout.setContentsMargins(25, 25, 25, 25)

        # Next button
        self.nextButton = QtWidgets.QPushButton("Continuer")
        self.buttonsLayout.addWidget(self.nextButton)
        self.nextButton.clicked.connect(self.sendChoice)

        # Previous button
        self.previousButton = QtWidgets.QPushButton("Retour")
        self.buttonsLayout.addWidget(self.previousButton)
        self.previousButton.clicked.connect(self.previousWindow)



    def setSport(self):
        sportName = self.co.execute(f"SELECT Name FROM Sports WHERE Id = {self.sportId}").fetchall()[0][0]

        self.sportLabel.setText(sportName)
    def getTeams(self):
        # Get teams
        teams = self.co.execute("SELECT Name FROM Teams")

        # Display teams
        for team in teams:
            self.team1DropDown.addItem(team[0])
            self.team2DropDown.addItem(team[0])


    def sendChoice(self):
        teamId1 = self.co.execute(f"SELECT Id FROM Teams WHERE Name = '{self.team1DropDown.currentText()}'").fetchall()
        teamId2 = self.co.execute(f"SELECT Id FROM Teams WHERE Name = '{self.team2DropDown.currentText()}'").fetchall()

        if teamId1 != teamId2 :
            mainWindow = self.parentWidget().parentWidget()
            mainWindow.choseSettings((self.sportId, int(teamId1[0][0]), int(teamId2[0][0])))


    def previousWindow(self):
        mainWindow = self.parentWidget().parentWidget()
        mainWindow.previousSettings()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GameSettingsWidget(1)

    window.update()

    window.show()

    sys.exit(app.exec())
