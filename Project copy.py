#imports
import pygame
import random


# -=-=-=-=-=-=-=-=-=-=- GAME -=-=-=-=-=-=-=-=-=-=-

#setup
pygame.init() #initialize pygame
screen = pygame.display.set_mode((400, 400)) #add screen, size should be 400x400 but I use width/height anyways (so this is changable)
width = screen.get_width() #set width/height
height = screen.get_height()
clock = pygame.time.Clock() #add clock
dt=0 #start dt
player_pos = pygame.Vector2(width/2, height/2) #add position
screen.fill("black") #background
pygame.draw.rect(screen, "green", (width/2, height/2, width/20, height/20)) #draw snake start
direction = "North" #start directions as north
new_direction = "North"
elapsed_time = 0 #add elapsed_time
game_tick = .6 #frame time in s
snake_length = 3 #starting snake length, also added in reset area, change both if you want to change it
high_score = 0 #start high score as 0
pos_dict = {(width/2, height/2):snake_length-1} #(x,y):val - position log
pos_fruit_x = 200 #just add fruit positions so it can be used in while loop
pos_fruit_y = 200
while pos_fruit_x == 200 and pos_fruit_y == 200: #find fruit position not on the snake starting spot
    pos_fruit_x = random.randint(1,19) * width/20
    pos_fruit_y = random.randint(1,19) * height/20 #add fruit (line below)
pygame.draw.circle(screen, "red", (pos_fruit_x+(width/40), pos_fruit_y+(height/40)), width/40, 0)
running = True #default running to true

#main func
def game():
    global elapsed_time
    global direction
    global new_direction
    global player_pos
    global pos_fruit_x
    global pos_fruit_y
    global pos_dict
    global snake_length
    global high_score
    global running
    
    direction = new_direction
    if new_direction == "North": #offset new player position by new direction vector
        player_pos.y -= height/20
    if new_direction == "South":
        player_pos.y += height/20
    if new_direction == "West":
        player_pos.x -= width/20
    if new_direction == "East":
        player_pos.x += width/20
    fruit_obtained = False #default false
    if player_pos == (pos_fruit_x, pos_fruit_y): #check if fruit obtained
        fruit_obtained = True #if so, record it and increase length of snake
        snake_length += 1
    break_pixel = 0 #default to none
    reset = False #default to false
    for key in pos_dict: #iterate position log
        value = pos_dict[key] #for each position, value = lifespan of position
        if value == 0: #if lifespan hits 0, draw over snake (deletes pixel)
            pygame.draw.rect(screen, "black", (key[0], key[1], width/20, height/20))
            break_pixel = key #record the key to be removed (can't remove it in 'for' loop)
        elif not(fruit_obtained): #if fruit isn't obtained
            pos_dict[key] = value-1 #decay the pixel by 1
        if key == player_pos or player_pos.x/(width/20) not in range(20) or player_pos.y/(height/20) not in range(20): #if collision with wall or self
            print('Score: '+str(snake_length-3)) #print score
            screen.fill("black") #reset screen
            snake_length = 3 #reset length
            pos_dict = {(width/2, height/2):snake_length-1} #reset position log
            player_pos = pygame.Vector2(width/2, height/2) #reset position
            pygame.draw.rect(screen, "green", (width/2, height/2, width/20, height/20)) #draw new position
            direction = "North" #reset directions
            new_direction = "North"
            reset = True #record reset happening, as break only exits the 'for' loop
            while True: #find a new fruit position (exception is center, where snake spawns)
                pos_fruit_x = random.randint(1,19) * width/20
                pos_fruit_y = random.randint(1,19) * height/20
                if pos_fruit_x != width/2 or pos_fruit_y != height/2:
                    break
            pygame.draw.circle(screen, "red", (pos_fruit_x+(width/40), pos_fruit_y+(height/40)), (width+height)/80, 0) #draw new fruit on new screen
            return
    pos_dict[(player_pos.x,player_pos.y)] = snake_length-1 #if none was detected, log new snake position
    if break_pixel != 0: #remove pixel outside of 'for' loop
        del pos_dict[break_pixel]
    if fruit_obtained == True: #if fruit is obtained
        pos_fruit_retry = True #find new fruit position
        while pos_fruit_retry:
            pos_fruit_retry = False
            pos_fruit_x = random.randint(0,19) * width/20
            pos_fruit_y = random.randint(0,19) * height/20
            pos_fruit_retry = (pos_fruit_x,pos_fruit_y) in pos_dict
        pygame.draw.circle(screen, "red", (pos_fruit_x+(width/40), pos_fruit_y+(height/40)), (width+height)/80, 0)
    pygame.draw.rect(screen, "green", (player_pos.x, player_pos.y, width/20, height/20)) #draw new snake body
    if snake_length > high_score: #highscore variable is 3 higher than displayed; score doesn't include starting 3 length
        high_score = snake_length #update highscore if higher than new score each frame
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, 70, 12)) #display scorebox background, display scores below
    screen.blit(pygame.font.SysFont('Arial', 10).render('Scr: '+str(snake_length-3)+'  HScr:'+str(high_score-3), False, 'white'), (0, 0))
    pygame.display.flip() #actually update everything on display

def state_update():
    direction_right = int(new_direction == "East")
    direction_left = int(new_direction == "West")
    direction_up = int(new_direction == "North")
    direction_down = int(new_direction == "South")
    loc_straight = ((direction_right-direction_left)*width/20+player_pos.x, (direction_down-direction_up)*height/20+player_pos.y)
    loc_left = ((direction_down-direction_up)*width/20+player_pos.x, (direction_left-direction_right)*height/20+player_pos.y)
    loc_right = ((direction_up-direction_down)*width/20+player_pos.x, (direction_right-direction_left)*height/20+player_pos.y)
    state = [int((loc_straight) in pos_dict or loc_straight[0]/(width/20) not in range(20) or loc_straight[1]/(height/20) not in range(20)),
        int((loc_right) in pos_dict or loc_right[0]/(width/20) not in range(20) or loc_right[1]/(height/20) not in range(20)),
        int((loc_left) in pos_dict or loc_left[0]/(width/20) not in range(20) or loc_left[1]/(height/20) not in range(20)),
        direction_left,
        direction_right,
        direction_up,
        direction_down, #state = collisions(straight, right, left), directions(left, right, up, down), fruit directions (west, east, north, south)
        int(pos_fruit_x < player_pos.x),
        int(pos_fruit_x > player_pos.x),
        int(pos_fruit_y < player_pos.y),
        int(pos_fruit_y > player_pos.y)]
    print(state)
    return state


while running:
    for event in pygame.event.get(): #check if quit, if so end loop
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed() #check for keys, set new direction to it (applies in frame, next frame checks updated "direction" var)
    if keys[pygame.K_w] and direction != "South":
        new_direction = "North"
    if keys[pygame.K_s] and direction != "North":
        new_direction = "South"
    if keys[pygame.K_a] and direction != "East":
        new_direction = "West"
    if keys[pygame.K_d] and direction != "West":
        new_direction = "East"
    dt = clock.tick(60) / 1000 #timer
    elapsed_time += dt #elapsed time counter, as dt just counts how much time in each 1/60 second tick passed in decimals
    if elapsed_time > game_tick: #if tick is reached
        elapsed_time -= game_tick #remove tick # from timer, effectively restarting it
        
        game()
        game_state = state_update()
       
print('Score: '+str(snake_length-3)) #when running loop ends (pygame.QUIT occurs, game closed out of)
print('High Score:'+str(high_score-3)) #record scores in console

# -=-=-=-=-=-=-=-=-=-=- GAME -=-=-=-=-=-=-=-=-=-=-


# -=-=-=-=-=-=-=-=-=-=- GAME -=-=-=-=-=-=-=-=-=-=-