from bookmark_verses_bible import *
from sqlite_bible import *
import sys
import os
from PyQt5 import uic
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc

# Code to show error, if the app crashes
import cgitb

cgitb.enable(format='text')


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit
class BookMarkPopUp(Qtw.QMainWindow):
    def __init__(self, name, chapter, translation):
        super().__init__()  # avoid code redundancy

        uic.loadUi(r"UI\BookMark Popup.ui", self)

        # setting a window icon
        self.setWindowIcon(Qtg.QIcon(r"Images\Window Icons\bible_bookmark.png"))

        self.show()  # show the UI

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

        add_bookmark = self.findChild(Qtw.QPushButton, "addBookMark")
        add_bookmark.clicked.connect(self.bookmark_verses)

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

        process_status = self.findChild(Qtw.QLabel, "processStatus")

        try:
            add_bookmark_to_database(book_name, chapter_number, verse_number, verse_text, translation_name)
            process_status.setText("Added BookMark")
            process_status.setStyleSheet("color: green")

        except:
            process_status.setText("Failed to Add")
            process_status.setStyleSheet("color: red")

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
        Function to update the chapter combobox with different Bible books
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
        Function to update the chapter combobox with different Bible books
        '''

        book_name = self.bookName.currentIndex()
        chapter_number = self.chapterNumber.currentIndex()
        verse_number = self.verseNumber.currentIndex()

        selected_verse = select_verse(book_name, chapter_number, verse_number)

        self.verseText.setText(selected_verse[0][0])



if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    bookmark_window = BookMarkPopUp()
    sys.exit(app.exec())
