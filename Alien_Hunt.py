import sys, os, pygame, random
from pygame.locals import *

x_coord=320
y_coord=580
x_speed=0
y_speed=0
enemy_controller=0
enemy_bullcontroller=0
bullet_controller=0
itteration=0
live=30
air=[]
enrow=[]
starrow = []

def init_window():
    pygame.init()
    window = pygame.display.set_mode((640, 640))
    pygame.display.set_caption('Alien hunt')

# Функция отображения картинок
def load_image(name, colorkey=None):
    # Добавляем к имени картинки имя папки
    fullname = os.path.join('Data', name)
    # Загружаем картинку
    image = pygame.image.load(fullname)
    image = image.convert()
    # Если второй параметр =-1 делаем прозрачным
    # цвет из точки 0,0
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def input(events):
    global x_coord, y_coord, x_speed, y_speed, bullet_controller, enemy_bullcontroller
    # Перехватываем нажатия клавиш на клавиатуре
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: x_speed=-1
            if event.key == pygame.K_RIGHT: x_speed=1
            if event.key == pygame.K_UP: y_speed=-1
            if event.key == pygame.K_DOWN: y_speed=1
            if event.key == pygame.K_SPACE:
                if (bullet_controller<1):
                    bullet_controller=1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: x_speed=0
            if event.key == pygame.K_RIGHT: x_speed=0
            if event.key == pygame.K_UP: y_speed=0
            if event.key == pygame.K_DOWN: y_speed=0
    # Меняем положение не выходя за рамки окна
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed
    if(x_coord<4): x_coord=4
    if(x_coord>580): x_coord=580
    if(y_coord<4): y_coord=4
    if(y_coord>580): y_coord=580
    

# Класс описывающий объекты
class obj(pygame.sprite.Sprite):
    def __init__(self, img, cX, cY):
        # Создаем спрайт из картинки
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(img, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Перемещаем картинку в её начальные координаты
        self.rect.x = cX
        self.rect.y = cY


# Создаём классы - наследники

#----------------------------------------------
# Космический корабль игрока
#----------------------------------------------

class space_ship(obj):
    def __init__(self, cX, cY):
        obj.__init__(self, "space_ship.bmp", cX, cY)
        
#----------------------------------------------
# Звезды
#----------------------------------------------

class star(obj):
    def __init__(self, cX, cY):
        obj.__init__(self, "star.bmp", cX, cY)
    def move(self): 
        self.rect.y=self.rect.y+1
        if(self.rect.y>580):
            self.rect.y=5
            self.rect.x=random.randint(10,630)

class star2(star):
    def __init__(self, cX, cY):
        obj.__init__(self, "star2.bmp", cX, cY)


#----------------------------------------------
# Пуля
#----------------------------------------------
        
class bullet(obj):
    
    def __init__(self, cX, cY):
        obj.__init__(self, "bullet.bmp", cX, cY)

    def create(self):
        global bullet_controller
        self.rect.x=x_coord+14
        self.rect.y=y_coord-5
        bullet_controller=2
    
    def move_bullet(self):
        global bullet_controller
        self.rect.y=self.rect.y-2
        if(self.rect.y<4):
            self.rect.x=650
            self.rect.y=650
            bullet_controller=0
        

#----------------------------------------------
# Космические корабли компьютерного противника
#----------------------------------------------

class enemy(obj):
    
    def __init__(self, cX, cY):
        obj.__init__(self, "enemy_ship.bmp", cX, cY)
        
    def recreate(self):
            self.rect.y=random.randint(-20,-5)
            self.rect.x=random.randint(2,632)
            
    def checkbullet(self, bullet):
        global bullet_controller
        col = pygame.sprite.collide_rect(self, bullet)
        if col == True:
            bullet.rect.x=0
            bullet.rect.y=0
            bullet_controller=0
            self.recreate()
            
    def move(self,controller):
        if controller==1:
            self.rect.y+=1
        if self.rect.y>580:
            self.recreate()
            
    def checkplayer(self,player):
        global live
        col = pygame.sprite.collide_rect(self, player)
        if col == True:
            live-=10
            self.recreate()
            if live<=0:
                player.rect.x=0
                player.rect.y=0
                pygame.quit()
                sys.exit(0)

    def shoot(self,bullet):
        global enemy_bullcontroller
        bullet.rect.x=self.rect.x+14
        bullet.rect.y=self.rect.y+5
        enemy_bullcontroller=1

#----------------------------------------------
# Пули кораблей компьютерного противника
#----------------------------------------------

class enemy_bullet(obj):
    
    def __init__(self, cX, cY):
        obj.__init__(self, "bullet.bmp", cX, cY)

    def move(self):
        global enemy_bullcontroller
        if enemy_bullcontroller==1:
            self.rect.y+=3
        if self.rect.y>580:
            enemy_bullcontroller=0
            self.rect.y=650
            self.rect.x=650
                
def action():
    global x_coord, y_coord, bullet_controller, enemy_controller, itteration, air, enrow, starrow

    # Создание и расстановка объектов
        
    screen = pygame.display.get_surface()
    spaceship = space_ship(0,0)
    Bullet = bullet(650,650)      
    air.append(spaceship)
    air.append(Bullet)
    for i in range(4):
        enrow.append(enemy(random.randint(7,637),random.randint(10,40)))
    for i in range(13):
        if(i<9):
            starr = star2(random.randint(10,630),random.randint(320,630))
        else:
            starr = star(random.randint(10,630),random.randint(10,630))
        starrow.append(starr)
    spaceships = pygame.sprite.RenderPlain(air)
    stars = pygame.sprite.RenderPlain(starrow)
    enemies = pygame.sprite.RenderPlain(enrow)
    timer=pygame.time.Clock()

    # Main game loop
    
    while 1:
        if itteration >= 300:
            itteration = 0
        if itteration%2 == 0:
            enemy_controller=1
        else:
            enemy_controller=0
        timer.tick(500)
        for i in range(4):
            enrow[i].move(enemy_controller)
            enrow[i].checkbullet(Bullet)
            enrow[i].checkplayer(spaceship)
        input(pygame.event.get())
        spaceship.rect.x=x_coord
        spaceship.rect.y=y_coord
        for i in range(13):
             starrow[i].move()
        if (bullet_controller==1):
             Bullet.create()
        if (bullet_controller==2):
            Bullet.move_bullet();

    # Обновление экрана.
                
        screen.fill(1)
        font = pygame.font.Font(None, 25)
        white    = ( 255, 255, 255)
        life=int(live/10)
        text = font.render("Live: "+str(life),True,white)
        screen.blit(text, [10,10])
        stars.update()
        spaceships.update()
        enemies.update()
        stars.draw(screen)
        spaceships.draw(screen)
        enemies.draw(screen)
        pygame.display.flip()
        itteration+=1

def main():
    init_window()
    action()

main()
