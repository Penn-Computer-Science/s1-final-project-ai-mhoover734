#imports
import pygame
import random
import numpy as np

#setup:
pygame.init()
screen = pygame.display.set_mode((400, 400))
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()
dt=0
player_pos = pygame.Vector2(width/2, height/2)
screen.fill("black")
pygame.draw.rect(screen, "green", (width/2, height/2, width/20, height/20))
direction = "North"
new_direction = "North"
elapsed_time = 0
game_tick = .005
snake_length = 3
high_score = 0
pos_dict = {(width/2, height/2):snake_length-1}
pos_fruit_x = 200
pos_fruit_y = 200
while pos_fruit_x == 200 and pos_fruit_y == 200:
    pos_fruit_x = random.randint(1,19) * width/20
    pos_fruit_y = random.randint(1,19) * height/20
pygame.draw.circle(screen, "red", (pos_fruit_x+(width/40), pos_fruit_y+(height/40)), width/40, 0)
running = True
reset = False
fruit_obtained = False
directions = ["North", "East", "South", "West"]

class SnakeGameAI:

    def __init__(self):
        self.elapsed_time = 0
        self.clock = pygame.time.Clock()
    #main func:
    def game(self):
        global elapsed_time
        global direction
        global new_direction
        global player_pos
        global pos_fruit_x
        global pos_fruit_y
        global fruit_obtained
        global pos_dict
        global snake_length
        global high_score
        global reset
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
        reset = False
        for key in pos_dict:
            value = pos_dict[key]
            if value == 0:
                pygame.draw.rect(screen, "black", (key[0], key[1], width/20, height/20))
                break_pixel = key
            elif not(fruit_obtained):
                pos_dict[key] = value-1
            if key == player_pos or player_pos.x/(width/20) not in range(20) or player_pos.y/(height/20) not in range(20):
                return True
        pos_dict[(player_pos.x,player_pos.y)] = snake_length-1
        if break_pixel != 0:
            del pos_dict[break_pixel]
        if fruit_obtained == True:
            pos_fruit_retry = True
            while pos_fruit_retry:
                pos_fruit_retry = False
                pos_fruit_x = random.randint(0,19) * width/20
                pos_fruit_y = random.randint(0,19) * height/20
                pos_fruit_retry = (pos_fruit_x,pos_fruit_y) in pos_dict
            pygame.draw.circle(screen, "red", (pos_fruit_x+(width/40), pos_fruit_y+(height/40)), (width+height)/80, 0)
        pygame.draw.rect(screen, "green", (player_pos.x, player_pos.y, width/20, height/20))
        if snake_length > high_score:
            high_score = snake_length
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 70, 12))
        screen.blit(pygame.font.SysFont('Arial', 10).render('Scr: '+str(snake_length-3)+'  HScr:'+str(high_score-3), False, 'white'), (0, 0))
        pygame.display.flip()
        return False

    #to reset the game when needed:
    def reset_game(self):
        global direction
        global new_direction
        global player_pos
        global pos_fruit_x
        global pos_fruit_y
        global pos_dict
        global snake_length
        global reset
        #print('Score: '+str(snake_length-3))
        screen.fill("black")
        snake_length = 3
        pos_dict = {(width/2, height/2):snake_length-1}
        player_pos = pygame.Vector2(width/2, height/2)
        pygame.draw.rect(screen, "green", (width/2, height/2, width/20, height/20))
        direction = "North"
        new_direction = "North"
        reset = True
        while True:
            pos_fruit_x = random.randint(1,19) * width/20
            pos_fruit_y = random.randint(1,19) * height/20
            if pos_fruit_x != width/2 or pos_fruit_y != height/2:
                break
        pygame.draw.circle(screen, "red", (pos_fruit_x+(width/40), pos_fruit_y+(height/40)), (width+height)/80, 0)

    #to calculate reward state:
    def reward_state(self):
        return (int(fruit_obtained)-int(reset))*10-.005

    #to get the current ingame status
    def state_update(self):
        direction_right = int(new_direction == "East")
        direction_left = int(new_direction == "West")
        direction_up = int(new_direction == "North")
        direction_down = int(new_direction == "South")
        loc_straight = ((direction_right-direction_left)*width/20+player_pos.x, (direction_down-direction_up)*height/20+player_pos.y)
        loc_left = ((direction_down-direction_up)*width/20+player_pos.x, (direction_left-direction_right)*height/20+player_pos.y)
        loc_right = ((direction_up-direction_down)*width/20+player_pos.x, (direction_right-direction_left)*height/20+player_pos.y)
        state = [int((loc_straight) in pos_dict or loc_straight[0]/(width/20) not in range(20) or loc_straight[1]/(height/20) not in range(20)), #collision ahead
            int((loc_right) in pos_dict or loc_right[0]/(width/20) not in range(20) or loc_right[1]/(height/20) not in range(20)), #collision right
            int((loc_left) in pos_dict or loc_left[0]/(width/20) not in range(20) or loc_left[1]/(height/20) not in range(20)), #collision left
            direction_left, #west
            direction_right, #east
            direction_up, #north
            direction_down, #south                                                        I N F O R M A T I O N
            int(pos_fruit_x < player_pos.x), #fruit west
            int(pos_fruit_x > player_pos.x), #fruit east
            int(pos_fruit_y < player_pos.y), #fruit north
            int(pos_fruit_y > player_pos.y)] #fruit south
        #print(state)#state = (straight, right, left,  left, right, up, down,  left, right, up, down)
        return state     #      \    collisions    /    \ snake direction  /    \ fruit direction  /

    #model input being left turn calls this
    def left_turn(self):
        global new_direction
        new_direction = directions[(directions.index(new_direction)+3)%4]

    #model input being right turn calls this
    def right_turn(self):
        global new_direction
        new_direction = directions[(directions.index(new_direction)+1)%4]

    #running loop
    '''
    def run_tick(self, action):
        #game = SnakeGameAI()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
        dt = clock.tick(60) / 1000
        self.elapsed_time += dt
        if self.elapsed_time > game_tick:
            self.elapsed_time -= game_tick
            if bool(action[1]):
                self.left_turn()
            elif bool(action[2]):
                self.right_turn()
            reward_value = game.game()
            return reward_value
            new_state = ga
            memory = old_state, new_state, reward_value, int(reset), action
            print(memory)'''
            #train the model
    def run_tick(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

        dt = self.clock.tick(60) / 1000
        self.elapsed_time += dt

        if self.elapsed_time > game_tick:
            self.elapsed_time -= game_tick

            if action[1]:
                self.left_turn()
            elif action[2]:
                self.right_turn()

            done = self.game()
            return done

        return False