from pygame import *
from random import randint
from time import time as timer    
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)

lost = 0
max_lost = 10
score = 0
shoot = 0

real_time = False
num_fire = 0
rel_time = 3

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Schwein")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
img_aster = "asteroid.png"
img_bullet = "bullet.png"
img_enemy = "ufo.png"
img_ship = "rocket.png"
img_galaxy = "galaxy.png"

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_width:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player(img_ship, 10, win_height-100, 80, 100, 10) 

for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width-80),-40, 80, 50, randint(1,5))
    monsters.add(monster)
    print(i)

for i in range(1,2):
    asteroid = Enemy(img_aster, randint(80, win_width-80),-40, 80, 50, randint(1,5))
    asteroids.add(asteroid)
    print(i)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
run = True
finish = False

clock = time.Clock()
FPS = 60


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if real_time == False:
                    if num_fire <= 4:
                        num_fire += 1
                        ship.fire()
                        shoot += 1
                        fire_sound.play()

                    else:
                        num_fire >= 4
                        last_time = timer()
                        real_time = True
                
    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        
        if real_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('ОНИ ЗАХОДЯТ К НАМ С ТЫЛА!!!! ПЕРЕЗАРЯЖАЮСЬ!!!!', 1, (150, 0, 0))
                window.blit(reload, (20, 460))

            else:
                num_fire = 0
                real_time = False

        for i in sprite_list:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width-80),-40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= 10:
            finish = True
            window.blit(win, (200, 200))




        text_shoot = font2.render("Выстрелов: " + str(shoot), 1, (255, 255, 255))
        window.blit(text_shoot, (10, 80))

        ship.reset()
        monsters.update()
        bullets.update()

        ship.update()
        monsters.draw(window)
        bullets.draw(window)
        display.update()
    
    clock.tick(FPS)