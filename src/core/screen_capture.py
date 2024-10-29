from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QRect
from PIL import ImageGrab
import sys
import os

class ScreenCaptureOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setGeometry(QApplication.primaryScreen().geometry())
        self.setWindowOpacity(0.3)  # Reduced opacity to see original colors better
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")  # Semi-transparent background
        self.show()

        self.start_pos = None
        self.end_pos = None
        self.capturing = False
        self.screenshot_count = self.get_screenshot_count()
        self.parent_widget = None

    def get_screenshot_count(self):
        count = 0
        while os.path.exists(f'images/captured_image_{count}.png'):
            count += 1
        return count

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.pos()
            self.capturing = True

    def mouseMoveEvent(self, event):
        if self.capturing:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.capturing:
            self.capturing = False
            self.capture_screen()
            self.hide()  # Hide instead of close

    def paintEvent(self, event):
        if self.capturing and self.start_pos and self.end_pos:
            painter = QPainter(self)
            pen = QPen(QColor(255, 255, 255), 2)
            painter.setPen(pen)
            rect = QRect(self.start_pos, self.end_pos).normalized()
            painter.drawRect(rect)

    def capture_screen(self):
        if self.start_pos and self.end_pos:
            # Make the overlay fully transparent before capture
            self.setWindowOpacity(0)
            self.repaint()
            
            # Add small delay to ensure opacity change is applied
            QApplication.processEvents()
            
            rect = QRect(self.start_pos, self.end_pos).normalized()
            screenshot = ImageGrab.grab(bbox=(rect.x(), rect.y(), rect.right(), rect.bottom()))
            
            # Ensure the images directory exists
            os.makedirs('images', exist_ok=True)
            
            screenshot.save(f'images/captured_image_{self.screenshot_count}.png')
            print(f"Screen captured and saved as 'captured_image_{self.screenshot_count}.png'")
            self.screenshot_count += 1
            
            # Restore overlay opacity
            self.setWindowOpacity(0.3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = ScreenCaptureOverlay()
    app.exec()