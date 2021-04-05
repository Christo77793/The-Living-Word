import sqlite3


# print(sqlite3.sqlite_version)
#
# conn = sqlite3.connect(r"Bible Database\bookmarked_verses.db")
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
    conn = sqlite3.connect(r"Bible Database\bookmarked_verses.db")
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


def show_bookmarks():

    print("TESTING\n\n")

    conn = sqlite3.connect(r"Bible Database\bookmarked_verses.db")

    cursor = conn.cursor()

    cursor.execute(f'''SELECT * FROM bookmarked_verses''')

    bookmarked = cursor.fetchall()

    conn.commit()
    conn.close()

    print(bookmarked)
    for x in bookmarked:
        print(x[0])
        print(x[1])
        print(x[2])
        print(x[3])

