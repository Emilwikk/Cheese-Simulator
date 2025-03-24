import pyglet
import math
from pyglet import shapes

# Create a window
window=pyglet.window.Window(1280,1024,"Cheese Simultator")

# Set background color
pyglet.gl.glClearColor(0.1, 0.1, 0.1, 1.0)

gravity = 9.81
rad = 10
k = 25

cheeseBatch = pyglet.graphics.Batch()

class cheeseParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.shape = shapes.Circle(x, y, rad, color=(250, 225, 10), batch=cheeseBatch)
    def update(self):
        self.x += self.vx
        self.y += self.vy

        #Collision with floor and roof
        if self.x<rad or self.x>1280-rad:
            self.vx = -0.8*self.vx
        if self.y<rad or self.y>1024-rad:
            self.vy = -0.8*self.vy

        # Address the sinking through floor issue
        if self.y-rad<0:
            self.y = rad
            if self.vy<0:
                self.vy *= -0.8
                if self.vy<1:
                    self.vy = 0


        # Acceleration due to gravity
        self.vy -= gravity*0.016

        #Leap frog time 



        self.shape.x = self.x
        self.shape.y = self.y 

class spring:
    def __init__(self, a, b, restLength, k):
        # a and b are the particles connected by the spring
        self.a = a
        self.b = b
        self.restLength = restLength
        self.k = k
    def force(self,dt):
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

        # Apply to particles  (dv = F/m*dt where m and dt is both 1 => dv = F)
        self.a.vx -= fx*dt
        self.a.vy -= fy*dt
        self.b.vx += fx*dt
        self.b.vy += fy*dt
        

        


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

def update(dt):
    for s in springs:
        s.force(dt)

    for p in cheeseParticles:
        p.update()

# 60 fps
pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
    window.clear()
    cheeseBatch.draw()

# Run the app loop
pyglet.app.run()