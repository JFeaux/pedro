#!/usr/bin/python

import os
import sys
import random
import time

import Tkinter as tk
import tkFont
import tkSimpleDialog
import tkMessageBox

from PIL import ImageTk, Image
import os

root = tk.Tk()

tmp = ImageTk.PhotoImage(Image.open("../deck/01c.png"))
height, width = tmp.height(), tmp.width()
print height, width

img1 = (Image.open("../deck/01c.png"))
img2 = (Image.open("../deck/02c.png"))
img3 = (Image.open("../deck/03c.png"))
img4 = (Image.open("../deck/04c.png"))
img5 = (Image.open("../deck/05c.png"))
img6 = (Image.open("../deck/06c.png"))
#img7 = (Image.open("../deck/07c.png"))
#img8 = (Image.open("../deck/08c.png"))
#img9 = (Image.open("../deck/09c.png"))

imgs = [
    img1,
    img2,
    img3,
    img4,
    img5,
    img6]
#    img7,
#    img8,
#    img9]

scale = .75
font_size = 20
x_center = scale * width / 2.
y_center = scale * height / 2.
dx = scale * width / 4.
for count, img in enumerate(imgs):
    imgs[count] = ImageTk.PhotoImage(img.resize(
        (int(scale * width), int(scale * height)), Image.ANTIALIAS))

hand_frame = tk.Canvas(root, width=dx * 11,
                       height=scale * height)
for count, img in enumerate(imgs):
    shift = count * dx
    hand_frame.create_image(shift + x_center, y_center, image=img)
hand_frame.pack(anchor=tk.CENTER)


button_font = tkFont.Font(family='Times', size=20)
bid_frame = tk.Frame(root)
bids = [i for i in range(6, 15)]


def disable(button):
    button['state'] = tk.DISABLED


def func():
    global hand_frame
    hand_frame.destroy()
    global bid_frame
    bid_frame.destroy()
    hand_frame = tk.Frame(root,
                          height=scale * height)
    buttons = [0 for i in range(9)]
    for count, img in enumerate(imgs):
        shift = count * dx
        if count == len(imgs) - 1:
            buttons[count] = tk.Button(
                hand_frame,
                height=scale * height,
                width=scale * width,
                image=img,
                command=lambda count=count: disable(
                    buttons[count]))
        else:
            buttons[count] = tk.Button(
                hand_frame,
                height=scale * height,
                width=dx,
                image=img,
                command=lambda count=count: disable(
                    buttons[count]))
        buttons[count].pack(side='left')
    hand_frame.pack(anchor=tk.CENTER)

b = tk.Button(bid_frame, text='PASS', font=button_font, command=func)
b.pack(side='left')
for bid in bids:
    b = tk.Button(bid_frame, text=bid, font=button_font, command=func)
    b.pack(side='left')
    if bid < 8:
        b['state'] = tk.DISABLED
bid_frame.pack(side='top')


root.mainloop()
