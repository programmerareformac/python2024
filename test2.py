import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
import sqlite3


class TextDatabaseApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle('Text Saver & Loader')
        self.setGeometry(300, 300, 400, 300)

        # Set up the text area
        self.text_area = QTextEdit(self)

        # Set up the buttons
        self.save_button = QPushButton('Save', self)
        self.load_button = QPushButton('Load', self)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
        self.setLayout(layout)

        # Connect buttons to their respective methods
        self.save_button.clicked.connect(self.save_text)
        self.load_button.clicked.connect(self.load_text)

        # Initialize database
        self.init_db()

    def init_db(self):
        # Connect to SQLite database or create it
        self.conn = sqlite3.connect('text_storage.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT
            )
        ''')
        self.conn.commit()

    def save_text(self):
        text_content = self.text_area.toPlainText()
        self.cursor.execute('INSERT INTO texts (content) VALUES (?)', (text_content,))
        self.conn.commit()
        QMessageBox.information(self, "Saved", "Text has been saved successfully!")

    def load_text(self):
        self.cursor.execute('SELECT content FROM texts ORDER BY id DESC LIMIT 1')
        result = self.cursor.fetchone()

        if result:
            self.text_area.setPlainText(result[0])
            QMessageBox.information(self, "Loaded", "Text has been loaded successfully!")
        else:
            QMessageBox.warning(self, "Error", "No text found in the database!")

    def closeEvent(self, event):
        # Close database connection on application exit
        self.conn.close()


# Main part of the application to run
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextDatabaseApp()
    window.show()  # This line is essential to display the window
    sys.exit(app.exec_())  # This starts the application's event loop
