import math

def calculate_trajectory(x0,y0,angle_degrees,distance):
    angel = math.radians(angle_degrees)
    x = x0 + distance * math.cos(angel)
    y = y0 + distance * math.sin(angel)
    return (x,y)

class Display_obj():
    def __init__(self,location,angle,sprite,speed,rect=False,speed_limit=0):
        self.speed = speed
        self.x = location[0]
        self.y = location[1]
        self.angle = angle
        self.sprite = sprite
        self.rect = rect
        self.speed_limit = speed_limit
    def update_location(self):
        self.x, self.y = calculate_trajectory(self.x, self.y, ((360 - self.angle) % 360) + 270, self.speed)
    def inforce_speed_limit(self):
        if self.speed > self.speed_limit:
            self.speed = self.speed_limit

class Shot(Display_obj):
    def __init__(self,location,angle,sprite,speed=20):
        super().__init__(location,angle,sprite,speed)


class Player_char():
    def __init__(self,location, angle, sprite, rect, speed_limit=15):
        self.speed_limit = speed_limit
    def update_location(self):
        self.x, self.y = calculate_trajectory(self.x, self.y, ((360 - self.angle) % 360) + 270, self.speed)
