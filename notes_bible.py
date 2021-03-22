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
        # uic.loadUi(r"UI\Test.ui", self)
        uic.loadUi(r"UI\Bible Notes.ui", self)

        # setting a window icon
        self.setWindowIcon(Qtg.QIcon(r"Images\logo 1.png"))

        self.show()

        self.accepted_file_types = "Text Document (*.txt);; Python (*.py)"  # file types that can be opened

        self.path = ""  # stores the current file's path

        self.changed_bold_value = False
        self.changed_italic_value = False
        self.changed_underline_value = False

        note_area = self.findChild(Qtw.QPlainTextEdit, "noteArea")

        self.boldButton.clicked.connect(lambda: self.change_font("Bold", self.changed_bold_value))
        self.italicButton.clicked.connect(lambda: self.change_font("Italic", self.changed_italic_value))
        self.underlineButton.clicked.connect(lambda: self.change_font("Underline", self.changed_underline_value))

        # File Actions

        # Open
        open_action = self.findChild(Qtw.QAction, "actionOpen")
        open_action.setShortcut(Qtg.QKeySequence.Open)
        open_action.triggered.connect(self.open_file)

        # Save
        save_action = self.findChild(Qtw.QAction, "actionSave")
        save_action.setShortcut(Qtg.QKeySequence.Save)
        save_action.triggered.connect(self.save_text)

        # Save As
        save_as_action = self.findChild(Qtw.QAction, "actionSave_As")
        save_as_action.setShortcut(Qtg.QKeySequence.SaveAs)
        save_as_action.triggered.connect(self.save_text_as)

        # Quick Acess

        # Undo
        undo_button = self.findChild(Qtw.QPushButton, "undoButton")
        undo_button.clicked.connect(note_area.undo)
        undo_button.setShortcut(Qtg.QKeySequence.Undo)

        # Redo
        redo_button = self.findChild(Qtw.QPushButton, "redoButton")
        redo_button.clicked.connect(note_area.redo)
        redo_button.setShortcut(Qtg.QKeySequence.Redo)

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

                note_area = self.findChild(Qtw.QPlainTextEdit, "noteArea")
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

        note_area = self.findChild(Qtw.QPlainTextEdit, "noteArea")
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
        # dialog_.setIcon(Qtw.QMessageBox.Critical)
        dialog_.show()

    def change_font(self, style, changed):
        '''
        Function to change between Bold, Italic and Underline
        '''
        note_area = self.findChild(Qtw.QPlainTextEdit, "noteArea")

        if style == "Bold":

            if not changed:
                self.changed_bold_value = True
                bold_font = Qtg.QFont()
                bold_font.setBold(True)
                note_area.setFont(bold_font)
            else:
                self.changed_bold_value = False
                bold_font = Qtg.QFont()
                bold_font.setBold(False)
                note_area.setFont(bold_font)

        if style == "Italic":

            if not changed:
                self.changed_italic_value = True
                italic_font = Qtg.QFont()
                italic_font.setItalic(True)
                note_area.setFont(italic_font)
            else:
                self.changed_italic_value = False
                italic_font = Qtg.QFont()
                italic_font.setItalic(False)
                note_area.setFont(italic_font)

        if style == "Underline":

            if not changed:
                self.changed_underline_value = True
                underline_font = Qtg.QFont()
                underline_font.setUnderline(True)
                note_area.setFont(underline_font)
            else:
                self.changed_underline_value = False
                underline_font = Qtg.QFont()
                underline_font.setUnderline(False)
                note_area.setFont(underline_font)


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    notes_window = NotesWindow()
    sys.exit(app.exec())
