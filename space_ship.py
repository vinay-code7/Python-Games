import pygame, sys, random, os
os.environ['SDL_VIDEO_WINDOW_POS'] = f"30,30"

PATH = "space_ship_assests/"

class SpaceShip(pygame.sprite.Sprite):
    
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.uncharged = pygame.image.load(path)
        self.charged = pygame.image.load(path)
        
        self.image  = self.charged
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.shield_surface = pygame.image.load(PATH + 'playerLife2_orange.png')
        self.health = 5
        
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_limit()
        self.disp_health()

    def screen_limit(self):
        if self.rect.right >= width: self.rect.right = width
        if self.rect.left <= 0: self.rect.left = 0
        if self.rect.top <=0 : self.rect.top= 0
        if self.rect.bottom >= height: self.rect.bottom = height

    def disp_health(self):
        for shield in range(self.health):
            screen.blit(self.shield_surface, (shield * 50 + 20, 20))

    def damage(self, damage):
        self.health -= damage

    def charge(self):
        self.image = self.charged

    def discharge(self):
        self.image = self.uncharged
        
class Meteor(pygame.sprite.Sprite):

    def __init__(self, path, x_pos, y_pos, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.x_speed, self.y_speed = x_speed, y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        if self.rect.top >= height: self.kill()

class Laser(pygame.sprite.Sprite):

    def __init__(self, path, pos, speed):
        super().__init__()
        self.image  = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    def update(self):
        self.rect.centery -= self.speed

        if self.rect.bottom <= 0: self.kill()

def main_game():
    global laser_active
    pygame.mouse.set_visible(False)
    
    # Drawing
    laser_group.draw(screen)
    spaceship_group.draw(screen)
    meteor_group.draw(screen)

    # Collisions
    if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
        spaceship_group.sprite.damage(1)   
    for laser in laser_group:
        pygame.sprite.spritecollide(laser, meteor_group, True)

    # Laser Timer
    if pygame.time.get_ticks() - laser_timer >= 200:
        laser_active = True
        spaceship_group.sprite.charge()
        
    # Update
    laser_group.update()
    spaceship_group.update()
    meteor_group.update()
    return 1

def game_over():
    pygame.mouse.set_visible(True)
    
    text = game_font.render("Game Over !!!", True, (250,250,250))
    text_rect = text.get_rect(center = (width//2, height//3))
    screen.blit(text, text_rect)
    
    score_text = game_font.render(f"Score : {score}", True, (250,250,250))
    score_rect = text.get_rect(center = (width//2 +20, height//2))
    screen.blit(score_text, score_rect)
    
# Setup
pygame.init()
clock = pygame.time.Clock()
score = 0
game_font = pygame.font.Font(PATH + 'LazenbyCompSmooth.ttf', 60)
laser_timer = 0
laser_active = True

# Screen
width, height = 1300,650
screen = pygame.display.set_mode((width,height))

# Space Ship
spaceship = SpaceShip(PATH + 'playerShip2_orange.png',0,0)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

# Meteors
meteor_group = pygame.sprite.Group()
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, 200)
meteors = (PATH + 'meteorGrey_med1.png',PATH + 'meteorGrey_med2.png',PATH + 'meteorGrey_big1.png',
           PATH + 'meteorGrey_big2.png',PATH + 'meteorGrey_big3.png',PATH + 'meteorGrey_big4.png')

#Laser
laser_group = pygame.sprite.Group()

def main_menu():
    font = pygame.font.Font(None,100)
    font_label = font.render("Press Any Key...",1,(255,255,255)) 
    font_rect = font_label.get_rect(center = (width//2,height//2))
    while True:
        screen.fill((0,0,0))
        screen.blit(font_label,font_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: return
        pygame.display.update()

main_menu()
# Game Loop
while True:
    # Events
    for event in pygame.event.get():
        
        # Exit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Spawn Meteors
        if event.type == METEOR_EVENT:
            meteor_path = random.choice(meteors)
            x_pos = random.randint(0,width)
            y_pos = random.randint(-500, -100)
            x_speed = random.randint(-1,1)
            y_speed = random.randint(3,6)
            meteor = Meteor(meteor_path, x_pos, y_pos, x_speed, y_speed)
            meteor_group.add(meteor)

        # Spawn Lasers
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and laser_active:
        #if pygame.mouse.get_pressed()[0]:
            try:
                laser = Laser(PATH + 'laserBlue01.png', pygame.mouse.get_pos(), 15)
                laser_group.add(laser)
                laser_active = False
                laser_timer = pygame.time.get_ticks()
                spaceship_group.sprite.discharge()
            except : pass
            
        # Restart
        if event.type == pygame.KEYDOWN and spaceship_group.sprite.health == 0:
            spaceship_group.sprite.health = 5
            meteor_group.empty()
            laser_group.empty()
            score = 0
            main_menu()

    # BG
    screen.fill(pygame.Color('grey10'))
    #screen.blit(BG, (0,0))

    # Game
    if spaceship_group.sprite.health > 0: score += main_game()
    else: game_over()
        
    pygame.display.update()
    clock.tick(120)
