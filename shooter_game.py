from pygame import *
from random import randint

window = display.set_mode((800,600))
display.set_caption('Шутер')
background = transform.scale(image.load("galaxy.jpg"),(800,600))
global miss
miss=0
global hits
hits=0
font.init()
font1=font.Font(None,36)
font2=font.Font(None,36)
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, player_speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width,height))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Enemy(GameSprite):
    def update(self):
        global miss
        self.rect.y+=self.speed

class Bullet(GameSprite):
    def fire(self):
        self.rect.y-=self.speed
clock = time.Clock()
FPS=60
player=GameSprite('rocket.png',350,500,10,100,100)
ufo_enemy=Enemy('ufo.png',randint(0,700),randint(0,5),5,128,64)
bullet=Bullet('bullet.png',player.rect.x,player.rect.y,20,10,10)
bullet.rect.x=-10
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
monsters=sprite.Group()
monsters.add(ufo_enemy)
bullets=sprite.Group()
bullets.add(bullet)
def new_enemy():
    ufo_enemy=Enemy('ufo.png',randint(0,700),randint(0,5),5,128,64)
    monsters.add(ufo_enemy)

game=True
while game:
    window.blit(background,(0,0))
    text_lose=font1.render("Пропущенно:"+ str(miss), 1,(255,255,255))
    text_hits=font2.render("Счёт:"+ str(hits),1 ,(255,255,255))
    window.blit(text_hits,(1,25))
    window.blit(text_lose,(1,1))
    bullets.update()
    monsters.update()
    bullets.draw(window)
    monsters.draw(window)
    keys_pressed = key.get_pressed()
    clock.tick(FPS)
    player.reset()
    ufo_enemy.reset()
    bullet.reset()
    for e in event.get():
        if e.type == QUIT:
            game = False
    if sprite.collide_rect(bullet,ufo_enemy):
        bullet.remove(bullets)
        ufo_enemy.remove(monsters)
        new_enemy()      
    if ufo_enemy.rect.y>500:
        ufo_enemy.rect.y=0
        miss+=1
        new_enemy()
    if player.rect.x>=700:
        player.rect.x-=10
    if player.rect.x<=0:
        player.rect.x+=10
    if keys_pressed[K_a]:
        player.rect.x-=10
    if keys_pressed[K_d]:
        player.rect.x+=10
    if keys_pressed[K_SPACE]:
        bullet.fire()
        bullet=Bullet('bullet.png',player.rect.x,player.rect.y,20,10,10)
        bullet.rect.x=player.rect.x+45
    display.update()