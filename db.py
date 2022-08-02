import os;
import sqlite3;
from tabulate import tabulate;


if not os.path.exists("./manga.db"):
    open("manga.db", "x"); 
    conn = sqlite3.connect("manga.db");
    cur = conn.cursor();

    cur.execute("""CREATE TABLE manga
                            (name TEXT,
                            last_chapter_read INTEGER)""");

    conn.commit();

else:
    conn = sqlite3.connect("manga.db");
    cur = conn.cursor();


def update(manga_name: str, chapter: int):

    cur.execute(f"""SELECT name FROM manga WHERE name = '{manga_name}'""");

    result = cur.fetchone();

    if result:
        cur.execute(f"""UPDATE manga SET last_chapter_read = {chapter} WHERE name = '{manga_name}'""");
        conn.commit();
        print("updated entry");
    else:
        cur.execute(f"""INSERT INTO manga (name, last_chapter_read) VALUES ('{manga_name}', {chapter})""") 
        conn.commit();
        print("added entry");

    #cur.execute("""INSERT INTO manga VALUES()""");

def get_db_raw():
    cur.execute("SELECT * FROM manga");
    result = cur.fetchall();
    return result;

def print_db():
    results = get_db_raw();
    
    print(tabulate(results, headers = ["manga", "chp"], tablefmt="psql"));


