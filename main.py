import pyglet
import math
from pyglet import shapes

# Create a window
window=pyglet.window.Window(1280,1024,"Cheese Simultator")

# Set background color
pyglet.gl.glClearColor(0.1, 0.1, 0.1, 1.0)

gravity = 9.81
rad = 10

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
        if self.x<0 or self.x>1280:
            self.vx = -0.8*self.vx
        if self.y<0 or self.y>1024:
            self.vy = -0.8*self.vy

        # Acceleration due to gravity
        self.vy -= gravity*0.016

        #Leap frog time 



        self.shape.x = self.x
        self.shape.y = self.y 

#class springs:
#    def __init__(self, a, b, restLength, k):
#        # a and b are the particles connected by the spring
#        self.a = a
#        self.b = b
#        self.restLength = restLength
#        self.k = k
#    def force(self):
#        xDist = self.b.x-self.a.x
#        yDist = self.b.y-self.a.y
#        dist = math.sqrt(xDist*xDist+yDist*yDist)
#
#        # No division by zero pls    
#        if dist == 0:
#            return
#        
#        # Magnitude of force
#        fMag = self.k*(self.restLength-dist)
#        # Force components
#        fx = fMag*(xDist/dist)
#        fy = fMag*(yDist/dist)
        

        


p1 = cheeseParticle(500,500)
p2 = cheeseParticle(p1.x+2*rad,p1.y)
p3 = cheeseParticle(p1.x+4*rad,p1.y)
p4 = cheeseParticle(p1.x, p1.y-2*rad)
p5 = cheeseParticle(p2.x,p1.y-2*rad)
p6 = cheeseParticle(p3.x,p1.y-2*rad)
cheeseParticles = [p1, p2, p3, p4, p5, p6]

def update(dt):
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