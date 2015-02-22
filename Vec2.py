import math

class Vec2():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def sqrd_length(self):
        return self.x * self.x + self.y * self.y
    
    def length(self):
        return math.sqrt(self.sqrd_length())
    
    def sqrd_dist_do(self, vec):
        return self.minus(vec).sqrd_length()
    
    def dist_to(self, vec):
        return self.minus(vec).length()
    
    def sqrt(self):
        return Vec2(math.sqrt(self.x), math.sqrt(self.y))
    
    def sqrd(self):
        return Vec2(self.x * self.x, self.y * self.y)
    
    def unit(self):
        length = 1
        if (not self.x == 0) or (not self.y == 0):
            len = self.length()
        return self.divide_with(len)
    
    def normalize(self):
        len = 1
        if (not self.x == 0) or (not self.y == 0):
            len = self.length()
        self.divide(len)
    
    def copy(self):
        return Vec2(self.x, self.y)
    
    def set(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def equals(self, vec):
        return self.x == vec.x and self.y == vec.y
    
    def equals_to(self, x=0, y=0):
        return self.x == x and self.y == y
    
    def add(self, vec):
        self.x += vec.x
        self.y += vec.y
        
    def plus(self, vec):
        return Vec2(self.x + vec.x, self.y + vec.y)
    
    def subtract(self, vec):
        self.x -= vec.x
        self.y -= vec.y
    
    def minus(self, vec):
        return Vec2(self.x - vec.x, self.y - vec.y)
    
    def times(self, multiple):
        if isinstance(multiple, Vec2):
            return Vec2(self.x * multiple.x, self.y * multiple.y)
        else:
            return Vec2(self.x * multiple, self.y * multiple)
    
    def multiply(self, multiple):
        if isinstance(multiple, Vec2):
            self.x *= multiple.x
            self.y *= multiple.y
        else:
            self.x *= multiple
            self.y *= multiple
     
    def divide(self, denom):
        if isinstance(denom, Vec2):
            self.x /= denom.x
            self.y /= denom.y
        else:
            self.x /= denom
            self.y /= denom
    
    def divideWith(self, denom):
        if isinstance(denom, Vec2):
            return Vec2(self.x / denom.x, self.y / denom.y)
        else:
            return Vec2(self.x / denom, self.y / denom)
    
    def dot(self, vec):
        return self.x * vec.x + self.y * vec.y
    
    def cross(self, vec):
        return self.x * vec.y - this.y * vec.x
    
    def projected_onto(self, vec):
        dir = vec.copy()
        if not dir.sqrd_length() == 1:
            dir.normalize()
        return dir.times(self.dot(dir))
    
    def perp_CCW(self):
        return Vec2(-self.y, self.x)
    
    def perp_CW(self):
        return Vec2(self.y, -self.x)
    
    def midpoint(self, vec, mp):
        mp = mp | 0.5
        return self.times(1-mp).plus(vec.times(mp))
    
    def angle(self):
        return math.atan2(self.y, self.x)
    
    def rotated(self, tilt_angle):
        angle = self.angle
        angle -= tilt_angle
        len = self.length()
        return Vec2(len * math.cos(angle), len * math.sin(angle))
    
    def rotate(self, tilt_angle):
        angle = self.angle
        angle -= tilt_angle
        len = self.length()
        self.x = len * math.cos(angle)
        self.y = len * math.sin(angle)