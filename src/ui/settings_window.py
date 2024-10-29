from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QApplication, QCheckBox, QComboBox
from src.config.settings import SettingsManager
import os

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager(os.path.join('data', 'settings.json'))
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Settings')
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.api_key_label = QLabel('OpenAI API Key:')
        self.api_key_input = QLineEdit()
        self.api_key_input.setText(self.settings_manager.get_setting('api_keys', {}).get('openai', ''))
        layout.addWidget(self.api_key_label)
        layout.addWidget(self.api_key_input)

        self.history_limit_label = QLabel('History Limit:')
        self.history_limit_input = QLineEdit()
        self.history_limit_input.setText(str(self.settings_manager.get_setting('history_limit', 15)))
        layout.addWidget(self.history_limit_label)
        layout.addWidget(self.history_limit_input)

        self.startup_enabled_label = QLabel('Startup Enabled:')
        self.startup_enabled_checkbox = QCheckBox()
        self.startup_enabled_checkbox.setChecked(self.settings_manager.get_setting('startup_enabled', True))
        layout.addWidget(self.startup_enabled_label)
        layout.addWidget(self.startup_enabled_checkbox)

        self.theme_label = QLabel('Theme:')
        self.theme_combobox = QComboBox()
        self.theme_combobox.addItems(['light', 'dark'])
        self.theme_combobox.setCurrentText(self.settings_manager.get_setting('theme', 'light'))
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combobox)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_settings(self):
        self.settings_manager.set_setting('api_keys', {'openai': self.api_key_input.text()})
        self.settings_manager.set_setting('history_limit', int(self.history_limit_input.text()))
        self.settings_manager.set_setting('startup_enabled', self.startup_enabled_checkbox.isChecked())
        self.settings_manager.set_setting('theme', self.theme_combobox.currentText())
        self.hide()  # Hide the window instead of closing it

if __name__ == "__main__":
    app = QApplication([])
    window = SettingsWindow()
    window.show()
    app.exec()
