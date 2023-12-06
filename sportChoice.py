import sqlite3
from PySide6 import QtCore, QtWidgets

class SportChoiceWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Properties
        self.width = 400
        self.height = 600
        self.setFixedSize(self.width, self.height)

        # list of buttons
        self.createSportsList()

        # First VBox (main)
        self.layout = QtWidgets.QVBoxLayout(self)

        # text/title fo widget (in first vbox)
        self.text = QtWidgets.QLabel("Choisissez un sport : ")
        self.layout.addWidget(self.text, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # ScrollBox
        self.scrollBox = QtWidgets.QScrollArea(self)
        self.layout.addWidget(self.scrollBox)

        self.scrollBox.setWidgetResizable(True)

        # Buttons vbox
        self.buttonLayout = QtWidgets.QVBoxLayout()

        # Buttons widget with vbox in it
        self.buttonWidget = QtWidgets.QWidget()
        self.buttonWidget.setLayout(self.buttonLayout)
        self.scrollBox.setWidget(self.buttonWidget)

        # 'Continue' Button
        self.continueButton = QtWidgets.QPushButton("Continuer")
        self.layout.addWidget(self.continueButton)

        self.continueButton.setDisabled(True)
        self.continueButton.clicked.connect(self.sendChoice)

        # Used for choice display
        self.previousChoice = None

        # Adding buttons to vbox
        for button in self.sports:
            button.setFixedHeight(30)
            self.buttonLayout.addWidget(button)
            button.clicked.connect(self.choice)


    # Create th sports list using SQL db
    def createSportsList(self):
        # SQL connection
        self.co = sqlite3.connect("JOs.db")

        # List of sports name
        namesList = self.co.execute("SELECT Name FROM Sports")

        self.sports = []
        for name in namesList:
            print(name)
            self.sports.append(QtWidgets.QPushButton(name[0]))


    # Sport choice
    def choice(self):
        if (self.previousChoice is not None):
            self.previousChoice.setStyleSheet("QPushButton {background-color: white;}")
        else:
            self.continueButton.setDisabled(False)

        button = self.sender()
        button.setStyleSheet("QPushButton {background-color: blue;}")

        self.previousChoice = button


    # Send choice to DB
    def sendChoice(self):
        sportId = self.co.execute(f"SELECT Id FROM Sports WHERE Name = '{self.previousChoice.text()}'").fetchall()

        mainWindow = self.parentWidget().parentWidget()
        mainWindow.choseSport(int(sportId[0][0]))