# Fly or Die
# 07/11/2017
# By: Aadar Gupta

# importing all required modules
import pygame
import random
import math
from os import path
import time

# all variables in capitals are constants

# defines directories/folders such as image and sound
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# declares width, height, frames per second and powerup time variables
WIDTH = 1000
HEIGHT = 600
FPS = 120
POWERUP_TIME = 5000

# defines colors: white, black, red, green
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# initialize pygame/sounds and creates and names window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fly or Die")
clock = pygame.time.Clock()


# defining a draw text function used to draw text on screen
def draw_text(surf, text, size, x, y):
    # defining font to use
    font = pygame.font.Font("mainFont.ttf", size)
    # defining the surface
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    # blitting the text to the screen
    surf.blit(text_surface, text_rect)

# defining mob function
def newmob():
    # redefining mob
    m = Mob()
    # adding mob to all sprites group
    all_sprites.add(m)
    # adding to mob to all mobs group
    mobs.add(m)

# defining the shield bar 
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    # defining the length and height of bar
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    # defining how much to fill the bar 
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    # drawing the bar to the screen
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# enemy life bar 
def draw_enemy_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    # defining the length and height of bar
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    # defining how much to fill the bar 
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    # drawing the bar to the screen
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# draws the three lifes at the top
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 60 * i
        img_rect.y = y
        surf.blit(img, img_rect)

# defines the player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # sets image and required sizing/location elements
        self.image = player_img
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        # speed
        self.speedx = 0
        # its shield/health 
        self.shield = 100
        # shoot delay
        self.shoot_delay = random.randrange(150, 200)
        self.last_shot = pygame.time.get_ticks()
        # amount of lives 
        self.lives = 3
        # not hidden
        self.hidden = False
        # showing that no powerup has been applied 
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
            
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            
        # controls for the game
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        # move left
        if keystate[pygame.K_LEFT]:
            self.speedx = -20
        if keystate[pygame.K_a]:
            self.speedx = -20
        # move right
        if keystate[pygame.K_d]:
            self.speedx = 20
        if keystate[pygame.K_RIGHT]:
            self.speedx = 20
        # shooting
        if keystate[pygame.K_SPACE]:
            self.shoot()
        # restrictions to not pass the width of screen
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    # powerup
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
        
    # shooting function for player
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # if its power is 1, then only shoots one at a time
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                
            # if its power is 2, then only shoots two at a time 
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.top)
                bullet2 = Bullet(self.rect.right, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)

    
    # hide function
    def hide(self):
        # hide the player temporarily
        self.rect.centerx = WIDTH / 2
        # hides
        self.hidden = True
        # timer for hiding
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

# defining the boss's sprite
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # defining its image 
        self.image_orig = boss_img
        self.player = player
        # adds a shoot delay
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = random.randrange(500, 800)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # shield 
        self.shield = 100
        # not hidden
        self.hidden = False
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        # position of boss
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = -200
        self.rect.bottom = 100
        self.speedy = 5
        self.speedx = 50
        self.last_update = pygame.time.get_ticks()

    def hide(self):
        # hide the boss temporarily
        self.rect.centerx = WIDTH / 2
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


    def update(self):
        # updating the boss's speed, and position
        if self.rect.center[0] > self.player.rect.center[0]:
            self.speedx = -10
            self.shoot()
        else:
            self.speedx = 10
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.y < 0:
            self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.speedy = random.randrange(1, 5)
        

    def shoot(self):
        # defining the boss's shoot function 
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet1 = Bullet1(self.rect.centerx, self.rect.bottom)
                all_sprites.add(bullet1)
                bossbullets.add(bullet1)

# defines the mob       
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # defines the image for the mob
        self.image_orig = random.choice(mob_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(20, 30)
        self.speedx = random.randrange(1, 5)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        # defines the rotation and movement for the mob
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 1
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        # updating the position and rotation of the image
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 20)
    
            
# creates the bullet for player
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # sets image and position
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -100

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# defines bullets for boss
class Bullet1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # sets image and position
        self.image = bullet1_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 50

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# defines a powerup
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        # defines random type of powerup
        self.type = random.choice(['shield', 'gun'])
        # defines images for powerup
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        # sets fall speed of powerup
        self.speedy = random.randint(2, 10)

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()

# the animation for explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        # sets its own size and position and image
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        # frame rate
        self.frame_rate = 75

    def update(self):
        # plays the images in the explosion
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                
# this is the starting screen
def show_screen1():
    screen.blit(background, background_rect)
    # shows name and rules 
    draw_text(screen, "Fly or Die", 150, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys or 'A D' to move, Space to fire", 40, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 30, WIDTH / 2, HEIGHT * 3 / 4)
    # updates the screen
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# defines win screen 
def show_win():
    screen.blit(background, background_rect)
    draw_text(screen, "You Win!", 150, WIDTH / 2, HEIGHT / 2 - 75)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
            
# Load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.jpg")).convert_alpha()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir,"mainplane.png")).convert_alpha()
player_mini_img = pygame.transform.scale(player_img, (50, 30))
player_mini_img.set_colorkey(BLACK)

boss_img = pygame.image.load(path.join(img_dir, "boss.png")).convert_alpha()

bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (20, 30))
bullet1_img = pygame.image.load(path.join(img_dir, "bulletforboss.png")).convert_alpha()
mob_images = []
mob_list = ['2plane.png', '3plane.png', '4plane.png']
for img in mob_list:
    mob_images.append(pygame.image.load(path.join(img_dir, img)).convert_alpha())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert_alpha()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bullet_box.png')).convert_alpha()
# Load all game sounds
bg = pygame.mixer.Sound(path.join(snd_dir, 'bg.ogg'))
bg.set_volume(0.4)
bg.play()
win = pygame.mixer.Sound(path.join(snd_dir, 'win.ogg'))


# Game loop
game_over = True
running = True
all_sprites = pygame.sprite.Group()
bossIsAlive = False
while running:
    if game_over:
        # displays the beginning screen and runs game 
        show_screen1()
        game_over = False
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bossbullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        # spawns new mobs
        for i in range(5):
            newmob()
            score = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # checks for boss is alive
    if bossIsAlive:
        bg.set_volume(1)
        # if boss is alive, checks for the bullets that hit the boss
        hits = pygame.sprite.spritecollide(boss, bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            # subtracts 2 from boss health
            boss.shield -= 2
            # plays explosion
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            # displays win and explosion if boss is dead 
            if boss.shield <= 0:
                expl = Explosion(hit.rect.center, 'lg')
                all_sprites.add(expl)
                boss.hide()
                all_sprites.remove(boss)
                bg.stop()
                win.play()
                show_win()
                time.sleep(5)
                running = False
         

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        # subtract 25 from player's health and play animation
        player.shield -= 25
        if score > 0:
            score -= 1
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        # spawn new mob
        newmob()
        # shows explosion and subtracts one life is player is dead
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.lives -= 1
            player.shield = 100
            
    # checks if boss bullets hit player
    hits = pygame.sprite.spritecollide(player, bossbullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        # subtract 50 points from player health
        player.shield -= 50
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        # subtracts one life is player is dead 
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.lives -= 1
            player.shield = 100
            
    # checks if player hit a power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            # adds health
            player.shield += 25
        if player.shield >= 100:
            player.shield = 100
        if hit.type == 'gun':
            # gives double bullets
            player.powerup()
        screen.fill(BLACK)
        screen.blit(background, background_rect)


       # if the player died and the explosion has finished playing. Restarts game
    if player.lives == 0 and not death_explosion.alive():
        boss = Boss()
        all_sprites.remove(boss)
        boss.hide()
        running = False
        for m in mobs:
            all_sprites.remove(m)
        mobs.empty()
        all_sprites.remove(boss)
        
        
    # spawns boss 
    if score == 100:
             for m in mobs:
                 all_sprites.remove(m)
             mobs.empty()
             bossIsAlive = True
             boss = Boss()
             all_sprites.add(boss)
             score += 1

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "Score: "+str(score), 50, WIDTH / 2, 10)
    if bossIsAlive:
        draw_enemy_bar(screen, 5, 30, boss.shield)
        draw_text(screen, "Boss", 20, 125, 27)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_text(screen, "Player", 20, 130, 5)
    draw_lives(screen, WIDTH - 200, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
