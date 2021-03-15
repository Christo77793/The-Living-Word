import sys
import random
import time
from sqlite_bible import *
from PyQt5 import uic
from PyQt5 import QtWidgets as Qtw
from PyQt5 import QtGui as Qtg
from PyQt5 import QtCore as Qtc

import cgitb

cgitb.enable(format='text')


class MainWindow(Qtw.QMainWindow):
    # class MainWindow(qtw.QWidget):
    stop_signal = Qtc.pyqtSignal()

    # docs
    def __init__(self):
        super().__init__()  # avoid code redundancy

        # loading the application's UI {stored as XML format}
        # uic.loadUi(r"UI\Test.ui", self)
        uic.loadUi(r"UI\Bible Design.ui", self)

        # setting a window icon
        self.setWindowIcon(Qtg.QIcon(r"Images\logo.png"))
        self.show()

        books_list = self.findChild(Qtw.QComboBox, "Book")  # instance of combo_box Book
        books_list_index = books_list.currentIndex()

        books_list.currentIndexChanged.connect(self.update_chapter_list)
        self.update_chapter_list(books_list_index)

        set_verses = self.findChild(Qtw.QPushButton, "showVerses")
        set_verses.clicked.connect(self.display_verses)

        about_project = self.findChild(Qtw.QAction, "about_project")
        about_project.triggered.connect(lambda: self.show_messagebox(1))

        about_technology = self.findChild(Qtw.QAction, "about_technology")
        about_technology.triggered.connect(lambda: self.show_messagebox(2))

        prev_chapter = self.findChild(Qtw.QPushButton, "prevChapter")
        prev_chapter.clicked.connect(self.previous_chapter)

        # if books_list_index == 0 and chapter_index == 0:
        #     prev_chapter.setEnabled(False)
        # else:
        #     prev_chapter.setEnabled(True)

        next_chapter = self.findChild(Qtw.QPushButton, "nextChapter")
        next_chapter.clicked.connect(self.next_chapter)

        # promises_traverse = random.randint(0, (len(bible_promises) - 1))
        # promises_traverse = 0

        promises_instance = self.p_instance = MyThread()
        promises_instance.start()
        promises_instance.bible_promise.connect(self.bible_promise_function)

        # verses_label = self.findChild(Qtw.QLabel, "versesLabel")
        # verses_label.installEventFilter(self)

        # self.verses_label = self.findChild(Qtw.QLabel, "versesLabel")
        # self.verses_label.installEventFilter(self)

    # def eventFilter(self, source, event):
    #
    #     if event.type() == Qtc.QEvent.ContextMenu and source is self.verses_label:
    #
    #         test = Qtw.QMenu(self)
    #
    #         test.addAction("Highlight")
    #
    #         if test.exec_(event.globalPos()):
    #             item = source.itemAt(event.pos())
    #             print(item.text())
    #
    #         return True
    #
    #     return super().eventFilter(source, event)

    def display_verses(self):
        book = self.findChild(Qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        chapter = self.findChild(Qtw.QComboBox, "Chapter")
        selected_chapter = chapter.currentText()

        translation = self.findChild(Qtw.QComboBox, "Translation")
        selected_translation = translation.currentText()

        verses = show_verses(selected_book, selected_chapter, selected_translation)

        verses_label = self.findChild(Qtw.QLabel, "versesLabel")
        display_verse = ""

        for verse_list in verses:
            display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br /><br />"
            verses_label.setText(display_verse)

    def next_chapter(self):

        book = self.findChild(Qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        translation = self.findChild(Qtw.QComboBox, "Translation")
        selected_translation = translation.currentText()

        chapter = self.findChild(Qtw.QComboBox, "Chapter")
        selected_chapter = str(int(chapter.currentText()))

        if selected_book == 65 and selected_chapter == "22":
            pass

        else:
            selected_chapter = str(int(chapter.currentText()) + 1)

            count_chapter = chapter.count()

            if int(selected_chapter) <= int(count_chapter):
                verses = show_verses(selected_book, selected_chapter, selected_translation)
            else:
                selected_book += 1
                selected_chapter = "1"
                verses = show_verses(selected_book, selected_chapter, selected_translation)
                book.setCurrentIndex(selected_book)

            verses_label = self.findChild(Qtw.QLabel, "versesLabel")
            display_verse = ""
            for verse_list in verses:
                display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br /><br />"
                verses_label.setText(display_verse)

            updated_chapter_index = chapter.findText(selected_chapter, Qtc.Qt.MatchFixedString)
            chapter.setCurrentIndex(updated_chapter_index)

    def previous_chapter(self):
        book = self.findChild(Qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        translation = self.findChild(Qtw.QComboBox, "Translation")
        selected_translation = translation.currentText()

        chapter = self.findChild(Qtw.QComboBox, "Chapter")
        selected_chapter = str(int(chapter.currentText()))

        if selected_book == 0 and selected_chapter == "1":
            pass

        else:
            selected_chapter = str(int(chapter.currentText()) - 1)

            if int(selected_chapter) > 0:

                verses = show_verses(selected_book, selected_chapter, selected_translation)

                verses_label = self.findChild(Qtw.QLabel, "versesLabel")
                display_verse = ""
                for verse_list in verses:
                    display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br /><br />"
                    verses_label.setText(display_verse)

                updated_index = chapter.findText(selected_chapter, Qtc.Qt.MatchFixedString)
                chapter.setCurrentIndex(updated_index)

            else:

                selected_book -= 1
                prev_chapter = str(len(chapter_list(selected_book)))
                selected_chapter = prev_chapter
                verses = show_verses(selected_book, selected_chapter, selected_translation)

                verses_label = self.findChild(Qtw.QLabel, "versesLabel")
                display_verse = ""

                for verse_list in verses:
                    display_verse += f"<b style='font-size: large'>{verse_list[3]}:</b> {verse_list[4]}<br /><br />"
                    verses_label.setText(display_verse)

                book.setCurrentIndex(selected_book)
                chapter.setCurrentIndex(int(prev_chapter) - 1)

    def update_chapter_list(self, book_name):
        chapters_combo_box = self.findChild(Qtw.QComboBox, "Chapter")
        chapters_combo_box.clear()

        chapters = chapter_list(book_name)

        for chapter in chapters:
            chapters_combo_box.addItem(str(chapter[0]))

        chapters_combo_box.setCurrentIndex(0)

    def bible_promise_function(self, verse):
        bible_promise_label = self.findChild(Qtw.QLabel, "bible_promise_text")
        bible_promise_label.setText(verse)

    def show_messagebox(self, num):
        title = ""
        text = ""

        if num == 1:
            text = "This is my final project for my 6th semester in Computer Applications. - Christopher J.S."
            title = "Project"
        elif num == 2:
            text = "Technology used is Python 3.9, framework used PyQT5, IDE used PyCharm"
            title = "Technology"

        message_ = Qtw.QMessageBox()
        message_.setWindowTitle(title)
        message_.setText(text)

        x = message_.exec()
        print(x)

    def closeEvent(self, event):
        promises_instance = self.p_instance = MyThread()
        self.stop_signal.connect(promises_instance.stop)


class MyThread(Qtc.QThread):
    bible_promise = Qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.continue_loop = True

    def run(self):
        previous_promise = ""
        while self.continue_loop:
            current_promise_shown = self.show_bible_promise()

            if current_promise_shown == previous_promise:
                continue

            previous_promise = current_promise_shown

            self.bible_promise.emit(current_promise_shown)
            # time.sleep(120)
            time.sleep(2)

    def show_bible_promise(self):
        verse = ""

        promises_number = random.randint(0, (len(bible_promises) - 1))

        b_promise = bible_promises[promises_number]

        for book_index in book_list:
            if b_promise[0] == book_index[1]:
                book_name = book_index[1]
                verse = daily_verses(book_index[0], b_promise[1], b_promise[2])[0][4] + f"<i> - {book_name} {b_promise[1]}:{b_promise[2]} <i/>"

        return verse

    def stop(self):
        self.continue_run = False


# object of QApplication represents the state of our apps
# tt takes a list of command line arguments
# app = QtWidgets.QApplication([])


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
