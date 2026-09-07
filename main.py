import pygame
import fun

pygame.init()

#Graphics
screen = pygame.display.set_mode((1280, 720))
ship_sprite = pygame.image.load("assets/ship.png").convert_alpha()
ship_sprite = pygame.transform.scale(ship_sprite,
                                    (ship_sprite.get_width() * 3,
                                    ship_sprite.get_height() *3))
shot_sprite = pygame.image.load("assets/shot_plain.png").convert_alpha()

active_player_shots = []

#functions
def display_sprite(x, y, sprite, angel, sprite_rect=False):
    rotated_sprite = pygame.transform.rotate(sprite, angel)
    if sprite_rect:
        sprite_rect.center = (round(x),round(y))
        rotated_rect = rotated_sprite.get_rect(center=sprite_rect.center)
        screen.blit(rotated_sprite,rotated_rect)
    else:
        screen.blit(rotated_sprite, (x, y))


def fire_shot(location, angle, sprite=shot_sprite):
    shot = fun.Shot(location, angle, sprite)
    active_player_shots.append(shot)



ship_positon = pygame.Vector2(400, 300)
ship_rect = ship_sprite.get_rect(center=(ship_positon))
shot_colldown = 0
clock = pygame.time.Clock()

player_angle = 0
player_speed = 0
player_speed_limit = 15

running = True
while running:
    #boarders
    if ship_positon.x > 1290:
        ship_positon.x = -10
    if ship_positon.x < -10:
        ship_positon.x = 1290
    if ship_positon.y > 730:
        ship_positon.y = -10
    if ship_positon.y < -10:
        ship_positon.y = 730


    #cool downs
    if shot_colldown > 0:
        shot_colldown -= 1


    #draw frame
    screen.fill((0,0,0))
    display_sprite(ship_positon.x, ship_positon.y, ship_sprite, player_angle, sprite_rect=ship_rect)
    for shot in active_player_shots:
        display_sprite(shot.x, shot.y, shot_sprite,shot.angle)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle +=3
    if keys[pygame.K_RIGHT]:
        player_angle -=3
    if keys[pygame.K_UP]:
        player_speed += .3
    if keys[pygame.K_DOWN] and player_speed > 0:
        player_speed -= .1
    if keys[pygame.K_SPACE] and shot_colldown <= 0:
        fire_shot((ship_positon.x,ship_positon.y),player_angle)
        shot_colldown = .2 * 60


    #Shots
    for shot in active_player_shots:
        shot.update_location()


    ship_positon.x, ship_positon.y = fun.calculate_trajectory(ship_positon.x, ship_positon.y, ((360 - player_angle) % 360) + 270, player_speed)


    #push to sceen
    pygame.display.flip()
    clock.tick(60)

    #Gravity and speed control / limits
    if player_speed > player_speed_limit:
        player_speed = player_speed_limit
    if player_speed > 0:
        player_speed -= .06
    elif player_speed < 0:
        player_speed = 0

    # Angle control
    if player_angle >= 360:
        player_angle = 0


pygame.quit()
