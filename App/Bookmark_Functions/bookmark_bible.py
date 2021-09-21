from App.Bookmark_Functions.sqlite_bookmark_bible import *
from App.SQLite.sqlite_bible import *
import sqlite3
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc

# Code to show error, if the app crashes
import cgitb

cgitb.enable(format='text')

DB_LOCATION = r"Bible Database\bookmarked_verses.db"


class ShowBookMarks(Qtw.QWidget):
    def __init__(self, current_name, current_chapter, current_translation):
        super().__init__()

        # loading the application's UI {stored as XML format}
        uic.loadUi(r"UI\Bookmarks Function.ui", self)

        name = current_name
        chapter = current_chapter
        translation = current_translation

        # setting a window icon
        self.setWindowIcon(Qtg.QIcon(r"Images\Window Icons\bible_view_bookmark.png"))

        # setting the title frame to be clicked on and move the app with it
        self.title_frame.mouseMoveEvent = self.move_with_click_title_bar

        self.setWindowFlag(Qtc.Qt.FramelessWindowHint)
        self.show()  # show the UI
        self.showMaximized()  # loads the app in full-screen

        # Window Manipulation Buttons

        self.minimiseButton.clicked.connect(lambda: self.showMinimized())
        self.restoreButton.clicked.connect(lambda: self.change_window_size())
        self.closeButton.clicked.connect(lambda: self.close())

        self.load_data()  # calls the load data function to load bookmarked verses

        self.total_count = self.tableWidget.rowCount()  # getting the count of the total number of rows

        book_name = self.findChild(Qtw.QComboBox, "bookName")
        book_name.setCurrentIndex(name)
        self.update_chapter_list()  # Count chapters of the first book
        book_name.currentIndexChanged.connect(self.update_chapter_list)  # Automatically update chapter count

        chapter_number = self.findChild(Qtw.QComboBox, "chapterNumber")
        chapter_number.setCurrentIndex(chapter)
        self.update_verse_list()  # Count verses of the first chapter of the first book
        chapter_number.currentIndexChanged.connect(self.update_verse_list)  # Automatically update verse count

        verse_number = self.findChild(Qtw.QComboBox, "verseNumber")
        self.show_selected_verse()  # Show the selected verse text of the selected book, chapter and verse
        verse_number.currentIndexChanged.connect(self.show_selected_verse)  # Automatically display selected verse

        translation_name = self.findChild(Qtw.QComboBox, "translationName")
        translation_name.setCurrentIndex(translation)
        translation_name.currentIndexChanged.connect(self.show_selected_verse)  # Automatically update the verse based on translation selected

        # Add
        add = self.findChild(Qtw.QPushButton, "addButton")
        add.clicked.connect(self.bookmark_verses)

        # Delete
        delete = self.findChild(Qtw.QPushButton, "deleteButton")
        delete.clicked.connect(self.remove_data)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def move_with_click_title_bar(self, event):
        '''
        Function to move the app as the user clicks and drags on the title bar
        '''
        if event.buttons() == Qtc.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def change_window_size(self):

        if self.isMaximized():
            self.showNormal()

        else:
            self.showMaximized()

    def load_data(self):
        '''
        Function to first reset the column length then to load all of the verses stored in the bookmarked_verses database and finally
        resize individual rows according to their content
        '''

        # remove all the existing rows
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)

        # resizes the column length
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, Qtw.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, Qtw.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, Qtw.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, Qtw.QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, Qtw.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(5, Qtw.QHeaderView.ResizeToContents)

        # collects verses from db
        conn = sqlite3.connect(DB_LOCATION)

        cursor = conn.cursor()

        result = cursor.execute(f'''
                                    SELECT 
                                        ROW_NUMBER() OVER(ORDER BY verse_count),
                                        book_name, 
                                        book_chapter, 
                                        book_verse_number, 
                                        verse_bookmarked, 
                                        translation_name
                                    FROM 
                                        bookmarked_verses
                                ''')

        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)  # sets the 'nth' row

            for column_number, column_data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, Qtw.QTableWidgetItem(str(column_data)))  # set the respective data in each column of the row

        # resizes rows according to its content
        self.tableWidget.resizeRowsToContents()

    def bookmark_verses(self):
        '''
        Function to add the selected book name, chapter number, verse number, verse text and translation name to the bookmarked_database file
        '''

        # Book name
        book_name = self.bookName.currentText()

        # Chapter number
        chapter_number = self.chapterNumber.currentText()

        # Translation name
        translation_name = self.translationName.currentText()

        # Verse Number
        verse_number = self.verseNumber.currentText()

        # Verse Text
        verse_text = self.verseText.toPlainText()

        process_status = self.findChild(Qtw.QLabel, "status_text")

        try:
            add_bookmark_to_database(book_name, chapter_number, verse_number, verse_text, translation_name)
            process_status.setText("Added BookMark")
            process_status.setStyleSheet("color: green")

            self.load_data()

        except:
            process_status.setText("Failed to Add")
            process_status.setStyleSheet("color: red")

    def remove_data(self):
        '''
        Function to delete a verse from the bookmarked_verses database.
        '''

        if self.total_count > 0:  # allow to delete bookmarks only if the total count is more than 0

            try:
                conn = sqlite3.connect(DB_LOCATION)

                cursor = conn.cursor()

                # Pop-Up to select the row number to be deleted

                widget = Qtw.QWidget()

                # User inputs the row number to be deleted
                row_ID = Qtw.QInputDialog.getInt(widget, "Delete BookMark", "Select BookMark number: ", min=1, max=self.total_count)
                row_ID = row_ID[0]

                cursor.execute(f'''CREATE TEMP TABLE temp_ AS SELECT verse_count, ROW_NUMBER() OVER(ORDER BY verse_count) AS row_id FROM bookmarked_verses''')

                cursor.execute(f'''
                                   DELETE FROM bookmarked_verses 
                                   WHERE 
                                        verse_count IN (
                                                       SELECT verse_count 
                                                       FROM temp_ 
                                                       WHERE row_id = {row_ID}
                                                      )
                                        ''')

                conn.commit()
                conn.close()

            except:
                # if deleting the verse from the database fails
                self.status_text.setText("Failed To Delete")
                self.status_text.setStyleSheet("color: red")

            else:

                if self.total_count == 0:
                    # Deleting since count is now 0

                    conn = sqlite3.connect(DB_LOCATION)

                    cursor = conn.cursor()

                    cursor.execute(f'''DELETE FROM bookmarked_verses''')

                    conn.commit()
                    conn.close()

                self.load_data()

        else:
            self.status_text.setText("Nothing to delete")
            self.status_text.setStyleSheet("color: black")

    def update_chapter_list(self):
        '''
        Function to update the chapter combobox with different Bible books
        '''

        book_name = self.bookName.currentIndex()

        chapters_combo_box = self.findChild(Qtw.QComboBox, "chapterNumber")
        chapters_combo_box.clear()  # clear the current list

        # Variable to store the returned value from the chapter_list function
        chapters = chapter_list(book_name)

        chapters_combo_box.addItems([str(chapter[0]) for chapter in chapters])

        chapters_combo_box.setCurrentIndex(0)  # Updating index

    def update_verse_list(self):
        '''
        Function to update the verses combobox with different chapters
        '''

        book_name = self.bookName.currentIndex()
        chapter_number = self.chapterNumber.currentIndex()

        verses_combo_box = self.findChild(Qtw.QComboBox, "verseNumber")
        verses_combo_box.clear()  # clear the current list

        # Variable to store the returned value from the verse_list function
        verses = verse_list(book_name, chapter_number)

        verses_combo_box.addItems([str(verse[0]) for verse in verses])

        verses_combo_box.setCurrentIndex(0)  # Updating index

    def show_selected_verse(self):
        '''
        Function to show the currently set verse as per provided book name, chapter number and verse number
        '''

        book_name = self.bookName.currentIndex()
        chapter_number = self.chapterNumber.currentIndex()
        verse_number = self.verseNumber.currentIndex()
        translation_name = self.translationName.currentText()

        # Variable to store the returned value from from the select_verse function
        selected_verse = select_verse(book_name, chapter_number, verse_number, translation_name)

        try:
            self.verseText.setText(selected_verse[0][0])
        except IndexError:
            pass


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    show_bookmarks = ShowBookMarks()
    sys.exit(app.exec())
