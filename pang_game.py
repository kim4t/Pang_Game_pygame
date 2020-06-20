# 1. if get rid of every ball (win)
# 2. if character collide with ball (lose)
# 3. time over (20 sec) (lose)
# 4. spend all of bullets (15) (lose) / player got 18 bullets and have to hit 15 bullet for win

import pygame
import os
#######################################################################
# initialization (must do)
pygame.init()

# set screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))


# set screen title
pygame.display.set_caption("Pang Game")

# FPS
clock = pygame.time.Clock()

##########################################################################

# 1. user game initialization (background, game image, coordinate, speed, font, time)
current_path = os.path.dirname(__file__)  # return current file location
image_path = os.path.join(current_path, "images")  # return image folder

# background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

#score
score = 0

# character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height-stage_height-character_height

# charcter move direction
character_to_x = 0
character_to_left = 0
character_to_right = 0
# charcter speed
character_speed = 5

# weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
number_of_weapon = 18

weapons = []

#weapon speed
weapon_speed = 10

# ball
ball_images = [
    pygame.image.load(os.path.join(image_path, "ball1.png")),
    pygame.image.load(os.path.join(image_path, "ball2.png")),
    pygame.image.load(os.path.join(image_path, "ball3.png")),
    pygame.image.load(os.path.join(image_path, "ball4.png"))]


# initial ball speed
ball_speed_y = [-18,-15,-12,-9]

# balls
balls = []

# first ball
balls.append({
    "pos_x" :50,  # x coordinate of ball
    "pos_y" :50,  # y coordinate of ball
    "img_idx" : 0, # index of image of ball
    "to_x" : 3,   # to right 3  
    "to_y" : -6,   # to bottom 6
    "init_spd_y" : ball_speed_y[0]}) # inital speed

# weapon and ball which will be removed
weapon_to_remove = -1
ball_to_remove = -1

# font
game_font = pygame.font.Font(None,40)
total_time = 30
start_ticks = pygame.time.get_ticks()-66

# terminate game message
game_result = "Game over"
running = True
while running:
    dt = clock.tick(30)  # set the fps

    # 2. handle event (keyboard, mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_left -= character_speed
            if event.key == pygame.K_RIGHT:
                character_to_right += character_speed
            if event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + character_width/2 - weapon_width/2
                weapon_y_pos = character_y_pos
                if(number_of_weapon>0):
                    weapons.append([weapon_x_pos,weapon_y_pos])
                    number_of_weapon -= 1
                    

        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_left = 0
            elif event.key == pygame.K_RIGHT:
                character_to_right = 0
            elif event.key == pygame.K_SPACE:
                pass
            

    # 3. set character position              
    character_x_pos += character_to_left +character_to_right
    if character_x_pos < 0:
        character_x_pos = 0
    if character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # set weapon position
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons ]

    weapons = [[w[0], w[1]] for w in weapons if w[1]>0]

    # set ball position
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        

        # if ball get to horizental wall, change ball derection
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] *= -1
        

        # if ball get to stage, bounced
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]

        else: # increase speed, ball is falling
            ball_val["to_y"] += 0.5

        # update ball position
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
        
    # 4. handle collision

    # character rect info update
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # ball and character collision
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
    
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        if character_rect.colliderect(ball_rect):
            running = False
            game_result = "Game over"
            break
        
        # ball and weapon collision
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # weapon rect info update
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # check collision
            if weapon_rect.colliderect(ball_rect):
                score += 10
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # if ball is not minimum size then split
                if ball_img_idx < 3:
                    # currntly ball size info
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # splited ball info
                    small_ball_rect = ball_images[ball_img_idx+1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # to left
                    balls.append({
                        "pos_x" :ball_pos_x + ball_width/2 - small_ball_width/2,  # x coordinate of ball
                        "pos_y" :ball_pos_y + ball_height/2 - small_ball_height/2,  # y coordinate of ball
                        "img_idx" : ball_img_idx+1, # index of image of ball
                        "to_x" : -3,   # to right 3  
                        "to_y" : -6,   # to bottom 6
                        "init_spd_y" : ball_speed_y[ball_img_idx+1]}) # inital speed

                    # to right
                    balls.append({
                        "pos_x" :ball_pos_x + ball_width/2 - small_ball_width/2,  # x coordinate of ball
                        "pos_y" :ball_pos_y + ball_height/2 - small_ball_height/2,  # y coordinate of ball
                        "img_idx" : ball_img_idx+1, # index of image of ball
                        "to_x" : 3,   # to right 3  
                        "to_y" : -6,   # to bottom 6
                        "init_spd_y" : ball_speed_y[ball_img_idx+1]}) # inital speed
                    
                    break
                else:
                    continue
                break

        # remove weapon and ball
        if weapon_to_remove > -1:
            del weapons[weapon_to_remove]
            weapon_to_remove = -1
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1
        
    
        # if eliminate every ball
        if(len(balls)==0):
            running = False
            game_result = "Mission Complete"

        # if spend all bullets
        if(number_of_weapon == 0 and len(balls)>0 and len(weapons)==0):
            running = False
            game_result = "Spent All of bullet"
            print(number_of_weapon)
            

    # score font
    score_font = game_font.render("Score: {}".format(int(score)),True,(255,255,255))

    # 5. draw on the screen
    screen.blit(background,(0,0))
    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
        

    screen.blit(stage,(0,screen_height-stage_height))
    screen.blit(score_font,(500,screen_height-stage_height/2))

    screen.blit(character, (character_x_pos,character_y_pos))
    
    # calculate elapsed time
    elapsed_time = (pygame.time.get_ticks() - start_ticks)/1000 
    timer = game_font.render("Time: {}".format(int(total_time - elapsed_time)),True,(255,255,255))
    screen.blit(timer,(10,10))
    if(total_time - elapsed_time<0):
        running = False
        game_result = "Time Over"
        break

    # left bullets
    left_bullets = game_font.render("Left bullet: {}".format(int(number_of_weapon)),True,(255,255,255))
    screen.blit(left_bullets,(400,10))

    # keep draw background
    pygame.display.update()

msg = game_font.render(game_result, True, (255,0,0)) 
msg_rect = msg.get_rect(center=(screen_width//2, screen_height//2))
screen.blit(msg,msg_rect)
pygame.display.update()

# delay two seconds
pygame.time.delay(2000)
# terminate pygame
pygame.quit()
