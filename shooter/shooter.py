from pygame import*
from time import time as timer
from random import*
'''Шрифт'''
font.init()
font = font.SysFont('Times New Roman', 50)
win = font.render('YOU WIN!', True, (255, 255, 0))
lose = font.render('YOU LOSE!', True, (255, 255, 255))
'''Переменные для картинок'''
img_back = 'fon2.png'
img_hero = 'cyborg.png'
img_enemy = 'dude.png'
img_bullet = 'bullet.png'
img_goal = 'princess_2.png'
'''Музыка'''
mixer.init()#подключение музыки к игре
mixer.music.load('AP.ogg')#загружаем файл/музыку
mixer.music.play()
fire = mixer.Sound('shotgun-fire-1.ogg')
'''Классы'''
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, x, y, width, height, speed):
        #вызываем конструктор класса (Sprite)
        sprite.Sprite.__init__(self)
        #каждый спрайт должен хранить image - изображение
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        #каждый спрайт должен хранить в себе rect -  прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    #метод отрисовки героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed 
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        #метод выстрела'используем место игрока, чтобы создать там пулю'
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.right, self.rect.centery, 24, 25, 8)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    side = "left"
    def update(self):
        if self.rect.x <= 470:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed    
class Enemy2(GameSprite):
    side = "up"
    def update(self):
        if self.rect.y <= 130:
            self.side = "up"
        if self.rect.y >= win_height - 100:
            self.side = "down"
        if self.side == "down":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

class Wall(sprite.Sprite):
    def __init__(self, red, green, blue, wall_x, wall_y, width,   height):
        super().__init__()
        self.red = red
        self.green = green
        self.blue = blue
        self.w = width
        self.h = height
        #каждый спрайт должен хранить свойство image - изображение
        self.image = Surface((self.w, self.h))
        self.image.fill((red, green, blue))
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()

'''Окно игры'''
#создаём окно
win_width = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load(img_back), (win_width, win_height))
'''Персонажи'''
hero = Player(img_hero, 5, win_height - 80, 45, 45, 5)
monster = Enemy(img_enemy, win_width - 80, 280, 65, 65 ,2)
monster2 = Enemy2(img_enemy, 70, 200, 65, 65, 2)
final = GameSprite(img_goal, win_width - 170, win_height - 460, 65, 65, 0)
'''Стены'''
w1 = Wall(127, 104, 100, 240, 109, 240, 10)
w2 = Wall(145, 19, 148, 230, 189, 110, 10)
w3 = Wall(90, 140, 10, 230, 109, 10, 80)
w4 = Wall(32, 32, 32, 330, 198, 10, 80)
w5 = Wall(255, 0, 10, 585, 111, 10, 120)
w6 = Wall(102, 0, 51, 220, 380, 240, 10)
w7 = Wall(255, 108, 72, 110, 275, 230, 10)
w8 = Wall(255, 55, 103, 110, 285, 10, 100)
w9 = Wall(255, 204, 204, 460, 230, 10, 160)
w10 = Wall(12, 0, 78, 470, 230, 125, 10)
'''Группы спрайтов'''
walls = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()
'''Добавление спрайтов в группу'''
monsters.add(monster)
monsters.add(monster2)

walls.add(w1)
walls.add(w2)
walls.add(w3)
walls.add(w4)
walls.add(w5)
walls.add(w6)
walls.add(w7)
walls.add(w8)
walls.add(w9)
walls.add(w10)
points = 0
'''Игровой Цикл'''
game = True
finish = False
clock = time.Clock()
FPS = 60
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
                fire.play()
                
    if finish != True:
        window.blit(back, (0, 0))
        walls.draw(window)
        monsters.update()
        monsters.draw(window)
        hero.reset()
        hero.update()
        final.reset()
        bullets.draw(window)
        bullets.update()
        sprite.groupcollide(bullets, walls, True, False)
        if sprite.groupcollide(bullets, monsters, True, True):
            points += 1
        x = font.render(str(points), True, (255, 255, 255))
        window.blit(x, (20, 20)) 
    
        if sprite.spritecollide(hero, walls, False):
            finish = True
            #boom.play() подключаем звуковой эфект
            window.blit(lose, (200, 200))

        if sprite.spritecollide(hero, monsters, False):
            finish = True
            #boom.play() подключаем звуковой эфект
            window.blit(lose, (200, 200)) 
        
        if sprite.collide_rect(hero, final):
            finish = True
            #boom.play() подключаем звуковой эфект
            window.blit(win, (200, 200))
        
    display.update()
    clock.tick(FPS)