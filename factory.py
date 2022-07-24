import requests;
import re;
from threading import Thread;
from PIL import Image;
from io import BytesIO;
from dataclasses import dataclass
from bs4 import BeautifulSoup;

@dataclass
class Manga:
    name: str;
    link: str;
    chapters: str;

@dataclass
class Page:
    num: int;
    image: Image;

def query(query):
    entry_arr = list();
    response = requests.get(f"https://ww5.manganelo.tv/search/{query}");
    soup = BeautifulSoup(response.content, 'html.parser');
    div = soup.find('div', {"class" : "container-main-left"}) \
            .find('div', {"class" : "panel-search-story"});

    items = div.findAll('div', {"class": "search-story-item"});

    for item in items:
        title = item.find('a', {"class" : "item-img"})['title'];
        href = item.find('a', {"class" : "item-img"})['href'];
        href = href[href.find("manga-"):]

        chap_info = item.find('a', {"class" : "item-chapter"}) \
                .text \
                .split();

        latest_chap = str();
        for i in range(len(chap_info)):
            if chap_info[i] == "Chapter":
                latest_chap = re.sub("[^0-9].:", "", chap_info[i+1]);
                break;

        entry = Manga(title, href, latest_chap);
        entry_arr.append(entry);

    return entry_arr;
  

def get_pages(manga: Manga, chapter: int):
    pages = list();
    url = f"https://ww5.manganelo.tv/chapter/{manga.link}/chapter-{chapter}";
    print(url); 
    response = requests.get(url);
    
    soup = BeautifulSoup(response.content, "html.parser");
    div = soup.find('div', {"class" : "body-site"}) \
        .find('div', {"class" : "container-chapter-reader"}) \
        .findAll('img');

    for page in div:
        try:
            pages.append(page['src']);
        except:
            pages.append(page['data-src']);

    return pages;

def dump_pages(pages: list()):
    header = {'Referer': 'https://readmanganato.com/'};
    
    for i in range(len(pages)):
        response = requests.get(pages[i], headers=header);
        file = open(f"dump/{i}.jpg", "wb");
        file.write(response.content);
        file.close();
        print(f"\r dumping pages {i}/{len(pages)}", end="");

def grab_images(pages: list(), start: int, end: int, images: list(), counter: list()):
    for i in range(start, end):
        response = requests.get(pages[i]);
        img = Image.open(BytesIO(response.content));
        counter[0] += 1;
        print(f"\r {counter[0]}/{len(pages)}", end="");

        page = Page(i, img);
        images.append(page);

    print();

def sort_pages(pages: list()):
    for i in range(len(pages)):
        for j in range(len(pages)-i-1):
            if pages[j].num > pages[j+1].num:
                pages[j], pages[j+1] = pages[j+1], pages[j];
    

def link_to_images(pages: list()):
    thread_arr, steps, images = list(), list(), list();
    threads = int(len(pages))//5;
    current = 0;
    step = round(len(pages)/threads);
    counter = [0];

    for i in range(threads+1):
        steps.append(current);
        current += step;
    
    if steps[-1] != len(pages):
        steps[-1] = len(pages);

    for i in range(len(steps)-1):
        process = Thread(target=grab_images, args=[pages, steps[i], steps[i+1], images, counter]); 
        process.start();
        thread_arr.append(process);

    for thread in thread_arr:
        thread.join();
    
    sort_pages(images);

    return images;

def show_pages(pages: list()):
    for page in pages:
        page.image.show(); 

