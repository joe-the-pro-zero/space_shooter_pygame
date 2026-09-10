import pygame
import logic
import os

pygame.init()

#Graphics
screen = pygame.display.set_mode((1280, 720))
ship_sprite = pygame.image.load("assets/ship.png").convert_alpha()
ship_sprite = pygame.transform.scale(ship_sprite,
                                    (ship_sprite.get_width() * 3,
                                    ship_sprite.get_height() *3))
shot_sprite = pygame.image.load("assets/shot_plain.png").convert_alpha()
enemy_sprite = pygame.image.load("assets/enemy.png").convert_alpha()
enemy_sprite = pygame.transform.scale(enemy_sprite,
                                    (enemy_sprite.get_width() * 3,
                                    enemy_sprite.get_height() *3))

#Fonts
alphabet_files = []
alpha_sprites = {}
files = os.listdir("./assets/fonts")
for filex in files:
    if filex[-4:] == ".png":
        alphabet_files.append(filex)

alphabet_files.sort()
for filex in alphabet_files:
        alpha_sprites[filex[:1]] = pygame.image.load(f"assets/fonts/{filex}").convert_alpha()

#Object
active_objects = {"active_player_shots":[],
                  "active_enemys":[],
                  "active_players":[],
                  "letters":[]
                      }

#functions
def screen_print(x, y, string, scale=1):
    for char in string:
        char_sprite = pygame.transform.scale(alpha_sprites[char],
                                    (alpha_sprites[char].get_width() * scale,
                                    alpha_sprites[char].get_height() * scale))
        active_objects["letters"].append(logic.Letter((x,y),char_sprite))
        x = x + 16 * scale

def display_sprite(x, y, sprite, angel, sprite_rect=False):
    rotated_sprite = pygame.transform.rotate(sprite, angel)
    if sprite_rect:
        sprite_rect.center = (round(x),round(y))
        rotated_rect = rotated_sprite.get_rect(center=sprite_rect.center)
        screen.blit(rotated_sprite,rotated_rect)
    else:
        screen.blit(rotated_sprite, (x, y))

def fire_shot(location, angle, sprite=shot_sprite):
    shot = logic.Shot(location, sprite, angle)
    active_objects["active_player_shots"].append(shot)

def collison_detect():
    for shot in active_objects["active_player_shots"]:
        for enemy in active_objects["active_enemys"]:
            if round(shot.y) in range(round(enemy.y-32), round(enemy.y+32)) and round(shot.x) in range(round(enemy.x-32), round(enemy.x+32)):
                active_objects["active_player_shots"].remove(shot)
                enemy.status = "COLLECT"
    for ship in active_objects["active_players"]:
        for enemy in active_objects["active_enemys"]:
            if round(ship.y) in range(round(enemy.y-32), round(enemy.y+32)) and round(ship.x) in range(round(enemy.x-32), round(enemy.x+32)):
                ship.status = "COLLECT"
                for key in active_objects:
                    for obj in active_objects[key]:
                        obj.status = "COLLECT"
                screen_print(360,200,"GAMEOVER",4)

def move_enemy():
    pass

def create_enemy(location):
    enemy = logic.Enemy(location, enemy_sprite)
    active_objects["active_enemys"].append(enemy)

ship_rect = ship_sprite.get_rect()
active_objects["active_players"].append(logic.Player_char((400,300), ship_sprite, rect=ship_rect))

shot_cooldown = 0
clock = pygame.time.Clock()

create_enemy((800,350))
create_enemy((500,300))
running = True
while running:

    #cool downs
    if shot_cooldown > 0:
        shot_cooldown -= 1

    #draw frame
    screen.fill((0,0,0))


    for key in active_objects:
        for obj in active_objects[key]:
            if obj.status == "ACTIVE":
                display_sprite(obj.x, obj.y, obj.sprite, obj.angle, obj.rect)

    #remove trash
    for key in active_objects:
        for obj in active_objects[key]:
            if obj.status == "COLLECT":
                active_objects[key].remove(obj)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Inputs
    keys = pygame.key.get_pressed()
    for obj in active_objects["active_players"]:
        if keys[pygame.K_LEFT]:
            obj.angle +=3
        if keys[pygame.K_RIGHT]:
            obj.angle -=3
        if keys[pygame.K_UP]:
            obj.speed +=.3
        if keys[pygame.K_DOWN] and obj.speed > 0:
            obj.speed -=.1
        if keys[pygame.K_SPACE] and shot_cooldown <= 0:
            fire_shot((obj.x,obj.y),obj.angle)
            shot_cooldown = .2 * 60

    #Update object locations
    for key in active_objects:
        for obj in active_objects[key]:
            obj.update_location()

    #push to sceen
    pygame.display.flip()
    clock.tick(60)

    #Gravity / speed control / limits
    for obj in active_objects["active_players"]:
        obj.enforce_drag()
        obj.enforce_speed_limit()
        obj.enforce_angle_limit()
        obj.enforce_boarder_loop()
    for shot in active_objects["active_player_shots"]:
        shot.enforce_boarder_limit()
    #for ship in active_objects["active_players"]:
    #    print(f"Speed: {ship.speed}\nAngle: {ship.angle}\nShip Location: {(ship.x,ship.y)}\nBullets_on_screen: {len(active_objects["active_player_shots"])}")

    collison_detect()
    #os.system("clear")
pygame.quit()
