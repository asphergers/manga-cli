from factory import *
from gui import *
import sys;

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

        pages = get_pages(manga, chapter);
        images = link_to_images(pages);
        gui_scroll(images);
        print();
    
    if inp[0] == "exit":
        sys.exit();
