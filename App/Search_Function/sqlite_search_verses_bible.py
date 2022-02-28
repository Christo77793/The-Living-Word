import sqlite3

DB_LOCATION = r"Bible Database\bible_database.db"


def find_verses(search_word):
    '''
    Function to find a verse from the database file

    :parameter: search_word -> The word entered by the user
    '''

    conn = sqlite3.connect(DB_LOCATION)

    cursor = conn.cursor()

    cursor.execute(f'''SELECT * FROM t_kjv
                    WHERE t LIKE "%{search_word}%"''')

    results = cursor.fetchall()

    conn.commit()
    conn.close()

    result_count = len(results)

    return result_count, results
