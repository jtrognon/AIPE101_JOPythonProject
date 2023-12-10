import sqlite3, sys
from PySide6 import QtCore, QtWidgets, QtGui

class GameScoreWidget(QtWidgets.QWidget):
    def __init__(self, infos):
        super().__init__()

        # unwrap infos
        self.sportId, self.team1Id, self.team2Id = infos

        # teams name
        self.team1Name = ""
        self.team2Name = ""

        # connect to JOs.db
        self.co = sqlite3.connect("JOs.db")

        # set points list
        self.pointsList = []
        self.setPointsList()

        # check if the game exist in DB
        self.doesGameExist()

        # Properties
        self.width = 1200
        self.height = 600
        self.setFixedSize(self.width, self.height)

        # Primary layout
        self.primaryLayout = QtWidgets.QGridLayout(self)

        # Ranking Layout
        self.rankingLayout = QtWidgets.QVBoxLayout()
        self.primaryLayout.addLayout(self.rankingLayout, 0, 0, 2, 1)

        # Main layout
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.primaryLayout.addLayout(self.mainLayout, 0, 1, 2, 1)

        # Points layout
        self.pointsLayout = QtWidgets.QVBoxLayout()
        self.primaryLayout.addLayout(self.pointsLayout, 1, 1)

        # Browsing layout
        self.browsingLayout = QtWidgets.QVBoxLayout()
        self.primaryLayout.addLayout(self.browsingLayout, 1, 2)

        # ---------------- Main layout ----------------
        # Main layout space up
        self.mainLayoutSpaceUp = QtWidgets.QWidget()
        self.mainLayout.addWidget(self.mainLayoutSpaceUp, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.mainLayoutSpaceUp.setFixedSize(10, 100)

        # Score layout
        self.scoreLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.scoreLayout)

        # Score space left
        self.spaceLeftScore = QtWidgets.QWidget()
        self.scoreLayout.addWidget(self.spaceLeftScore)
        self.spaceLeftScore.setFixedSize(450, 1)

        # ---------------Team 1 ----------------
        # Team 1 score
        self.team1ScoreLayout = QtWidgets.QVBoxLayout()
        self.scoreLayout.addLayout(self.team1ScoreLayout)

        # Team 1 label
        self.team1ScoreLabel = QtWidgets.QLabel("Équipe 1 : ")
        self.team1ScoreLayout.addWidget(self.team1ScoreLabel, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.team1ScoreLabel.setFont(QtGui.QFont("Arial", 15))

        # Team 1 score
        self.team1ScoreDisplay = QtWidgets.QLabel("0")
        self.team1ScoreLayout.addWidget(self.team1ScoreDisplay, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.team1ScoreDisplay.setFont(QtGui.QFont("Arial", 100))

        # Score delimiter label
        self.delimiterScore = QtWidgets.QLabel("-")
        self.scoreLayout.addWidget(self.delimiterScore, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.delimiterScore.setFont(QtGui.QFont("Arial", 100))

        # ---------------Team 2 ----------------
        # Team 2 score
        self.team2ScoreLayout = QtWidgets.QVBoxLayout()
        self.scoreLayout.addLayout(self.team2ScoreLayout)

        # Team 2 label
        self.team2ScoreLabel = QtWidgets.QLabel("Équipe 2 : ")
        self.team2ScoreLayout.addWidget(self.team2ScoreLabel, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.team2ScoreLabel.setFont(QtGui.QFont("Arial", 15))

        # Team 2 score
        self.team2ScoreDisplay = QtWidgets.QLabel("0")
        self.team2ScoreLayout.addWidget(self.team2ScoreDisplay, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.team2ScoreDisplay.setFont(QtGui.QFont("Arial", 100))

        # Score space down
        self.scoreSpaceDown = QtWidgets.QWidget()
        self.mainLayout.addWidget(self.scoreSpaceDown, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.scoreSpaceDown.setFixedSize(10, 50)

        # Score space right
        self.spaceRightScore = QtWidgets.QWidget()
        self.scoreLayout.addWidget(self.spaceRightScore)
        self.spaceRightScore.setFixedSize(450, 1)

        # Update score
        self.updateScore()

        # Set teams label's text
        self.setTeamsLabelName()

        # --------------- additional infos ---------------

        # Additional infos layout
        self.additionalInfosLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.addLayout(self.additionalInfosLayout)

        # Additional infos label
        self.additionalInfosLabel = QtWidgets.QLabel("Informations additionelles : ")
        self.additionalInfosLayout.addWidget(self.additionalInfosLabel, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Additional infos display
        self.additionalInfosDisplay = QtWidgets.QLabel()
        self.additionalInfosLayout.addWidget(self.additionalInfosDisplay, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.additionalInfosDisplay.setFont(QtGui.QFont("Arial", 20))
        self.updateAdditionalInfos()

        # Score layout spaceDown
        self.scoreLayoutSpaceDown = QtWidgets.QWidget()
        self.mainLayout.addWidget(self.scoreLayoutSpaceDown, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.scoreLayoutSpaceDown.setFixedSize(10, 200)

        # ---------------- Points management ----------------

        # Management points label
        self.managementPointsLabel = QtWidgets.QLabel("Gestion des points : ")
        self.pointsLayout.addWidget(self.managementPointsLabel, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.managementPointsLabel.setFixedHeight(20)

        # Points management layout
        self.pointsManagementLayout = QtWidgets.QHBoxLayout()
        self.pointsLayout.addLayout(self.pointsManagementLayout)

        # Team 1 points management layout
        self.team1GlobalPointsManagementLayout = QtWidgets.QVBoxLayout()
        self.pointsManagementLayout.addLayout(self.team1GlobalPointsManagementLayout)
        self.team1PointsManagementLayout = QtWidgets.QHBoxLayout()
        self.team1GlobalPointsManagementLayout.addLayout(self.team1PointsManagementLayout)

        # Add points to first team button
        self.addScoreT1Button = QtWidgets.QPushButton(f"Ajouter 1 point à {self.team1Name}")
        self.team1PointsManagementLayout.addWidget(self.addScoreT1Button)
        self.addScoreT1Button.setFixedWidth(200)
        self.addScoreT1Button.clicked.connect(self.addSubstractScore)

        # Remove points to first team button
        self.substractScoreT1Button = QtWidgets.QPushButton(f"Enlever 1 point à {self.team1Name}")
        self.team1PointsManagementLayout.addWidget(self.substractScoreT1Button)
        self.substractScoreT1Button.setFixedWidth(200)
        self.substractScoreT1Button.clicked.connect(self.addSubstractScore)

        # Entry to choose nb of points
        self.team1EntryNbOfPoints = QtWidgets.QLineEdit()
        self.team1EntryNbOfPoints.setPlaceholderText("Nombre de points")
        self.team1EntryNbOfPoints.setInputMask("99")
        self.team1GlobalPointsManagementLayout.addWidget(self.team1EntryNbOfPoints, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.team1EntryNbOfPoints.setFixedSize(150, 20)

        # ------------------- Team 2 -------------------

        # Team 2 points management layout
        self.team2GlobalPointsManagementLayout = QtWidgets.QVBoxLayout()
        self.pointsManagementLayout.addLayout(self.team2GlobalPointsManagementLayout)
        self.team2PointsManagementLayout = QtWidgets.QHBoxLayout()
        self.team2GlobalPointsManagementLayout.addLayout(self.team2PointsManagementLayout)

        # Add points to second team button
        self.addScoreT2Button = QtWidgets.QPushButton(f"Ajouter 1 point à {self.team2Name}")
        self.team2PointsManagementLayout.addWidget(self.addScoreT2Button)
        self.addScoreT2Button.setFixedWidth(200)
        self.addScoreT2Button.clicked.connect(self.addSubstractScore)

        # Remove points to second team button
        self.substractScoreT2Button = QtWidgets.QPushButton(f"Enlever 1 point à {self.team2Name}")
        self.team2PointsManagementLayout.addWidget(self.substractScoreT2Button)
        self.substractScoreT2Button.setFixedWidth(200)
        self.substractScoreT2Button.clicked.connect(self.addSubstractScore)

        # Entry to choose nb of points
        self.team2EntryNbOfPoints = QtWidgets.QLineEdit()
        self.team2EntryNbOfPoints.setPlaceholderText("Nombre de points")
        self.team2EntryNbOfPoints.setInputMask("99")
        self.team2GlobalPointsManagementLayout.addWidget(self.team2EntryNbOfPoints, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.team2EntryNbOfPoints.setFixedSize(150, 20)

        # Management layout space down
        self.managementLayoutSpaceDown = QtWidgets.QWidget()
        self.pointsLayout.addWidget(self.managementLayoutSpaceDown, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.managementLayoutSpaceDown.setFixedSize(10, 50)

        # Check game
        self.checkGame()

        # check if the game need entries
        self.needEntryPoint()

        # ----------------- Nav button -----------------
        # New game button
        self.navButton = QtWidgets.QPushButton("Nouveau match")
        self.navButton.clicked.connect(self.newGame)
        self.browsingLayout.addWidget(self.navButton)

        # Reset button
        self.resetButton = QtWidgets.QPushButton("Remettre à 0")
        self.resetButton.clicked.connect(self.resetGame)
        self.browsingLayout.addWidget(self.resetButton)


    def setTeamsLabelName(self):
        """
        Set the text for the teams label
        """
        self.team1Name = self.co.execute(f"SELECT Name FROM Teams WHERE Id = {self.team1Id}").fetchall()[0][0]
        self.team2Name = self.co.execute(f"SELECT Name FROM Teams WHERE Id = {self.team2Id}").fetchall()[0][0]

        self.team1ScoreLabel.setText(self.team1Name)
        self.team2ScoreLabel.setText(self.team2Name)


    def updateScore(self):
        """
        Update the score labels
        """

        score1, score2 = self.co.execute(f"SELECT ScoreT1, ScoreT2 FROM Games WHERE SportId = {self.sportId} AND Team1Id = {self.team1Id} AND Team2Id = {self.team2Id}").fetchall()[0]

        self.team1ScoreDisplay.setText(str(score1))
        self.team2ScoreDisplay.setText(str(score2))


    def updateAdditionalInfos(self):
        """
        Update additional infos
        """

        additionalInfos = self.co.execute(f"SELECT Infos FROM Games WHERE SportId = {self.sportId} AND Team1Id = {self.team1Id} AND Team2Id = {self.team2Id}").fetchall()[0][0]

        if additionalInfos == "":
            self.additionalInfosLayout.setEnabled(False)
            self.additionalInfosLabel.setHidden(True)
        else:
            self.additionalInfosDisplay.setText(additionalInfos)

    def addSubstractScore(self):
        """
        Update score in SQL DB and label
        :param team: update first or second team score
        :param add: add or substract points
        :return: None
        """
        buttonText = self.sender().text()
        if len(buttonText) == 18 + len(self.team1Name): # Team 1
            team = 1
        else: # Team 2
            team = 2

        if buttonText[0] == 'A':
            add = True
        else:
            add = False


        score = self.co.execute(f"SELECT scoreT{team} FROM Games WHERE SportId = {self.sportId} AND Team1Id = {self.team1Id} AND Team2Id = {self.team2Id}").fetchall()[0][0]
        sportName = self.co.execute(f"SELECT Name FROM Sports WHERE Id = {self.sportId}").fetchall()[0][0]

        if sportName == "Water polo" or sportName == "Badminton" or sportName == "Fencing" or sportName == "Football" or sportName == "Judo" or sportName == "Table tennis":
            if add:
                scoreIncrement = int(score) + 1
            elif score != "0":
                scoreIncrement = int(score) - 1
            else:
                scoreIncrement = "0"
        elif sportName == "Archery" or sportName == "Basketball" or sportName == "Field hockey" or sportName == "Handball" or sportName == "Rugby sevens" or sportName == "Shooting" or sportName == "Volleyball":
            if team == 1:
                scoreEntry = self.team1EntryNbOfPoints.text()
            else:
                scoreEntry = self.team2EntryNbOfPoints.text()

            if scoreEntry == "":
                scoreIncrement = int(score)
            else:
                scoreIncrement = int(score) + int(scoreEntry)

        else:
            scoreIndex = self.pointsList.index(score)
            if add:
                score = scoreIndex + 1
                if len(self.pointsList) != score:
                    scoreIncrement = self.pointsList[score]
                else:
                    scoreIncrement = self.pointsList[0]
                    self.endGame(team)
            else:
                score = scoreIndex - 1
                if score >= 0:
                    scoreIncrement = self.pointsList[score]
                else:
                    scoreIncrement = self.pointsList[score + 1]

        self.co.execute(f"UPDATE Games SET ScoreT{team} = '{scoreIncrement}' WHERE SportId = {self.sportId} AND Team1Id = {self.team1Id} AND Team2Id = {self.team2Id}")

        self.updateScore()
        self.co.commit()

    def setPointsList(self):
        """
        Get and set the points list.
        :return: None
        """
        pointsString = self.co.execute(f"SELECT PointIncrement FROM Sports WHERE Id = {self.sportId}").fetchall()[0][0]
        self.pointsList = pointsString.split('-')

    def endGame(self, winTeam): # winTeam = 1 or 2
        sportName = self.co.execute(f"SELECT Name FROM Sports WHERE Id = {self.sportId}").fetchall()[0][0]
        if sportName == "Tennis":
            self.co.execute(f"UPDATE Games SET ScoreT1 = '0' WHERE SportId = {self.sportId} AND Team1Id = {self.team1Id} AND Team2Id = {self.team2Id}")
            self.co.execute(f"UPDATE Games SET ScoreT2 = '0' WHERE SportId = {self.sportId} AND Team1Id = {self.team1Id} AND Team2Id = {self.team2Id}")

            sets = self.additionalInfosDisplay.text()
            sets = sets.split(" | ")
            currentSet = sets[-1].split('-')

            currentSet[winTeam-1] = int(currentSet[winTeam-1]) + 1
            currentSetWinTeam = int(currentSet[winTeam-1])

            sets[-1] = f"{currentSet[0]}-{currentSet[1]}"

            if currentSetWinTeam == 7:
                if len(sets) >= 6:
                    self.endSport()
                sets.append("0-0")

            setsText = ""
            for setI in sets:
                setsText += setI + " | "
            setsText = setsText[:len(setsText)-3]

            self.co.execute(f"UPDATE Games SET Infos = '{setsText}' WHERE SportId = {self.sportId} AND Team1Id = {self.team1Id} AND Team2Id = {self.team2Id}")
            self.updateAdditionalInfos()


    def endSport(self):
        self.addScoreT1Button.setEnabled(False)
        self.addScoreT2Button.setEnabled(False)
        self.substractScoreT1Button.setEnabled(False)
        self.substractScoreT2Button.setEnabled(False)

    def checkGame(self):
        sportName = self.co.execute(f"SELECT Name FROM Sports WHERE Id = {self.sportId}").fetchall()[0][0]
        if sportName == "Tennis":
            sets = self.additionalInfosDisplay.text()
            sets = sets.split(" | ")

            if len(sets) == 7:
                self.endSport()

    def doesGameExist(self):
        """
        Check if the game exist in the DB
        :return: None
        """
        game = self.co.execute(f"SELECT * FROM Games WHERE SportId = {self.sportId} AND Team1Id = {self.team1Id} AND Team2Id = {self.team2Id}").fetchall()

        sportName, pointIncrement = self.co.execute(f"SELECT Name, PointIncrement FROM Sports WHERE Id = {self.sportId}").fetchall()[0]
        scoreInnit = pointIncrement.split('-')[0]

        if sportName == "Tennis":
            infos = "0-0"
        else:
            infos = ""

        if game == []:
            self.co.execute(f"INSERT INTO Games(SportId, Team1Id, Team2Id, ScoreT1, ScoreT2, Infos)"
                            f"VALUES ({self.sportId}, {self.team1Id}, {self.team2Id}, {scoreInnit}, {scoreInnit}, '{infos}')")
        self.co.commit()

    def newGame(self):
        """
        Go to SportChoice window
        :return: None
        """
        mainWindow = self.parentWidget().parentWidget()
        mainWindow.previousSettings()

    def resetGame(self):
        sportName, pointIncrement = self.co.execute(f"SELECT Name, PointIncrement FROM Sports WHERE Id = {self.sportId}").fetchall()[0]
        scoreInnit = pointIncrement.split('-')[0]

        if sportName == "Tennis":
            infos = "0-0"
        else:
            infos = ""

        self.co.execute(f"UPDATE Games SET ScoreT1 = {scoreInnit}, ScoreT2 = {scoreInnit}, Infos = '{infos}' WHERE SportId = {self.sportId} AND Team1Id = {self.team1Id} AND Team2Id = {self.team2Id}")
        self.co.commit()
        self.updateScore()
        self.updateAdditionalInfos()

        self.addScoreT1Button.setEnabled(True)
        self.addScoreT2Button.setEnabled(True)
        self.substractScoreT1Button.setEnabled(True)
        self.substractScoreT2Button.setEnabled(True)

    def needEntryPoint(self):
        """
        Check if the sport need entries to add points.
        :return: None
        """
        sportName = self.co.execute(f"SELECT Name FROM Sports WHERE Id = {self.sportId}").fetchall()[0][0]
        if sportName == "Basketball" or sportName == "Field hockey" or sportName == "Handball" or sportName == "Volleyball":
            self.team1EntryNbOfPoints.setInputMask("9")
            self.team2EntryNbOfPoints.setInputMask("9")
        elif sportName != "Archery" and sportName != "Shooting":
            self.team1EntryNbOfPoints.setHidden(True)
            self.team2EntryNbOfPoints.setHidden(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GameScoreWidget((13, 1, 2))

    window.update()

    window.show()

    sys.exit(app.exec())
