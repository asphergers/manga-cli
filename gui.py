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

def gui_scroll(pages: list()):
    image_arr = list();
    root = Tk();
    width = root.winfo_screenwidth();
    height = root.winfo_screenheight(); 

    canvas = Canvas(root, bg="Black", width=width, height=height);
    canvas.pack();

    for page in pages:
        image = page.image;
        w, h = image.size;

        image_arr.append([ImageTk.PhotoImage(image), h]);

    y = 0;
    for image in image_arr:
        label = Label(canvas, image=image[0]);
        canvas.create_window(width/2, y, anchor="n", window=label);
        y += image[1];
    
    scroll_bar = Scrollbar(canvas, orient="vertical", command=canvas.yview);
    scroll_bar.place(relx=1, rely=0, relheight=1, anchor='ne');
    canvas.config(yscrollcommand=scroll_bar.set, scrollregion=(0, 0, 0, y));
    canvas.config(yscrollincrement=2);

    def scroll(speed):
        canvas.yview_scroll(speed, "units");

    root.bind("j", lambda event: scroll(20));
    root.bind("k", lambda event: scroll(-20));



    root.mainloop();

