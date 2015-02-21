G = 6.37e-11

import math, pygame, time, sys
from Vec2 import *

# pygame.init()
# screen = pygame.display.set_mode((640, 480))
# pixels = pygame.PixelArray(screen)

class Ship():
    def __init__(self, pos, mass, radius=0, force=Vec2(0, 0)):
        self.pos = pos
        self.mass = mass
        self.force = force
        self.radius = radius
    
    def add_force(self, vector):
        #self.force = vector_add(self.force, vector)
        self.force.add(vector)
    
    def update_pos(self):
        y_acceleration = self.force.x / self.mass
        x_acceleration = self.force.y / self.mass
        acceleration = math.sqrt(y_acceleration ** 2 + x_acceleration ** 2)
        self.pos[0] += x_acceleration
        self.pos[1] += y_acceleration

class Planet(Ship):
    def __init__(self, name, pos, mass, radius):
        super().__init__(pos, mass, radius)
        self.name = name
        
def vector_add(vec1, vec2):
    res = [vec1[0] + vec2[0], vec1[1] + vec2[1]]
    return res

def distance(planet1, planet2):
    return math.sqrt(((planet1.pos[0] - planet2.pos[0])**2) + ((planet1.pos[1] - planet2.pos[1])**2))

player_mass = 15000
masses = [5.97e24, 7.34e22]

earth = Planet("Earth", [2, 2], 5.97e24, 6378000)
#moon = Planet("Moon", [2, 2], 7.34e22, 1737000)
# mars = Planet("Mars", [3, 3], 7.34e22, 6378000)
# apollo = Planet("LEM", [3, 2], 15000, 10)
# man = Planet("Human", [3, 2], 70, 2)
ship = Ship(pos=[2, 100000], mass=15000)
# ship.add_force([-2, 0])
# ship.add_force([3, 0])
ships = [earth, ship]
while True:
    # for event in pygame.event.get():
        # if event.type == pygame.QUIT:
            # sys.exit()
    screen.fill((255, 255, 255)) #Fills screen with white
    ship.add_force(Vec2(0, 2500000))
    for planet in ships:
        for planet2 in ships:
            if not planet == planet2:
                force_magnitude = G * planet.mass * planet2.mass / (distance(planet, planet2) + planet.radius + planet2.radius) ** 2
                # if not planet.pos[1] - planet2.pos[1] == 0:
                    # force_ratio = math.fabs(planet.pos[0] - planet2.pos[0]) / math.fabs(planet.pos[1] - planet2.pos[1])
                    # force_angle = math.atan(force_ratio)
                    # force = [math.sin(force_angle) * force_magnitude, math.cos(force_angle) * force_magnitude]
                # else:
                    # force = [force_magnitude, 0]
                force = Vec2(planet2.pos[1] - planet.pos[1], planet2.pos[0] - planet.pos[0])
                force.normalize()
                force.multiply(force_magnitude)
                if hasattr(planet, "name") and hasattr(planet2, "name"):
                    print(planet.name, " and ", planet2.name, " is: ", force.x, force.y)
                elif hasattr(planet, "name") and not hasattr(planet2, "name"):
                    print(planet.name, " and Ship is: ", force.x, force.y)
                elif not hasattr(planet, "name") and hasattr(planet2, "name"):
                    print("Ship and ", planet2.name, " is: ", force.x, force.y)
                else:
                    print("Ship and Ship is: ", force.x, force.y)
                planet.add_force(force)

    print("Ship force:", ship.force.x / ship.mass, ship.force.y / ship.mass)
    print("Distance:", distance(earth, ship))
    for planet in ships:
        planet.update_pos()
        planet.force = Vec2(0, 0)
        #pixels[round(planet.pos[0] / 10000), round(planet.pos[1] / 10000)] = (0, 0, 0) #Draws a dot where the planet should be.
    print("Position:", ship.pos)
    #ship.force = Vec2(0, 0)
    print("")
    time.sleep(1)