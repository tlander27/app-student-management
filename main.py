from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, \
    QWidget, QGridLayout, QLineEdit, QPushButton, \
    QMainWindow, QTableWidget, QTableWidgetItem, \
    QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3 as sql

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedSize(480, 380)
        # Create root menu options
        file_menu_item = self.menuBar().addMenu("&File")
        edit_menu_item = self.menuBar().addMenu("&Edit")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add submenu items and actions
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # Add edit items and actions
        edit_student_action = QAction("Search", self)
        edit_student_action.triggered.connect(self.search)
        edit_menu_item.addAction(edit_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Create table layout for data
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sql.connect("database.db")
        results = connection.execute("select * from students")
        # Avoid overwriting entries
        self.table.setRowCount(0)
        # Loop results to add to table widget
        for row_num, row_data in enumerate(results):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        search_dialog = SearchDialog()
        search_dialog.exec()

    def about(self):
        pass

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # Add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add courses combobox list
        self.course_name = QComboBox()
        courses = sorted(["Biology", "Software Engineering",
                   "Math", "Astronomy", "Physics"])
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton("Submit")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()

        connection = sql.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("insert into students (name, course, mobile) "
                       "values (?,?,?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()
        # self.close()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Search")
        self.setFixedSize(300, 100)

        layout = QVBoxLayout()

        # Add search widget
        self.search_string = QLineEdit()
        self.search_string.setPlaceholderText("Enter a student name")
        layout.addWidget(self.search_string)

        # Add search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search(self):
        search_str = self.search_string.text().title()
        connection = sql.connect("database.db")
        cursor = connection.cursor()
        query = "select * from students where name = ?"
        results = connection.execute(query, (search_str, ))
        rows = list(results)
        items = window.table.findItems(search_str, Qt.MatchFlag.MatchFixedString)

        for item in items:
            print(item)
            window.table.item(item.row(), 1).setSelected(True)


if __name__ == "__main__":
    # Initialize application window
    app = QApplication(sys.argv)
    window = MainWindow()
    # Initialize application loop
    window.show()
    window.load_data()
    sys.exit(app.exec())