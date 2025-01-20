import pygame
import time
import random

#Get Font
pygame.font.init()



#Screen Width and Height
WIDTH, HEIGHT = 900, 650

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Coffee Shooter")


#Game Background
BG = pygame.transform.scale(pygame.image.load('gameBackground.png'), (WIDTH, HEIGHT))

#Variable used to establish frame rate while the game is running
clock = pygame.time.Clock()


#Dimensions and movement for game objects

PLAYER_WIDTH = 70
PLAYER_HEIGHT = 70
PLAYER_VEL = 10
SHOT_WIDTH = 40
SHOT_HEIGHT = 40
SHOT_VEL = 7.5
COFFEE_WIDTH = 50
COFFEE_HEIGHT = 50
COFFEE_VEL = 3
BOSS_WIDTH = 650
BOSS_HEIGHT = 250
BOSS_VEL = 10


#Images for game objects and the font
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load('burr_grinder.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))
COFFEE_IMAGE = pygame.transform.scale(pygame.image.load('coffee_bean.png'), (COFFEE_WIDTH, COFFEE_HEIGHT))
BLADE_IMAGE = pygame.transform.scale(pygame.image.load('blade_shot.png'), (SHOT_WIDTH, SHOT_HEIGHT))
FONT = pygame.font.SysFont("comicsans", 30)
BOSS_IMAGE = pygame.transform.scale(pygame.image.load('coffee_bean.png'), (BOSS_WIDTH, BOSS_HEIGHT))
BOSS_SHOT = pygame.transform.scale(pygame.image.load('boss_shot.png'), (SHOT_WIDTH, SHOT_HEIGHT))

#Make the graphics for the game
def draw(player, elapsed_time, coffees, shots, boss, boss_shots, boss_health_bar, lives):
    #Draw the background.
    WIN.blit(BG, (0,0))

    #Text for in-game timer
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "green")

    WIN.blit(time_text, (10,10))
    
    #Draw the player
    WIN.blit(PLAYER_IMAGE, (player.x, player.y))

    #Draw the boss
    if boss:

        WIN.blit(BOSS_IMAGE, (boss.x, boss.y))

        #Draw the boss's health bar
        pygame.draw.rect(WIN, "red", boss_health_bar)

        #Draw the boss projectiles
        for boss_attack in boss_shots:

            WIN.blit(BOSS_SHOT, (boss_attack.x, boss_attack.y))

    #Draw the shots
    for shot in shots:
        
        WIN.blit(BLADE_IMAGE, (shot.x, shot.y))

    
    #Draw the coffee beans 
    for coffee in coffees:
        WIN.blit(COFFEE_IMAGE, (coffee.x, coffee.y))

    for live in lives:
        WIN.blit(PLAYER_IMAGE, (live.x, live.y))
    
    pygame.display.update()

#Create the falling objects to destroy.
def create_coffee():

    #Random spawn location for falling object
    coffee_x = random.randint(0, WIDTH - COFFEE_WIDTH)

    #Location and size of the falling object
    coffee_rect = pygame.Rect(coffee_x, -COFFEE_HEIGHT, COFFEE_WIDTH, COFFEE_HEIGHT)

    #Return a dictionary to use for object collision and to track health of the falling object
    return {"rect": coffee_rect, "health": 1}

def create_boss(defeated_boss, speed):

    #Random X-location for boss
    boss_x = random.randrange(0, WIDTH - BOSS_WIDTH, 10)

    #Location and size of the boss object
    boss_rect = pygame.Rect(boss_x, 100, BOSS_WIDTH, BOSS_HEIGHT)

    #Beginning boss value
    if defeated_boss == 0:

        #Return a dictionary to use for object collision and to track boss health
        return {"rect": boss_rect, "health": 50, "boss_vel": speed}

    #Increase boss's health by the bosses defeated and increase boss's speed by 1.5 times for the 2nd and 3rd boss
    elif 0 < defeated_boss <=3:
        return {"rect": boss_rect, "health": (defeated_boss +1) * 50, "boss_vel": speed * 1.5}

    #Increase boss's health by the bosses defeated and increase boss's speed by 2 times for the 4th and final boss
    else:
        return {"rect": boss_rect, "health": (defeated_boss +1) * 50, "boss_vel": speed * 2}


def main():
    #Initialize while loop to run the game
    run = True

    #Create the player object
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    #Use to subtract the difference between start time and the start of the time.time() function
    start_time = time.time()
    
    #Initialize elapsed_time
    elapsed_time = 0

    #This number equates to 4 seconds when using the clock.tick function.
    coffee_add_increment = 2000

    #Coffee count
    coffee_count = 0

    #List used to store each created object to draw
    coffees = []

    #List to store all the shots fired by the player
    shots = []

    #List to store all the shots coming from the boss
    boss_shots = []
    
    #Boolean used to end the game if the player gets hit
    hit = False

    #Initialize boss before being created
    boss = None

    #Counter used to initialize boss
    boss_count = 0

    #Used to determine whether a new boss should be created
    defeated_boss = 0

    #Boss movement counter used to regulate movement
    move_count = 0

    #Boss attack count initialized to 0 to use later on for projectile spawning
    last_attack = 0

    #Boss attack delay count
    delay_attack = 0.10

    #Player attack delay count
    player_attack_delay = 0.07

    #Player projectile count initialized to 0 to use later on for player's projectile spawning
    shot_attack = 0

    #Initialize for boss moving downwards
    down = 0

    #Used for random x movement of boss
    boss_x_count = 0

    #Assign a random location on the screen to use to move boss upwards later
    x_location = random.randrange(0, WIDTH - BOSS_WIDTH)

    #Player Health
    player_health = 3

    #Player i-frame timing for boss initialized for time.time() function
    boss_hitting_player_iframe = 0

    #Player i-frame
    damage_delay = 0.30

    #Player i-frame timing for boss attack hitting player initialized for time.time() function
    boss_attack_hitting_player_iframe = 0

    #Player i-frame timing for coffee bean projectile hitting player initialized for time.time() function
    coffee_bean_hitting_player_iframe = 0

    #Player lives on screen
    lives = [pygame.Rect(650, 10, PLAYER_WIDTH, PLAYER_HEIGHT),
            pygame.Rect(720, 10, PLAYER_WIDTH, PLAYER_HEIGHT),
            pygame.Rect(790, 10, PLAYER_WIDTH, PLAYER_HEIGHT)]

    while run:
        #coffee_count becomes 1000 every 60 frames
        coffee_count += clock.tick(60)
        
        #Time the game has been running
        elapsed_time = time.time() - start_time

        #Add new coffee beans every 2 seconds
        if coffee_count > coffee_add_increment:

            #Add 3 coffee beans every iteration.
            for i in range(3):

                #Add the coffee to the coffees array to use for the draw function.
                coffees.append(create_coffee())

            #Decreases original by 50 after every iteration with 200 being the lowest possible value.
            coffee_add_increment = max(700, coffee_add_increment - 50)

            #Returns coffee_count to 0 after every iteration.
            coffee_count = 0

        #Create the boss.   
        if elapsed_time > 1 and boss is None and boss_count == 0:

            #Reset the down counter for downwards mobility later on
            down = 0

            #Run the create_boss function and store in a variable for later use
            boss = create_boss(defeated_boss, BOSS_VEL)

            if boss:

                #Create the boss's health bar
                boss_health = pygame.Rect(WIDTH / 4, 60, 400, 20)

                #Used to dynamically change boss's health bar upon each hit
                full_health = boss["health"]

            #Crete a boss hitbox to compensate for the fact that the rect object is bigger than the picture
            boss_hitbox = boss["rect"].inflate(-300,-90)

            #Use to move boss downwards when health reaches below half
            boss_half = boss["health"] / 2

        #Create up to 5 new bosses once conditions are met    
        if 0 < defeated_boss <= 5 and boss is None and elapsed_time / defeated_boss >= 30: 

            #Counter used to spawn boss once conditions are met
            boss_count = 0

        #Moves the boss to the left side of the screen    
        if boss and boss["rect"].x - BOSS_VEL >= -150 and move_count == 0:

            #Move the boss to the left
            boss["rect"].x -= boss["boss_vel"] 

            #Move the hitbox upon each frame with the boss
            boss_hitbox = boss["rect"].inflate(-300,-90)

        #Moves the boss to the right side of the screen once the boss reaches the beginning screen width    
        elif boss and boss["rect"].x - BOSS_VEL <= -150:

            #Used to move boss upwards only when count reaches a certain number
            boss_x_count += 1

            #The boss movement count increases by 1 to prevent boss object from moving left
            move_count = 1
 
            #Move boss to the right
            boss["rect"].x += boss["boss_vel"]

            #Move the hitbox upon each frame with the boss
            boss_hitbox = boss["rect"].inflate(-300,-90)

        #Continues to move the boss to the right side of the screen    
        elif boss and move_count == 1 and boss["rect"].x + BOSS_VEL + BOSS_WIDTH <= WIDTH + 150:
            
            #Move the boss to the right
            boss["rect"].x += boss["boss_vel"]

            #Move the hitbox upon each frame with the boss
            boss_hitbox = boss["rect"].inflate(-300,-90)

        #Moves the boss to the left again once the boss's x movement goes past the screen-width size    
        elif boss and boss["rect"].x + BOSS_VEL + BOSS_WIDTH >= WIDTH + 150:

            #Accumulates when the boss hits the left side of the screen
            boss_x_count += 1

            #The boss movement count adjusts back to 0 to run the if condition for left movement
            move_count = 0
            
        #Logic to move the boss downwards toward the player
        if boss and boss["health"] <= boss_half and boss['rect'].y + BOSS_HEIGHT <= HEIGHT and down == 0:
            
            #Reset count to use to move boss upwards later
            boss_x_count = 0

            #Move_count increased to 2 in order to avoid the boss moving left or right
            move_count = 2
            
            #Move the boss down
            boss["rect"].y += boss["boss_vel"]

            #Move the hitbox upon each frame with the boss
            boss_hitbox = boss["rect"].inflate(-300,-90)

        #Logic to revert back to regular horizontal movement
        elif boss and boss['rect'].y + BOSS_HEIGHT >= HEIGHT and boss["rect"].x <= WIDTH + 150 and move_count == 2:

            #Down increased to 1 as soon as the boss hits the bottom
            down = 1

            #Move count reverted back to 0 to move the boss left again
            move_count = 0

            #Move the hitbox upon each frame with the boss
            boss_hitbox = boss["rect"].inflate(-300,-90)

        #Logic to start moving the boss upwards once the boss hits a random x-axis.
        elif boss and boss["rect"].y >= 100 and down == 1 and boss_x_count > 2:

            #Once the boss reaches the original spawn point, revert back to regular horizontal movement
            if boss["rect"].y <= 100:
                
                #Used to revert back to leftwards movement
                move_count = 0

                #Counter set to 2 to avoid upwards and downwards movement
                down = 2

                #Reset boss_x_count to get next generated boss to move up
                boss_x_count = 0

            #Condition that checks if the boss is within a random rect.x location assigned
            elif boss["rect"].x <= x_location + boss["boss_vel"] and boss["rect"].x >= x_location - boss["boss_vel"]:

                #Ensure that the boss moves up
                boss["rect"].x = x_location

                #Move count to prevent horizontal movement while moving upwards
                move_count = 2

                #Begin to move the boss upwards
                boss["rect"].y -= boss["boss_vel"]

                #Move the hitbox upon each frame with the boss
                boss_hitbox = boss["rect"].inflate(-300,-90)

        #Logic to set up the boss attack
        if boss: 
            
            #Used to subtract from the bosses last attack
            current_time = time.time()

            #If the current if block math is greater than the delay_attack variable, execute
            if current_time - last_attack >= delay_attack:

                #Spawn the boss projectile
                boss_attack = pygame.Rect(boss["rect"].x + boss["rect"].width // 2 - SHOT_WIDTH // 2, boss["rect"].y + 130, SHOT_WIDTH, SHOT_HEIGHT)

                #Logic to limit boss attack on the screen and only attack when the boss is in a certain vertical position
                if len(boss_shots) < 15 and boss["rect"].y == 100:

                    #Add each boss projectile onto a list to render
                    boss_shots.append(boss_attack)
                
                #Store the value of the time the last attack released to keep the boss attack logic going
                last_attack = current_time

            #Loop to set-up each boss attack
            for boss_attack in boss_shots[:]:

            #Attack moves downwards each iteration
                boss_attack.y += 10

            #Removes the attack from the boss_attack list everytime the attack goes off-screen
                if boss_attack.y + SHOT_HEIGHT > HEIGHT:
                    boss_shots.remove(boss_attack)

                #If the boss object hits the player, end the game
                elif boss_attack.colliderect(player):
                    
                    #Code block to activate player i-frame upon being hit by boss projectile
                    boss_attack_time = time.time()

                    if boss_attack_time - boss_attack_hitting_player_iframe >= damage_delay:

                        player_health -= 1

                        #Remove lives from the screen after being hit
                        lives.pop()

                        boss_shots.remove(boss_attack)

                    boss_attack_hitting_player_iframe = boss_attack_time

                elif player_health <= 0:

                    hit = True

                    break

        #Add a quit option for the game. 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #Add pause functionaility to the game
            if event.type == pygame.KEYDOWN:

                #If k on the keyboard is hit, pause the game
                if event.key == pygame.K_k:
                    # Pause the game
                    paused = True

                    pause_text = FONT.render("Paused", 1, "green")
                    WIN.blit(pause_text, (WIDTH/2 - pause_text.get_width()/2, HEIGHT/2 - pause_text.get_height()/2))
                    pygame.display.update()
                    
                    #Check again to see if k is pressed to unpause the game
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_k:
                                    paused = False

                            #Added the quit option again to be able to exit the game while the game is paused
                            elif event.type == pygame.QUIT:
                                paused = False
                                run = False
                                break
        #Player controls.    
        keys  = pygame.key.get_pressed()

        #Left movement
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL

        #Right movement
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        #Up movement
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >=0:
            player.y -= PLAYER_VEL

        #Down movement    
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL

        #Shoot button   
        if keys[pygame.K_SPACE]:
            
            #Track current time to use for regulating player projectile frequency
            shot_time = time.time()

            #Used the current time minus the last shot that spawned if greater than spawn delay
            if shot_time - shot_attack >= player_attack_delay:


            #Create the object for the player to shoot
                shot = pygame.Rect(player.x + player.width // 2 - SHOT_WIDTH // 2, player.y, SHOT_WIDTH, SHOT_HEIGHT)

            #Maximum number of shots possible to have on screen at a time
                if len(shots) < 25:

                    #Add new shots each time the spacebar key is hit
                    shots.append(shot)
                
                #Re-initialze shot_attack to the time the last player projectile spawned
                shot_attack = shot_time

        #Create a for-loop of a copy of the shots list to track the shots shown on screen and to check for collisions      
        for shot in shots[:]:

            #Shot moves upwards each iteration
            shot.y -= SHOT_VEL

            #Removes the shot from the shots list everytime the shot goes off-screen
            if shot.y + SHOT_HEIGHT < 0:
                shots.remove(shot)

            #Boss health goes down when a shot hits    
            elif boss and shot.colliderect(boss["rect"]):

                #Lower boss's health when player's projectile hits
                boss["health"] -= 1

                #Try block used to avoid a ZeroDivisionError when boss's health hits zero
                try:
                    
                    #Lower bosses health graphic each time boss is hit
                    boss_health.width -= 250 / full_health

                #When boss's health reaches zero, keep running the program
                except ZeroDivisionError:
                    continue

                #Exception handling added just in case player projectile hits multiple objects at once
                try:

                    #Remove player's projectile to manage memory
                    shots.remove(shot)

                except ValueError:
                    continue

                #Remove the boss once health hits 0
                if boss and boss["health"] <= 0:

                    #Despawn boss upon defeat
                    boss = None

                    #Increase the boss count to prevent the create_boss() function to run immediately
                    boss_count += 1

                    #Defeated boss counter used to run different if/else block in the create_boss() function
                    defeated_boss += 1

                    #Reset boss movement for the next create_boss iteration
                    move_count = 0

                    #Reset boss_shots to zero to prevent boss_shots from being spawned when another boss gets created
                    boss_shots = []

                    break
                
                

            #Reduce coffee bean health when a shot hits a coffee bean and destroy boss projectiles                 
            else:

                #Run a for loop on a copy of the boss_attack list to avoid RunTimeErrors
                #and to avoid skipping iterations after deleting a boss attack
                for boss_attack in boss_shots[:]:
                    
                    #If player shots hit boss's projectiles, do the following
                    if shot.colliderect(boss_attack):

                        #Despawn boss and player's projectiles to manage memory
                        boss_shots.remove(boss_attack)

                        #Exception handling added just in case player projectile hits multiple objects at once
                        try:

                            #Remove player's projectile to manage memory
                            shots.remove(shot)

                        except ValueError:
                            continue

                        #End loop once target is destroyed to avoid looping errors
                        break

                #Run a for loop on a copy of the coffees list to avoid RunTimeErrors
                #and to avoid skipping iterations after deleting coffee bean
                for coffee in coffees[:]:
                    
                    #If the player's shot hits the target, do the following
                    if shot.colliderect(coffee["rect"]):

                        #Subtract health from the target, then despawn player projectile to manage memory
                        coffee["health"] -= 1

                        #Exception handling added just in case player projectile hits multiple objects at once
                        try:

                            #Remove player's projectile to manage memory
                            shots.remove(shot)

                        except ValueError:
                            continue

                        #Despawn target once count hits zero
                        if coffee["health"] <= 0:

                            coffees.remove(coffee)

                        #End loop once target is destroyed to avoid looping errors    
                        break
        

        #Run a for loop on a copy of the coffees list to avoid RunTimeErrors
        #and to avoid skipping iterations after deleting coffee bean
        for coffee in coffees[:]:

            #coffee y coordinate value moving down based on COFFEE_VEL value
            coffee["rect"].y += COFFEE_VEL

            #If coffee bean is off screen remove the coffee bean from the coffees list
            if coffee["rect"].y > HEIGHT:
                coffees.remove(coffee)

            #Set the collision for the player hitting the coffee bean  
            elif coffee["rect"].colliderect(player):
                
                #Code block for player i-frame on falling projectil hitting player
                coffee_time = time.time()
                
                if coffee_time - coffee_bean_hitting_player_iframe >= damage_delay:


                    player_health -= 1

                    #Remove live from the screen after being hit
                    lives.pop()

                    coffees.remove(coffee)
                
                coffee_bean_hitting_player_iframe = coffee_time

            elif player_health <= 0:

                hit = True
                break

        #Use the boss hitbox to detect collision with the player
        if boss and boss_hitbox.colliderect(player):

            #Code block to set up the player's i-frame for when the player hit's the boss's body
            boss_hits = time.time()

            if boss_hits - boss_hitting_player_iframe >= damage_delay:

                player_health -= 1

                #Remove live from the screen after being hit
                lives.pop()
            
            boss_hitting_player_iframe = boss_hits

        elif player_health <= 0:

            #End the game if the boss hits the player
            hit = True

        #End game if hit.
        if hit:

            #Print the end game text
            lost_text = FONT.render("YOU LOSE! GOOD DAY SIR!", 1, "green")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        #Draw the game.    
        draw(player, elapsed_time, [coffee["rect"] for coffee in coffees], shots, boss["rect"] if boss else pygame.Rect(0, 0, 0, 0), boss_shots, boss_health if boss else pygame.Rect(0,0,0,0), lives)
        

    pygame.quit()

#Run the main function if it's not being used as an import file

if __name__ == "__main__":
    main()
