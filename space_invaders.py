import pygame, random, sys
pygame.init()
clock = pygame.time.Clock()

W, H = 1000, 650
WIN = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Invaders")

# Assests Path
PATH = "space_invaders_assests/"

# Space Ships
RED_SHIP = pygame.image.load(PATH + 'enemyRed2.png')
GREEN_SHIP = pygame.image.load(PATH + 'enemyGreen2.png')
BLUE_SHIP = pygame.image.load(PATH + 'enemyBlue2.png')

# Player Ship
YELLOW_SHIP = pygame.image.load(PATH + 'ship.png')

# Lasers
RED_LASER = pygame.image.load(PATH + 'laserRed01.png')
GREEN_LASER = pygame.image.load(PATH + 'laserGreen11.png')
BLUE_LASER = pygame.image.load(PATH + 'laserBlue01.png')
YELLOW_LASER = pygame.image.load(PATH + 'pixel_laser_yellow.png')

# BG
BG = (64,0,64)

# Pause
pause_img = pygame.image.load(PATH + 'pause.png')
pause_rect = pause_img.get_rect(center = (W - 30, 70))

class Ship:
    COOLDOWN = 15

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y =y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self,window):
        for laser in self.lasers:
            laser.draw(window)
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def move_laser(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen():
                self.lasers.remove(laser)
            elif laser.collision(obj):
                self.lasers.remove(laser)
                if laser.img == RED_LASER:
                    obj.health -= 10
                elif laser.img == GREEN_LASER:
                    obj.health -= 2
                elif laser.img == BLUE_LASER:
                    obj.health -= 5
                

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 6, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_laser(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def health_bar(self,window):
        pygame.draw.rect(window, (255,0,0), (10, 50, self.max_health, 20))
        if self.health > 0: pygame.draw.rect(window, (0,255,0), (10, 50, self.health, 20))

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

class Enemy(Ship):
    COLOR_MAP = {"red" : (RED_SHIP, RED_LASER),"green" : (GREEN_SHIP, GREEN_LASER),"blue" : (BLUE_SHIP, BLUE_LASER),}
    
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 48, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self,vel):
        self.y += vel

    def off_screen(self):
        return self.y >= H or self.y <= -50

    def collision(self, obj):
        return COLLIDE(self, obj)

def COLLIDE(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask ,(offset_x, offset_y)) != None

def MAIN_GAME():
    # Player
    player = Player(W//2 - 50, H - 150)
    vel = 5
    laser_vel_player = -10

    # Enemy
    enemies = []
    for i in range(5):
        enemy = Enemy(random.randrange(50, W - 100), random.randrange(-500, -100), random.choice(["red","blue","green"]))
        enemies.append(enemy)
    enemy_vel = 1
    laser_vel_enemy = 5

    # Stats
    level = 1
    lives = 5
    wave = 5
    lost = 0
    pause = False

    # Limit
    w_lim = W - player.get_width()
    h_lim = H - player.get_height() - 10

    # Font
    main_font = pygame.font.SysFont('Papyrus', 25,1)
    lost_font = pygame.font.SysFont('Papyrus', 50,1)

    def redraw_window():
        WIN.fill(BG)

        # Pause
        WIN.blit(pause_img, pause_rect)

        # Enemy
        for enemy in enemies:
            enemy.draw(WIN)

        # Ship
        player.draw(WIN)

        # Draw Text
        lives_label = main_font.render(f"Invasion Left: {lives}",1,(255,255,255))
        level_label = main_font.render(f"Wave: {level}",1,(255,255,255))
        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (W - level_label.get_width() - 10, 10))

        # Lost
        if lost:
            lost_label = lost_font.render("You Lost !!", 1, (255,255,255))
            WIN.blit(lost_label, (W//2 - lost_label.get_width()//2, H//2 - lost_label.get_height()//2))
        
        pygame.display.update()

    # Game Loop
    while True:

        # Events
        for event in pygame.event.get():
            
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Pause
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        pause = False
                    else:
                        pause = True

        # Movements
        if not lost and not pause:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:     # left
                player.x -= vel
                if player.x <= 0:
                    player.x = 0
                    
            if keys[pygame.K_d]:    # right
                player.x += vel
                if player.x >= w_lim:
                    player.x = w_lim
                    
            if keys[pygame.K_w]:    # up
                player.y -= vel
                if player.y <= 0:
                    player.y = 0
                    
            if keys[pygame.K_s]:    # down
                player.y += vel
                if player.y >= h_lim:
                    player.y = h_lim

            if keys[pygame.K_SPACE]:    # shoot
                player.shoot()

            # Draw and Increase Enemy and Lasers 
            if len(enemies) == 0:
                level += 1
                wave += 2
                #enemy_vel += 0.5
                #laser_vel_enemy += 0.5
                for i in range(wave):
                    enemy = Enemy(random.randrange(50, W - 100), random.randrange(-500, -100), random.choice(["red","blue","green"]))
                    enemies.append(enemy)
                    
            for enemy in enemies[:]:
                enemy.move(int(enemy_vel))
                enemy.move_laser(int(laser_vel_enemy), player)

                if random.randrange(0, 200) == 1:
                    enemy.shoot()

                if COLLIDE(enemy,player):
                    player.health -= 10
                    enemies.remove(enemy)
                
                elif enemy.y > H:
                    lives -= 1
                    enemies.remove(enemy)

        # Lost
        if lives <= 0 or player.health <= 0: lost += 1
        if lost > 200: main_menu()

        # Pause
        if pause:
            pause_label = lost_font.render("Paused", 1, (255,255,255))
            WIN.blit(pause_label, (W//2 - pause_label.get_width()//2, H//2 - pause_label.get_height()//2))
            pygame.display.update()
            continue

        # Laser
        player.move_laser(laser_vel_player, enemies)

        redraw_window()
        clock.tick(70)

def main_menu():
    title = pygame.font.SysFont('comicsans',80)
    while True:
        WIN.fill((0,0,0))

        title_label = title.render("Press Enter To Start...",1,(255,255,255))
        title_rect = title_label.get_rect(center = (W//2, H//2))
        WIN.blit(title_label, title_rect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    MAIN_GAME()
main_menu()
