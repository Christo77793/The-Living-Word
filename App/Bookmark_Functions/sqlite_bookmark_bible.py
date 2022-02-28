import sqlite3

BM_DB_LOCATION = r"Bible Database\bookmarked_verses.db"
MAIN_DB_LOCATION = r"Bible Database\bible_database.db"


def create_bookmark_db():
    '''
    Code to create bookmarked_verses database file
    '''

    conn = sqlite3.connect(BM_DB_LOCATION)

    c = conn.cursor()

    c.execute("""
                CREATE TABLE bookmarked_verses (
                    verse_count integer primary key,
                    book_name text,
                    book_chapter integer,
                    book_verse_number integer,
                    verse_bookmarked text,
                    translation_name text)
            """)

    conn.commit()
    conn.close()


def add_bookmark_to_database(book_name, chapter_number, verse_number, verse_text, translation_name):
    '''
    Function to add a bookmark to the database file

    :parameter: book_name -> Book Name
    :parameter: chapter_number -> Chapter Number
    :parameter: verse_number -> Verse Number
    :parameter: verse_text -> Verse Text
    :parameter: translation_name -> Translation Name
    '''

    conn = sqlite3.connect(BM_DB_LOCATION)
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
                  INSERT INTO bookmarked_verses Values (
                    null,
                    '{book_name}',
                     {chapter_number},
                     {verse_number},
                    "{verse_text}",
                    '{translation_name}')
              """)

    conn.commit()
    conn.close()
