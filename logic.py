import math

def calculate_trajectory(x0,y0,angle_degrees,distance):
    angel = math.radians(angle_degrees)
    x = x0 + distance * math.cos(angel)
    y = y0 + distance * math.sin(angel)
    return (x,y)

class Display_obj():
    def __init__(self,location,sprite, angle=0,rect=False,speed_limit=0):
        self.x = location[0]
        self.y = location[1]
        self.sprite = sprite
        self.rect = rect
        self.speed_limit = speed_limit
        self.speed = 0
        self.angle = angle
        self.status = "ACTIVE"
        self.draw_layer = 1
        self.collison_layer = 1
    def update_location(self):
        self.x, self.y = calculate_trajectory(self.x, self.y, ((360 - self.angle) % 360) + 270, self.speed)
    def enforce_speed_limit(self):
        if self.speed > self.speed_limit:
            self.speed = self.speed_limit
    def enforce_angle_limit(self):
        if self.angle >= 360:
            self.angle = 0
        if self.angle <= -360:
            self.angle = 0
    def enforce_drag(self):
        if self.speed > 0:
            self.speed -= .06
        if self.speed < 0:
            self.speed = 0

class Shot(Display_obj):
    def __init__(self,location ,sprite, angle):
        super().__init__(location,sprite,angle=angle)
        self.speed = 20
        self.size = (8, 8)

    def enforce_boarder_limit(self):
        if self.x > 1290:
            self.status = "COLLECT"
        if self.x < -10:
            self.status = "COLLECT"
        if self.y > 730:
            self.status = "COLLECT"
        if self.y < -10:
            self.status = "COLLECT"

class Player_char(Display_obj):
    def __init__(self, location, sprite, rect=False, speed_limit=15):
        super().__init__(location, sprite, rect=rect, speed_limit=speed_limit)
        self.shape = (48, 48)

    def enforce_boarder_loop(self):
        if self.x > 1290:
            self.x = -10
        if self.x < -10:
            self.x = 1290
        if self.y > 730:
            self.y = -10
        if self.y < -10:
            self.y = 730

class Enemy(Display_obj):
    def __init__(self, location, sprite, angle=0):
        super().__init__(location, sprite, angle=angle)
        self.size = (48, 48)

class Letter(Display_obj):
    def __init__(self, location,sprite, angle=0):
        super().__init__(location, sprite, angle=angle)

