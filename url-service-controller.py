import sys
import requests
import pyperclip 
import validators  
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QHBoxLayout, QDialog, QProgressBar, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

class LoadingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading...")
        self.setFixedSize(250, 100)
        
        self.label = QLabel("Generating shortened URL...", self)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Create a progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Indeterminate mode
        self.progress_bar.setTextVisible(False)  # Hide text

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # Theme Selector (Radio Buttons)
        self.theme_label = QLabel("Select Theme:", self)
        layout.addWidget(self.theme_label)

        self.light_mode_radio = QRadioButton("Light Mode")
        self.dark_mode_radio = QRadioButton("Dark Mode")
        self.light_mode_radio.setChecked(True)  # Default selection
        
        # Group radio buttons
        self.theme_group = QButtonGroup(self)
        self.theme_group.addButton(self.light_mode_radio)
        self.theme_group.addButton(self.dark_mode_radio)

        layout.addWidget(self.light_mode_radio)
        layout.addWidget(self.dark_mode_radio)

        # Save and Apply Button
        self.save_button = QPushButton("Save and Apply", self)
        layout.addWidget(self.save_button)

        # Spacer for better alignment
        layout.addStretch()

        # Bottom acknowledgment section
        self.powered_label = QLabel('<a href="https://tinyurl.com/app/terms">Powered by: TinyURL</a>', self)
        self.powered_label.setOpenExternalLinks(True)  # Enable hyperlinking
        self.powered_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.powered_label)

        self.dev_label = QLabel('<a href="https://github.com/Nico-Darth">Developed by: Niels Coert</a>', self)
        self.dev_label.setOpenExternalLinks(True)  # Enable hyperlinking
        self.dev_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.dev_label)

        self.setLayout(layout)
        self.save_button.clicked.connect(self.apply_theme)

    def apply_theme(self):
        if self.light_mode_radio.isChecked():
            app.setStyleSheet("")  # Light mode (default style)
        elif self.dark_mode_radio.isChecked():
            app.setStyleSheet("QWidget { background-color: #2e2e2e; color: #ffffff; }")
        QMessageBox.information(self, "Settings", "Theme applied successfully!")


    def apply_theme(self):
        if self.light_mode_radio.isChecked():
            app.setStyleSheet("")  # Light mode (default style)
        elif self.dark_mode_radio.isChecked():
            app.setStyleSheet("QWidget { background-color: #2e2e2e; color: #ffffff; }")
        QMessageBox.information(self, "Settings", "Theme applied successfully!")

class UrlShortenerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('URL Shortener')
        self.setGeometry(300, 300, 400, 250)

        layout = QVBoxLayout()

        # Label for the input field
        self.label = QLabel('Enter URL to shorten:')
        layout.addWidget(self.label)

        self.url_input = QLineEdit(self)
        layout.addWidget(self.url_input)

        self.shorten_button = QPushButton('Shorten URL', self)
        self.shorten_button.clicked.connect(self.shorten_url)
        layout.addWidget(self.shorten_button)

        # Result layout
        self.result_layout = QHBoxLayout()
        self.result_label = QLabel('Shortened URL will appear here.')
        self.result_label.setOpenExternalLinks(True)  # Allow hyperlinking
        self.result_layout.addWidget(self.result_label)

        self.copy_button = QPushButton('Copy URL', self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.result_layout.addWidget(self.copy_button)

        layout.addLayout(self.result_layout)

        # Add Settings Button
        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def shorten_url(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, 'Input Error', 'Please enter a valid URL.')
            return

        # Validate the URL
        if not validators.url(url):
            QMessageBox.warning(self, 'Invalid URL', 'The URL entered is not valid. Please enter a valid URL.')
            return

        # Show loading dialog
        self.loading_dialog = LoadingDialog()
        self.loading_dialog.show()

        # Start a new thread for URL shortening
        self.thread = ShortenUrlThread(url)
        self.thread.finished.connect(self.on_url_shortened)
        self.thread.start()

    def on_url_shortened(self, shortened_url):
        # Store the shortened URL to display after the timer
        self.shortened_url = shortened_url

        # Start the timer for a minimum of 5 seconds
        QTimer.singleShot(5000, self.update_result_label)

    def update_result_label(self):
        self.loading_dialog.close()
        if self.shortened_url:
            self.result_label.setText(f'<a href="{self.shortened_url}">{self.shortened_url}</a>')
        else:
            QMessageBox.warning(self, 'Error', 'Failed to shorten URL. Please try again.')

    def copy_to_clipboard(self):
        shortened_url = self.result_label.text()
        if '<a href="' in shortened_url:
            # Extract the URL from the hyperlink
            start = shortened_url.find('"') + 1
            end = shortened_url.rfind('"')
            url = shortened_url[start:end]
            pyperclip.copy(url)
            QMessageBox.information(self, 'Copied', 'Shortened URL copied to clipboard!')
        else:
            QMessageBox.warning(self, 'Copy Error', 'No URL to copy.')

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.exec_()

class ShortenUrlThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run (self):
        try:
            response = requests.get(f'http://tinyurl.com/api-create.php?url={self.url}')
            if response.status_code == 200:
                shortened_url = response.text
                self.finished.emit(shortened_url)
            else:
                self.finished.emit(None)
        except Exception:
            self.finished.emit(None)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UrlShortenerApp()
    ex.show()
    sys.exit(app.exec_())
