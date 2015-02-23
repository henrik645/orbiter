G = 6.37e-11
SIZE_FACTOR = 50000
TICKS_PER_SEC = 250
PLANETS_FILE = "resources/planets.json"
SHIPS_FILE = "resources/ships.json"
BG_COLOR = (255, 255, 255)

import math, pygame, time, sys, os, json
from Vec2 import *

pygame.init()
icon = pygame.image.load("resources/icon.png")
pygame.display.set_caption("Orbiter v0.1 Alpha", "Orbiter") #Sets caption and icon caption (for smaller displays)
pygame.display.set_icon(icon)
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pixels = pygame.PixelArray(screen)
clock = pygame.time.Clock()

class Ship():
    def __init__(self, pos, mass, radius=1, force=Vec2(0, 0), velocity=Vec2(0, 0), acceleration=Vec2(0, 0), name="Ship", color=(0, 0, 0)):
        self.pos = pos
        self.mass = mass
        self.force = force
        self.radius = radius
        self.velocity = velocity
        self.acceleration = acceleration
        self.name = name
        self.color = color
    
    def add_force(self, vector):
        self.force = self.force.plus(vector)
    
    def update_pos(self):
        self.acceleration = self.force.divideWith(self.mass)
        print(self.name)
        print("Acceleration:", self.acceleration.x, self.acceleration.y)
        print("Velocity:", self.velocity.x, self.velocity.y)
        self.velocity = self.velocity.plus(self.acceleration)
        print("Velocity:", self.velocity.x, self.velocity.y)
        self.pos[0] += self.velocity.x
        self.pos[1] += self.velocity.y
        print("")

class Planet(Ship):
    def __init__(self, name, pos, mass, radius, color):
        super().__init__(pos, mass, radius)
        self.name = name
        self.color = color
        
def vector_add(vec1, vec2):
    res = [vec1[0] + vec2[0], vec1[1] + vec2[1]]
    return res

def distance(planet1, planet2):
    return math.sqrt(((planet1.pos[0] - planet2.pos[0])**2) + ((planet1.pos[1] - planet2.pos[1])**2))

def init(planets, ships, save=None):
    if not (os.path.isfile(planets) and os.path.isfile(ships)):
        return False
    else:
        planets_file = open(planets)
        planets = json.loads(planets_file.read())
        ships = []
        for planet in planets:
            planet_object = Planet(name=planet['name'], radius=planet['radius'], mass=planet['mass'], pos=planet['position'], color=planet['color'])
            if 'force' in planet:
                force = Vec2(planet['force'][0], planet['force'][1])
                planet_object.add_force(force)
            ships.append(planet_object)
        return ships

player_mass = 15000
masses = [5.97e24, 7.34e22]

result = init(PLANETS_FILE, SHIPS_FILE)
if not result:
    print("An error occured during bootstrap.")
    sys.exit()
else:
    ships = result

earth = ships[0]
# earth = Planet("Earth", [2, 2], 5.97e24, 6378000)
ship = Ship(pos=[0, 7578000], mass=15000)
ships.append(ship)
# moon = Planet("Moon", [2, -8078000], 7.34e22, 1737000)
# ships = [earth, ship]
ship.add_force(Vec2(110000000, 0))
#moon.add_force(Vec2(-5.37e+26, 0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: #Mouse wheel down
                SIZE_FACTOR += 500
            elif event.button == 5: #Mouse wheel up
                if SIZE_FACTOR - 500 >= 0:
                    SIZE_FACTOR -= 500
    screen.fill(BG_COLOR) #Fills screen with white
    for planet in ships:
        for planet2 in ships:
            if not planet == planet2:
                print(distance(planet, planet2))
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
        print(math.ceil(planet.pos[0] / SIZE_FACTOR) + round(width / 2))
        print(math.ceil(planet.pos[1] / SIZE_FACTOR) + round(height / 2))
        print(math.ceil(planet.radius / SIZE_FACTOR))
        pygame.draw.circle(screen, planet.color, [math.ceil(planet.pos[0] / SIZE_FACTOR) + round(width / 2), math.ceil(planet.pos[1] / SIZE_FACTOR) + round(height / 2)], math.ceil(planet.radius / SIZE_FACTOR)) #Draws a dot where the planet should be.
    pygame.display.flip()
    print("Position:", ship.pos)
    print("")
    print("FPS:", clock.get_fps())
    print("")
    clock.tick(TICKS_PER_SEC) #Ticks the clock. Also sets max framerate