import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
running = True
dt=0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
screen.fill("black")
direction = "North"
elapsed_time = 0
movement_tick = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # fill the screen with a color to wipe away anything from last frame

    # RENDER YOUR GAME HERE
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and direction != "South":
        direction = "North"
    if keys[pygame.K_s] and direction != "North":
        direction = "South"
    if keys[pygame.K_a] and direction != "East":
        direction = "West"
    if keys[pygame.K_d] and direction != "West":
        direction = "East"
    
    dt = clock.tick(60) / 1000  # limits FPS to 60
    elapsed_time += dt
    if elapsed_time > .3:
        elapsed_time -= .3
        if direction == "North":
            player_pos.y -= 20
        if direction == "South":
            player_pos.y += 20
        if direction == "West":
            player_pos.x -= 20
        if direction == "East":
            player_pos.x += 20
        pygame.draw.rect(screen, "green", (player_pos[0], player_pos[1], 20, 20))
    # flip() the display to put your work on screen
    pygame.display.flip()
    

pygame.quit()