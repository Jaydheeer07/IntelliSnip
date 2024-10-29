from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class FloatingChatWindow(QWidget):
    # Define signals at class level
    retry_requested = pyqtSignal()
    window_closed = pyqtSignal()

    def __init__(self, image_path):  # Removed app_instance parameter
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setGeometry(100, 100, 400, 500)

        self.image_path = image_path
        self.dragging = False
        self.offset = None
        self.initUI()
        self.loadPosition()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.dragging and self.offset:
            new_pos = self.mapToGlobal(event.position().toPoint() - self.offset)
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def initUI(self):
        self.layout = QVBoxLayout()

        # Title bar
        self.title_bar = QWidget()
        self.title_layout = QHBoxLayout(self.title_bar)
        self.title_label = QLabel("IntelliSnip Chat")
        self.title_layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_bar)

        self.image_label = QLabel(self)
        self.image_label.setPixmap(
            QPixmap(self.image_path).scaled(
                400, 300, Qt.AspectRatioMode.KeepAspectRatio
            )
        )
        self.layout.addWidget(self.image_label)

        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)
        self.layout.addWidget(self.chat_area)

        self.input_area = QTextEdit(self)
        self.input_area.setMaximumHeight(50)
        self.layout.addWidget(self.input_area)

        self.button_layout = QHBoxLayout()
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_chat)
        self.retry_button = QPushButton("Retry", self)
        self.retry_button.clicked.connect(self.retry_capture)
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.clicked.connect(self.close_window)

        self.button_layout.addWidget(self.send_button)
        self.button_layout.addWidget(self.clear_button)
        self.button_layout.addWidget(self.retry_button)
        self.button_layout.addWidget(self.exit_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def retry_capture(self):
        self.hide()
        self.retry_requested.emit()  # Emit signal for retry

    def close_window(self):
        self.hide()
        self.window_closed.emit()  # Emit signal when window is closed

    def send_message(self):
        message = self.input_area.toPlainText()
        if message:
            self.chat_area.append(message)
            self.input_area.clear()

    def clear_chat(self):
        self.chat_area.clear()

    def savePosition(self):
        with open("chat_position.txt", "w") as f:
            f.write(f"{self.x()},{self.y()}")

    def loadPosition(self):
        try:
            with open("chat_position.txt", "r") as f:
                x, y = map(int, f.read().split(","))
                self.move(x, y)
        except FileNotFoundError:
            pass

    def moveEvent(self, event):
        self.savePosition()
        super().moveEvent(event)

    def resizeEvent(self, event):
        self.savePosition()
        super().resizeEvent(event)

    def closeEvent(self, event):
        self.savePosition()
        self.hide()
        event.ignore()
