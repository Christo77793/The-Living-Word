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
class NotesWindow(Qtw.QMainWindow):
    def __init__(self):
        super().__init__()  # avoid code redundancy

        # loading the application's UI {stored as XML format}
        uic.loadUi(r"UI\Bible Notes.ui", self)

        # setting a window icon
        self.setWindowIcon(Qtg.QIcon(r"Images\Window Icons\bible_notes.png"))

        self.setWindowFlag(Qtc.Qt.FramelessWindowHint)  # removes standard title
        self.show()  # show the UI
        self.showMaximized()  # loads the app in full-screen
        self.shareButton.hide()  # temporarily hiding till share function implemented

        # Window Manipulation Buttons

        self.minimiseButton.clicked.connect(lambda: self.showMinimized())
        self.restoreButton.clicked.connect(lambda: self.change_window_size())
        self.closeButton.clicked.connect(lambda: self.close())

        self.accepted_file_types = "Text Document (*.txt);; Python (*.py)"  # file types that can be opened

        self.path = ""  # stores the current file's path

        # initial values for the bold, italic, and underline buttons to represent their active state
        self.changed_bold_value = False
        self.changed_italic_value = False
        self.changed_underline_value = False

        # Bold
        self.boldButton.clicked.connect(lambda: self.change_font("Bold", self.changed_bold_value))

        # Italic
        self.italicButton.clicked.connect(lambda: self.change_font("Italic", self.changed_italic_value))

        # Underline
        self.underlineButton.clicked.connect(lambda: self.change_font("Underline", self.changed_underline_value))

        # Font Selection

        # Font Combo
        font_button = self.findChild(Qtw.QFontComboBox, "changeFontButton")
        font_button.currentFontChanged.connect(self.noteArea.setCurrentFont)  # Set the combo box to the current font

        available_font_sizes = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

        # Font Size
        font_size_button = self.findChild(Qtw.QComboBox, "changeFontSizeButton")
        font_size_button.addItems([str(size) for size in available_font_sizes])  # Loop through available sizes and add them

        font_size_button.setCurrentIndex(4)
        self.noteArea.setFontPointSize(9)

        font_size_button.currentIndexChanged.connect(lambda size: self.noteArea.setFontPointSize(int(available_font_sizes[size])))

        # File Actions

        new_action = self.findChild(Qtw.QPushButton, "newButton")
        new_action.clicked.connect(lambda: self.noteArea.clear())

        # Open
        open_action = self.findChild(Qtw.QPushButton, "openButton")
        open_action.setShortcut(Qtg.QKeySequence.Open)
        open_action.clicked.connect(self.open_file)

        # Save
        save_action = self.findChild(Qtw.QPushButton, "saveButton")
        save_action.setShortcut(Qtg.QKeySequence.Save)
        save_action.clicked.connect(self.save_text)

        # Save As
        save_as_action = self.findChild(Qtw.QPushButton, "saveAsButton")
        save_as_action.clicked.connect(self.save_text_as)

        # Quick Access

        # Undo
        undo_button = self.findChild(Qtw.QPushButton, "undoButton")
        undo_button.clicked.connect(self.noteArea.undo)
        undo_button.setShortcut(Qtg.QKeySequence.Undo)

        # Redo
        redo_button = self.findChild(Qtw.QPushButton, "redoButton")
        redo_button.clicked.connect(self.noteArea.redo)
        redo_button.setShortcut(Qtg.QKeySequence.Redo)

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

    def open_file(self):
        '''
        Function to open a file
        '''

        path, test = Qtw.QFileDialog.getOpenFileName(
            parent=self,
            caption="Open File",
            directory="",
            filter=self.accepted_file_types
        )

        if path:
            try:
                with open(path, "r") as f:
                    text = f.read()
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path

                note_area = self.findChild(Qtw.QTextEdit, "noteArea")
                note_area.setPlainText(text)

                self.change_window_title()

    def change_window_title(self):
        '''
        Function that updates the application title
        '''

        self.setWindowTitle("{0} ".format(os.path.basename(self.path) if self.path else "Untitled"))

    def save_text(self):
        '''
        Function to save a file
        '''

        if self.path is None:
            self.save_text_as()
        else:
            try:

                note_area = self.findChild(Qtw.QPlainTextEdit, "noteArea")
                text_to_be_saved = note_area.toPlainText()

                with open(self.path, "w") as f:
                    f.write(text_to_be_saved)
                    f.close()

            except Exception as e:
                self.dialog_message(str(e))

    def save_text_as(self):
        '''
        Function to save a file as
        '''

        path, test = Qtw.QFileDialog.getSaveFileName(
            parent=self,
            caption="Save File As",
            directory="",
            filter=self.accepted_file_types
        )

        note_area = self.findChild(Qtw.QTextEdit, "noteArea")
        text_to_be_saved_as = note_area.toPlainText()

        if not path:
            return
        else:
            try:
                with open(path, "w") as f:
                    f.write(text_to_be_saved_as)
                    f.close()

            except Exception as e:
                self.dialog_message(str(e))

            else:
                self.path = path
                self.change_window_title()

    def dialog_message(self, message):
        '''
        Function to show an error message, if some error occurs
        :parameter: message -> Show the current error
        '''

        dialog_ = Qtw.QMessageBox(self)
        dialog_.setText(message)
        dialog_.setIcon(Qtw.QMessageBox.Critical)
        dialog_.show()

    def change_font(self, style, changed):
        '''
        Function to select and de-select font styles of Bold, Italic and Underline
        '''

        # Checking which to style to turn on/off

        if style == "Bold":

            if not changed:
                self.changed_bold_value = True

                # changing button color of bold to show it's active
                self.boldButton.setStyleSheet("QPushButton{ background-color: rgb(55, 117, 244); } QPushButton:hover{ background-color: rgb(47, 102, 211); }")
                self.noteArea.setFontWeight(Qtg.QFont.Bold)
            else:
                self.changed_bold_value = False

                # changing button color of bold to show it's not active
                self.boldButton.setStyleSheet("QPushButton{ background-color: rgb(30, 30, 30); } QPushButton:hover{ background-color: rgb(25, 25, 25); }")
                self.noteArea.setFontWeight(Qtg.QFont.Normal)

        if style == "Italic":

            if not changed:
                self.changed_italic_value = True

                # changing button color of italic to show it's active
                self.italicButton.setStyleSheet("QPushButton{ background-color: rgb(55, 117, 244); } QPushButton:hover{ background-color: rgb(47, 102, 211); }")

                self.noteArea.setFontItalic(True)
            else:
                self.changed_italic_value = False

                # changing button color of italic to show it's not active
                self.italicButton.setStyleSheet("QPushButton{ background-color: rgb(30, 30, 30); } QPushButton:hover{ background-color: rgb(25, 25, 25); }")

                self.noteArea.setFontItalic(False)

        if style == "Underline":

            if not changed:
                self.changed_underline_value = True

                # changing button color of underline to show it's active
                self.underlineButton.setStyleSheet("QPushButton{ background-color: rgb(55, 117, 244); } QPushButton:hover{ background-color: rgb(47, 102, 211); }")

                self.noteArea.setFontUnderline(True)
            else:
                self.changed_underline_value = False

                # changing button color of underline to show it's not active
                self.underlineButton.setStyleSheet("QPushButton{ background-color: rgb(30, 30, 30); } QPushButton:hover{ background-color: rgb(25, 25, 25); }")

                self.noteArea.setFontUnderline(False)


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    notes_window = NotesWindow()
    sys.exit(app.exec())
