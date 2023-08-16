import sys, random, pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()
w, h = 400,700
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Knife Hit')

PATH = "knife_hit_assests/"

class Board:
    def __init__(self):
        self.speed = random.randint(-2,2)
        if self.speed == 0: self.speed = -1
        self.angle = 0
        self.original_image =  pygame.image.load(PATH + 'board/'+str(random.randint(2,23))+'.png')
                
    def update(self):
        self.angle += self.speed
        self.image = pygame.transform.rotozoom(self.original_image, self.angle , 1)
        self.rect = self.image.get_rect(center = (w//2, h//4))
        if abs(self.angle) == 360: self.angle = 0

class Knife:
    def __init__(self):
        self.speed = 25
        self.angle = 0
        self.original_image = pygame.image.load(PATH + 'pic.png')
        self.image = pygame.transform.rotozoom(self.original_image , 0 ,0.6)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.original_image.get_rect(center = (w//2,h))
        self.y = h
        self.x = w//2 - self.image.get_width()//2

    def update(self):
        if not(self.rect.centery <= h//2):
            self.y -= self.speed
            self.rect.centery -= self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

class Main:
    def __init__(self):
        self.collision = False
        self.total = int(total_knife)
        self.bg = [ ]
        for i in range(3):
            self.color = random.randint(0,255)
            self.bg.append(self.color)
        self.board = Board()

        self.knives = []

        self.knife_image = pygame.transform.rotozoom(pygame.image.load(PATH + 'knife.png'), 0 ,0.6)
        self.knife_rect = self.knife_image.get_rect(center = (w//2,0))
        self.knife_rect.bottom = h
        self.k = pygame.transform.rotozoom(self.knife_image, 90 ,0.5)

        self.shoot = pygame.mixer.Sound(PATH + "sound/sfx_shieldUp.ogg")
        self.again = pygame.mixer.Sound(PATH + "sound/sfx_shieldDown.ogg")
        self.over = pygame.mixer.Sound(PATH + "sound/sfx_zap.ogg")
        self.text = pygame.font.Font(PATH + 'sound/PoetsenOne-Regular.ttf', 80)

    def update(self):
        self.board.update()
        
        for knife in self.knives:
            knife.update()
            self.rotate_knife(knife)

        self.collide()
        
        self.score_surface = self.text.render(str(stage), True, (255,255,255))

    def draw(self):
        if self.total: screen.blit(self.knife_image, self.knife_rect)

        for knife in self.knives:
            knife.draw()
        
        screen.blit(self.board.image, self.board.rect)
        
        for i in range(self.total): screen.blit(self.k,(0, -i*40 + 3*w//2))
        
        screen.blit(self.score_surface,(10,-10))

    def collide(self):
        for obj1 in self.knives:
            for obj2 in self.knives:
                if obj1 != obj2:
                    offset_x = obj2.rect.x- obj1.rect.x
                    offset_y = obj2.rect.y - obj1.rect.y
                    if obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None:
                        self.collision = True
                        return

    def rotate_knife(self,knife):
        if knife.rect.centery <= h//2:
            knife.original_image = pygame.image.load(PATH + 'picture.png')
            knife.image = pygame.transform.rotozoom(knife.original_image, knife.angle,0.6)
            knife.rect = knife.image.get_rect(center = (w//2,h//4))
            knife.mask = pygame.mask.from_surface(knife.image)
            knife.angle += self.board.speed
            if abs(knife.angle) == 360: knife.angle = 0

def start():
    global total_knife,stage
    total_knife = 5
    stage = 1

def lost():
    lost = pygame.font.Font(PATH + 'sound/PoetsenOne-Regular.ttf', 40)
    lost_label = lost.render("You Lost !!",1,(255,255,255))
    lost_rect = lost_label.get_rect(center = (w//2,h//2))
    screen.blit(lost_label,lost_rect)
    pygame.display.update()
    pygame.time.delay(1000)

start()
game = Main()

while True:
    screen.fill(tuple(game.bg))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if game.total and event.key == pygame.K_SPACE:
                knife = Knife()
                game.knives.append(knife)
                game.total -= 1
                pygame.mixer.Sound.play(game.shoot)

            elif not(game.total or event.key == pygame.K_SPACE):
                total_knife += 0.3
                stage += 1
                game = Main()
                pygame.mixer.Sound.play(game.again)

    if game.collision:
        lost()
        start()
        game = Main()
            
    game.update()
    game.draw()
    pygame.display.update()
    clock.tick(70)
