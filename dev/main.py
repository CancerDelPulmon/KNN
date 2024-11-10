import sys
from PySide6.QtWidgets import QApplication

from model import Model
from view import View



class Main():
    def __init__(self):   
        self.app = QApplication(sys.argv)
        self.model = Model()
        self.view = View(self.model)

    def run (self):
        self.view.show()

        self.model.compactness() # pour test 
    


if __name__ == "__main__":
    main = Main()
    main.run()
    sys.exit(main.app.exec())