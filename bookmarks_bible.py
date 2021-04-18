# from bible import MainWindow
from bookmark_popup_bible import *
import sqlite3
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc

# Code to show error, if the app crashes
import cgitb

cgitb.enable(format='text')


# main_app_object = MainWindow()  # an object of the MainWindow class


class ShowBookMarks(Qtw.QMainWindow):
    def __init__(self, current_name, current_chapter, current_translation):
        super().__init__()

        # loading the application's UI {stored as XML format}
        uic.loadUi(r"UI\View BookMarks.ui", self)

        name = current_name
        chapter = current_chapter
        translation = current_translation

        # setting a window icon
        self.setWindowIcon(Qtg.QIcon(r"Images\Window Icons\bible_view_bookmark.png"))

        self.show()  # show the UI

        self.load_data()  # calls the load data function to load bookmarked verses

        self.total_count = self.tableWidget.rowCount()  # getting the count of the total number of rows

        # Add
        add = self.findChild(Qtw.QPushButton, "addButton")
        add.clicked.connect(lambda: self.bookmark_popup(name, chapter, translation))

        # Delete
        delete = self.findChild(Qtw.QPushButton, "deleteButton")
        delete.clicked.connect(self.remove_data)

    def load_data(self):
        '''
        Function to load all of the verses stored in the bookmarked_verses database.
        '''

        conn = sqlite3.connect(r"Bible Database\bookmarked_verses.db")

        cursor = conn.cursor()

        sql_command = "SELECT * FROM bookmarked_verses"

        result = cursor.execute(f'''{sql_command}''')

        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)  # sets the 'nth' row

            for column_number, column_data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, Qtw.QTableWidgetItem(str(column_data)))  # set the respective data in each column of the row

    def bookmark_popup(self, selected_book, selected_chapter, selected_translation):
        '''
        Function to show a pop-up that adds the bookmark. Values are passed to the __init__ method of the BookMarkPop class.
        '''

        self.bookmark_pop_ui = BookMarkPopUp(selected_book, selected_chapter, selected_translation)

    def remove_data(self):
        '''
        Function to delete a verse from the bookmarked_verses database.
        '''

        if self.total_count > 0:  # allow to delete bookmarks only if the total count is more than 0

            try:
                conn = sqlite3.connect(r"Bible Database\bookmarked_verses.db")

                cursor = conn.cursor()

                # Pop-Up to select the row number to be deleted

                widget = Qtw.QWidget()

                # User inputs the row number to be deleted
                row_ID = Qtw.QInputDialog.getInt(widget, "Delete BookMark", "Select BookMark number: ", min=1, max=self.total_count)
                row_ID = row_ID[0]

                cursor.execute(f'''DELETE FROM bookmarked_verses WHERE ROWID = {row_ID}''')

                conn.commit()
                conn.close()

            except:
                # if deleting the verse from the database fails
                self.deletionStatus.setText("Failed To Delete")

            else:
                self.tableWidget.removeRow(row_ID - 1)  # removes the deleted row from the QTableWidget
                self.total_count = self.tableWidget.rowCount()
                # self.deletionStatus.setText("Deleted")

        else:
            self.deletionStatus.setText("Nothing to delete")


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    show_bookmarks = ShowBookMarks()
    sys.exit(app.exec())
