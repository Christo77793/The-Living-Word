import sqlite3


def show_verses(book_id, chapter_id):
    conn = sqlite3.connect(r"Bible Database\bible_database.db")

    cursor = conn.cursor()

    book_id += 1
    book_id = str(book_id)

    if type(chapter_id) is not str:
        chapter_id = str(chapter_id)

    cursor.execute(f'''SELECT * FROM t_kjv
                    WHERE b = {book_id} AND c = {chapter_id}''')

    selected_verses = cursor.fetchall()

    conn.commit()
    conn.close()

    return selected_verses


def chapter_list(book_id):
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
