from Notes import *
from Bookmark_Functions import *
from SQLite import *
import sys
import random
import time
from PyQt5 import uic
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc

# Code to show error, if the app crashes
import cgitb

cgitb.enable(format='text')


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit
class MainWindow(Qtw.QMainWindow):
    stop_signal = Qtc.pyqtSignal()

    def __init__(self):
        super().__init__()  # avoid code redundancy

        # loading the application's UI {stored as XML format}
        uic.loadUi(r"UI\Bible Design.ui", self)

        # setting a window icon
        self.setWindowIcon(Qtg.QIcon(r"Images\Window Icons\bible_main.png"))

        self.app_title.mouseMoveEvent = self.move_with_click_title_bar

        self.setWindowFlag(Qtc.Qt.FramelessWindowHint)
        self.show()  # show the UI
        self.showMaximized()  # loads the app in full-screen

        # Window Manipulation Buttons

        self.minimiseButton.clicked.connect(lambda: self.showMinimized())
        self.restoreButton.clicked.connect(lambda: self.change_window_size())
        self.closeButton.clicked.connect(lambda: self.close())

        # Toggle Menu Buttons

        # Menu
        menu = self.findChild(Qtw.QPushButton, "menuButton")
        menu.clicked.connect(self.change_menu_width)

        # Notes
        note_maker = self.findChild(Qtw.QPushButton, "notesButton")
        note_maker.clicked.connect(self.open_note_maker)

        # View BookMarks
        view_bookmarks = self.findChild(Qtw.QPushButton, "bookmarkButton")
        view_bookmarks.clicked.connect(self.open_view_bookmarks)

        # About
        about = self.findChild(Qtw.QPushButton, "aboutButton")
        about.clicked.connect(self.show_about_message)

        # Show promises
        self.p_instance = MyThread()  # creating thread instance
        self.p_instance.start()  # start thread
        self.p_instance.bible_promise.connect(self.bible_promise_function)  # emitting thread value

        # ComboBoxes

        # Books
        books_list = self.findChild(Qtw.QComboBox, "Book")
        self.update_chapter_list()  # Count chapter of the first book)
        books_list.currentIndexChanged.connect(self.update_chapter_list)  # Automatically update chapter count

        # Verses Functions

        # Show selected verses
        set_verses = self.findChild(Qtw.QPushButton, "showVerses")
        set_verses.clicked.connect(self.display_verses)

        # Show next chapter's verses
        prev_chapter = self.findChild(Qtw.QPushButton, "prevChapter")
        prev_chapter.clicked.connect(self.previous_chapter)

        # Show previous chapter's verses
        next_chapter = self.findChild(Qtw.QPushButton, "nextChapter")
        next_chapter.clicked.connect(self.next_chapter)

        # Displaying Verses

        # Setting a custom context menu
        verses_label = self.findChild(Qtw.QLabel, "versesLabel")  # instance of verses label
        verses_label.setContextMenuPolicy(Qtc.Qt.CustomContextMenu)
        verses_label.customContextMenuRequested.connect(self.verses_custom_context_menu)

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

    def change_menu_width(self):
        '''
        Function to expand and restore the toggle menu.
        '''

        toggle_frame_length = self.findChild(Qtw.QFrame, "side_menu_frame")
        toggle_width = toggle_frame_length.width()

        max_width = 156
        min_width = 68

        if toggle_width == min_width:
            # Expanding
            set_width_ = max_width

        else:
            # Restoring
            set_width_ = min_width

        menu_bar_frame = self.findChild(Qtw.QFrame, "side_menu_frame")

        self.animation = Qtc.QPropertyAnimation(menu_bar_frame, b"minimumWidth")
        self.animation.setDuration(300)  # duration in ms
        self.animation.setStartValue(toggle_width)  # from value
        self.animation.setEndValue(set_width_)  # to value
        self.animation.setEasingCurve(Qtc.QEasingCurve.InOutCubic)  # animation style of toggle
        self.animation.start()

    def open_note_maker(self):
        '''
        Function to open the note maker UI.
        '''

        self.note_ui = NotesWindow()

    def open_view_bookmarks(self):
        '''
        Function to open the view bookmarks UI.
        '''

        # Book name
        book = self.findChild(Qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        # Chapter number
        chapter = self.findChild(Qtw.QComboBox, "Chapter")
        selected_chapter = chapter.currentIndex()

        # Translation selected
        translation = self.findChild(Qtw.QComboBox, "Translation")
        selected_translation = translation.currentIndex()

        self.view_bookmark_ui = ShowBookMarks(selected_book, selected_chapter, selected_translation)

    def show_about_message(self):
        '''
        Function to show the about message to let users know why this project was made and with what.
        '''

        message_ = Qtw.QMessageBox()
        message_.setWindowTitle("About")
        message_.setWindowIcon(Qtg.QIcon(r"Images\Popup Icons\menu_about.png"))
        message_.setText("This is my final project for my 6th semester in Computer Applications. Technology used is Python 3.9, framework used PyQT5, IDE used PyCharm.")

        x = message_.exec()  # executes the function
        print(x)

    def display_verses(self):
        '''
        Function related to the 'Get Verses' button. Takes the book name, chapter number as well as the selected translation to display verses from the sqlite_bible file.
        '''

        # Book name
        book = self.findChild(Qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        # Chapter number
        chapter = self.findChild(Qtw.QComboBox, "Chapter")
        selected_chapter = chapter.currentText()

        # Translation selected
        translation = self.findChild(Qtw.QComboBox, "Translation")
        selected_translation = translation.currentText()

        # Variable to store the returned value from the show_verses function
        verses = show_verses(selected_book, selected_chapter, selected_translation)

        verses_label = self.findChild(Qtw.QLabel, "versesLabel")  # instance of verses label
        display_verse = ""

        for verse_list in verses:
            # verse_list iterates through the verses list
            if verse_list == verses[-1]:
                # removing extra break if it is the last verse
                display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br />"
                verses_label.setText(display_verse)
            else:
                display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br /><br />"
                verses_label.setText(display_verse)

    def next_chapter(self):
        '''
        Shows the verses of the next chapter.
        '''

        book = self.findChild(Qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        translation = self.findChild(Qtw.QComboBox, "Translation")
        selected_translation = translation.currentText()

        chapter = self.findChild(Qtw.QComboBox, "Chapter")
        selected_chapter = str(int(chapter.currentText()))

        if selected_book == 65 and selected_chapter == "22":
            pass
            # skip the function if it is the last book and chapter

        else:
            selected_chapter = str(int(chapter.currentText()) + 1)  # selecting next chapter

            count_chapter = chapter.count()  # gets chapter count

            if int(selected_chapter) <= int(count_chapter):
                # if more chapters in the selected book

                verses = show_verses(selected_book, selected_chapter, selected_translation)
            else:
                # if no more chapters in the selected book

                selected_book += 1  # select next book
                selected_chapter = "1"
                verses = show_verses(selected_book, selected_chapter, selected_translation)
                book.setCurrentIndex(selected_book)  # updating index

            verses_label = self.findChild(Qtw.QLabel, "versesLabel")
            display_verse = ""

            for verse_list in verses:
                if verse_list == verses[-1]:
                    # removing extra break if it is the last verse
                    display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br />"
                    verses_label.setText(display_verse)
                else:
                    display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br /><br />"
                    verses_label.setText(display_verse)

            # Updating ComboBoxes
            updated_chapter_index = chapter.findText(selected_chapter, Qtc.Qt.MatchFixedString)
            chapter.setCurrentIndex(updated_chapter_index)

    def previous_chapter(self):
        '''
        Shows the verses of the previous chapter.
        '''

        book = self.findChild(Qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        translation = self.findChild(Qtw.QComboBox, "Translation")
        selected_translation = translation.currentText()

        chapter = self.findChild(Qtw.QComboBox, "Chapter")
        selected_chapter = str(int(chapter.currentText()))

        if selected_book == 0 and selected_chapter == "1":
            pass
            # skip the function if it is the first book and chapter

        else:
            selected_chapter = str(int(chapter.currentText()) - 1)  # selecting previous chapter

            if int(selected_chapter) > 0:
                # if there exists preceding chapters in the selected book

                verses = show_verses(selected_book, selected_chapter, selected_translation)

                verses_label = self.findChild(Qtw.QLabel, "versesLabel")
                display_verse = ""
                for verse_list in verses:
                    if verse_list == verses[-1]:
                        # removing extra break if it is the last verse
                        display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br />"
                        verses_label.setText(display_verse)
                    else:
                        display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br /><br />"
                        verses_label.setText(display_verse)

                # Updating ComboBoxes
                updated_index = chapter.findText(selected_chapter, Qtc.Qt.MatchFixedString)
                chapter.setCurrentIndex(updated_index)

            else:
                # if first chapter in the selected book

                selected_book -= 1  # select previous book
                prev_chapter = str(len(chapter_list(selected_book)))
                selected_chapter = prev_chapter
                verses = show_verses(selected_book, selected_chapter, selected_translation)

                verses_label = self.findChild(Qtw.QLabel, "versesLabel")
                display_verse = ""

                for verse_list in verses:
                    if verse_list == verses[-1]:
                        # removing extra break if it is the last verse
                        display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br />"
                        verses_label.setText(display_verse)
                    else:
                        display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br /><br />"
                        verses_label.setText(display_verse)

                # Updating ComboBoxes
                book.setCurrentIndex(selected_book)
                chapter.setCurrentIndex(int(prev_chapter) - 1)

    def update_chapter_list(self):
        '''
        Function to update the chapter combobox with different Bible books.
        '''

        book_name = self.Book.currentIndex()  # index value of the book name

        chapters_combo_box = self.findChild(Qtw.QComboBox, "Chapter")
        chapters_combo_box.clear()  # clear the current list

        # Variable to store the returned value from the chapter_list function
        chapters = chapter_list(book_name)

        chapters_combo_box.addItems([str(chapter[0]) for chapter in chapters])  # Adding the chapters

        chapters_combo_box.setCurrentIndex(0)  # Updating index

    def bible_promise_function(self, verse):
        '''
        Function that takes the value from the QThread class to show a Biblical Promise.

        :parameter: verse -> Promise to show
        '''

        bible_promise_label = self.findChild(Qtw.QLabel, "bible_promise_text")
        bible_promise_label.setText(verse)

    def verses_custom_context_menu(self):
        '''
        Function that shows a custom context menu.
        '''

        # Context Menu
        context_menu_option = Qtw.QMenu()

        # BookMark
        bookmark_button = context_menu_option.addAction("BookMark")
        bookmark_button.triggered.connect(self.bookmark_popup)  # Execute bookmark function

        # Clear
        clear_text = '''<html>
                            <head/>
                            <body>
                                <p>Click on Get Verses to start viewing verses.<br/></p>
                                <p>Right Click to:</p><p>1. Add a BookMark</p>
                                <p>2. Clear the screen<br/></p>
                                <p>Shortcuts:</p>
                                <p>1. Enter : Get Verses</p>
                                <p>2. -&gt; : Next</p>
                                <p>3. &lt;- : Previous</p>
                            </body>
                        </html>'''

        clear_button = context_menu_option.addAction("Clear")  # Adding an option to clear text
        clear_button.triggered.connect(lambda: self.versesLabel.setText(clear_text))

        cursor = Qtg.QCursor()
        context_menu_option.exec_(cursor.pos())

    def bookmark_popup(self):
        '''
        Function to show a pop-up that adds the bookmark. Values are passed to the __init__ method of the BookMarkPop class.
        '''

        # Book name
        book = self.findChild(Qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        # Chapter number
        chapter = self.findChild(Qtw.QComboBox, "Chapter")
        selected_chapter = chapter.currentIndex()

        # Translation selected
        translation = self.findChild(Qtw.QComboBox, "Translation")
        selected_translation = translation.currentIndex()

        self.bookmark_ui = BookMarkPopUp(selected_book, selected_chapter, selected_translation)

    def closeEvent(self, event):
        '''
        Qt Class to end events when app closes.
        '''

        promises_instance = self.p_instance = MyThread()
        self.stop_signal.connect(promises_instance.stop)  # Stopping the Bible promise function when app ends


# noinspection PyMethodMayBeStatic
class MyThread(Qtc.QThread):
    bible_promise = Qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.continue_loop = True

    def run(self):
        previous_promise = ""

        while self.continue_loop:
            # While loop to be continued
            current_promise_shown = self.show_bible_promise()

            if current_promise_shown == previous_promise:
                continue
                # run again if the current promise is the same as the next promise

            previous_promise = current_promise_shown

            self.bible_promise.emit(current_promise_shown)  # Send current Bible Promise
            time.sleep(120)

    def show_bible_promise(self):
        '''
        Function to show current Bible Promise from the bible_promises variable in sqlite_bible.py
        '''

        verse = ""

        promises_number = random.randint(0, (len(bible_promises) - 1))  # getting a random verse

        b_promise = bible_promises[promises_number]

        for book_index in book_list:
            if b_promise[0] == book_index[1]:
                book_name = book_index[1]
                verse = daily_verses(book_index[0], b_promise[1], b_promise[2])[0][4] + f"<i> - {book_name} {b_promise[1]}:{b_promise[2]} <i/>"

        return verse

    def stop(self):
        # called when the app ends
        # noinspection PyAttributeOutsideInit
        self.continue_run = False


# object of QApplication represents the state of our apps
# tt takes a list of command line arguments
# app = QtWidgets.QApplication([])


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
