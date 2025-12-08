import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 400))
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()
running = True
dt=0
player_pos = pygame.Vector2(width/2, height/2)
screen.fill("black")
direction = "North"
new_direction = "North"
elapsed_time = 0
movement_tick = False
game_tick = .3 #ms
starting_length = 3
snake_length = 3
pos_dict = {(width/2, height/2):starting_length-1}
            #(x,y):val
pos_fruit_x = 200
pos_fruit_y = 200
pos_fruit_retry = True
while pos_fruit_retry:
    pos_fruit_retry = False
    pos_fruit_x = random.randint(1,20) * width/20
    pos_fruit_y = random.randint(1,20) * height/20
    for key in pos_dict:
        if (pos_fruit_x, pos_fruit_y) == key:
            pos_fruit_retry = True
pygame.draw.circle(screen, "red", (pos_fruit_x+(width/40), pos_fruit_y+(height/40)), 10, 0)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # fill the screen with a color to wipe away anything from last frame

    
    # RENDER YOUR GAME HERE]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and direction != "South":
        new_direction = "North"
    if keys[pygame.K_s] and direction != "North":
        new_direction = "South"
    if keys[pygame.K_a] and direction != "East":
        new_direction = "West"
    if keys[pygame.K_d] and direction != "West":
        new_direction = "East"
    dt = clock.tick(60) / 1000  # limits FPS to 60
    elapsed_time += dt
    if elapsed_time > game_tick:
        elapsed_time -= game_tick
        direction = new_direction
        if new_direction == "North":
            player_pos.y -= height/20
        if new_direction == "South":
            player_pos.y += height/20
        if new_direction == "West":
            player_pos.x -= width/20
        if new_direction == "East":
            player_pos.x += width/20
        fruit_obtained = False
        if player_pos == (pos_fruit_x, pos_fruit_y):
            fruit_obtained = True
            snake_length += 1
        break_pixel = 0
        for key in pos_dict:
            value = pos_dict[key]
            if value == 0:
                pygame.draw.rect(screen, "black", (key[0], key[1], 20, 20))
                break_pixel = key
            elif not(fruit_obtained):
                pos_dict[key] = value-1
            if key == player_pos or player_pos.x/(width/20) not in range(20) or player_pos.y/(height/20) not in range(20):
                print(pos_fruit_x, pos_fruit_y)
                pygame.quit()
                quit()
        pos_dict[(player_pos.x,player_pos.y)] = snake_length-1
        if break_pixel != 0:
            del pos_dict[break_pixel]
        

        if fruit_obtained == True:
            pos_fruit_retry = True
            while pos_fruit_retry:
                pos_fruit_retry = False
                pos_fruit_x = random.randint(1,19) * width/20
                pos_fruit_y = random.randint(1,19) * height/20
                for key in pos_dict:
                    if (pos_fruit_x, pos_fruit_y) == key:
                        pos_fruit_retry = True
            pygame.draw.circle(screen, "red", (pos_fruit_x+(width/40), pos_fruit_y+(height/40)), 10, 0)
        #pygame.draw.circle(screen, blue, (400, 300), 50, 0)
        #print(pos_fruit_x, pos_fruit_y)
        #pygame.draw.rect(screen, "red", (pos_fruit_x, pos_fruit_y, 20, 20))
        #print(pos_dict)
        pygame.draw.rect(screen, "green", (player_pos[0], player_pos[1], 20, 20))
    # flip() the display to put your work on screen
    pygame.display.flip()
    

pygame.quit()