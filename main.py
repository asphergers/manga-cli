from factory import *
from gui import *
from threading import Thread;
import sys;


def get_images(manga, chapter):
    pages = get_pages(manga, chapter);
    images = link_to_images(pages);

    return images;

def auto_next(manga, starting_chap, auto=False):
    images = get_images(manga, starting_chap);
    Gui_Scroll(images);
    
    if auto:
        while True:
            starting_chap += 1;
            next_images = get_images(manga, starting_chap);
            Gui_Scroll(next_images);
            print();
    else:
        print();


while True:
    inp = input("$ ").split(' ');

    if inp[0] == "search":
        term = input("query: ");
        mangas = query(f"{term}");
        print(f"showing results for {term}");
        for i in range(len(mangas)):
            print(f"{i+1}: {mangas[i].name} ({mangas[i].chapters})");
        
        index = int(input("choose manga: "));
        manga = mangas[index-1]
        print(f"chose {manga.name} ({manga.chapters})");

        chapter = int(input(f"choose chapter (1-{manga.chapters}): "));

        auto_next(manga, chapter, True);
    
    if inp[0] == "exit":
        sys.exit();


