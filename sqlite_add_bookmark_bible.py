import sqlite3


# # Code to create bookmarked_verses database file
# conn = sqlite3.connect(r"Bible Database/bookmarked_verses.db")
#
# c = conn.cursor()
#
# c.execute("""
#     Create Table bookmarked_verses (
#         book_name text,
#         book_chapter integer,
#         book_verse_number integer,
#         verse_bookmarked text,
#         translation_name text)
# """)
#
# conn.commit()
# conn.close()


def add_bookmark_to_database(book_name, chapter_number, verse_number, verse_text, translation_name):
    '''
    Function to add a bookmark to the database file

    :param: book_name -> Book Name
    :param: chapter_number -> Chapter Number
    :param: verse_number -> Verse Number
    :param: verse_text -> Verse Text
    :param: translation_name -> Translation Name
    '''

    conn = sqlite3.connect(r"Bible Database/bookmarked_verses.db")
    c = conn.cursor()

    if type(book_name) is not str:
        book_name = str(book_name)

    if type(chapter_number) is not int:
        chapter_number = int(chapter_number)

    if type(verse_number) is not int:
        verse_number = int(verse_number)

    if type(verse_text) is not str:
        verse_text = str(verse_text)

    if type(translation_name) is not str:
        translation_name = str(translation_name)

    c.execute(f"""
                Insert Into bookmarked_verses Values (
                    '{book_name}',
                     {chapter_number},
                     {verse_number},
                    '{verse_text}',
                    '{translation_name}')
                """)

    conn.commit()
    conn.close()
