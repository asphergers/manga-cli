from factory import get_pages, link_to_images, query, Manga;
from gui import Gui_Scroll;
import db;
import sys;

def get_input(message: str, parent):

    result = input(message);

    if result == "root":
        root();
    elif result == "back":
        parent();

    return result;

def get_images(manga: Manga, chapter: int):
    pages = get_pages(manga, chapter);
    images = link_to_images(pages);

    return images;


def auto_next(manga: Manga, starting_chap: int, auto=False):
    if auto:
        while True:
            next_images = get_images(manga, starting_chap);
            db.update(manga.name, starting_chap);
            Gui_Scroll(next_images);
            starting_chap +=1;
            print();
    else:
        images = get_images(manga, starting_chap);
        db.update(manga.name, starting_chap);
        Gui_Scroll(images);
        print();


def root():
    print("welcome to manga_cli, enter the command 'help' for help");
    while True:
        inp = input("$ ");

        if inp == "search":
            search_display();
        if inp == "db":
            db_display();
        if inp == "exit":
            sys.exit();

# MANGA SEARCH SECTION

def search_display():
    search_term = get_input("query: ", root);
    mangas = query(f"{search_term}");

    for i in range(len(mangas)):
        print(f"{i+1}: {mangas[i].name} ({mangas[i].chapters})");

    index = get_input("choose manga: ", root);

    try:
        index = int(index);
    except ValueError:
        print("not an int");
        search_display();

    chapter_select_display(int(index), mangas);

def chapter_select_display(index: int, mangas: list[Manga]):
    manga = mangas[index-1];

    chapter = get_input(f"choose chapter (1 - {manga.chapters}): ", search_display);

    try:
        chapter = int(chapter);
    except ValueError:
        print("not an int");
        chapter_select_display(index, mangas);

    reading_type = get_input("auto download next chapter?[y/n]: ", search_display);

    if reading_type[0].lower() == "y":
        auto_next(manga, int(chapter), True);
    elif reading_type[0].lower() == "n":
        auto_next(manga, int(chapter), False);
    else:
        print("not a valid response");
        chapter_select_display(index, mangas);

    chapter_select_display(index, mangas);


# HELP SECTION

def help_display():
    print("coming soon");

# DB SECTION

def db_display():
    print("Commands");
    print("--------");
    print("info - display the entire manga table");
    print("search - find a manga by name");

    while True:
        command = get_input("Command: ", root);

        if command == "info":
            db.print_db();

        if command == "search":
            term = get_input("search term: ", db_display);

            db.search_by_name(term);
        
root();
