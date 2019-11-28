from tkinter import *
from PIL import Image, ImageTk
import math
import random
"""
Written By Sam da Costa
References
character sprites: https://davidjakubec.itch.io/characters-sprite-sheet
Dungeon sprites: https://0x72.itch.io/dungeontileset-ii
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
        self.mouseX = 0
        self.mouseY = 0
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
        char.weapon.pointAtMouse()
        self.window.after(self.loopSpeed,self.gameloop)

    def setBinds(self):
        self.canvas.bind()

    def main(self):
        self.background = Background(self.width, self.height)
        self.canvas.bind("<KeyPress>", self.keyPressedHandler)
        self.canvas.bind("<KeyRelease>", self.releaseHandler)
        self.canvas.bind("<Motion>", self.handleMouseMovement)
        self.gameloop()
        self.canvas.pack()
        self.window.mainloop()

    def handleMouseMovement(self, event):
        self.mouseX, self.mouseY = event.x, event.y

    def keyPressedHandler(self, event):
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

class Weapon:
    def __init__(self, x, y):
        global app
        self.rotation = 0
        width = 10
        self.length = 70
        self.x = x
        self.y = y
        self.coords = [x,y,x+self.length, y]

        self.skin = app.canvas.create_line(self.coords,fill = "brown",width=width)
        app.canvas.tag_lower(self.skin)

    def move(self,x,y):
        app.canvas.move(self.skin, x, y)
        self.x += x
        self.y += y

    def pointAtMouse(self):
        if (app.mouseX-self.x != 0):
            angle = math.atan((app.mouseY-self.y)/(app.mouseX-self.x))
            self.rotate(angle)
            self.rotation = angle

    def rotate(self, angle):
        if app.mouseX < self.x:
            self.coords = [self.x, self.y, self.x+(self.length*math.cos(angle+math.pi)), self.y+(self.length*math.sin(angle+math.pi))]
        else:
            self.coords = [self.x, self.y, self.x+(self.length*math.cos(angle)), self.y+(self.length*math.sin(angle))]
        app.canvas.coords(self.skin, self.coords)
def get2Dlist(x,y,fill = "#"):
    outer = []
    for y1 in range(y):
        inner = []
        for x1 in range(x):
            inner.append(x1)
        outer.append(inner)
    return outer

class Background:
    def __init__(self, width, height):
        wFillNum = int(width/16)
        hFillNum = int(height/16)
        self.matrix = get2Dlist(wFillNum, hFillNum)
        for x in range(0, width, 16):
            for y in range(0, height, 16):
                choice = random.randint(1,9)
                if choice == 1:
                    img = PhotoImage(master = app.canvas, file="floor_1.png")

                elif choice == 2:
                    img = PhotoImage(master = app.canvas, file="floor_2.png")

                elif choice == 3:
                    img = PhotoImage(master = app.canvas, file="floor_3.png")

                elif choice == 4:
                    img = PhotoImage(master = app.canvas, file="floor_4.png")

                elif choice == 5:
                    img = PhotoImage(master = app.canvas, file="floor_5.png")

                elif choice == 6:
                    img = PhotoImage(master = app.canvas, file="floor_6.png")

                elif choice == 7:
                    img = PhotoImage(master = app.canvas, file="floor_7.png")

                elif choice == 8:
                    img = PhotoImage(master = app.canvas, file="floor_8.png")

                if not (y >= len(self.matrix) or x >= len(self.matrix[0])):
                    print("run")
                    self.matrix[y][x] = app.canvas.create_image(x,y, image = img)




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
        self.weapon = Weapon(x,y)
        self.weapon.rotation = 0

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
        self.updateSkin()


    def leftRelease(self):
        self.movement[1] = 0
        self.updateSkin()

    def downRelease(self):
        self.movement[2] = 0
        self.updateSkin()

    def rightRelease(self):
        self.movement[3] = 0
        self.updateSkin()

    def move(self):
        if self.movement[0]:
            app.canvas.move(self.img, 0, -self.moveSpeed)
            app.canvas.move(self.hitbox, 0, -self.moveSpeed)
            self.weapon.move(0, -self.moveSpeed)

        if self.movement[1]:
            app.canvas.move(self.img, -self.moveSpeed, 0)
            app.canvas.move(self.hitbox, -self.moveSpeed, 0)
            self.weapon.move(-self.moveSpeed, 0)

        if self.movement[2]:
            app.canvas.move(self.img, 0, self.moveSpeed)
            app.canvas.move(self.hitbox, 0, self.moveSpeed)
            self.weapon.move(0, self.moveSpeed)

        if self.movement[3]:
            app.canvas.move(self.img, self.moveSpeed, 0)
            app.canvas.move(self.hitbox, self.moveSpeed, 0)
            self.weapon.move(self.moveSpeed, 0)

    def updateSkin(self):
        if self.movement[0]:
            app.canvas.itemconfigure(self.img, image = self.cBehind)
        elif self.movement[1]:
            app.canvas.itemconfigure(self.img, image = self.cLeft)
        elif self.movement[2]:
            app.canvas.itemconfigure(self.img, image = self.cFront)
        elif self.movement[3]:
            app.canvas.itemconfigure(self.img, image = self.cRight)






global app
app = App()

char = Character("cFront.png", 100,100, showHitbox = hitsOn)

app.main()
