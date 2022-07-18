from PIL import Image, ImageTk;
from itertools import cycle;
from tkinter import Canvas, Frame, PhotoImage, Button, Tk, Label, Scrollbar, CENTER;



def gui_flip(pages: list()):

    root = Tk();
    root.resizable();


    image_list = list();
    index = 0;

    for i in range(len(pages)):
        w, h = pages[i].image.size;

        diff = h - 1080;
        new_h = h - diff;
        new_w = w - diff;

        new_page = ImageTk.PhotoImage(pages[i].image.resize((new_w, new_h), Image.ANTIALIAS));

        image_list.append(new_page);

    frame = Frame(root, width=230, height=200);
    frame.pack();

    label = Label(frame, image=image_list[index]);
    label.pack();

    def next():
        nonlocal index;
        index += 1;
        label.config(image=image_list[index]);

    root.bind("a", lambda event: next());


    root.mainloop();

class Gui_Scroll:
    def __init__(self, pages: list()):
        self.pages = pages;
        self.image_arr = list();
        self.root = Tk();
        self.width = self.root.winfo_screenwidth();
        self.height = self.root.winfo_screenheight();
        self.canvas = Canvas(self.root, bg="black", width = self.width, height = self.height);
        self.canvas.pack();

        self.build();

        self.root.mainloop();
    
    def build(self):
        for page in self.pages:
            image = page.image;
            w, h = image.size;

            self.image_arr.append([ImageTk.PhotoImage(image), h]);
        
        self.y = 0;
        for image in self.image_arr:
            print(image);
            label = Label(self.canvas, image=image[0]);
            self.canvas.create_window(self.width/2, self.y, anchor="n", window=label);
            self.y += image[1];
        
        self.scroll_bar = Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview);
        self.scroll_bar.place(relx = 1, rely = 0, relheight= 1, anchor='ne');
        self.canvas.config(yscrollcommand=self.scroll_bar.set, scrollregion=(0, 0, 0, self.y));
        self.canvas.config(yscrollincrement=2);

        self.root.bind("j", lambda event: self.scroll(20));
        self.root.bind("k", lambda event: self.scroll(-20));

    
    def scroll(self, speed):
        self.canvas.yview_scroll(speed, "units");

