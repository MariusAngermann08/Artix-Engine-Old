from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

app = QApplication([])  # Create the application

file_path = 'documentation.pdf'  # Replace with the actual path to your PDF file

# Open the PDF file in a window
QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

app.exec()  # Start the application event loop
