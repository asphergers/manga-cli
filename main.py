from factory import get_pages, link_to_images, query, Manga;
from gui import Gui_Scroll;
import db;
import sys;


def get_images(manga: Manga, chapter: int):
    pages = get_pages(manga, chapter);
    images = link_to_images(pages);

    return images;

def get_input(message: str):
    if message == "exit":
        sys.exit();
    result = input(message);
    return result;

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


while True:
    inp = input("$ ").split(' ');

    if inp[0] == "search":
        term = get_input("query: ");
        mangas = query(f"{term}");
        print(f"showing results for {term}");
        for i in range(len(mangas)):
            print(f"{i+1}: {mangas[i].name} ({mangas[i].chapters})");
        
        index = int(get_input("choose manga: "));
        manga = mangas[index-1]
        print(f"chose {manga.name} ({manga.chapters})");

        chapter = int(get_input(f"choose chapter (1-{manga.chapters}): "));

        reading_type = get_input("auto download next chapter?[y/n]");

        if reading_type.lower() == "y":
            auto_next(manga, chapter, True);
        elif reading_type.lower() == "n":
            auto_next(manga, chapter, False);
        else:
            print("not a valid respone");
            print("exiting");
            sys.exit();

    

    if inp[0] == "info":
        print(db.get_db_raw())

    if inp[0] == "exit":
        sys.exit();


