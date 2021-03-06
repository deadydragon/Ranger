from os import path
import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 60
BOSSPEW = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

img_dir = path.dirname(__file__)

ANIMATION = ['bg_1.png', 'bg_2.png', 'bg_3.png', 'bg_4.png',
             'bg_5.png', 'bg_6.png', 'bg_7.png', 'bg_8.png']

koord = {1: (60, 60), 2: (300, 180), 3: (180, 420), 4: (300, 540)}
koord2 = {1: ('planet.png', (550, 550), (650, 420)), 2: ('planet2.png', (550, 550), (650, 420)),
          3: ('planet3.png', (1100, 600), (1000, 450)), 4: ('planet4.png', (530, 530), (600, 370))}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ranger")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemyBullets = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        player_img = pygame.image.load(path.join(img_dir, 'sheep.png')).convert()
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (30, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_2]:
            self.speedx = -8
        if keystate[pygame.K_3]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def die(self):
        self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        mob_img = pygame.image.load(path.join(img_dir, 'meteor.jpg')).convert()
        self.image = mob_img
        self.image = pygame.transform.scale(mob_img, (50, 45))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemyBullets.add(bullet)


class LeftEnemyShip(pygame.sprite.Sprite):
    def __init__(self, num):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        mob_img = pygame.image.load(path.join(img_dir, 'meteor.jpg')).convert()
        self.image = mob_img
        self.image = pygame.transform.scale(mob_img, (50, 45))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = -15 - num * 30
        self.rect.y = random.randrange(HEIGHT - self.rect.height - 300)
        self.speedx = 5

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH + 20:
            self.rect.x = -15
            self.rect.y = random.randrange(HEIGHT - self.rect.height - 200)

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemyBullets.add(bullet)


class RightEnemyShip(pygame.sprite.Sprite):
    def __init__(self, num):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        mob_img = pygame.image.load(path.join(img_dir, 'meteor.jpg')).convert()
        self.image = mob_img
        self.image = pygame.transform.scale(mob_img, (50, 45))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 500 + 15 + num * 30
        self.rect.y = random.randrange(HEIGHT - self.rect.height - 300)
        self.speedx = 5

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.left < -20:
            self.rect.x = 500 + 15
            self.rect.y = random.randrange(HEIGHT - self.rect.height - 200)

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemyBullets.add(bullet)


class MainGun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        player_img = pygame.image.load(path.join(img_dir, 'sheep.png')).convert()
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (30, 50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = 50
        self.rightPos = 400
        self.leftPos = 200
        self.speedx = 10

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemyBullets.add(bullet)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx = -10
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = 10

    def checkposition(self):
        if self.rect.right > self.rightPos:
            self.speedx = -10
        elif self.rect.left < self.leftPos:
            self.speedx = 10
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 8

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > 600:
            self.kill()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 120

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (0, 0, 0), (x * self.cell_size, y * self.cell_size,
                                                     self.cell_size, self.cell_size), 5)


class Urovni:
    def __init__(self, lvl):
        self.lvl = lvl
        self.x = 0
        self.y = 0

    def moving(self, lvl=1):
        self.lvl = lvl
        if self.lvl == 1:
            k = koord.get(self.lvl)
            self.x = k[0]
            self.y = k[1]
        elif self.lvl == 2:
            k = koord.get(self.lvl)
            self.x = k[0]
            self.y = k[1]
        elif self.lvl == 3:
            k = koord.get(self.lvl)
            self.x = k[0]
            self.y = k[1]
        elif self.lvl == 4:
            k = koord.get(self.lvl)
            self.x = k[0]
            self.y = k[1]

        pygame.draw.circle(screen, (250, 250, 250), (self.x, HEIGHT - self.y), 50)
        self.image = pygame.Surface((50, 40))
        player_img = pygame.image.load(path.join(img_dir, 'sheep.png')).convert()
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (30, 50))
        self.image.set_colorkey(WHITE)



def decoration():
    imagefon = pygame.image.load(path.join(img_dir, 'fon.jpg')).convert_alpha()
    imagefon = pygame.transform.scale(imagefon, (800, 900))
    imagefon_top = screen.get_height() - imagefon.get_height()
    imagefon_left = screen.get_width() // 2 - imagefon.get_width() // 2
    screen.blit(imagefon, (imagefon_left, imagefon_top))
    image = pygame.image.load(path.join(img_dir, 'planet.png')).convert_alpha()
    image = pygame.transform.scale(image, (180, 180))
    image_rect = image.get_rect(bottomright=(150, 620))
    screen.blit(image, image_rect)
    image2 = pygame.image.load(path.join(img_dir, 'planet2.png')).convert_alpha()
    image2 = pygame.transform.scale(image2, (150, 150))
    image2_rect = image2.get_rect(bottomright=(370, 490))
    screen.blit(image2, image2_rect)
    image3 = pygame.image.load(path.join(img_dir, 'planet3.png')).convert_alpha()
    image3 = pygame.transform.scale(image3, (360, 190))
    image3_rect = image3.get_rect(bottomright=(380, 275))
    screen.blit(image3, image3_rect)
    image4 = pygame.image.load(path.join(img_dir, 'planet4.png')).convert_alpha()
    image4 = pygame.transform.scale(image4, (180, 180))
    image4_rect = image4.get_rect(bottomright=(385, 145))
    screen.blit(image4, image4_rect)


def hero(name):
    image = pygame.image.load(name).convert_alpha()
    image = pygame.transform.scale(image, (600, 800))
    image_rect = image.get_rect(bottomright=(390, 835))
    screen.blit(image, image_rect)


def planet(name, kord, razmer):
    image = pygame.image.load(name).convert_alpha()
    image = pygame.transform.scale(image, kord)
    image_rect = image.get_rect(bottomright=razmer)
    screen.blit(image, image_rect)


def fon(name):
    imagefon = pygame.image.load(name).convert_alpha()
    imagefon = pygame.transform.scale(imagefon, (800, 900))
    imagefon_top = screen.get_height() - imagefon.get_height()
    imagefon_left = screen.get_width() // 2 - imagefon.get_width() // 2
    screen.blit(imagefon, (imagefon_left, imagefon_top))


def draw_txt(num, n):
    string1 = ["Хэй! привет! неплохо летаешь! и мне нужна твоя помощь!", "Есть такой капитнан Адориус", "Он собирает себе супер корабль!!", "Если он сделает это, его нельзя будет победить!", "Помешай ему, лети на Рогус и забери деталь!"]
    string2 = ["Ура! первая деталь у нас!", "Но нельзя расслабляться, капитан уже летит за следующей!", "Дай ему отпор на Уранусе, ты должен победить!", "А я пока пойду поем перепечки...", "Ах, да. будь осторожен! \'тьмок\'"]
    string3 = ["Неплохо, ты смог заполучить вторую деталь!", "Теперь нам необходима третья деталь корабля.", "Отправляйся на Нептуний и заполучи ее.", "Я верю в тебя, у тебя все получится.", "Я буду ждать тебя на Вальмадуре."]
    string4 = ["Отличноо, мы смогли получить последнюю деталь.", "Теперь мы вместе полтим на нашу главную миссию.", "Надо быть осторожными, у нашего врага огромная армия.", "Но можешь не волноваться, ведь корабль созданый тобой, в миллионы раз лучше.", "Ух, сейчас повеселимся сполна."]
    string5 = ["Ахахаха, как же ловко я обвела тебя вокруг пальца.", "Ты оказался глупее чем я думала.", "Но ты очень помог мне своей работой, теперь я смогу захватить весь этот мир.", "Спасибо тебе за это.", "А теперь тебе суждено умереть!"]
    string6 = ["Невероятно, ты оказался смелым воином.","Ведь несмотря на предательство союзников ты не сдался, а проодолжил бороться со злом,","хоть этим злом и оказались твои бывшие союзники.","Ты сражался храбо, хоть силы противника во много раз превосходили твои.","Спасибо что ты освободил космос и подарил его жителям свободу."]

    strings = {1: string1, 2: string2, 3: string3, 4: string4, 5: string5, 6: string6}

    font = pygame.font.Font(None, 25)
    text = font.render(strings[num][n], 1, (100, 255, 100))
    text_x = 10
    text_y = HEIGHT - 100
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (0, HEIGHT - 100,
                                           WIDTH, 100), 1)


def main():
    n = 0
    background = pygame.image.load(path.join(img_dir, ANIMATION[n])).convert()
    background_rect = background.get_rect()
    running = True
    while running:
        clock.tick(12)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

        screen.fill(BLACK)
        screen.blit(background, background_rect)
        background = pygame.image.load(path.join(img_dir, ANIMATION[n + 1])).convert()
        n += 1
        if n == 7:
            n = -1

        mainString = ["Давным-давно в далёкой галактике...", "Один маленький повстанец нашел остатки",
                      "старого корабля...", "Так начались его приключения", "в БОЛЬШОМ МИРЕ",
                      "Но для начала ему предстояло", "обратить на себя внимание....",
                      "используй кнопки 2 и 3 чтобы рулить кораблём", "и пробел чтобы уничтожать всё на своем пути",
                      "(жми пробел чтобы начать свой путь)"]
        ix = 100
        for i in range(len(mainString)):
            font = pygame.font.Font(None, 30)
            introText = font.render(mainString[i], 1, BLACK)
            screen.blit(introText, ((WIDTH // 2) - 230, HEIGHT // 2 - ix))
            i += 1
            ix -= 25

        pygame.display.flip()


def reset(level):
    n = 0
    background = pygame.image.load(path.join(img_dir, ANIMATION[n])).convert()
    background_rect = background.get_rect()
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    resetString = ["Похоже, твой космолёт подбили", "Однако, тебе удалось выжить", "(Жми пробел для реванша)"]
    ix = 100
    for i in range(len(resetString)):
        font = pygame.font.Font(None, 30)
        introText = font.render(resetString[i], 1, BLACK)
        screen.blit(introText, ((WIDTH // 2) - 230, HEIGHT // 2 - ix))
        i += 1
        ix -= 25
    pygame.display.flip()
    pygame.time.wait(1000)
    running = True
    while running:
        clock.tick(12)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

        screen.fill(BLACK)
        screen.blit(background, background_rect)
        background = pygame.image.load(path.join(img_dir, ANIMATION[n + 1])).convert()
        n += 1
        if n == 7:
            n = -1
        ix = 100
        for i in range(len(resetString)):
            font = pygame.font.Font(None, 30)
            introText = font.render(resetString[i], 1, BLACK)
            screen.blit(introText, ((WIDTH // 2) - 230, HEIGHT // 2 - ix))
            i += 1
            ix -= 25
        pygame.display.flip()

    LEVELS[level]()


def complete(num):
    n = 0
    background = pygame.image.load(path.join(img_dir, ANIMATION[n])).convert()
    background_rect = background.get_rect()
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    completeString = ["Победа", "Жми пробел для продолжения"]
    ix = 100
    for i in range(len(completeString)):
        font = pygame.font.Font(None, 30)
        introText = font.render(completeString[i], 1, BLACK)
        screen.blit(introText, ((WIDTH // 2) - 230, HEIGHT // 2 - ix))
        i += 1
        ix -= 25
    pygame.display.flip()
    pygame.time.wait(1000)
    running = True
    while running:
        clock.tick(12)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

        screen.fill(BLACK)
        screen.blit(background, background_rect)
        background = pygame.image.load(path.join(img_dir, ANIMATION[n + 1])).convert()
        n += 1
        if n == 7:
            n = -1
        ix = 100
        for i in range(len(completeString)):
            font = pygame.font.Font(None, 30)
            introText = font.render(completeString[i], 1, BLACK)
            screen.blit(introText, ((WIDTH // 2) - 230, HEIGHT // 2 - ix))
            i += 1
            ix -= 25
        pygame.display.flip()
    speak(num)


def home(num):
    board = Board(4, 5)
    pers = Urovni(num)
    # background = pygame.image.load(path.join(img_dir, ANIMATION[0])).convert()
    # background_rect = background.get_rect()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                if event.key == pygame.K_UP:
                    if num == 4:
                        num = 1
                    else:
                        num += 1
                if event.key == pygame.K_DOWN:
                    if num == 1:
                        num = 4
                    else:
                        num -= 1

        screen.fill(BLACK)
        # screen.blit(background, background_rect)
        board.render()
        decoration()
        pers.moving(num)
        pygame.display.flip()

    LEVELS[num]()


def speak(num):
    lvl = num
    forplanet = koord2.get(lvl)
    fon('fon.jpg')
    planet(forplanet[0], forplanet[1], forplanet[2])
    hero('hero4.png')
    n = 0
    draw_txt(num, n)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    n += 1

        forplanet = koord2.get(lvl)
        fon('fon.jpg')
        planet(forplanet[0], forplanet[1], forplanet[2])
        hero('hero4.png')
        if n < 5:
            draw_txt(num, n)
        else:
            running = False
        pygame.display.flip()
    home(num)


def level_0():
    clock.tick(FPS)
    score = 5
    n = 0
    background = pygame.image.load(path.join(img_dir, ANIMATION[n])).convert()
    background_rect = background.get_rect()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    running = True
    while running:
        scoreText = "Осталось противников: " + str(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for _ in hits:
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
            score -= 1

        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
            running = False

        if score <= 0:
            running = False

        font = pygame.font.Font(None, 30)
        scoreText = font.render(scoreText, 1, BLACK)
        screen.blit(scoreText, (10, 10))

        introString = "Первый полёт"
        introText = font.render(introString, 1, BLACK)
        screen.blit(introText, (WIDTH - 150, 10))

        pygame.display.flip()
        screen.blit(background, background_rect)
        background = pygame.image.load(path.join(img_dir, ANIMATION[n + 1])).convert()
        n += 1
        if n == 7:
            n = -1
        all_sprites.draw(screen)

    player.kill()
    for i in mobs:
        i.kill()
    if score <= 0:
        complete(1)
    else:
        reset(0)


def level_1():
    clock.tick(FPS)
    score = 5
    pewTime = 0
    n = 0
    background = pygame.image.load(path.join(img_dir, ANIMATION[n])).convert()
    background_rect = background.get_rect()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    running = True
    while running:
        pewTime += 1
        scoreText = "Осталось противников: " + str(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        for mob in mobs:
            if pewTime == 1:
                mob.shoot()

        if pewTime == 48:
            pewTime = 0

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for _ in hits:
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
            score -= 1

        hits = pygame.sprite.groupcollide(enemyBullets, bullets, True, True)

        hits = pygame.sprite.spritecollide(player, mobs, False)
        bulletHits = pygame.sprite.spritecollide(player, enemyBullets, False)
        if hits or bulletHits:
            running = False

        if score <= 0:
            running = False

        font = pygame.font.Font(None, 30)
        scoretext = font.render(scoreText, 1, BLACK)
        screen.blit(scoretext, (10, 10))

        introString = "Уровень 1"
        introText = font.render(introString, 1, BLACK)
        screen.blit(introText, (WIDTH - 110, 10))

        pygame.display.flip()
        screen.blit(background, background_rect)
        background = pygame.image.load(path.join(img_dir, ANIMATION[n + 1])).convert()
        n += 1
        if n == 7:
            n = -1
        all_sprites.draw(screen)

    player.kill()
    for i in mobs:
        i.kill()
    for i in enemyBullets:
        i.kill()
    if score <= 0:
        complete(2)
    else:
        reset(1)


def level_2():
    clock.tick(FPS)
    score = 10
    pewTime = 0
    n = 0
    background = pygame.image.load(path.join(img_dir, ANIMATION[n])).convert()
    background_rect = background.get_rect()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        m = LeftEnemyShip(i)
        all_sprites.add(m)
        mobs.add(m)

    running = True
    while running:
        pewTime += 1
        scoreText = "Осталось противников: " + str(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        for mob in mobs:
            if pewTime == 1:
                mob.shoot()

        if pewTime == 48:
            pewTime = 0

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for _ in hits:
            m = LeftEnemyShip(random.randrange(0, 3))
            all_sprites.add(m)
            mobs.add(m)
            score -= 1

        hits = pygame.sprite.groupcollide(enemyBullets, bullets, True, True)

        hits = pygame.sprite.spritecollide(player, mobs, False)
        bulletHits = pygame.sprite.spritecollide(player, enemyBullets, False)
        if hits or bulletHits:
            running = False

        if score <= 0:
            running = False

        font = pygame.font.Font(None, 30)
        scoretext = font.render(scoreText, 1, BLACK)
        screen.blit(scoretext, (10, 10))

        introString = "Уровень 2"
        introText = font.render(introString, 1, BLACK)
        screen.blit(introText, (WIDTH - 110, 10))

        pygame.display.flip()
        screen.blit(background, background_rect)
        background = pygame.image.load(path.join(img_dir, ANIMATION[n + 1])).convert()
        n += 1
        if n == 7:
            n = -1
        all_sprites.draw(screen)

    player.kill()
    for i in mobs:
        i.kill()
    for i in enemyBullets:
        i.kill()
    if score <= 0:
        complete(3)
    else:
        reset(2)


def level_3():
    clock.tick(FPS)
    score = 10
    pewTime = 0
    n = 0
    background = pygame.image.load(path.join(img_dir, ANIMATION[n])).convert()
    background_rect = background.get_rect()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        m = RightEnemyShip(i)
        all_sprites.add(m)
        mobs.add(m)

    running = True
    while running:
        pewTime += 1
        scoreText = "Осталось противников: " + str(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        for mob in mobs:
            if pewTime == 1:
                mob.shoot()

        if pewTime == 48:
            pewTime = 0

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for _ in hits:
            m = RightEnemyShip(random.randrange(0, 3))
            all_sprites.add(m)
            mobs.add(m)
            score -= 1

        hits = pygame.sprite.groupcollide(enemyBullets, bullets, True, True)

        hits = pygame.sprite.spritecollide(player, mobs, False)
        bulletHits = pygame.sprite.spritecollide(player, enemyBullets, False)
        if hits or bulletHits:
            running = False

        if score <= 0:
            running = False

        font = pygame.font.Font(None, 30)
        scoretext = font.render(scoreText, 1, BLACK)
        screen.blit(scoretext, (10, 10))

        introString = "Уровень 3"
        introText = font.render(introString, 1, BLACK)
        screen.blit(introText, (WIDTH - 110, 10))

        pygame.display.flip()
        screen.blit(background, background_rect)
        background = pygame.image.load(path.join(img_dir, ANIMATION[n + 1])).convert()
        n += 1
        if n == 7:
            n = -1
        all_sprites.draw(screen)

    player.kill()
    for i in mobs:
        i.kill()
    for i in enemyBullets:
        i.kill()
    if score <= 0:
        complete(4)
    else:
        reset(3)


def level_4():
    clock.tick(FPS)
    score = 10
    pewTime = 0
    n = 0
    background = pygame.image.load(path.join(img_dir, ANIMATION[n])).convert()
    background_rect = background.get_rect()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        m = RightEnemyShip(i)
        all_sprites.add(m)
        mobs.add(m)

    running = True
    while running:
        pewTime += 1
        scoreText = "Осталось противников: " + str(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()

        for mob in mobs:
            if pewTime == 1:
                mob.shoot()

        if pewTime == 48:
            pewTime = 0

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for _ in hits:
            m = RightEnemyShip(random.randrange(0, 3))
            all_sprites.add(m)
            mobs.add(m)
            score -= 1

        hits = pygame.sprite.groupcollide(enemyBullets, bullets, True, True)

        hits = pygame.sprite.spritecollide(player, mobs, False)
        bulletHits = pygame.sprite.spritecollide(player, enemyBullets, False)
        if hits or bulletHits:
            running = False

        if score <= 0:
            running = False

        font = pygame.font.Font(None, 30)
        scoretext = font.render(scoreText, 1, BLACK)
        screen.blit(scoretext, (10, 10))

        introString = "Уровень 4"
        introText = font.render(introString, 1, BLACK)
        screen.blit(introText, (WIDTH - 110, 10))

        pygame.display.flip()
        screen.blit(background, background_rect)
        background = pygame.image.load(path.join(img_dir, ANIMATION[n + 1])).convert()
        n += 1
        if n == 7:
            n = -1
        all_sprites.draw(screen)
    player.kill()
    for i in mobs:
        i.kill()
    for i in enemyBullets:
        i.kill()
    if score <= 0:
        boss()
    else:
        reset(4)


def boss():
    clock.tick(FPS)
    pewTime = 0
    boss = 10
    n = 0
    background = pygame.image.load(path.join(img_dir, ANIMATION[n])).convert()
    background_rect = background.get_rect()
    player = Player()
    all_sprites.add(player)
    mainBoss = MainGun()
    all_sprites.add(mainBoss)

    running = True
    while running:
        pewTime += 1
        scoreText = "Босс: " + str(boss)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            elif event.type == BOSSPEW:
                mainBoss.checkposition()
                print('yaaaay')

        all_sprites.update()
        pygame.time.set_timer(BOSSPEW, 2000)

        if pewTime == 0:
            mainBoss.shoot()

        if pewTime == 24:
            pewTime = 0

        hits = pygame.sprite.spritecollide(mainBoss, bullets, False)
        for _ in hits:
            boss -= 1

        hits = pygame.sprite.groupcollide(enemyBullets, bullets, True, True)

        bulletHits = pygame.sprite.spritecollide(player, enemyBullets, False)
        if bulletHits:
            running = False

        if boss <= 0:
            running = False

        font = pygame.font.Font(None, 30)
        scoretext = font.render(scoreText, 1, BLACK)
        screen.blit(scoretext, (10, 10))

        introString = "BOSS FIGHT"
        introText = font.render(introString, 1, BLACK)
        screen.blit(introText, (WIDTH - 150, 10))

        pygame.display.flip()
        screen.blit(background, background_rect)
        background = pygame.image.load(path.join(img_dir, ANIMATION[n + 1])).convert()
        n += 1
        if n == 7:
            n = -1
        all_sprites.draw(screen)

    mainBoss.kill()
    player.kill()
    if boss <= 0:
        complete(1)
    else:
        reset(4)


def quit():
    pygame.quit()


LEVELS = {0: level_0, 1: level_1, 2: level_2, 3: level_3, 4: level_4}

if __name__ == "__main__":
    main()
    level_0()
