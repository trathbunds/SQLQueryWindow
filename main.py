
import sys

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QPushButton, QTableView, QTextEdit, \
    QVBoxLayout, QWidget, QFileDialog, QAbstractItemView
import sqlite3



class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setup_ui()
        self.activateWindow()
        self.show()

    def setup_ui(self):
        #SQLlite3 Connection
        #self.connection_name_label = QLabel('Connection Name')
        #self.connection_textbox = QLineEdit()
        self.connection_button = QPushButton('Connect')
        self.connection_button.clicked.connect(self.connect_to_db)

        #Query Tabel
        self.query_table = QTableView()
        self.table_viewModel = QStandardItemModel()
        self.query_table.setModel(self.table_viewModel)
        self.query_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        #Run Queries
        self.query_textbox = QTextEdit()
        self.query_run = QPushButton('Run Query')
        self.query_reset = QPushButton('Reset Query')
        self.query_run.clicked.connect(self.run_query)
        self.query_reset.clicked.connect(self.reset_query)

        #Layout
        self.layout = QVBoxLayout()
        #self.layout.addWidget(self.connection_name_label)
        #self.layout.addWidget(self.connection_textbox)
        self.layout.addWidget(self.connection_button)
        self.layout.addWidget(self.query_table)
        self.layout.addWidget(self.query_textbox)
        self.layout.addWidget(self.query_run)
        self.layout.addWidget(self.query_reset)
        self.setLayout(self.layout)

    def connect_to_db(self):
        self.database_name = QFileDialog.getOpenFileName(self,'Open Database','c:\\',"Database (*.db)")
        connection_name = self.database_name
        #self.db = "{}.db".format(connection_name)
        print(self.database_name[0])
        self.db_connection = sqlite3.connect(self.database_name[0])

    def run_query(self):
        query = self.query_textbox.toPlainText()
        #self.db_connection.execute(query)
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        #print(cursor.fetchall())

        headers = list(map(lambda x: x[0], cursor.description))
        #self.query_table.setHorizontalHeader(headers)
        data = cursor.fetchall()
        print(f'Data:\n{data}')
        self.table_viewModel.clear()

        self.table_viewModel.setHorizontalHeaderLabels(headers)
        for rowIdx, row in enumerate(data):
            print(f'Row:\n{row}')
            print(enumerate(row))
            for (col, val,) in enumerate(row):
                newItem = QStandardItem(self.list_to_str(val))
                self.table_viewModel.setItem(rowIdx, col, newItem)

            #SELECT name FROM sqlite_master WHERE type='table'

        #self.query_table.setModel(cursor.fetchall())

        self.query_table.model().layoutChanged.emit()
        self.query_table.sortByColumn(0, Qt.AscendingOrder)

    def list_to_str(self, lst):
        if type(lst) is list:  # apply conversion to list columns
            return "||".join(lst)
        elif lst is None:
            return ""
        else:
            return str(lst)

    def reset_query(self):
        self.query_textbox.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mWindow = MainWindow()
    sys.exit(app.exec_())

#Window
#Textbox = Connection Name
#Button = Connect

#QTableView
#Textbox = Query
#Button = Run
#Button = Reset
