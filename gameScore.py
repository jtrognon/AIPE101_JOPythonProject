import sqlite3, sys
from PySide6 import QtCore, QtWidgets, QtGui

class GameScoreWidget(QtWidgets.QWidget):
    def __init__(self, sportId):
        super().__init__()

        # Properties
        self.width = 1200
        self.height = 600
        self.setFixedSize(self.width, self.height)




if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = GameScoreWidget(1)

    window.update()

    window.show()

    sys.exit(app.exec())
