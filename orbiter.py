G = 6.37e-11

import math, pygame, time, sys
from Vec2 import *

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pixels = pygame.PixelArray(screen)
size_factor = 50000

class Ship():
    def __init__(self, pos, mass, radius=1, force=Vec2(0, 0), velocity=Vec2(0, 0), acceleration=Vec2(0, 0), name="Ship"):
        self.pos = pos
        self.mass = mass
        self.force = force
        self.radius = radius
        self.velocity = velocity
        self.acceleration = acceleration
        self.name = name
    
    def add_force(self, vector):
        self.force = self.force.plus(vector)
    
    def update_pos(self):
        self.acceleration = self.force.divideWith(self.mass)
        #acceleration = math.sqrt(y_acceleration ** 2 + x_acceleration ** 2)
        print(self.name)
        print("Acceleration:", self.acceleration.x, self.acceleration.y)
        print("Velocity:", self.velocity.x, self.velocity.y)
        self.velocity = self.velocity.plus(self.acceleration)
        print("Velocity:", self.velocity.x, self.velocity.y)
        self.pos[0] += self.velocity.x
        self.pos[1] += self.velocity.y
        print("")

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
ship = Ship(pos=[2, 7078000], mass=15000)
moon = Planet("Moon", [2, -8078000], 7.34e22, 1737000)
ships = [earth, ship, moon]
ship.add_force(Vec2(110000000, 0))
moon.add_force(Vec2(-5.37e+26, 0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((255, 255, 255)) #Fills screen with white
    for planet in ships:
        for planet2 in ships:
            if not planet == planet2:
                force_magnitude = G * planet.mass * planet2.mass / distance(planet, planet2) ** 2
                print("Force magnitude:", force_magnitude)
                force = Vec2(planet2.pos[0] - planet.pos[0], planet2.pos[1] - planet.pos[1])
                print("Vector:", force.x, force.y)
                force.normalize()
                print("Normalized:", force.x, force.y)
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
    print("Velocity:", ship.velocity.x, ship.velocity.y)
    print("Earth Velocity:", earth.velocity.x, earth.velocity.y)
    print("Earth acceleration:", earth.acceleration.x, earth.acceleration.y)
    print("Earth force:", earth.force.x, earth.force.y)
    for planet in ships:
        planet.update_pos()
        planet.force = Vec2(0, 0)
        print(math.ceil(planet.pos[0] / size_factor) + round(width / 2))
        print(math.ceil(planet.pos[1] / size_factor) + round(height / 2))
        print(math.ceil(planet.radius / size_factor))
        #if isinstance(planet, Planet) and math.ceil(planet.radius / size_factor) > 1:
        pygame.draw.circle(screen, (0, 0, 0), [math.ceil(planet.pos[0] / size_factor) + round(width / 2), math.ceil(planet.pos[1] / size_factor) + round(height / 2)], math.ceil(planet.radius / size_factor)) #Draws a dot where the planet should be.
        #else:
            #pixels[math.ceil(planet.pos[0] / size_factor) + round(width / 2), math.ceil(planet.pos[1] / size_factor) + round(height / 2)] = (0, 0, 0)
    pygame.display.flip()
    print("Position:", ship.pos)
    print("")
    #time.sleep(1)
    time.sleep(0.004)