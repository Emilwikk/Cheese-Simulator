# Python Cheese Simulator


import pyglet
import math
from pyglet import shapes

# Create a window
screenHeight = 1024
screenWidth = 2000
window=pyglet.window.Window(screenWidth,screenHeight,"Cheese Simultator")

# Set background color
pyglet.gl.glClearColor(0.1, 0.1, 0.1, 1.0)

gravity = 9.81*100
rad = 10
k = 850
global dragging
global chosenP
fricTol = 0.01
fricCoef = 0.5

cheeseBatch = pyglet.graphics.Batch()

class cheeseParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

        # Velocity for half dt forward, for leap frog algorithm
        self.vxHalf = 0
        self.vyHalf = 0
        self.shape = shapes.Circle(x, y, rad, color=(250, 225, 10), batch=cheeseBatch)
    def update(self,dt):
        #self.x += self.vx*dt
        #self.y += self.vy*dt

        # Leap frog position
        self.x += self.vxHalf*dt
        self.y += self.vyHalf*dt

        #Collision with floor, ceiling and walls
        if self.x<rad or self.x>1280-rad:
            self.vx = -0.8*self.vx
        if self.y<rad or self.y>1024-rad:
            self.vy = -0.8*self.vy

        # Address the sinking through floor issue
        if self.y-rad<0:
            self.y = rad
            if self.vyHalf<0:
                self.vyHalf *= -0.8
                if self.vyHalf<1:
                    self.vyHalf = 0

        # Ceiling
        if self.y+rad>screenHeight:
            self.y = screenHeight-rad
            if self.vyHalf>0:
                self.vyHalf *= -0.8
                if self.vyHalf>-1:
                    self.vyHalf = 0

        # Right wall
        if self.x+rad>screenWidth:
            self.x = screenWidth-rad
            if self.vxHalf>0:
                self.vxHalf *= -0.8
                if self.vxHalf>-1:
                    self.vxHalf = 0

        # Left wall
        if self.x-rad<0:
            self.x = rad
            if self.vxHalf<0:
                self.vxHalf *= -0.8
                if self.vxHalf<1:
                    self.vxHalf = 0


        # Acceleration due to gravity
        self.vyHalf -= gravity*dt

        # Friction
        if self.y < rad+fricTol:
            self.vxHalf += (1-2*(self.vxHalf>0))*fricCoef*gravity*dt

        self.shape.x = self.x
        self.shape.y = self.y 

class spring:
    def __init__(self, a, b, restLength, k):
        # a and b are the particles connected by the spring
        self.a = a
        self.b = b
        self.restLength = restLength
        self.k = k
    def halfForce(self,dt):
        xDist = self.b.x-self.a.x
        yDist = self.b.y-self.a.y
        dist = math.sqrt(xDist*xDist+yDist*yDist)

        # No division by zero pls    
        if dist == 0:
            return
        
        # Magnitude of force
        fMag = self.k*(self.restLength-dist)
        # Force components
        fx = fMag*(xDist/dist)
        fy = fMag*(yDist/dist)

        # Damping
        dampCoef = 3
        dx = xDist/dist
        dy = yDist/dist

        relVx = self.b.vx-self.a.vx
        relVy = self.b.vy-self.a.vy
        dot = relVx*dx + relVy*dy # Projection of velocity along spring

        damp_fx = dampCoef*dot*dx
        damp_fy = dampCoef*dot*dy

        fx = fx - damp_fx
        fy = fy - damp_fy
        
        #Leap frog half step
        self.a.vxHalf -= 0.5*dt*fx
        self.a.vyHalf -= 0.5*dt*fy
        self.b.vxHalf += 0.5*dt*fx
        self.b.vyHalf += 0.5*dt*fy

    def Force(self,dt):
        xDist = self.b.x-self.a.x
        yDist = self.b.y-self.a.y
        dist = math.sqrt(xDist*xDist+yDist*yDist)

        # No division by zero pls    
        if dist == 0:
            return
        
        # Magnitude of force
        fMag = self.k*(self.restLength-dist)
        # Force components
        fx = fMag*(xDist/dist)
        fy = fMag*(yDist/dist)

        # Damping
        dampCoef = 3
        dx = xDist/dist
        dy = yDist/dist

        relVx = self.b.vxHalf-self.a.vxHalf
        relVy = self.b.vyHalf-self.a.vyHalf
        dot = relVx*dx + relVy*dy # Projection of velocity along spring

        damp_fx = dampCoef*dot*dx
        damp_fy = dampCoef*dot*dy

        fx = fx - damp_fx
        fy = fy - damp_fy

        # Leap frog final step
        self.a.vx = self.a.vxHalf-0.5*fx*dt
        self.a.vy = self.a.vyHalf-0.5*fy*dt
        self.b.vx = self.b.vxHalf+0.5*fx*dt
        self.b.vy = self.b.vyHalf+0.5*fy*dt
    

        


p1 = cheeseParticle(500,500)
p2 = cheeseParticle(p1.x+2*rad,p1.y)
p3 = cheeseParticle(p1.x+4*rad,p1.y)
p4 = cheeseParticle(p1.x, p1.y-2*rad)
p5 = cheeseParticle(p2.x,p1.y-2*rad)
p6 = cheeseParticle(p3.x,p1.y-2*rad)
cheeseParticles = [p1, p2, p3, p4, p5, p6]

s12 = spring(p1, p2, 2*rad, k)
s14 = spring(p1, p4, 2*rad, k)
s15 = spring(p1, p5, 2*rad, k)
s23 = spring(p2, p3, 2*rad, k)
s24 = spring(p2, p4, 2*rad, k)
s25 = spring(p2, p5, 2*rad, k)
s26 = spring(p2, p6, 2*rad, k)
s35 = spring(p3, p5, 2*rad, k)
s36 = spring(p3, p6, 2*rad, k)
s45 = spring(p4, p5, 2*rad, k)
s56 = spring(p5, p6, 2*rad, k)
springs = [s12, s14, s15, s23, s24, s25, s26, s35, s36, s45, s56]

def find_particle(x,y,cheeseParticles):
    for p in cheeseParticles:
        #if x<p.x+rad and x>p.x-rad and y<p.y+rad and y>p.y-rad:
        if (p.x-x)*(p.x-x) + (p.y-y)*(p.y-y) < rad*rad:
            return p
    return 

def update(dt):
    for s in springs:
        s.halfForce(dt)

    for p in cheeseParticles:
        p.update(dt)

    for s in springs:
        s.Force(dt)
    
@window.event
def on_mouse_press(x,y,button,modifier):
    global chosenP
    global dragging
    chosenP = find_particle(x,y,cheeseParticles)
    if chosenP != None:
        chosenP.x = x
        chosenP.y = y
        chosenP.vx = 0
        chosenP.vy = 0
        dragging = True

@window.event
def on_mouse_release(x,y,button,modifier):
    global dragging
    global chosenP
    dragging = False

@window.event
def on_mouse_drag(x,y,dx,dy,button,modifier):
    global chosenP
    global dragging
    if dragging == True:
        chosenP.x = x
        chosenP.y = y
        chosenP.vx = dx
        chosenP.vy = dy
        chosenP.vxHalf = dx
        chosenP.vyHalf = dy


# 60 fps
pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    cheeseBatch.draw()

# Run the app loop
pyglet.app.run()