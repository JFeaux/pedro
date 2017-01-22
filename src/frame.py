#!/usr/bin/python

import os
import sys
import random 
import time
import copy

from itertools import product

import Tkinter as tk
import tkFont
import tkSimpleDialog
import tkMessageBox

from PIL import ImageTk, Image

root=tk.Tk()
root.title('Pedro')

screen_height=root.winfo_screenwidth()
screen_width=root.winfo_screenheight()

tmp=ImageTk.PhotoImage(Image.open("../deck/01c.png"))
height,width=tmp.height(),tmp.width()

frame=tk.Frame(root,height = screen_height, width = screen_width,bg='forest green',borderwidth=5,relief='ridge')

name_font=tkFont.Font(family='Times',size=16)

img1 = (Image.open("../deck/01c.png"))
img2 = (Image.open("../deck/02c.png"))
img3 = (Image.open("../deck/03c.png"))
img4 = (Image.open("../deck/04c.png"))
img5 = (Image.open("../deck/05c.png"))
img6 = (Image.open("../deck/06c.png"))
img7 = (Image.open("../deck/07c.png"))
img8 = (Image.open("../deck/08c.png"))
img9 = (Image.open("../deck/09c.png"))

small_img=ImageTk.PhotoImage(img9.resize((int(0.25*width),int(0.25*height)),Image.ANTIALIAS))


imgs=[
    img1,
    img2,
    img3,
    img4,
    img5,
    img6]
    #    img7,
    #    img8,
    #    img9]

scale=.6
font_size=20
x_center=scale*width/2.
y_center=scale*height/2.
dx=scale*width/4.
for count,img in enumerate(imgs):
  imgs[count]=ImageTk.PhotoImage(img.resize((int(scale*width),int(scale*height)),Image.ANTIALIAS))

hand1=tk.Canvas(frame,width=dx*8,
    height=scale*height)
for count,img in enumerate(imgs):
  shift=count*dx
  hand1.create_image(shift+x_center,y_center,image=img)

hand2=tk.Canvas(frame,width=dx*8,
    height=scale*height)
for count,img in enumerate(imgs):
  shift=count*dx
  hand2.create_image(shift+x_center,y_center,image=img)

hand3=tk.Canvas(frame,width=dx*8,
    height=scale*height)
for count,img in enumerate(imgs):
  shift=count*dx
  hand3.create_image(shift+x_center,y_center,image=img)

hand4=tk.Canvas(frame,width=dx*8,
    height=scale*height)
for count,img in enumerate(imgs):
  shift=count*dx
  hand4.create_image(shift+x_center,y_center,image=img)

name1=tk.Label(frame,text='Player 1',bg='forest green',fg='white',font=name_font)
name2=tk.Label(frame,text='Player 2',bg='forest green',fg='white',font=name_font)
name3=tk.Label(frame,text='Player 3',bg='forest green',fg='white',font=name_font)
name4=tk.Label(frame,text='Player 4',bg='forest green',fg='white',font=name_font)

scale=.6/2
imgs[0]=small_img
x_center=scale*width/2.
y_center=scale*height/2.
old_trick1=tk.Canvas(frame,width=4*scale*width,height=scale*height)
for i in range(4):
  shift=i*width*.25
  old_trick1.create_image(shift+x_center,y_center,image=imgs[0])

old_trick2=tk.Canvas(frame,width=4*scale*width,height=scale*height)
for i in range(4):
  shift=i*width*.25
  old_trick2.create_image(shift+x_center,y_center,image=imgs[0])

old_trick3=tk.Canvas(frame,width=4*scale*width,height=scale*height)
for i in range(4):
  shift=i*width*.25
  old_trick3.create_image(shift+x_center,y_center,image=imgs[0])

old_trick4=tk.Canvas(frame,width=4*scale*width,height=scale*height)
for i in range(4):
  shift=i*width*.25
  old_trick4.create_image(shift+x_center,y_center,image=imgs[0])

old_trick5=tk.Canvas(frame,width=4*scale*width,height=scale*height)
for i in range(4):
  shift=i*width*.25
  old_trick5.create_image(shift+x_center,y_center,image=imgs[0])

scale=0.6
x_center=scale*width/2.
y_center=scale*height/2.

current_trick1=tk.Canvas(frame,width=scale*height,height=scale*height)
current_trick2=tk.Canvas(frame,width=scale*height,height=scale*height)
current_trick3=tk.Canvas(frame,width=scale*height,height=scale*height)
current_trick4=tk.Canvas(frame,width=scale*height,height=scale*height)

x_center=width*scale
y_center=height*scale
current_trick1.create_image(x_center,y_center,image=imgs[1])
current_trick2.create_image(x_center,y_center,image=imgs[2])
current_trick3.create_image(x_center,y_center,image=imgs[3])
current_trick4.create_image(x_center,y_center,image=imgs[4])


spacer1=tk.Label(frame,text='          ')
spacer2=tk.Label(frame,text='               ')

spacer1.grid(row=0,column=1)
spacer2.grid(row=0,column=6)

name1.grid(row=0,column=0)
hand1.grid(row=1,column=0,rowspan=2)

name4.grid(row=7,column=0)
hand4.grid(row=8,column=0,rowspan=2)

name2.grid(row=0,column=5)
hand2.grid(row=1,column=5,rowspan=2)

name3.grid(row=7,column=5)
hand3.grid(row=8,column=5,rowspan=2)

current_trick1.grid(row=3,column=2,rowspan=2)
current_trick2.grid(row=3,column=3,rowspan=2)
current_trick3.grid(row=5,column=2,rowspan=2)
current_trick4.grid(row=5,column=3,rowspan=2)

old_trick1.grid(row=1,column=7)#,sticky='NE')
old_trick2.grid(row=2,column=7)#,sticky='SW')
old_trick3.grid(row=3,column=7)#,sticky='NW')
old_trick4.grid(row=4,column=7)#,sticky='SE')
old_trick5.grid(row=5,column=7)#,sticky='NE')
#
#
#root.grid_columnconfigure(1,weight=2)
#root.grid_columnconfigure(4,weight=2)
#
#root.grid_columnconfigure(0,weight=1)
#root.grid_columnconfigure(5,weight=1)


#hand_frame.pack(anchor=tk.CENTER)



#var=tk.StringVar()
#score_frame=tk.Label(root,height=10,width=screen_width,textvariable=var)
#
#var.set('We: {} They: {}'.format(14,24))
#score_frame.pack(side='bottom')
#

frame.pack()
root.mainloop()


