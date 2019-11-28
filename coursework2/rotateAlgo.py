def rotate(self, angle):
    temp = self.coords
    for i in range(0,len(temp),2):
        #move shape to origin then use matrix multiplication to rotate
        temp[i] -= self.x
        temp[i+1] -= self.y
        new = []
        #aliases

        x = temp[i]
        y = temp[i+1]
        new.append((x*math.cos(angle))-(y*math.sin(angle)))
        new.append((x*math.sin(angle))+(y*math.cos(angle)))

        temp[i] = new[0]
        temp[i+1] = new[1]

        #move back
        temp[i] += self.x
        temp[i+1] += self.y

    self.coords = temp
    app.canvas.coords(self.skin, self.coords)
    self.rotation += angle
def move(self,x,y):
    app.canvas.move(self.skin, x, y)
    self.x += x
    self.y += y
