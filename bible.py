import sys
import random
import time
from sqlite_bible import show_verses, chapter_list, daily_verses, book_list, bible_promises
from PyQt5 import uic
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):
    # class MainWindow(qtw.QWidget):
    stop_signal = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()  # avoid code redundancy

        # loading the application's UI {stored as XML format}
        # uic.loadUi(r"UI\Test.ui", self)
        uic.loadUi(r"UI\Bible Design.ui", self)

        # setting a window icon
        self.setWindowIcon(qtg.QIcon(r"Images\logo.png"))
        self.show()

        books_list = self.findChild(qtw.QComboBox, "Book")  # instance of combo_box Book
        books_list_index = books_list.currentIndex()

        books_list.currentIndexChanged.connect(self.update_chapter_list)
        self.update_chapter_list(books_list_index)

        set_verses = self.findChild(qtw.QPushButton, "showVerses")
        set_verses.clicked.connect(self.display_verses)

        prev_chapter = self.findChild(qtw.QPushButton, "prevChapter")
        prev_chapter.clicked.connect(self.previous_chapter)

        # if books_list_index == 0 and chapter_index == 0:
        #     prev_chapter.setEnabled(False)
        # else:
        #     prev_chapter.setEnabled(True)

        next_chapter = self.findChild(qtw.QPushButton, "nextChapter")
        next_chapter.clicked.connect(self.next_chapter)

        # promises_traverse = random.randint(0, (len(bible_promises) - 1))
        # promises_traverse = 0

        promises_instance = self.p_instance = MyThread()
        promises_instance.start()
        promises_instance.bible_promise.connect(self.bible_promise_function)

        # next_promise = self.findChild(qtw.QPushButton, "next_promise")
        # next_promise.clicked.connect(self.traverse_next_promise())

    def display_verses(self):
        book = self.findChild(qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        chapter = self.findChild(qtw.QComboBox, "Chapter")
        selected_chapter = chapter.currentText()

        translation = self.findChild(qtw.QComboBox, "Translation")
        selected_translation = translation.currentText()

        verses = show_verses(selected_book, selected_chapter, selected_translation)

        verses_label = self.findChild(qtw.QLabel, "versesLabel")
        display_verse = ""

        for verse_list in verses:
            display_verse += f"<u><b>Verse {verse_list[3]}:</b></u> {verse_list[4]}<br /><br />"
            verses_label.setText(display_verse)

    def next_chapter(self):

        book = self.findChild(qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        translation = self.findChild(qtw.QComboBox, "Translation")
        selected_translation = translation.currentText()

        chapter = self.findChild(qtw.QComboBox, "Chapter")
        selected_chapter = str(int(chapter.currentText()) + 1)

        count_chapter = chapter.count()

        if int(selected_chapter) <= int(count_chapter):
            verses = show_verses(selected_book, selected_chapter, selected_translation)
        else:
            selected_book += 1
            selected_chapter = "1"
            verses = show_verses(selected_book, selected_chapter, selected_translation)
            book.setCurrentIndex(selected_book)

        verses_label = self.findChild(qtw.QLabel, "versesLabel")
        display_verse = ""
        for verse_list in verses:
            display_verse += f"<u><b>Verse {verse_list[3]}:</b></u> {verse_list[4]}<br /><br />"
            verses_label.setText(display_verse)

        updated_chapter_index = chapter.findText(selected_chapter, qtc.Qt.MatchFixedString)
        chapter.setCurrentIndex(updated_chapter_index)

    def previous_chapter(self):
        book = self.findChild(qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        translation = self.findChild(qtw.QComboBox, "Translation")
        selected_translation = translation.currentText()

        chapter = self.findChild(qtw.QComboBox, "Chapter")
        selected_chapter = str(int(chapter.currentText()) - 1)

        if int(selected_chapter) > 0:

            verses = show_verses(selected_book, selected_chapter, selected_translation)

            verses_label = self.findChild(qtw.QLabel, "versesLabel")
            display_verse = ""
            for verse_list in verses:
                display_verse += f"<u><b>Verse {verse_list[3]}:</b></u> {verse_list[4]}<br /><br />"
                verses_label.setText(display_verse)

            updated_index = chapter.findText(selected_chapter, qtc.Qt.MatchFixedString)
            chapter.setCurrentIndex(updated_index)

        else:

            selected_book -= 1
            prev_chapter = str(len(chapter_list(selected_book)))
            selected_chapter = prev_chapter
            verses = show_verses(selected_book, selected_chapter, selected_translation)

            verses_label = self.findChild(qtw.QLabel, "versesLabel")
            display_verse = ""

            for verse_list in verses:
                display_verse += f"<u><b>Verse {verse_list[3]}:</b></u> {verse_list[4]}<br /><br />"
                verses_label.setText(display_verse)

            book.setCurrentIndex(selected_book)
            chapter.setCurrentIndex(int(prev_chapter) - 1)

    def update_chapter_list(self, book_name):

        # book_combo_box = self.findChild(qtw.QComboBox, "Book")
        # book_index = book_combo_box.currentIndex()
        # print(book_index)

        chapters_combo_box = self.findChild(qtw.QComboBox, "Chapter")
        chapters_combo_box.clear()

        chapters = chapter_list(book_name)

        for chapter in chapters:
            chapters_combo_box.addItem(str(chapter[0]))

        chapters_combo_box.setCurrentIndex(0)

    def bible_promise_function(self, verse):
        bible_promise_label = self.findChild(qtw.QLabel, "bible_promise_text")
        bible_promise_label.setText(verse)

    def closeEvent(self, event):
        promises_instance = self.p_instance = MyThread()
        self.stop_signal.connect(promises_instance.stop)


class MyThread(qtc.QThread):
    bible_promise = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.continue_loop = True

    def run(self):
        temp = 1
        test1 = ""
        while self.continue_loop:
            test = self.function_T(temp)

            if test == test1:
                continue

            test1 = test

            self.bible_promise.emit(test)
            time.sleep(120)
            temp += 1

    def function_T(self, temp):
        verse = ""

        promises_number = random.randint(0, (len(bible_promises) - 1))

        b_promise = bible_promises[promises_number]

        for book_index in book_list:
            if b_promise[0] == book_index[1]:
                book_name = book_index[1]
                verse = daily_verses(book_index[0], b_promise[1], b_promise[2])[0][4] + f"<i> - {book_name} {b_promise[1]}:{b_promise[2]} <i/>"
                print(f"Verse {temp}\n", verse)

        return verse

    def stop(self):
        self.continue_run = False


# object of QApplication represents the state of our apps
# tt takes a list of command line arguments
# app = QtWidgets.QApplication([])


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
