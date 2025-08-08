import pygame
import sys
import random

# to display scores
is_running = True
scores = 0
pygame.init()
pygame.font.init()
pygame.font.get_init()

#loading sounds
stage_music = pygame.mixer.Sound('sounds/bit_surf_bg.mp3')
eat_sound = pygame.mixer.Sound('sounds/eat_sound.mp3')

timer = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))

#Title and Icon and Images
pygame.display.set_caption("Fruit Land")
game_icon = pygame.image.load('images/logo.png')
pygame.display.set_icon(game_icon)

#fruit class
class fruit:
    def __init__(self, image):
        self.image = image
        # when you draw, it spits out the rectange object
        self.x = random.randint(10, 785)
        self.y = random.randint(10, 30)
        self.velocity = random.randint(2,6)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
    
#player class
class player:
    def __init__(self):
        self.image = pygame.image.load('images/boar_player.png')
        self.x = 368
        self.y = 480
        self.speed = 8
        self.x_change = 0
        self.y_change = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


player = player()

# background color
background = (144,237,236)

#fruits images
fruits_images = {
    "apple" : pygame.image.load('images/apple.png'),
    "artichoke" :pygame.image.load('images/artichoke.png'),
    "avocado" : pygame.image.load('images/avocado.png'),
    "fennel" : pygame.image.load('images/fennel.png'),
    "grapes" : pygame.image.load('images/fennel.png'),
    "lemon" : pygame.image.load('images/lemon.png'),
    "peach" : pygame.image.load('images/peach.png'),
    "pineapple" : pygame.image.load('images/pineapple.png'),
    "watermelon" : pygame.image.load('images/watermelon.png')
}
fruits = []

def check_bound(x,y):
    global player
    if x >= 740:
        player.x = 740
    if x <= 0:
        player.x = 0
    if y <= 0:
        player.y = 0
    if y >= 540:
        player.y = 540

def draw_player(x,y):
    global player
    screen.blit(player.image, (x,y))
    
def add_fruits(count):
    global fruits
    global fruits_images
    for i in range(count):
        fruit_pic = random.choice(list(fruits_images.values()))
        food = fruit(fruit_pic)
        fruits.append(food)

def check_collisions(player,fruit):
    global scores
    global spawn_fruit
    if player.mask.overlap(fruit.mask,(fruit.x - player.x, fruit.y - player.y)):
        scores += 1
        eat_sound.play()
        fruit.mask.clear()
        spawnned_fruits.remove(fruit)
        print(f"score : {scores}")
    

def update_score():
    font1 = pygame.font.SysFont('freesanbold.ttf', 50)
    score_text = font1.render(str(scores), True, (0,0,0))
    score_Rect = score_text.get_rect()
    screen.blit(score_text, score_Rect)

#timer evnet
spawn_fruit = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_fruit, 500)

add_fruits(30) 
# to move and remove the spawneed fruits which were controlled by the timer.
if is_running:
    stage_music.play(-1)
spawnned_fruits = []
while is_running:
    screen.fill(background)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            pygame.quit()
            sys.exit()

        
        if event.type == spawn_fruit and len(fruits) > 0:
            print("spawn fruit is being called\n")
            curr_fruit = fruits.pop()
            spawnned_fruits.append(curr_fruit)
        
        if event.type == pygame.KEYDOWN:#if any keys are being pressed.
            if event.key == pygame.K_UP:# if they key that is being pressed is the  up key. 
                player.y_change = -player.speed
            if event.key == pygame.K_DOWN:  
                player.y_change = player.speed
            if event.key == pygame.K_RIGHT:
                player.x_change = player.speed
            if event.key == pygame.K_LEFT:
                player.x_change = -player.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.y_change = 0
            if event.key == pygame.K_DOWN:
                player.y_change = 0
        
            if event.key == pygame.K_RIGHT:
                player.x_change = 0
            if event.key == pygame.K_LEFT:
                player.x_change = 0
    if len(spawnned_fruits) > 0:
        for fruit in spawnned_fruits:
            screen.blit(fruit.image,(fruit.x, fruit.y))
            check_collisions(player,fruit)
            fruit.y += 5
    player.x += player.x_change
    player.y += player.y_change
    check_bound(player.x, player.y)
    draw_player(player.x, player.y)
    pygame.display.update()
    timer.tick(60)
pygame.mixer.music.unload()

