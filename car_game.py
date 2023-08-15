
import time, sys
from random import choice

import pygame
pygame.mixer.pre_init(44100,-16,1,512)
pygame.init()

PATH = "car_game_assests/"

class CAR:
    def __init__(self):
        self.car_image = pygame.transform.scale(pygame.image.load(PATH + 'car.png').convert_alpha(),(60,120))
        self.car_rect = self.car_image.get_rect(center=(width//2, height - 100))
        self.mask = pygame.mask.from_surface(self.car_image)
        self.car_speed = [0,0]

    def draw_car(self):
        screen.blit(self.car_image, self.car_rect)
        if self.car_rect.top <= 0 : self.car_rect.top = 0
        if self.car_rect.bottom >= height: self.car_rect.bottom = height
        if self.car_rect.left <= 17: self.car_rect.left = 17
        if self.car_rect.right >= width-20: self.car_rect.right = width-20

    def move_car(self):
        self.car_rect.y += self.car_speed[1]
        self.car_rect.x += self.car_speed[0]

class BASE:
    def __init__(self):
        self.base_image = pygame.transform.scale(pygame.image.load(PATH + 'base.png').convert_alpha(),(20,650))
        self.base_rect = self.base_image.get_rect(center = (0,0))
        self.base_speed = 2

    def draw_base(self):
        self.base_rect.y += self.base_speed
        if self.base_rect.y >= height :
            self.base_rect.y = 0
            
        screen.blit(self.base_image, (width -20, self.base_rect.y - height))
        screen.blit(self.base_image, (width - 20, self.base_rect.y))
        screen.blit(self.base_image, (0, self.base_rect.y - height))
        screen.blit(self.base_image, (0, self.base_rect.y))

class OBJECT:
    def __init__(self):
        self.object_image = pygame.transform.scale(pygame.image.load(PATH + 'car.png').convert_alpha(),(60,120))
        self.object_image = pygame.transform.rotate(self.object_image, 180)
        self.mask = pygame.mask.from_surface(self.object_image)
        
        self.object_rect1 = self.object_image.get_rect(center = (-50,-50))
        self.object_rect2 = self.object_image.get_rect(center = (-50,-50))
        self.object_rect3 = self.object_image.get_rect(center = (-50,-50))

        self.x_pos = [80, 130, 210, 270,350]
        self.y_pos = [-180,70, 320, 570]
        for index,i in enumerate(self.y_pos):
            self.y_pos[index] = i - 700

    def draw_object(self):
        
        self.object_rect1.y += object_speed
        self.object_rect2.y += object_speed
        self.object_rect3.y += object_speed

        screen.blit(self.object_image, self.object_rect1)
        screen.blit(self.object_image, self.object_rect2)
        screen.blit(self.object_image, self.object_rect3)

        if self.object_rect1.top > height: self.spawn_object1()
        elif self.object_rect2.top > height : self.spawn_object2()
        elif self.object_rect3.top > height : self.spawn_object3()

        self.x_pos = [80, 130, 210, 270,350]
        
    def spawn_object1(self):
        self.x = choice(self.x_pos)
        self.y = choice(self.y_pos)
        self.object_rect1 = self.object_image.get_rect(center = (self.x,self.y))
        self.x_pos.remove(self.x)

    def spawn_object2(self):
        self.x = choice(self.x_pos)
        self.y = choice(self.y_pos)
        self.object_rect2 = self.object_image.get_rect(center = (self.x,self.y))
        self.x_pos.remove(self.x)

    def spawn_object3(self):
        self.x = choice(self.x_pos)
        self.y = choice(self.y_pos)
        self.object_rect3 = self.object_image.get_rect(center = (choice(self.x_pos), choice(self.y_pos)))
        
class MAIN:
    def __init__(self):
        self.car = CAR()
        self.base = BASE()
        self.object = OBJECT()
        self.score = 0
        self.over_sound = pygame.mixer.Sound(PATH + 'sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound(PATH + 'sfx_point.wav')

    def everything(self):
        self.car.draw_car()
        self.base.draw_base()
        self.object.draw_object()
        self.car.move_car()
        self.draw_score()
        self.check_collision()
        self.double_spawn()

    def draw_score(self):
        score_font = pygame.font.Font(PATH + 'PoetsenOne-Regular.ttf', 50)
        score_surface = score_font.render(str(self.score)+'s', True, (0,0,0))
        score_rect = score_surface.get_rect(center = (width//2,50))
        screen.blit(score_surface,score_rect)

    def check_collision(self):
        self.objects = [self.object.object_rect1, self.object.object_rect2, self.object.object_rect3]
        for rect in self.objects:
            off_x = rect.x - self.car.car_rect.x
            off_y = rect.y - self.car.car_rect.y
            if self.car.mask.overlap(self.object.mask ,(off_x,off_y)) != None:
                self.over_sound.play()
                time.sleep(2)
                self.restart()

    def double_spawn(self):
        self.objects = [self.object.object_rect1, self.object.object_rect2, self.object.object_rect3]
        for i in self.objects:
            for j in self.objects:
                if i != j:
                    if i.colliderect(j):
                        j.x = choice(self.object.x_pos)
                        j.y = choice(self.object.y_pos)

    def restart(self):
        self.car = CAR()
        self.base = BASE()
        self.object = OBJECT()
        self.score = -2

width, height = 420, 650
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Car Game')

bg = pygame.transform.scale(pygame.image.load(PATH + 'bg.png').convert(),(width,height))
main_game = MAIN()
frame_rate = 120

object_speed = 3

SCORE = pygame.USEREVENT
pygame.time.set_timer(SCORE, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCORE:
            main_game.score += 1
            main_game.score_sound.play()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                main_game.car.car_speed[1] = 2
            if event.key == pygame.K_UP:
                main_game.car.car_speed[1] = -2
            if event.key ==pygame.K_LEFT:
                main_game.car.car_speed[0] = -3
            if event.key ==pygame.K_RIGHT:
                main_game.car.car_speed[0] = 3   
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                main_game.car.car_speed[1] = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                main_game.car.car_speed[0] = 0
        
    screen.blit(bg,(0,0))
    main_game.everything()
    
    pygame.display.update()
    clock.tick(frame_rate)

