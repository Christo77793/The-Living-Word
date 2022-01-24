from App.Search_Function.sqlite_search_verses_bible import *
from App.SQLite.sqlite_bible import *
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc

# Code to show error, if the app crashes
import cgitb

cgitb.enable(format='text')


class SearchVerses(Qtw.QWidget):
    def __init__(self):
        super().__init__()

        # loading the application's UI {stored as XML format}
        uic.loadUi(r"UI\Search Function.ui", self)

        # setting a window icon
        self.setWindowIcon(Qtg.QIcon(r"Images\Window Icons\bible_search_verses.png"))

        # setting the title frame to be clicked on and move the app with it
        self.title_frame.mouseMoveEvent = self.move_with_click_title_bar

        self.setWindowFlag(Qtc.Qt.FramelessWindowHint)  # removes standard title
        self.show()  # show the UI

        # Window Manipulation Buttons

        self.minimiseButton.clicked.connect(lambda: self.showMinimized())
        self.restoreButton.clicked.connect(lambda: self.change_window_size())
        self.closeButton.clicked.connect(lambda: self.close())

        # Setting search results as nothing

        self.versesReturned.setText("")

        # Search verses

        self.searchButton.clicked.connect(self.search_verses)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qtc.Qt.LeftButton:
            self.change_window_size()

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
            self.restoreButton.setIcon(Qtg.QIcon(r"Images\Buttons\restore.png"))
        else:
            self.showMaximized()
            self.restoreButton.setIcon(Qtg.QIcon(r"Images\Buttons\window.png"))

    def search_verses(self):

        if self.userInput.text() == "" or self.userInput.text().isspace():
            pass
            print("Nothing")

        else:
            user_input = self.userInput.text()

            number_of_verses, verses = find_verses(user_input)

            temp_counter = 1
            temp_verses = ""

            for verse in verses:

                main_string = verse[4]
                text1 = "<mark style='background-color: #3775f4'>"
                text2 = "</mark>"

                temp_string = main_string.lower()
                temp_input = user_input.lower()
                index = temp_string.index(temp_input)

                final_string = main_string[:index] + text1 + main_string[index: index + len(user_input)] + text2 + main_string[index + len(user_input):]

                for book_name in book_list:
                    if verse[1] == book_name[0]:

                        if temp_counter == number_of_verses:
                            temp_verses += f"{temp_counter}. {book_name[1]} {verse[2]}:{verse[3]} - {final_string}"
                            print("Reached Last Line")

                        else:
                            temp_verses += f"{temp_counter}. {book_name[1]} {verse[2]}:{verse[3]} - {final_string}<br /><br />"
                            temp_counter += 1

            self.versesReturnedCount.setText(f"Count: {number_of_verses}")
            self.versesReturned.setText(temp_verses)


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    show_bookmarks = SearchVerses()
    sys.exit(app.exec())
