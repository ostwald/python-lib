
from Tkinter import *
import Image, ImageTk
win = Tk()

## imgdir = "/Users/ostwald/Desktop/to Print/"
## imgfile = Image.open (imgdir+"greek_alphabet.gif")

imgdir = "/Volumes/Info_Space/AnisArt/Images/Originals/summer2005 paintings/"
imgfile = Image.open (imgdir+"DSCN8013.jpg")

img = ImageTk.PhotoImage(imgfile)
# img = PhotoImage(imgdir+"greek_alphabet.gif")
can = Canvas(win)
can.config (bg="black")
can.pack(fill=BOTH)
can.create_image(2, 2, image=img, anchor=NW)           # x, y coordinates
can.config (width=img.width(), height=img.height())
win.mainloop()

