import sys
from PyQt5 import uic
from sqlite_bible import show_verses, chapter_list
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class BibleAppWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()  # avoid code redundancy

        # loading the application's UI {stored as XML format}
        uic.loadUi(r"UI\First.ui", self)

        # setting a window icon
        self.setWindowIcon(qtg.QIcon(r"Images\logo.png"))
        self.show()

        books_list = self.findChild(qtw.QComboBox, "Book")  # instance of combo_box Book
        books_list_index = books_list.currentIndex()

        # chapter = self.findChild(qtw.QComboBox, "Chapter")  # instance of combo_box Chapter
        # chapter_index = chapter.currentIndex()

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

    def display_verses(self):
        book = self.findChild(qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        chapter = self.findChild(qtw.QComboBox, "Chapter")
        selected_chapter = chapter.currentText()

        verses = show_verses(selected_book, selected_chapter)
        #versesLabel
        verses_label = self.findChild(qtw.QLabel, "versesLabel")
        display_verse = ""
        for verse_list in verses:
            display_verse += f"<u><b>Verse {verse_list[3]}:</b></u> {verse_list[4]}<br /><br />"
            verses_label.setText(display_verse)

    def next_chapter(self):
        book = self.findChild(qtw.QComboBox, "Book")
        selected_book = book.currentIndex()

        chapter = self.findChild(qtw.QComboBox, "Chapter")
        selected_chapter = str(int(chapter.currentText()) + 1)

        count_chapter = chapter.count()

        if int(selected_chapter) <= int(count_chapter):
            verses = show_verses(selected_book, selected_chapter)
        else:
            selected_book += 1
            selected_chapter = "1"
            verses = show_verses(selected_book, selected_chapter)
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

        chapter = self.findChild(qtw.QComboBox, "Chapter")
        selected_chapter = str(int(chapter.currentText()) - 1)

        if int(selected_chapter) > 0:

            verses = show_verses(selected_book, selected_chapter)

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
            verses = show_verses(selected_book, selected_chapter)

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


# object of QApplication represents the state of our apps
# tt takes a list of command line arguments
# app = QtWidgets.QApplication([])


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    bibleApp = BibleAppWindow()
    sys.exit(app.exec())
