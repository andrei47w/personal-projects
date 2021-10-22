import math
import os,sys
from tkinter import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

HEIGHT = 975

xpos = 0
ypos = 0
xp = 0
yp = 0

maps = ['Reserve', 'Woods', 'Shoreline', 'Customs', 'Interchange']
ratio = [126, 34, 51, 174, 53]
map = 0

def on_closing():
    sys.exit()

def set_Reserve():
    global map
    map = 0
    main_root.destroy()

def set_Woods():
    global map
    map = 1
    main_root.destroy()

def set_Shoreline():
    global map
    map = 2
    main_root.destroy()

def set_Customs():
    global map
    map = 3
    main_root.destroy()

def set_Interchange():
    global map
    map = 4
    main_root.destroy()

main_root = Tk()
main_root.geometry('212x275')
main_root.configure(background="#3C3F41")
main_root.title('EFT Distance Calculator')
main_root.resizable(False, False)

lbl = Label(master=main_root, text='     ', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11 bold')
lbl.grid(row=2, column=0, sticky='')
lbl = Label(master=main_root, text='      Choose Map', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11 bold')
lbl.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='')
button = Button(master=main_root, text="Reserve", command=set_Reserve, width=14, height=0, bg="#3C3F41", fg="#BBBBBB", font='Consolas 11 bold')
button.grid(row=3, column=1, sticky='W')
button2 = Button(master=main_root, text="Woods", command=set_Woods, width=14, height=0, bg="#3C3F41", fg="#BBBBBB", font='Consolas 11 bold')
button2.grid(row=4, column=1, sticky='W')
button3 = Button(master=main_root, text="Shoreline", command=set_Shoreline, width=14, height=0, bg="#3C3F41", fg="#BBBBBB", font='Consolas 11 bold')
button3.grid(row=5, column=1, sticky='W')
button4 = Button(master=main_root, text="Customs", command=set_Customs, width=14, height=0, bg="#3C3F41", fg="#BBBBBB", font='Consolas 11 bold')
button4.grid(row=6, column=1, sticky='W')
button5 = Button(master=main_root, text="Interchange", command=set_Interchange, width=14, height=0, bg="#3C3F41", fg="#BBBBBB", font='Consolas 11 bold')
button5.grid(row=7, column=1, sticky='W')
lbl = Label(master=main_root, text='', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11 bold')
lbl.grid(row=8, column=1, sticky=' ')
lbl = Label(master=main_root, text='', bg="#3C3F41", fg="#BBBBBB", font='Consolas 11 bold')
lbl.grid(row=9, column=1, sticky=' ')
lbl = Label(master=main_root, text='v0.3', bg="#3C3F41", fg="#BBBBBB", font='Consolas 9 bold')
lbl.grid(row=10, column=2, sticky='SE')

main_root.protocol("WM_DELETE_WINDOW", on_closing)
mainloop()

def callback(event):
    canvas.create_image(0, 0, anchor=NW, image=img)
    global xp
    global yp
    python_green = "#004EFF"
    x1, y1 = (xp - 5), (yp - 5)
    x2, y2 = (xp + 5), (yp + 5)
    canvas.create_oval(x1, y1, x2, y2, fill=python_green)

    lbl.config(text="Current pos: " + str(event.x) + " " + str(event.y))
    global xpos, ypos
    xpos = event.x
    ypos = event.y
    # √((x_2-x_1)²+(y_2-y_1)²)
    if xp != 0 and yp != 0:
        # math.trunc
        dist = math.floor(math.sqrt((xp - event.x) ** 2 + (yp - event.y) ** 2) / ratio[map] * 50*10)/10
        lbl3.config(text="| Distance: " + str(dist) + 'm')

        canvas.create_line(xp, yp, xpos, ypos, width=2, fill=python_green)

    python_green = "#FF000d"
    x1, y1 = (xpos - 3), (ypos - 3)
    x2, y2 = (xpos + 3), (ypos + 3)
    canvas.create_oval(x1, y1, x2, y2, fill=python_green)




def set_pos():
    global xp
    global yp
    xp = xpos
    yp = ypos
    canvas.create_image(0, 0, anchor=NW, image=img)
    python_green = "#004EFF"
    x1, y1 = (xpos - 5), (ypos - 5)
    x2, y2 = (xpos + 5), (ypos + 5)
    canvas.create_oval(x1, y1, x2, y2, fill=python_green)

    lbl2.config(text="| Player pos: " + str(xpos) + " " + str(ypos))


root = Tk()
root.configure(background="#3C3F41")
root.title('EFT Distance Calculator')
root.resizable(False, False)

img = PhotoImage(file=maps[map] + '.ppm')

canvas = Canvas(root, width=img.width(), height=HEIGHT, bg="#3C3F41")
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor=NW, image=img)
canvas.bind("<Button-1>", callback)
canvas.pack()


button = Button(master=root, text="Set pos", command=set_pos, width=14, height=0, bg="#3C3F41", fg="#BBBBBB", font='Consolas 11 bold')
button.place(y=HEIGHT - 30, x=0)
lbl = Label(master=root, text='Current pos:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 15 bold')
lbl.place(y=HEIGHT - 29, x=130)

lbl2 = Label(master=root, text='| Player pos:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 15 bold')
lbl2.place(y=HEIGHT - 29, x=450)

lbl3 = Label(master=root, text='| Distance:', bg="#3C3F41", fg="#BBBBBB", font='Consolas 15 bold')
lbl3.place(y=HEIGHT - 29, x=790)

mainloop()



