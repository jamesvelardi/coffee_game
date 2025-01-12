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

clock = pygame.time.Clock()


#Dimensions and movement for game objects

PLAYER_WIDTH = 70
PLAYER_HEIGHT = 70
PLAYER_VEL = 10
SHOT_WIDTH = 40
SHOT_HEIGHT = 40
SHOT_VEL = 5
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
def draw(player, elapsed_time, coffees, shots, boss, boss_shots):
    #Draw the background.
    WIN.blit(BG, (0,0))

    #Text for in-game timer
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")

    WIN.blit(time_text, (10,10))
    
    #Draw the player
    WIN.blit(PLAYER_IMAGE, (player.x, player.y))

    #Draw the boss
    if boss:
        WIN.blit(BOSS_IMAGE, (boss.x, boss.y))

        for boss_attack in boss_shots:

            WIN.blit(BOSS_SHOT, (boss_attack.x, boss_attack.y))

    #Draw the shots
    for shot in shots:
        
        WIN.blit(BLADE_IMAGE, (shot.x, shot.y))

    
    #Draw the coffee beans 
    for coffee in coffees:
        WIN.blit(COFFEE_IMAGE, (coffee.x, coffee.y))
    
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

    #Location and size of the boss object
    boss_rect = pygame.Rect(150, 100, BOSS_WIDTH, BOSS_HEIGHT)

    #Beginning boss value
    if defeated_boss == 0:

        #Return a dictionary to use for object collision and to track boss health
        return {"rect": boss_rect, "health": 10, "boss_vel": speed}

    #Double bosses health and speed every iteration
    elif defeated_boss > 0:
        return {"rect": boss_rect, "health": (defeated_boss +1) * 10, "boss_vel": speed * defeated_boss}


def main():
    #Initialize while loop to run the game
    run = True

    #Create the player object
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    #Use to subtract the difference between start time and the start of the time.time() function
    start_time = time.time()
    
    #Initialize elapsed_time
    elapsed_time = 0

    #This number equates to 2 seconds when using the clock.tick function.
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

    #Boolean for space bar hit
    space_bar = False

    #Initialize boss before being created
    boss = None

    #Counter used to initialize boss
    boss_count = 0

    #Used to determine whether a new boss should be created
    defeated_boss = 0

    #Boss movement counter used to regulate movement
    move_count = 0

    #Boss attack count used to delay attack

    last_attack = 0

    #Boss attack delay count

    delay_attack = 0.10

    #Initialize for boss moving downwards
    down = 0

    #Random X-location for boss
    boss_x = random.randrange(0, WIDTH - BOSS_WIDTH, 10)

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
            coffee_add_increment = max(200, coffee_add_increment - 50)

            #Returns coffee_count to 0 after every iteration.
            coffee_count = 0

        #Create the boss.   
        if elapsed_time > 1 and boss is None and boss_count == 0:

            #Run the create_boss function and store in a variable for later use
            boss = create_boss(defeated_boss, BOSS_VEL)

            #Crete a boss hitbox to compensate for the fact that the rect object is bigger than the picture
            boss_hitbox = boss["rect"].inflate(-300,-90)

            #Use to move boss downwards when health reaches below half
            boss_half = boss["health"] / 2

        #Create up to 5 new bosses once conditions are met    
        if 0 < defeated_boss <= 5 and boss is None and elapsed_time / defeated_boss >= 10: 

            #Track the amount of bosses
            boss_count = 0

        #Moves the boss to the left side of the screen    
        if boss and boss["rect"].x - BOSS_VEL >= -150 and move_count == 0:

            #Move the boss to the left
            boss["rect"].x -= boss["boss_vel"] 

            #Move the hitbox upon each frame with the boss
            boss_hitbox = boss["rect"].inflate(-300,-90)

        #Moves the boss to the right side of the screen once the boss reaches the beginning screen width    
        elif boss and boss["rect"].x <= -150:

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

            #The boss movement count adjusts back to 0 to run the if condition for left movement
            move_count = 0
            
        #Logic to move the boss downwards toward the player
        if boss and boss["health"] <= boss_half and boss['rect'].y + BOSS_HEIGHT <= HEIGHT and down == 0:
            #Move_count increased to 2 in order to avoid the boss moving left or right
            move_count = 2
            
            #Move the boss down
            boss["rect"].y += boss["boss_vel"]

            #Move the hitbox upon each frame with the boss
            boss_hitbox = boss["rect"].inflate(-300,-90)

        #Logic to revert back to regular horizontal movement
        elif boss and boss['rect'].y + BOSS_HEIGHT >= HEIGHT and boss["rect"].x <= WIDTH + 150 and move_count !=1 and boss["rect"].x != boss_x:

            #Down increased to 1 as soon as the boss hits the bottom
            down = 1

            #Move count reverted back to 0 to move the boss left again
            move_count = 0

            #Move the hitbox upon each frame with the boss
            boss_hitbox = boss["rect"].inflate(-300,-90)

        #Logic to start moving the boss upwards once the boss hits a random x-axis.
        elif boss and boss["rect"].y + BOSS_HEIGHT >= HEIGHT and boss["rect"].x == boss_x:

            #Move count to prevent horizontal movement while moving upwards
            move_count = 2

            #Begin to move the boss upwards
            boss["rect"].y -= boss["boss_vel"]

            #Move the hitbox upon each frame with the boss
            boss_hitbox = boss["rect"].inflate(-300,-90)

        #Move boss upwards until the boss reaches a certain point on the y-axis
        elif boss and boss["rect"].y >= 100 and boss["rect"].x == boss_x and down == 1:
            
            #Once the boss reaches the original spawn point, revert back to regular horizontal movement
            if boss["rect"].y <= 100:
                
                #Used to revert back to leftwards movement
                move_count = 0

                #Counter set to 2 to avoid triggering the other if/else blocks using the random boss_x variable
                down = 2

            else:

                #Move boss upwards
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
                boss_attack = pygame.Rect(boss["rect"].x + boss["rect"].width // 2 - SHOT_WIDTH // 2, boss["rect"].y, SHOT_WIDTH, SHOT_HEIGHT)

                #Logic to limit boss attack on the screen and only attack when the boss is in a certain vertical position
                if len(boss_shots) < 15 and boss["rect"].y == 100:

                    #Add each boss projectile onto a list to render
                    boss_shots.append(boss_attack)
                
                #Store the value of the time the last attack released to keep the boss attack logic going
                last_attack = current_time

            #Loop to set-up each boss attack
            for boss_attack in boss_shots[:]:

            #Attack moves downwards each iteration
                boss_attack.y += SHOT_VEL

            #Removes the attack from the boss_attack list everytime the attack goes off-screen
                if boss_attack.y + SHOT_HEIGHT > HEIGHT:
                    boss_shots.remove(boss_attack)

                #If the boss object hits the player, end the game
                elif boss_attack.colliderect(player):
                        hit = True

                        break



        #Add a quit option for the game. 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
            
            if not space_bar:
            #Create the object for the player to shoot
                shot = pygame.Rect(player.x + player.width // 2 - SHOT_WIDTH // 2, player.y, SHOT_WIDTH, SHOT_HEIGHT)

            #Maximum number of shots possible to have on screen at a time
                if len(shots) < 50:

                    #Add new shots each time the spacebar is hit
                    shots.append(shot)

                space_bar = True
        else:
            space_bar = False

        #Create a for-loop of a copy of the shots list to track the shots shown on screen and to check for collisions      
        for shot in shots[:]:

            #Shot moves upwards each iteration
            shot.y -= SHOT_VEL

            #Removes the shot from the shots list everytime the shot goes off-screen
            if shot.y + SHOT_HEIGHT < 0:
                shots.remove(shot)

            #Boss health goes down when a shot hits    
            elif boss and shot.colliderect(boss["rect"]):
                boss["health"] -= 1
                shots.remove(shot)

                #Remove the boss once health hits 0
                if boss and boss["health"] <= 0:
                    boss = None

                    #Increase the boss count to prevent the create_boss() function to run
                    boss_count += 1
                    defeated_boss += 1
                    move_count = 0
                    break
                
                

            #Reduce coffee bean health when a shot hits a coffee bean and destroy boss projectiles                 
            else:

                #Run a for loop on a copy of the boss_attack list to avoid RunTimeErrors
                #and to avoid skipping iterations after deleting a boss attack
                for boss_attack in boss_shots[:]:
                    
                    if shot.colliderect(boss_attack):
                        boss_shots.remove(boss_attack)
                        shots.remove(shot)
                        break

                #Run a for loop on a copy of the coffees list to avoid RunTimeErrors
                #and to avoid skipping iterations after deleting coffee bean
                for coffee in coffees[:]:

                    if shot.colliderect(coffee["rect"]):
                        coffee["health"] -= 1
                        shots.remove(shot)
                        if coffee["health"] <= 0:
                            coffees.remove(coffee)
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
                coffees.remove(coffee)
                hit = True
                break

        #Use the boss hitbox to detect collision with the player
        if boss and boss_hitbox.colliderect(player):

            #End the game if the boss hits the player
            hit = True

        #End game if hit.
        if hit:

            #Print the end game text
            lost_text = FONT.render("YOU LOSE! GOOD DAY SIR!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        #Draw the game.    
        draw(player, elapsed_time, [coffee["rect"] for coffee in coffees], shots, boss["rect"] if boss else pygame.Rect(0, 0, 0, 0), boss_shots)


    pygame.quit()

#Run the main function if it's not being used as an import file

if __name__ == "__main__":
    main()
