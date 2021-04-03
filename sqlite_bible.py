import sqlite3

# Stores the Bible book's name and it's respective count number
book_list = [(1, "Genesis"), (2, "Exodus"), (3, "Leviticus"), (4, "Numbers"), (5, "Deuteronomy"), (6, "Joshua"),
             (7, "Judges"), (8, "Ruth"), (9, "1 Samuel"), (10, "2 Samuel"), (11, "1 Kings"), (12, "2 Kings"),
             (13, "1 Chronicles"), (14, "2 Chronicles"), (15, "Ezra"), (16, "Nehemiah"), (17, "Esther"), (18, "Job"),
             (19, "Psalms"), (20, "Proverbs"), (21, "Ecclesiastes"), (22, "Song of Solomon"), (23, "Isaiah"), (24, "Jeremiah"),
             (25, "Lamentations"), (26, "Ezekiel"), (27, "Daniel"), (28, "Hosea"), (29, "Joel"), (30, "Amos"),
             (31, "Obadiah"), (32, "Jonah"), (33, "Micah"), (34, "Nahum"), (35, "Habakkuk"), (36, "Zephaniah"),
             (37, "Haggai"), (38, "Zechariah"), (39, "Malachi"), (40, "Matthew"), (41, "Mark"), (42, "Luke"),
             (43, "John"), (44, "Acts"), (45, "Romans"), (46, "1 Corinthians"), (47, "2 Corinthians"), (48, "Galatians"),
             (49, "Ephesians"), (50, "Philippians"), (51, "Colossians"), (52, "1 Thessalonians"), (53, "2 Thessalonians"), (54, "1 Timothy"),
             (55, "2 Timothy"), (56, "Titus"), (57, "Philemon"), (58, "Hebrews"), (59, "James"), (60, "1 Peter"),
             (61, "2 Peter"), (62, "1 John"), (63, "2 John"), (64, "3 John"), (65, "Jude"), (66, "Revelation")]

# Stores the list of Bible promises
bible_promises = [["Job", 8, 7], ["1 Chronicles", 16, 34], ["James", 1, 17],
                  ["Psalms", 34, 8], ["Genesis", 28, 15], ["Isaiah", 41, 10],
                  ["Revelation", 3, 8], ["Haggai", 2, 19], ["Psalms", 50, 15]]


def show_verses(book_id, chapter_id, translation_filter, verse_id=""):
    '''
    Function to show the verses from the provided book name, chapter number and the selected translation

    :parameter: book_id -> Contains the book name's index number
    :parameter: chapter_id -> Contains the chapter number
    :parameter: translation_filter -> Contains the translation's index
    '''
    conn = sqlite3.connect(r"Bible Database\bible_database.db")

    cursor = conn.cursor()

    book_id += 1
    book_id = str(book_id)

    if type(chapter_id) is not str:
        chapter_id = str(chapter_id)  # converting to string

    if translation_filter == "KJV":
        selected_translation = "t_kjv"

    elif translation_filter == "ASV":
        selected_translation = "t_asv"

    elif translation_filter == "BBE":
        selected_translation = "t_bbe"

    elif translation_filter == "WBT":
        selected_translation = "t_wbt"

    elif translation_filter == "YLT":
        selected_translation = "t_ylt"

    else:  # DARBY
        selected_translation = "t_dby"

    if not verse_id:
        cursor.execute(f'''SELECT * FROM {selected_translation}
                    WHERE b = {book_id} AND c = {chapter_id}''')

        selected_verses = cursor.fetchall()
    else:
        if type(verse_id) is not str:
            verse_id = str(verse_id)  # converting to string

        cursor.execute(f'''SELECT * FROM {selected_translation}
                            WHERE b = {book_id} AND c = {chapter_id} and v = {verse_id}''')

        selected_verses = cursor.fetchall()

    conn.commit()
    conn.close()

    return selected_verses


def chapter_list(book_id):
    '''
    Function to return the number of chapters in a book
    :parameter: book_id -> Contains the book name's index number
    '''

    conn = sqlite3.connect(r"Bible Database\bible_database.db")

    cursor = conn.cursor()

    book_id += 1
    book_id = str(book_id)

    cursor.execute(f'''SELECT c FROM t_kjv
                       WHERE b = {book_id}
                       GROUP BY c''')

    chapter_count = cursor.fetchall()

    conn.commit()
    conn.close()

    return chapter_count


def daily_verses(book_id, chapter_id, verse_id):
    '''
    Function to show the verses from the provided book name, chapter number and the selected verse

    :parameter: book_id -> Contains the book name's index number
    :parameter: chapter_id -> Contains the chapter number
    :parameter: verse_id -> Contains the verse number
    '''
    conn = sqlite3.connect(r"Bible Database\bible_database.db")

    cursor = conn.cursor()

    if type(book_id) is not str:
        book_id = str(book_id)

    if type(chapter_id) is not str:
        chapter_id = str(chapter_id)

    if type(verse_id) is not str:
        verse_id = str(verse_id)

    cursor.execute(f'''SELECT * FROM t_kjv
                        WHERE b = {book_id} AND c = {chapter_id} AND v = {verse_id}''')

    selected_verses = cursor.fetchall()

    conn.commit()
    conn.close()

    return selected_verses
