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
    shot = fun.Shot(location, sprite, angle)
    active_player_shots.append(shot)

ship_rect = ship_sprite.get_rect(center=(400,300))
ship = fun.Player_char((400,300), ship_sprite, rect=ship_rect)
#ship_positon = pygame.Vector2(400, 300)

shot_colldown = 0
clock = pygame.time.Clock()


running = True
while running:
    #boarders
    if ship.x > 1290:
        ship.x = -10
    if ship.x < -10:
        ship.x = 1290
    if ship.y > 730:
        ship.y = -10
    if ship.y < -10:
        ship.y = 730

    #cool downs
    if shot_colldown > 0:
        shot_colldown -= 1


    #draw frame
    screen.fill((0,0,0))
    display_sprite(ship.x, ship.y, ship.sprite, ship.angle, ship.rect)
    for shot in active_player_shots:
        display_sprite(shot.x, shot.y, shot_sprite,shot.angle)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.angle +=3
    if keys[pygame.K_RIGHT]:
        ship.angle -=3
    if keys[pygame.K_UP]:
        ship.speed += .3
    if keys[pygame.K_DOWN] and ship.speed > 0:
        ship.speed -= .1
    if keys[pygame.K_SPACE] and shot_colldown <= 0:
        fire_shot((ship.x,ship.y),ship.angle)
        shot_colldown = .2 * 60

    #Update object locations
    for shot in active_player_shots:
        shot.update_location()
    ship.update_location()

    #push to sceen
    pygame.display.flip()
    clock.tick(60)

    #Gravity and speed control / limits
    ship.enforce_drag()
    ship.enforce_speed_limit()
    ship.enforce_angle_limit()
    #print(f"Speed: {ship.speed}\nAngle: {ship.angle}")


pygame.quit()
