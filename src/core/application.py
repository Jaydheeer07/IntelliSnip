import os
import sys

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from screen_capture import ScreenCaptureOverlay

from src.config.settings import SettingsManager
from src.ui.settings_window import SettingsWindow


class IntelliSnipApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.overlay = None
        self.settings_window = None
        self.initUI()
        self.load_settings()

    def initUI(self):
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon(os.path.join("resources", "icon.png")))
        self.tray_icon.setVisible(True)

        self.menu = QMenu()

        self.capture_action = QAction("Capture Screen", self)
        self.capture_action.triggered.connect(self.capture_screen)
        self.menu.addAction(self.capture_action)

        self.settings_action = QAction("Settings", self)
        self.settings_action.triggered.connect(self.open_settings)
        self.menu.addAction(self.settings_action)

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.quit)
        self.menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.menu)

    def load_settings(self):
        self.settings_manager = SettingsManager(os.path.join("data", "settings.json"))
        self.settings = self.settings_manager.settings

    def save_settings(self):
        self.settings_manager.save_settings()

    def capture_screen(self):
        if self.overlay is None or not self.overlay.isVisible():
            self.overlay = ScreenCaptureOverlay()
            self.overlay.show()

    def open_settings(self):
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = SettingsWindow()
            self.settings_window.show()

    def quit(self):
        self.save_settings()
        super().quit()


if __name__ == "__main__":
    app = IntelliSnipApp(sys.argv)
    sys.exit(app.exec())
