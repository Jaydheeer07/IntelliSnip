import unittest

from PyQt6.QtWidgets import QApplication

from src.ui.floating_chat_window import FloatingChatWindow


class TestFloatingChatWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication([])
        self.image_path = "images/captured_image_0.png"
        self.window = FloatingChatWindow(self.image_path)
        self.window.show()  # Ensure the window is visible

    def test_initial_state(self):
        self.assertTrue(self.window.isVisible())
        self.assertEqual(self.window.image_label.pixmap().isNull(), False)

    def test_send_message(self):
        self.window.input_area.setPlainText("Test Message")
        self.window.send_message()
        self.assertEqual(self.window.chat_area.toPlainText(), "Test Message")

    def test_clear_chat(self):
        self.window.chat_area.setPlainText("Test Message")
        self.window.clear_chat()
        self.assertEqual(self.window.chat_area.toPlainText(), "")

    def test_retry_capture(self):
        self.window.retry_requested.connect(lambda: self.assertTrue(True))
        self.window.retry_capture()
        self.assertFalse(self.window.isVisible())

    def test_close_window(self):
        self.window.window_closed.connect(lambda: self.assertTrue(True))
        self.window.close_window()
        self.assertFalse(self.window.isVisible())

    def tearDown(self):
        self.window.close()
        self.app.quit()


if __name__ == "__main__":
    unittest.main()
