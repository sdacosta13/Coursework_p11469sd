from tkinter import *
from PIL import ImageTk
from PIL import Image as ImagePIL
from functools import partial
import math
import random
import database
import sys
"""
Written By Sam da Costa
References
character sprites: https://davidjakubec.itch.io/characters-sprite-sheet
Dungeon sprites: https://0x72.itch.io/dungeontileset-ii
Zombie sprites: https://opengameart.org/content/zombie-animations
Shotgun shell sprite: https://opengameart.org/content/shotgun-0
MG ammo: https://opengameart.org/content/2d-guns
Backdrop for the menu: https://opengameart.org/content/opp2017-castle-tiles
https://opengameart.org/content/game-over-5
"""


def getPlatform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'win32': 'Windows',
        'linux': 'Linux'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


global osName
osName = getPlatform()

hitsOn = False


def overlapping(a, b):
    global app

    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    else:
        return False


def getMatrix(obj):
    x = obj.x
    y = obj.y
    list1 = [x - (obj.targetWidth/2), y - (obj.targetHeight/2),
             x + (obj.targetWidth/2), y + (obj.targetHeight/2)]
    return list1


class App():
    def __init__(self):
        global osName
        self.width = 1920
        self.height = 1080
        self.page = "Menu"
        self.spacePressed = 0
        self.saveName = ""
        self.saving = 0
        self.mouseX = 0
        self.mouseY = 0
        self.boss = 0
        self.window = Tk()
        self.window.title("Game")
        self.window.resizable(0, 0)
        self.window.geometry('%dx%d' % (self.width, self.height))
        self.canvas = Canvas(self.window, bg="red", width=self.width, height=self.height)
        self.canvas.focus_set()
        self.loopSpeed = 25
        self.ticks = 0
        self.moonwalk = 0
        self.zombies = []
        self.tickText = self.canvas.create_text(
            self.width-100, 15, fill="white", font="Verdana 20 italic bold", text=str(self.ticks))
        self.leaderboardText = self.canvas.create_text(
            self.width/2, self.height/16, fill="white", font="Verdana 40 italic bold", text="Leaderboard", state="hidden")

        self.images = []
        self.multiplier = 1
        self.score = 0
        self.drops = []
        self.paused = False
        self.leaderboardB = self.canvas.create_rectangle(
            0, 0, self.width, self.height, fill="red", state="hidden")
        self.gameover = False
        if(osName == "Windows"):
            self.keys = {
                "Up Key": 87,
                "Left Key": 65,
                "Down Key": 83,
                "Right Key": 68,
                "Space": 32,
                "Machine Gun": 49,
                "Shotgun": 50,
                "Escape": 0,
                "Return": 0,
                "Boss Key": 0
            }
        else:
            self.keys = {
                "Up Key": 25,
                "Left Key": 38,
                "Down Key": 39,
                "Right Key": 40,
                "Space": 65,
                "Machine Gun": 10,
                "Shotgun": 11,
                "Escape": 9,
                "Return": 36,
                "Boss Key": 56
            }

    def gameloop(self):
        if self.boss:
            self.bossImg.setNormal()
        self.canvas.pack()
        if not self.paused:
            for i in self.zombies:
                i.age()
                if collideHitWithCoord(char.hitbox, i.x, i.y):
                    if i.state == "walk":
                        self.gameover = True
            for z in self.drops:
                if collideHitWithCoord(char.hitbox, z.x, z.y):
                    if z.choice == "Machine Gun":
                        char.weapon.mgAmmo += 15
                    elif z.choice == "Shotgun":
                        char.weapon.shotAmmo += 4
                    self.drops.remove(z)
                    z.kill()
            char.weapon.buffer += 1
            if char.weapon.buffer >= char.weapon.firerate:
                char.weapon.buffer = 0
                if char.weapon.mgFiring and char.weapon.currentWeapon == "Machine Gun":
                    if char.x <= self.mouseX:
                        char.weapon.fire(char.weapon.rotation)
                    else:
                        char.weapon.fire(char.weapon.rotation+math.pi)
            for i in self.zombies:
                for j in char.weapon.bullets:
                    if i != None and j != None:
                        if i.state == "walk":
                            if overlapping(getMatrix(i), getMatrix(j)):
                                if random.randint(0, 5) == 1:
                                    self.drops.append(Drop(i.x, i.y))
                                i.kill()
                                j.kill()

                                self.score += 10
            if self.zombies == []:
                self.multiplier += 2
                for i in range(self.multiplier):
                    self.zombies.append(Zombie())
            self.ticks += 1
            self.canvas.itemconfigure(self.tickText, text=str(self.score))
            if char.weapon.currentWeapon == "Machine Gun":
                self.canvas.itemconfigure(self.ammoText, text="Ammo: " + str(char.weapon.mgAmmo))
            elif char.weapon.currentWeapon == "Shotgun":
                self.canvas.itemconfigure(self.ammoText, text="Ammo: " + str(char.weapon.shotAmmo))

            char.move()
            char.weapon.pointAtMouse()
            char.weapon.advance()
        if not self.gameover:
            if self.page == "Menu":
                self.window.after(self.loopSpeed, self.runMenu)
            else:
                self.window.after(self.loopSpeed, self.gameloop)
        else:
            self.page = "Menu"

            self.window.after(self.loopSpeed, self.gameOverScreen)

    def gameOverScreen(self, event=None):
        self.gameOverScreen1 = Background(self.width, self.height, name="game_over.png")
        self.canvas.tag_raise(self.gameOverScreen1)
        self.window3 = SaveWindow()
        #self.window.after(5000, self.saveScore)

    def saveScore(self, event=None):
        while self.window3.data == "":
            pass
        database.update(app.saveName, char.weapon.shotAmmo,
                        char.weapon.mgAmmo, self.multiplier, self.score)
        self.window.after(5, self.runMenu)

    def resetGame(self):
        self.multiplier = 1
        self.zombies = []
        self.gameover = False
        char.weapon.mgAmmo = 60
        char.weapon.shotAmmo = 16
        self.score = 0

    def unpause(self, event=None):
        for i in range(len(self.pauseB)):
            self.pauseB[i].setHidden()
        self.paused = False

    def pause(self, event):
        for i in range(len(self.pauseB)):
            self.pauseB[i].setNormal()
        self.paused = True

    def linkFunc(self, event):
        self.resetGame()
        self.unpause()
        self.main()

    def startWithRec(self, event=None):
        data = self.window2.data
        char.weapon.shotAmmo = data[0]
        char.weapon.mgAmmo = data[1]
        self.multiplier = data[2]
        self.score = data[3]
        self.zombies = []
        self.unpause()
        self.main()

    def setMenuToShow(self, event=None):
        self.page = "Menu"

    def saveGame(self, event=None):
        self.window1 = SaveWindow()

    def loadGame(self, event=None):
        self.window2 = LoadWindow()

    def changeKeys(self, event=None):
        self.window4 = Keys()

    def runMenu(self, event=None):
        self.leaderboardButton = MenuButton(
            self.width, self.height, "Menu", 13, bindFunc=self.returnToMenu)
        self.leaderboardButton.setHidden()
        self.bossImg = Background2(self.width, self.height, "excel.png")
        self.bossImg.setHidden()
        self.backgroundMenu = Background(self.width, self.height, name="guide_castle.png")
        self.pauseB = [MenuButton(self.width, self.height,
                                  "Return to Game", 1, bindFunc=self.unpause),
                       MenuButton(self.width, self.height,
                                  "Save", 3, bindFunc=self.saveGame),
                       MenuButton(self.width, self.height,
                                  "Key Bindings", 5, bindFunc=self.changeKeys),
                       MenuButton(self.width, self.height,
                                  "Cheat Codes", 7, bindFunc=self.unpause),
                       MenuButton(self.width, self.height,
                                  "Exit to menu", 9, bindFunc=self.setMenuToShow)]
        for i in self.pauseB:
            i.setHidden()

        self.menuButtons = []
        coords = [
            (self.width/2)-(self.width/8), self.height/16,
            (self.width/2)+(self.width/8), 3*self.height/16
        ]

        self.menuButtons.append(MenuButton(self.width, self.height, "Intresting game name", 1))
        self.menuButtons.append(MenuButton(self.width, self.height,
                                           "Start game", 4, bindFunc=self.linkFunc))
        self.menuButtons.append(MenuButton(self.width, self.height,
                                           "Load Game", 7, bindFunc=self.loadGame))
        self.menuButtons.append(MenuButton(self.width, self.height,
                                           "Leaderboard", 10, bindFunc=self.loadBoard))
        self.canvas.pack()
        self.window.mainloop()
        # self.canvas.itemconfigure(self.backgroundMenu, status="hidden")

    def main(self, event=None):
        self.page = "Gameloop"
        self.backgroundGame = Background(self.width, self.height)
        self.weaponText = self.canvas.create_text(
            200, 15, fill="white", font="Verdana 20 italic bold", text="Weapon: "+char.weapon.currentWeapon)
        self.ammoText = self.canvas.create_text(
            600, 15, fill="white", font="Verdana 20 italic bold", text="Ammo: "+str(char.weapon.shotAmmo))
        self.canvas.tag_raise(char.img)
        self.canvas.tag_raise(char.weapon.skin)
        self.canvas.bind("<KeyPress>", self.keyPressedHandler)
        self.canvas.bind("<KeyRelease>", self.releaseHandler)
        self.canvas.bind("<Motion>", self.handleMouseMovement)
        for i in range(self.multiplier):
            self.zombies.append(Zombie())
        self.canvas.tag_raise(self.tickText)
        self.canvas.pack()
        self.gameloop()

    def loadBoard(self, event=None):
        self.canvas.itemconfigure(self.leaderboardB, state="normal")
        self.canvas.tag_raise(self.leaderboardB)
        self.canvas.itemconfigure(self.leaderboardText, state="normal")
        self.canvas.tag_raise(self.leaderboardText)
        self.leaderboardButton.setNormal()
        data = database.getScores()
        self.leaderboardRecs = []
        if(len(data) > 10):
            data = data[0:10]
        for i in range(len(data)):
            self.leaderboardRecs.append(self.canvas.create_text(self.width/2, (self.height/16)*(i+2),
                                                                fill="white", font="Verdana 20 italic bold", text=str(data[i][0]) + " " + str(data[i][1])))

    def returnToMenu(self, event=None):
        self.canvas.itemconfigure(self.leaderboardB, state="hidden")
        self.canvas.itemconfigure(self.leaderboardText, state="hidden")
        self.leaderboardButton.setHidden()
        for i in self.leaderboardRecs:
            self.canvas.itemconfigure(i, state="hidden")

    def handleMouseMovement(self, event):
        self.mouseX, self.mouseY = event.x, event.y

    def keyPressedHandler(self, event):
        if event.keycode == self.keys["Boss Key"]:
            if not self.boss:
                self.bossImg.setNormal()
                self.boss = 1
                print("run1")
                for i in self.zombies:
                    i.setNormal()
            else:
                self.bossImg.setHidden()
                self.boss = 0
                print("run2")
                for i in self.zombies:
                    i.setHidden()
        if not self.saving:
            if event.keycode == self.keys["Up Key"]:
                # w pressed
                char.upPressed()
            elif event.keycode == self.keys["Left Key"]:
                # a pressed
                char.leftPressed()
            elif event.keycode == self.keys["Down Key"]:
                # s pressed
                char.downPressed()
            elif event.keycode == self.keys["Right Key"]:
                # d pressed
                char.rightPressed()
            elif event.keycode == self.keys["Space"]:
                char.weapon.mgFiring = True
                if (not self.spacePressed) and char.weapon.currentWeapon == "Shotgun":
                    if char.x <= self.mouseX:
                        char.weapon.fire(char.weapon.rotation)
                    else:
                        char.weapon.fire(char.weapon.rotation+math.pi)
                    self.spacePressed = 1
            elif event.keycode == self.keys["Machine Gun"]:
                char.weapon.currentWeapon = "Machine Gun"
                self.canvas.itemconfig(self.weaponText, text="Weapon: Machine Gun")
            elif event.keycode == self.keys["Shotgun"]:
                char.weapon.currentWeapon = "Shotgun"
                self.canvas.itemconfig(self.weaponText, text="Weapon: Shotgun")
            elif event.keycode == self.keys["Escape"]:
                if app.paused:
                    self.unpause(0)
                else:
                    self.pause(0)

    def releaseHandler(self, event):
        if not self.saving:
            if event.keycode == self.keys["Up Key"]:
                char.upRelease()
            if event.keycode == self.keys["Left Key"]:
                char.leftRelease()
            if event.keycode == self.keys["Down Key"]:
                char.downRelease()
            if event.keycode == self.keys["Right Key"]:
                char.rightRelease()
            if event.keycode == self.keys["Space"]:
                char.weapon.mgFiring = False
                if self.spacePressed:
                    self.spacePressed = 0


class MenuButton:
    def __init__(self, width, height, text, pos, fillCol="blue", bindFunc=None):
        global app
        coords = [
            (width/2)-(width/8), height*(pos/16),
            (width/2)+(width/8), height*((pos+2)/16)
        ]
        textCoord = [
            width/2, height*(pos+1)/16
        ]
        self.rect = app.canvas.create_rectangle(*coords, fill=fillCol)
        self.text = app.canvas.create_text(
            textCoord, text=text, fill="white", font="Verdana 20 italic bold")
        app.canvas.tag_bind(self.rect, "<Button-1>", bindFunc)
        app.canvas.tag_bind(self.text, "<Button-1>", bindFunc)
        app.canvas.tag_raise(self.rect)
        app.canvas.tag_raise(self.text)

    def setHidden(self):
        app.canvas.itemconfigure(self.rect, state="hidden")
        app.canvas.itemconfigure(self.text, state="hidden")
        app.canvas.tag_lower(self.rect)
        app.canvas.tag_lower(self.text)

    def setNormal(self):
        app.canvas.itemconfigure(self.rect, state="normal")
        app.canvas.itemconfigure(self.text, state="normal")

        app.canvas.tag_raise(self.rect)
        app.canvas.tag_raise(self.text)


class Weapon:
    def __init__(self, x, y):
        global app
        self.rotation = 0
        width = 10
        self.length = 70
        self.x = x
        self.y = y
        self.currentWeapon = "Shotgun"  # MG or Shotgun
        self.references = []
        self.coords = [x, y, x+self.length, y]
        self.bullets = []
        self.skin = app.canvas.create_line(self.coords, fill="brown", width=width)
        app.canvas.tag_lower(self.skin)
        self.mgFiring = False
        self.buffer = 0
        self.firerate = 8  # increase to slow
        self.shotAmmo = 16
        self.mgAmmo = 60

    def move(self, x, y):
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
            self.coords = self.x, self.y, self.x + \
                (self.length*math.cos(angle+math.pi)), self.y+(self.length*math.sin(angle+math.pi))
        else:
            self.coords = self.x, self.y, self.x + \
                (self.length*math.cos(angle)), self.y+(self.length*math.sin(angle))
        app.canvas.coords(self.skin, self.coords)

    def fire(self, angle):
        if self.currentWeapon == "Machine Gun" and self.mgAmmo != 0:
            buck = Buckshot(self.x, self.y, angle, 45)
            self.bullets.append(buck)
            self.mgAmmo -= 1

        elif self.currentWeapon == "Shotgun" and self.shotAmmo != 0:
            buck1 = Buckshot(self.x, self.y, angle, 45)
            buck2 = Buckshot(self.x, self.y, angle+math.pi/32, 45)
            buck3 = Buckshot(self.x, self.y, angle-math.pi/32, 45)
            self.bullets.append(buck1)
            self.bullets.append(buck2)
            self.bullets.append(buck3)
            buck4 = Buckshot(self.x, self.y, angle, 45)
            buck5 = Buckshot(self.x, self.y, angle+math.pi/32, 45)
            buck6 = Buckshot(self.x, self.y, angle-math.pi/32, 45)
            self.bullets.append(buck4)
            self.bullets.append(buck5)
            self.bullets.append(buck6)
            self.shotAmmo -= 1

    def advance(self):

        for i in self.bullets:

            if i.fRange == 0:
                i.kill()

            else:
                i.advance()


class SaveWindow:
    def __init__(self):
        self.top = Toplevel()
        self.top.title("Please enter your name")
        self.entry = Entry(self.top)
        self.entry.pack()
        self.button = Button(self.top, text="Enter", command=self.quit)
        self.button.pack()
        self.data = ""

    def quit(self):
        app.saveName = self.entry.get()
        self.data = self.entry.get()
        database.update(app.saveName, char.weapon.shotAmmo,
                        char.weapon.mgAmmo, app.multiplier, app.score)
        if app.gameover:
            app.window.after(5, app.saveScore)
        self.top.destroy()


class LoadWindow:
    def __init__(self):
        self.top = Toplevel()
        self.top.title("Please Select Your Profile")
        self.var = StringVar(self.top)
        self.var.set("")
        data = database.queryForNames()
        newData = []
        for i in data:
            newData.append(str(i[0]))
        self.selector = OptionMenu(self.top, self.var, *newData)
        self.selector.pack()
        self.button = Button(self.top, text="Enter", command=self.quit)
        self.button.pack()

    def quit(self):
        if self.var != "":
            userName = self.var.get()
            self.data = database.query(userName)
            self.top.destroy()
            app.startWithRec()


class Keys:
    def __init__(self):
        self.top = Toplevel()
        self.top.title("Change Keys")

        self.labels = []
        self.labelsText = []
        self.buttons = []
        self.stringVars = []
        self.focus = ""
        i = 0
        for key, value in app.keys.items():

            self.labels.append(Label(self.top, text=key).grid(row=i, column=0))
            self.labelsText.append(key)
            buttonWithArg = partial(self.setKey, i)
            x = StringVar(self.top, value)
            self.stringVars.append(x)
            self.buttons.append(Button(self.top, textvariable=x,
                                       command=buttonWithArg).grid(row=i, column=1))

            i += 1
        self.top.bind("<KeyPress>", self.handleInput)
        self.quitBut = Button(self.top, text="Quit", command=self.quit).grid(row=i+1, column=1)

    def handleInput(self, event=None):
        if self.focus != "":
            app.keys[self.focus] = event.keycode
            pos = self.labelsText.index(self.focus)
            self.stringVars[pos].set(event.keycode)

    def setKey(self, button):
        self.focus = self.labelsText[button]

    def quit(self, event=None):
        self.top.destroy()


class Zombie:
    def __init__(self):
        global app

        self.x = random.randint(0, app.width)
        self.y = random.randint(0, app.height)
        self.imageName = "appear/appear_1.png"
        self.imageID = 1
        img = ImagePIL.open(self.imageName)
        self.targetWidth = 72
        self.targetHeight = 94
        img = img.resize((self.targetWidth, self.targetHeight))
        photoImg = ImageTk.PhotoImage(img, master=app.window)
        self.imgRef = photoImg
        self.img = app.canvas.create_image(self.x, self.y, image=photoImg)
        self.buffer = 0
        self.state = "birth"
        self.speed = 5
        self.direction = "L"

    def setHidden(self):
        app.canvas.itemconfigure(self.img, state="hidden")

    def setNormal(self):
        app.canvas.itemconfigure(self.img, state="normal")

    def move(self):
        if not((char.x - self.x) == 0):
            angle = math.atan((char.y-self.y)/(char.x-self.x))
        else:
            angle = math.pi/2
        if char.x < self.x:
            angle += math.pi

        if char.x < self.x:
            if app.moonwalk:
                self.direction = "R"
            else:
                self.direction = "L"
        else:
            if app.moonwalk:
                self.direction = "L"
            else:
                self.direction = "R"

        moveX = self.speed*math.cos(angle)
        moveY = self.speed*math.sin(angle)
        self.x += moveX
        self.y += moveY

    def age(self):
        if self.state == "walk":
            self.move()

        if self.buffer > 1:
            self.buffer = 0
            if self.state == "birth":
                if self.imageID < 10:
                    self.imageID += 1
                    self.imageName = list(self.imageName)
                    self.imageName[14] = str(self.imageID)
                    self.imageName = "".join(self.imageName)
                    img = ImagePIL.open(self.imageName)
                    img = img.resize((72, 94))
                    photoImg = ImageTk.PhotoImage(img, master=app.window)
                    self.imgRef = photoImg
                    self.img = app.canvas.create_image(self.x, self.y, image=photoImg)
                    if self.imageID == 10:
                        self.state = "walk"
                        self.imageID = 0
                        self.imageName = "walk//go_0L.png"
            elif self.state == "walk":
                if self.imageID < 10:
                    self.imageName = list(self.imageName)
                    self.imageName[9] = str(self.imageID)
                    if self.direction == "R":
                        self.imageName[10] = "R"
                    elif self.direction == "L":
                        self.imageName[10] = "L"
                    self.imageName = "".join(self.imageName)
                    img = ImagePIL.open(self.imageName)
                    img = img.resize((72, 94))
                    photoImg = ImageTk.PhotoImage(img, master=app.window)
                    self.imgRef = photoImg
                    self.img = app.canvas.create_image(self.x, self.y, image=photoImg)
                    self.imageID += 1
                if self.imageID == 10:
                    self.imageID = 0
            elif self.state == "die":
                if self.imageID < 8:
                    self.imageName = list(self.imageName)
                    self.imageName[9] = str(self.imageID)
                    self.imageName = "".join(self.imageName)
                    img = ImagePIL.open(self.imageName)
                    img = img.resize((72, 94))
                    photoImg = ImageTk.PhotoImage(img, master=app.window)
                    self.imgRef = photoImg
                    self.img = app.canvas.create_image(self.x, self.y, image=photoImg)
                    self.imageID += 1
                    if self.imageID == 8:
                        del app.zombies[app.zombies.index(self)]

        else:
            self.buffer += 1

    def kill(self):
        self.imageID = 1
        self.state = "die"
        self.imageName = "die//die_1.png"


class Buckshot:
    def __init__(self, x, y, angle, fRange):
        img = ImagePIL.open("buckshot.png")
        self.targetWidth = 20
        self.targetHeight = 20
        img = img.resize((self.targetWidth, self.targetHeight))
        photoImg = ImageTk.PhotoImage(img, master=app.window)
        char.weapon.references.append(photoImg)
        self.img = app.canvas.create_image(x, y, image=photoImg)
        self.angle = angle

        self.fRange = fRange
        self.x = x
        self.y = y
        self.distance = 45

    def advance(self):
        if self.fRange != 0:
            self.fRange -= 1
            moveX = self.distance*math.cos(self.angle)
            moveY = self.distance*math.sin(self.angle)
            app.canvas.move(self.img, moveX, moveY)
            self.x += moveX
            self.y += moveY

    def kill(self):
        app.canvas.delete(self.img)
        del char.weapon.bullets[char.weapon.bullets.index(self)]


def get2Dlist(x, y, fill="#"):
    outer = []
    for y1 in range(y):
        inner = []
        for x1 in range(x):
            inner.append(str(x1))
        outer.append(list(inner))
    return outer


class Background:
    def __init__(self, width, height, name="background.png"):
        img = ImagePIL.open(name)
        img = img.resize((width, height))
        photoImg = ImageTk.PhotoImage(img, master=app.window)
        app.window.background = photoImg
        self.img = app.canvas.create_image(width/2, height/2, image=photoImg)
        app.canvas.tag_lower(photoImg)


class Background2:
    def __init__(self, width, height, name):
        img = ImagePIL.open(name)
        img = img.resize((width, height))
        photoImg = ImageTk.PhotoImage(img, master=app.window)
        self.ref = photoImg
        self.img = app.canvas.create_image(width/2, height/2, image=photoImg)

    def setHidden(self):
        app.canvas.itemconfigure(self.img, state="hidden")
        app.canvas.tag_lower(self.img)

    def setNormal(self):
        app.canvas.itemconfigure(self.img, state="normal")
        app.canvas.tag_raise(self.img)


class Drop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        width = app.width
        height = app.height
        self.choice = random.choice(["Shotgun", "Machine Gun"])
        if self.choice == "Shotgun":
            img = ImagePIL.open("shell.png")
        elif self.choice == "Machine Gun":
            img = ImagePIL.open("ammobox.png")
        img = img.resize((int(width/20), int(height/20)))
        photoImg = ImageTk.PhotoImage(img, master=app.window)
        self.imageRef = photoImg
        app.canvas.create_image(x, y, image=photoImg)

    def kill(self):
        del self


def collideHitWithCoord(hitbox, x, y):
    coords = app.canvas.coords(hitbox)
    if (coords[0] < x < coords[2]) and (coords[1] < y < coords[3]):
        return True
    else:
        return False


class Sprite:
    def __init__(self, image, x, y, showHitbox=False):
        global app
        self.moveSpeed = 15
        img = PhotoImage(master=app.canvas, file=image)
        imgDimensions = [img.width(), img.height()]
        app.img = img
        self.img = app.canvas.create_image(x, y, image=img)

        if showHitbox:
            self.hitbox = app.canvas.create_oval(x-(imgDimensions[0]/2), y-(imgDimensions[1]/2), x+(
                imgDimensions[0]/2), y+(imgDimensions[1]/2), fill="blue", outline="")
        else:
            self.hitbox = app.canvas.create_oval(
                x-(imgDimensions[0]/2), y-(imgDimensions[1]/2), x+(imgDimensions[0]/2), y+(imgDimensions[1]/2), outline="")
        app.canvas.tag_raise(self.img)
        app.canvas.tag_lower(self.hitbox)


class Character(Sprite):
    def __init__(self, image, x, y, showHitbox=False):
        Sprite.__init__(self, image, x, y, showHitbox=showHitbox)
        self.movement = [0, 0, 0, 0]
        self.cFront = PhotoImage(master=app.canvas, file="cFront.png")
        self.cLeft = PhotoImage(master=app.canvas, file="cLeft.png")
        self.cRight = PhotoImage(master=app.canvas, file="cRight.png")
        self.cBehind = PhotoImage(master=app.canvas, file="cBehind.png")
        self.weapon = Weapon(x, y)
        self.weapon.rotation = 0
        self.x = x
        self.y = y

    def upPressed(self):
        self.movement[0] = 1
        self.movement[2] = 0
        app.canvas.itemconfigure(self.img, image=self.cBehind)

    def leftPressed(self):
        self.movement[1] = 1
        self.movement[3] = 0
        app.canvas.itemconfigure(self.img, image=self.cLeft)

    def downPressed(self):
        self.movement[2] = 1
        self.movement[0] = 0
        app.canvas.itemconfigure(self.img, image=self.cFront)

    def rightPressed(self):
        self.movement[3] = 1
        self.movement[1] = 0
        app.canvas.itemconfigure(self.img, image=self.cRight)

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
            self.y -= self.moveSpeed

        if self.movement[1]:
            app.canvas.move(self.img, -self.moveSpeed, 0)
            app.canvas.move(self.hitbox, -self.moveSpeed, 0)
            self.weapon.move(-self.moveSpeed, 0)
            self.x -= self.moveSpeed

        if self.movement[2]:
            app.canvas.move(self.img, 0, self.moveSpeed)
            app.canvas.move(self.hitbox, 0, self.moveSpeed)
            self.weapon.move(0, self.moveSpeed)
            self.y += self.moveSpeed

        if self.movement[3]:
            app.canvas.move(self.img, self.moveSpeed, 0)
            app.canvas.move(self.hitbox, self.moveSpeed, 0)
            self.weapon.move(self.moveSpeed, 0)
            self.x += self.moveSpeed

    def updateSkin(self):
        if self.movement[0]:
            app.canvas.itemconfigure(self.img, image=self.cBehind)
        elif self.movement[1]:
            app.canvas.itemconfigure(self.img, image=self.cLeft)
        elif self.movement[2]:
            app.canvas.itemconfigure(self.img, image=self.cFront)
        elif self.movement[3]:
            app.canvas.itemconfigure(self.img, image=self.cRight)


global app
app = App()

char = Character("cFront.png", 100, 100, showHitbox=hitsOn)

app.runMenu()
