from tkinter import *
from PIL import Image, ImageTk

import random
"""
Written By Sam da Costa
References
character sprites: https://davidjakubec.itch.io/characters-sprite-sheet
"""

hitsOn = True

def overlapping(a,b):
    a = canvas.coords(a)
    b = canvas.coords(b)

    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    else:
        return False



class App():
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.window = Tk()
        self.window.title("Game")
        self.window.resizable(0,0)
        self.window.geometry('%dx%d' % (self.width, self.height))
        self.canvas = Canvas(self.window, bg = "red", width = self.width, height = self.height)
        self.canvas.focus_force()
        self.loopSpeed = 10
        self.ticks = 0
        self.tickText = self.canvas.create_text(self.width-30, 15, fill = "white", font="Verdana 20 italic bold", text=str(self.ticks))

    def gameloop(self):
        self.ticks += 1
        self.canvas.itemconfigure(self.tickText, text = str(self.ticks))
        self.canvas.pack()
        char.move()
        self.window.after(self.loopSpeed,self.gameloop)

    def setBinds(self):
        self.canvas.bind()

    def main(self):
        self.canvas.bind("<KeyPress>", self.keyPressedHandler)
        self.canvas.bind("<KeyRelease>", self.releaseHandler)
        self.gameloop()
        self.canvas.pack()
        self.window.mainloop()

    def keyPressedHandler(self, event):
        print(event.keycode)
        """windowsKeys
        uKey = 87
        lKey = 65
        dKey = 83
        rKey = 68
        """
        uKey = 25
        lKey = 38
        dKey = 39
        rKey = 40
        if event.keycode == uKey:
            #w pressed
            char.upPressed()
        elif event.keycode == lKey:
            #a pressed
            char.leftPressed()
        elif event.keycode == dKey:
            #s pressed
            char.downPressed()
        elif event.keycode == rKey:
            #d pressed
            char.rightPressed()

    def releaseHandler(self, event):
        """windowsKeys
        uKey = 87
        lKey = 65
        dKey = 83
        rKey = 68
        linuxKeys
        """
        uKey = 25
        lKey = 38
        dKey = 39
        rKey = 40
        if event.keycode == uKey:
            char.upRelease()
        if event.keycode == lKey:
            char.leftRelease()
        if event.keycode == dKey:
            char.downRelease()
        if event.keycode == rKey:
            char.rightRelease()




class Sprite:
    def __init__(self, image, x, y, showHitbox = False):
        global app
        self.moveSpeed = 3
        img = PhotoImage(master = app.canvas, file=image)
        imgDimensions = [img.width(), img.height()]
        app.img = img
        self.img = app.canvas.create_image(x, y, image = img)



        if showHitbox:
            self.hitbox = app.canvas.create_oval(x-(imgDimensions[0]/2),y-(imgDimensions[1]/2),x+(imgDimensions[0]/2),y+(imgDimensions[1]/2),fill = "blue", outline ="")
        else:
            self.hitbox = app.canvas.create_oval(x-(imgDimensions[0]/2),y-(imgDimensions[1]/2),x+(imgDimensions[0]/2),y+(imgDimensions[1]/2), outline ="")
        app.canvas.tag_raise(self.img)
        app.canvas.tag_lower(self.hitbox)



class Character(Sprite):
    def __init__(self, image, x, y, showHitbox = False):
        Sprite.__init__(self, image, x, y, showHitbox = showHitbox)
        self.movement = [0,0,0,0]
        self.cFront = PhotoImage(master = app.canvas, file = "cFront.png")
        self.cLeft = PhotoImage(master = app.canvas, file = "cLeft.png")
        self.cRight = PhotoImage(master = app.canvas, file = "cRight.png")
        self.cBehind = PhotoImage(master = app.canvas, file = "cBehind.png")


    def upPressed(self):
        self.movement[0] = 1
        self.movement[2] = 0
        app.canvas.itemconfigure(self.img, image = self.cBehind)


    def leftPressed(self):
        self.movement[1] = 1
        self.movement[3] = 0
        app.canvas.itemconfigure(self.img, image = self.cLeft)

    def downPressed(self):
        self.movement[2] = 1
        self.movement[0] = 0
        app.canvas.itemconfigure(self.img, image = self.cFront)

    def rightPressed(self):
        self.movement[3] = 1
        self.movement[1] = 0
        app.canvas.itemconfigure(self.img, image = self.cRight)


    def upRelease(self):
        self.movement[0] = 0


    def leftRelease(self):
        self.movement[1] = 0


    def downRelease(self):
        self.movement[2] = 0


    def rightRelease(self):
        self.movement[3] = 0

    def move(self):
        if self.movement[0]:
            app.canvas.move(self.img, 0, -self.moveSpeed)
            app.canvas.move(self.hitbox, 0, -self.moveSpeed)
        if self.movement[1]:
            app.canvas.move(self.img, -self.moveSpeed, 0)
            app.canvas.move(self.hitbox, -self.moveSpeed, 0)
        if self.movement[2]:
            app.canvas.move(self.img, 0, self.moveSpeed)
            app.canvas.move(self.hitbox, 0, self.moveSpeed)
        if self.movement[3]:
            app.canvas.move(self.img, self.moveSpeed, 0)
            app.canvas.move(self.hitbox, self.moveSpeed, 0)








global app
app = App()

char = Character("cFront.png", 100,100, showHitbox = hitsOn)

app.main()
