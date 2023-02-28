import sqlite3

def createDataTable():
    con = sqlite3.connect("SI.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS show("
                "id String PRIMARY KEY,"
                "type String not null,"
                "title String not null,"
                "director String,"
                "cast String,"
                "country String,"
                "date_added String not null,"
                "release_year integer not null,"
                "rating String not null,"
                "duration String not null,"
                "listed_in text not null,"
                "description text not null"
                ")")


createDataTable()

