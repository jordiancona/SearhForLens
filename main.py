#!/usr/bin/env python3
import sys
import os

# Add root directory to python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from src.gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SearchForLens")
    app.setOrganizationName("GravitationalLensingTools")

    # Set Application & Window Icon
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.png")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)

    window = MainWindow()
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
