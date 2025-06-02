import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QComboBox, QStatusBar, QScrollArea, QDockWidget
)
from PyQt5.QtCore import Qt
from datetime import date


class BookManager(QWidget):
    def __init__(self):
        super().__init__()
        self.data = []
        self.id_counter = 1

        self.main_layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.genre_input = QComboBox()
        self.genre_input.addItems(["Fiksi", "Non-Fiksi", "Biografi", "Fantasi", "Sains", "Lainnya"])
        self.notes_input = QLineEdit()

        add_button = QPushButton("Simpan Buku")
        add_button.clicked.connect(self.add_book)

        form_layout.addWidget(QLabel("Judul Buku:"))
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(QLabel("Penulis:"))
        form_layout.addWidget(self.author_input)
        form_layout.addWidget(QLabel("Genre:"))
        form_layout.addWidget(self.genre_input)
        form_layout.addWidget(QLabel("Catatan:"))
        form_layout.addWidget(self.notes_input)
        form_layout.addWidget(add_button)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(form_widget)

        self.main_layout.addWidget(scroll_area)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Penulis", "Genre", "Catatan", "Tanggal"])
        self.main_layout.addWidget(self.table)

        self.setLayout(self.main_layout)

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        genre = self.genre_input.currentText()
        notes = self.notes_input.text()
        tanggal = date.today().isoformat()

        if title and author:
            self.data.append((self.id_counter, title, author, genre, notes, tanggal))
            self.id_counter += 1
            self.refresh_table()
            self.title_input.clear()
            self.author_input.clear()
            self.notes_input.clear()

    def refresh_table(self):
        self.table.setRowCount(len(self.data))
        for row, item in enumerate(self.data):
            for col, value in enumerate(item):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def search_book(self, text):
        for row in range(self.table.rowCount()):
            title_item = self.table.item(row, 1)
            if title_item:
                self.table.setRowHidden(row, text.lower() not in title_item.text().lower())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("– Manajemen Koleksi Buku– ")
        self.setGeometry(100, 100, 1000, 600)

        self.book_tab = BookManager()
        self.setCentralWidget(self.book_tab)

        status = QStatusBar()
        status.showMessage("Ni Putu Alvina Putri – F1D022017")
        self.setStatusBar(status)

        self.init_dock_search()

    def init_dock_search(self):
        self.search_dock = QDockWidget("Pencarian Buku", self)
        self.search_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik judul buku...")
        self.search_input.textChanged.connect(self.book_tab.search_book)

        self.search_dock.setWidget(self.search_input)
        self.search_dock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.search_dock)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
