import pygame
import sys
import random
from path import *

# Initialize Pygame
pygame.init()

# Initialize the mixer module
pygame.mixer.init()

#Create a clock object to control the frame rate of the game
clock = pygame.time.Clock()

# Setting different game states
MENU = 0 #opening screen
LEVELS = 1 #levels display screen
EASY = 2 #easy game screen
MEDIUM = 3 #medium game screen
HARD = 4 #hard game screen
WIN = 5 #win screen
TRY_AGAIN = 6 #try again screen

# Setting the screen width and height
SCREEN_WIDTH = 552
SCREEN_HEIGHT = 552

# Define colors
WHITE=(255,255,255)
LGREEN = (144, 238, 144)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LBROWN=(205,133,63)
RED=(255,0,0)
LBLUE=(135,206,235)
GRAY=(128,128,128)
LPINK=(255,192,203)

# Setting up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MAZE GAME")

# Loading images
background = pygame.transform.scale(pygame.image.load("bg.jpg"), (552, 552))
background2 = pygame.transform.scale(pygame.image.load("bg2.png"), (552, 552))

#Setting initial game state
game_state = MENU

# Initialize mixer for music
pygame.mixer.init()

#Load music
menu_music="menu_music.mp3"
pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1)

#Score
global score_value
score_value=0
#Lives
global lives
lives=3

#Load font
font = pygame.font.Font(None, 36)
font1 = pygame.font.Font('freesansbold.ttf', 16)

#easy level game screen
def easy_level():
    #setting the parameters for maze
    WIDTH = 31
    HEIGHT = 31
    MARGIN = 2
    ROWS = 15
    COLS = 15
    #Set of sprite images for walls
    sprite_images=[
    pygame.transform.scale(pygame.image.load("sprite1.jpg"),(31,31)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite2.jpg"),(31,31)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite3.jpg"),(31,31)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite4.jpg"),(31,31)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite5.jpg"),(31,31)).convert_alpha()
]
    # Initialize maze grid
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    #Create a 2D list to store the images for each block
    images=[[random.choice(sprite_images) for _ in range(COLS)] for _ in range(ROWS)]
    # Recursive backtracking algorithm for maze generation
    def recursive_backtracking(x, y):
        maze[x][y] = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = x + 2*dx, y + 2*dy
            if 0 <= new_x < ROWS and 0 <= new_y < COLS and maze[new_x][new_y]:
                maze[x + dx][y + dy] = 0
                recursive_backtracking(new_x, new_y)
    #write maze
    List = []
    def write_maze_solution(maze, filename):
        with open(filename, 'w') as file:
            for row in maze:
                line = ' '.join(map(str, row)) + '\n'
                file.write(line)
                List.append(line.strip())
                
    
    # Call recursive_backtracking function to generate maze
    recursive_backtracking(1, 1)
    # Write maze solution to a file
    write_maze_solution (maze, 'maze_solution.txt')

    
    for i in range(len(List)):
        List[i] = List[i].split(' ')

    path = find_path(List)

    with open("path.txt","w") as file:
        file.write(str(path))

    # Draw the maze
    def draw_maze(screen):
        for row in range(ROWS):
            for col in range(COLS):
                if maze[row][col]==0:
                    color=LBLUE
                    pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                if maze[row][col]==1:#If it's a sprite blit the image
                    screen.blit(images[row][col],((MARGIN+WIDTH)*col+MARGIN,(MARGIN+HEIGHT)*row+MARGIN))
    # Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self, image):
            super().__init__()
            self.image = image
            self.rect=self.image.get_rect()
            self.rect.x = MARGIN + WIDTH
            self.rect.y = MARGIN + HEIGHT

        def move(self, dx, dy):
            new_x = self.rect.x + dx
            new_y = self.rect.y + dy
            if 0 <= new_x <= (WIDTH + MARGIN) * COLS - WIDTH and 0 <= new_y <= (HEIGHT + MARGIN) * ROWS - HEIGHT:
                if not maze[new_y // (HEIGHT + MARGIN)][new_x // (WIDTH + MARGIN)]:
                    self.rect.x = new_x
                    self.rect.y = new_y
                else:
                    global lives
                    lives-=1
                    collision=pygame.mixer.Sound('collision.mp3')
                    collision.play()
                    if lives<=0:
                        lives=0
                        
        def get_position(self):
            return self.rect.x,self.rect.y
    #collectible class
    class Collectible(pygame.sprite.Sprite):
        def __init__(self, image):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.spawn_collectible()
        def spawn_collectible(self):
            while True:
                x=random.randint(0,COLS-1)
                y=random.randint(0,ROWS-1)
                if not maze[y][x]:
                    self.rect.x = x * (WIDTH + MARGIN) + MARGIN
                    self.rect.y = y * (HEIGHT + MARGIN)+ MARGIN
                    break

        def update(self, player):
            if pygame.sprite.collide_rect(self, player):
                global score_value
                score_value += 10
                self.spawn_collectible()



    #Score
    font=pygame.font.SysFont('Marker Felt',32)
    textX=10
    textY=510
    def show_score(x,y):
        score=font.render("Score : "+str(score_value),True,(0,0,0))
        screen.blit(score,(x,y))
    #Lives
    textx=180
    texty=510
    def show_lives(x,y):
            live=font.render("Lives : "+str(lives),True,(0,0,0))
            screen.blit(live,(x,y))
    #Timer
    pygame.time.set_timer(pygame.USEREVENT,1000)
    textA=320
    textB=510
    global counter
    counter=25
    text='25'
    def show_timer(x,y):
        timer=font.render("Time Left : "+str(counter),True,(0,0,0))
        screen.blit(timer,(x,y))
    #show level
    textC=20
    textD=530
    def show_level(x,y):
        slevel=font1.render("LEVEL 1:Reach the bottom right corner without colliding in 25s",True,(0,0,0))
        screen.blit(slevel,(x,y))
    # Main function
    def main():
        # Generate maze
        recursive_backtracking(1,1)
        player_image=pygame.transform.scale(pygame.image.load("puppy.jpg"),(31,31)).convert_alpha()
        # Create player object
        player = Player(player_image)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        # Create collectible object
        collectible_image = pygame.transform.scale(pygame.image.load("collectible.png"), (31, 31)).convert_alpha()
        collectible1 = Collectible(collectible_image)
        collectible2 = Collectible(collectible_image)
        collectible3 = Collectible(collectible_image)
        all_sprites.add(collectible1,collectible2,collectible3)
        font = pygame.font.SysFont(None, 36)
        done = False
        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                global score_value
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.USEREVENT: #for timer
                    global counter
                    counter-=1
                    if counter>0:
                        text=str(counter)
                    else:
                        global lives
                        lives -= 1
                        collision=pygame.mixer.Sound('collision.mp3') #for collision sound
                        collision.play()
                        if lives == 0:
                            lose()
                        counter = 25
                elif event.type == pygame.KEYDOWN:
                    global score_value
                    if event.key == pygame.K_LEFT:
                        player.move(-WIDTH - MARGIN, 0)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                    elif event.key == pygame.K_RIGHT:
                        player.move(WIDTH + MARGIN, 0)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                    elif event.key == pygame.K_UP:
                        player.move(0, -HEIGHT - MARGIN)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                    elif event.key == pygame.K_DOWN:
                        player.move(0, HEIGHT + MARGIN)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                elif player.get_position()==((MARGIN+HEIGHT)*(COLS-2),(MARGIN+WIDTH)*(ROWS-2)) and counter>0:
                    global game_state
                    game_state = MEDIUM #redirection to medium level if wins easy level within 3 lives
                    medium_level()
                elif player.get_position()!=((MARGIN+HEIGHT)*(COLS-2),(MARGIN+WIDTH)*(ROWS-2)) and lives==0:
                    lose() #redirection to try again screen if loses
                    pygame.display.update()

            screen.fill(LBLUE)
            draw_maze(screen)
            all_sprites.draw(screen)
            collectible1.update(player)
            collectible2.update(player)
            collectible3.update(player)
            show_score(textX,textY)
            show_lives(textx,texty)
            show_timer(textA,textB)
            show_level(textC,textD)
            pygame.display.flip()
            clock.tick(120)
    main()
    
#medium game screen
def medium_level():
    #maze parameters
    WIDTH = 24
    HEIGHT = 24
    MARGIN = 2
    ROWS = 19
    COLS = 21
    #Set of sprite images for walls
    sprite_images=[
    pygame.transform.scale(pygame.image.load("sprite1.jpg"),(24,24)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite2.jpg"),(24,24)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite3.jpg"),(24,24)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite4.jpg"),(24,24)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite5.jpg"),(24,24)).convert_alpha()
]
    # Initialize maze grid
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    #Create a 2D list to store the images for each block
    images=[[random.choice(sprite_images) for _ in range(COLS)] for _ in range(ROWS)]
    # Recursive backtracking algorithm for maze generation
    def recursive_backtracking(x, y):
        maze[x][y] = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = x + 2*dx, y + 2*dy
            if 0 <= new_x < ROWS and 0 <= new_y < COLS and maze[new_x][new_y]:
                maze[x + dx][y + dy] = 0
                recursive_backtracking(new_x, new_y)
    #write maze
    List = []
    def write_maze_solution(maze, filename):
        with open(filename, 'w') as file:
            for row in maze:
                line = ' '.join(map(str, row)) + '\n'
                file.write(line)
                List.append(line.strip())
                
    
    # Call recursive_backtracking function to generate maze
    recursive_backtracking(1, 1)
    # Write maze solution to a file
    write_maze_solution (maze, 'maze_solution.txt')

    
    for i in range(len(List)):
        List[i] = List[i].split(' ')

    path = find_path(List)

    with open("path.txt","w") as file:
        file.write(str(path))

    # Draw the maze
    def draw_maze(screen):
        for row in range(ROWS):
            for col in range(COLS):
                if maze[row][col]==0:
                    color=LBLUE
                    pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                if maze[row][col]==1:#If it's a sprite blit the image
                    screen.blit(images[row][col],((MARGIN+WIDTH)*col+MARGIN,(MARGIN+HEIGHT)*row+MARGIN))
    # Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self, image):
            super().__init__()
            self.image = image
            self.rect=self.image.get_rect()
            self.rect.x = MARGIN + WIDTH
            self.rect.y = MARGIN + HEIGHT

        def move(self, dx, dy):
            new_x = self.rect.x + dx
            new_y = self.rect.y + dy
            if 0 <= new_x <= (WIDTH + MARGIN) * COLS - WIDTH and 0 <= new_y <= (HEIGHT + MARGIN) * ROWS - HEIGHT:
                if not maze[new_y // (HEIGHT + MARGIN)][new_x // (WIDTH + MARGIN)]:
                    self.rect.x = new_x
                    self.rect.y = new_y
                else:
                    global lives
                    lives-=1
                    collision=pygame.mixer.Sound('collision.mp3')
                    collision.play()
                    if lives<=0:
                        lives=0
                        
        def get_position(self):
            return self.rect.x,self.rect.y
    #collectibles class
    class Collectible(pygame.sprite.Sprite):
        def __init__(self, image):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.spawn_collectible()
        def spawn_collectible(self):
            while True:
                x=random.randint(0,COLS-1)
                y=random.randint(0,ROWS-1)
                if not maze[y][x]:
                    self.rect.x = x * (WIDTH + MARGIN) + MARGIN
                    self.rect.y = y * (HEIGHT + MARGIN)+ MARGIN
                    break

        def update(self, player):
            if pygame.sprite.collide_rect(self, player):
                global score_value
                score_value += 10
                self.spawn_collectible()



    #Score
    font=pygame.font.SysFont('Marker Felt',32)
    textX=10
    textY=510
    def show_score(x,y):
        score=font.render("Score : "+str(score_value),True,(0,0,0))
        screen.blit(score,(x,y))
    #Lives
    textx=180
    texty=510
    def show_lives(x,y):
            live=font.render("Lives : "+str(lives),True,(0,0,0))
            screen.blit(live,(x,y))
    #Timer
    pygame.time.set_timer(pygame.USEREVENT,1000)
    textA=320
    textB=510
    global counter
    counter=30
    text='30'
    def show_timer(x,y):
        timer=font.render("Time Left : "+str(counter),True,(0,0,0))
        screen.blit(timer,(x,y))
    #show level
    textC=20
    textD=530
    def show_level(x,y):
        slevel=font1.render("LEVEL 2:Reach the bottom right corner in 20s",True,(0,0,0))
        screen.blit(slevel,(x,y))
    # Main function
    def main():
        # Generate maze
        recursive_backtracking(1,1)
        player_image=pygame.transform.scale(pygame.image.load("puppy.jpg"),(24,24)).convert_alpha()
        # Create player object
        player = Player(player_image)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        # Create collectible object
        collectible_image = pygame.transform.scale(pygame.image.load("collectible.png"), (24,24)).convert_alpha()
        collectible1 = Collectible(collectible_image)
        collectible2 = Collectible(collectible_image)
        collectible3 = Collectible(collectible_image)
        collectible4 = Collectible(collectible_image)
        all_sprites.add(collectible1,collectible2,collectible3,collectible4)
        font = pygame.font.SysFont(None, 36)
        done = False
        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.USEREVENT:
                    global counter
                    counter-=1
                    if counter>0:
                        text=str(counter)
                    else:
                        global lives
                        lives -= 1
                        collision=pygame.mixer.Sound('collision.mp3') #sound when player collides with walls
                        collision.play()
                        if lives == 0:
                            lose() #if lives become 0,redirect to try again screen
                        counter = 30
                elif event.type == pygame.KEYDOWN:
                    global score_value
                    if event.key == pygame.K_LEFT:
                        player.move(-WIDTH - MARGIN, 0)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                    elif event.key == pygame.K_RIGHT:
                        player.move(WIDTH + MARGIN, 0)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                    elif event.key == pygame.K_UP:
                        player.move(0, -HEIGHT - MARGIN)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                    elif event.key == pygame.K_DOWN:
                        player.move(0, HEIGHT + MARGIN)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0

                elif player.get_position()==((MARGIN+HEIGHT)*(COLS-2),(MARGIN+WIDTH)*(ROWS-2)):
                    global game_state
                    game_state = HARD #redirecting to hard level if player clears this level within 3 lives
                    hard_level()
                elif player.get_position()!=((MARGIN+HEIGHT)*(COLS-2),(MARGIN+WIDTH)*(ROWS-2)) and lives==0:
                    lose() #redirecting to try again screen if player runs out of lives
                    pygame.display.update()

            screen.fill(LBLUE)
            draw_maze(screen)
            all_sprites.draw(screen)
            collectible1.update(player)
            collectible2.update(player)
            collectible3.update(player)
            collectible4.update(player)
            show_score(textX,textY)
            show_lives(textx,texty)
            show_timer(textA,textB)
            show_level(textC,textD)
            pygame.display.flip()
            clock.tick(120)
    main()

#hard level screen
def hard_level():
    #maze parameters
    WIDTH = 20
    HEIGHT = 20
    MARGIN = 2
    ROWS = 23
    COLS = 25
    #Set of sprite images
    sprite_images=[
    pygame.transform.scale(pygame.image.load("sprite1.jpg"),(20,20)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite2.jpg"),(20,20)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite3.jpg"),(20,20)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite4.jpg"),(20,20)).convert_alpha(),
    pygame.transform.scale(pygame.image.load("sprite5.jpg"),(20,20)).convert_alpha()
]

    # Initialize maze grid
    maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    #Create a 2D list to store the images for each block
    images=[[random.choice(sprite_images) for _ in range(COLS)] for _ in range(ROWS)]
    # Recursive backtracking algorithm for maze generation
    def recursive_backtracking(x, y):
        maze[x][y] = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = x + 2*dx, y + 2*dy
            if 0 <= new_x < ROWS and 0 <= new_y < COLS and maze[new_x][new_y]:
                maze[x + dx][y + dy] = 0
                recursive_backtracking(new_x, new_y)
    #write maze
    List = []
    def write_maze_solution(maze, filename):
        with open(filename, 'w') as file:
            for row in maze:
                line = ' '.join(map(str, row)) + '\n'
                file.write(line)
                List.append(line.strip())
                
    
    # Call recursive_backtracking function to generate maze
    recursive_backtracking(1, 1)
    # Write maze solution to a file
    write_maze_solution (maze, 'maze_solution.txt')

    
    for i in range(len(List)):
        List[i] = List[i].split(' ')

    path = find_path(List)

    with open("path.txt","w") as file:
        file.write(str(path))

    # Draw the maze
    def draw_maze(screen):
        for row in range(ROWS):
            for col in range(COLS):
                if maze[row][col]==0:
                    color=LBLUE
                    pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * col + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

                if maze[row][col]==1:#If it's a sprite blit the image
                    screen.blit(images[row][col],((MARGIN+WIDTH)*col+MARGIN,(MARGIN+HEIGHT)*row+MARGIN))
    # Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self, image):
            super().__init__()
            self.image = image
            self.rect=self.image.get_rect()
            self.rect.x = MARGIN + WIDTH
            self.rect.y = MARGIN + HEIGHT

        def move(self, dx, dy):
            new_x = self.rect.x + dx
            new_y = self.rect.y + dy
            if 0 <= new_x <= (WIDTH + MARGIN) * COLS - WIDTH and 0 <= new_y <= (HEIGHT + MARGIN) * ROWS - HEIGHT:
                if not maze[new_y // (HEIGHT + MARGIN)][new_x // (WIDTH + MARGIN)]:
                    self.rect.x = new_x
                    self.rect.y = new_y
                else:
                    global lives
                    lives-=1
                    collision=pygame.mixer.Sound('collision.mp3')
                    collision.play()
                    if lives<=0:
                        lives=0
                        
        def get_position(self):
            return self.rect.x,self.rect.y
    #collectible class
    class Collectible(pygame.sprite.Sprite):
        def __init__(self, image):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.spawn_collectible()
        def spawn_collectible(self):
            while True:
                x=random.randint(0,COLS-1)
                y=random.randint(0,ROWS-1)
                if not maze[y][x]:
                    self.rect.x = x * (WIDTH + MARGIN) + MARGIN
                    self.rect.y = y * (HEIGHT + MARGIN)+ MARGIN
                    break

        def update(self, player):
            if pygame.sprite.collide_rect(self, player):
                global score_value
                score_value += 10
                self.spawn_collectible()


    #Score
    font=pygame.font.SysFont('Marker Felt',32)
    textX=10
    textY=510
    def show_score(x,y):
        score=font.render("Score : "+str(score_value),True,(0,0,0))
        screen.blit(score,(x,y))
    #Lives
    textx=180
    texty=510
    def show_lives(x,y):
            live=font.render("Lives : "+str(lives),True,(0,0,0))
            screen.blit(live,(x,y))
    #Timer
    pygame.time.set_timer(pygame.USEREVENT,1000)
    textA=320
    textB=510
    global counter
    counter=35
    text='35'
    def show_timer(x,y):
        timer=font.render("Time Left : "+str(counter),True,(0,0,0))
        screen.blit(timer,(x,y))
    #show level
    textC=20
    textD=530
    def show_level(x,y):
        slevel=font1.render("LEVEL 3:Reach the bootom right corner without colliding in 15s",True,(0,0,0))
        screen.blit(slevel,(x,y))
    # Main function
    def main():
        # Generate maze
        recursive_backtracking(1,1)
        player_image=pygame.transform.scale(pygame.image.load("puppy.jpg"),(20,20)).convert_alpha()
        # Create player object
        player = Player(player_image)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        # Create collectible object
        collectible_image = pygame.transform.scale(pygame.image.load("collectible.png"), (20,20)).convert_alpha()
        collectible1 = Collectible(collectible_image)
        collectible2 = Collectible(collectible_image)
        collectible3 = Collectible(collectible_image)
        collectible4 = Collectible(collectible_image)
        collectible5 = Collectible(collectible_image)
        all_sprites.add(collectible1,collectible2,collectible3,collectible4,collectible5)
        font = pygame.font.SysFont(None, 36)
        done = False
        clock = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.USEREVENT:
                    global counter
                    counter-=1
                    if counter>0:
                        text=str(counter)
                    else:
                        global lives
                        lives -= 1
                        collision=pygame.mixer.Sound('collision.mp3')#sound if particle collides with walls
                        collision.play()
                        if lives == 0:
                            lose() #redirecting to try again screen if player loses all lives
                        counter = 35
                elif event.type == pygame.KEYDOWN:
                    global score_value
                    if event.key == pygame.K_LEFT:
                        player.move(-WIDTH - MARGIN, 0)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                    elif event.key == pygame.K_RIGHT:
                        player.move(WIDTH + MARGIN, 0)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                    elif event.key == pygame.K_UP:
                        player.move(0, -HEIGHT - MARGIN)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                    elif event.key == pygame.K_DOWN:
                        player.move(0, HEIGHT + MARGIN)
                        if lives >0:
                            score_value+=1
                        else:
                            score_value+=0
                elif player.get_position()==((MARGIN+HEIGHT)*(COLS-2),(MARGIN+WIDTH)*(ROWS-2)):
                    global game_state
                    game_state = WIN #win screen if player successfully completes this  level under 3 tries
                    win_screen() 
                elif player.get_position()!=((MARGIN+HEIGHT)*(COLS-2),(MARGIN+WIDTH)*(ROWS-2)) and lives==0:
                    lose() # redirecting to try again screen if player loses lives
                    pygame.display.update()

            screen.fill(LBLUE)
            draw_maze(screen)
            all_sprites.draw(screen)
            collectible1.update(player)
            collectible2.update(player)
            collectible3.update(player)
            collectible4.update(player)
            collectible5.update(player)
            show_score(textX,textY)
            show_lives(textx,texty)
            show_timer(textA,textB)
            show_level(textC,textD)
            pygame.display.flip()
            clock.tick(120)
    main()

#win screen
def win_screen():
    def main():
        done=False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    levels()
                    pygame.display.update()   #updating the display screen
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.quit()            
            back=pygame.transform.scale(pygame.image.load("win.jpg"),(552,552))
            screen.blit(back,(0,0))
            font=pygame.font.Font(None,36)
            text10=font.render("Press P to play again",True,LPINK) 
            text11=font.render("Press Q to end game",True,RED) 
            text9=font.render("~Snigdha Reddy:)",True,(0,0,0))
            text10_rect = text10.get_rect(center=(250, 300))  
            text11_rect = text11.get_rect(center=(250, 370)) 
            text9_rect=text9.get_rect(center=(440,450))
            screen.blit(text10, text10_rect) 
            screen.blit(text11,text11_rect) 
            screen.blit(text9,text9_rect)       
            pygame.display.update()
            clock.tick(120)
        pygame.display.flip()
    main()
    
#try again or gameover screen   
def lose():
    def main():
        done=False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.KEYDOWN and event.key==pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    levels()
                    pygame.display.update() 
            back=pygame.transform.scale(pygame.image.load("lose.png"),(552,552))
            screen.blit(back,(0,0))
            font=pygame.font.Font(None,36)
            text12=font.render("Press Q to exit the game",True,RED)
            screen.blit(text12,(150,280))
            text13=font.render("Press P to play again",True,LBROWN) 
            screen.blit(text13,(150,320))
            pygame.display.update()
            clock.tick(60)
        pygame.display.flip()
    main()
    
#displaying all the levels screen   
def levels():
    def main():
        done=False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit() 
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    easy_level()
                    pygame.display.update()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    medium_level()
                    pygame.display.update()                    
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    hard_level()
                    pygame.display.update()                                  
            screen.blit(background2, (0, 0))
            text6 = font.render("Choose the level:", True, (0, 0, 255))
            text6_rect =text6.get_rect(center=(370,150))
            text7 = font1.render("Help the puppy reach the bottom",True,(0,0,0))
            text7_rect =text7.get_rect(center=(400,200))
            text8 = font1.render("right of maze to get help:(",True,(0,0,0))
            text8_rect =text8.get_rect(center=(380,230))
            text1 = font.render("Press 1 for easy level", True, WHITE)
            text1_rect = text1.get_rect(center=(340, 300))
            text2 = font.render("Press 2 for moderate level", True, WHITE)
            text2_rect = text1.get_rect(center=(350, 350))
            text3 = font.render("Press 3 for hard level", True, WHITE)
            text3_rect = text1.get_rect(center=(350, 400))
            tb1=pygame.Surface((340,160))
            tb1.fill(LBROWN)
            screen.blit(tb1,(200,270))
            screen.blit(text6, text6_rect)
            screen.blit(text7,text7_rect)
            screen.blit(text8,text8_rect)
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            screen.blit(text3, text3_rect)
            global score_value
            score_value=0
            global lives
            lives=3
            pygame.display.update()
    main()
    
#main game loop   
run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        if game_state == MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                game_state = LEVELS
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                run = False
        elif game_state == LEVELS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_state = EASY
                elif event.key == pygame.K_2:
                    game_state = MEDIUM
                elif event.key == pygame.K_3:
                    game_state = HARD

    screen.fill((0, 0, 0))  # Clear the screen 
    #we set the initial game screen to menu,so we write it under main game loop      
    if game_state == MENU:
        screen.blit(background, (0, 0))
        title=pygame.transform.scale(pygame.image.load("thelostpuppy.png"),(300,300))
        title_rect=title.get_rect(center=(330,100))
        screen.blit(title,title_rect)
        text4 = font.render("Press A to start playing", True, GRAY)
        text4_rect = text4.get_rect(center=(320, 350))
        text5 = font.render("Press Q to exit", True, GRAY)
        text5_rect = text5.get_rect(center=(300, 400))
        tb2=pygame.Surface((290,100))
        tb2.fill(LBLUE)
        screen.blit(tb2,(170,330))
        screen.blit(text4, text4_rect)
        screen.blit(text5, text5_rect)
        pygame.display.update()
    #displaying levels screen
    elif game_state == LEVELS:
        screen.blit(background2, (0, 0))
        text6 = font.render("Choose the level:", True, (0, 0, 255))
        text6_rect =text6.get_rect(center=(370,150))
        text7 = font1.render("Help the puppy reach the bottom",True,(0,0,0))
        text7_rect =text7.get_rect(center=(400,200))
        text8 = font1.render("right of maze to get help:(",True,(0,0,0))
        text8_rect =text8.get_rect(center=(380,230))
        text1 = font.render("Press 1 for easy level", True, WHITE)
        text1_rect = text1.get_rect(center=(340, 300))
        text2 = font.render("Press 2 for moderate level", True, WHITE)
        text2_rect = text1.get_rect(center=(350, 350))
        text3 = font.render("Press 3 for hard level", True, WHITE)
        text3_rect = text1.get_rect(center=(350, 400))
        tb1=pygame.Surface((340,160))
        tb1.fill(LBROWN)
        screen.blit(tb1,(200,270))
        screen.blit(text6, text6_rect)
        screen.blit(text7,text7_rect)
        screen.blit(text8,text8_rect)
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)
        pygame.display.update() 
    elif game_state == EASY:
        easy_level() #calling the function
        break
    elif game_state == MEDIUM:
        medium_level() #calling the function
        break
    elif game_state == HARD:
        hard_level() #calling the function
        break
    clock.tick(120)

