"""
EIOS Desktop Application
Release 19.2
"""

from desktop.main_window import MainWindow


class DesktopApplication:

    def __init__(self, dossier):

        self.dossier = dossier
        self.window = MainWindow(self.dossier)

    def run(self):

        self.window.run()


def launch(dossier):

    app = DesktopApplication(dossier)
    app.run()


if __name__ == "__main__":

    print("Please launch EIOS from main.py")