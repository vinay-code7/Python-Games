# 150 Lines

def main():
    global p1, p2, t
    import time, os
    player_1 = input("Name of Player 1: ")
    player_2 = input("Name of Player 2: ")

    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
    import pygame

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    clock = pygame.time.Clock()

    i = (400,520)
    screen = pygame.display.set_mode(i)
    pygame.display.set_caption('Tic - Tac - Toe')
    grey = (90, 88, 88)
    white = (255,255,255)

    PATH = "tic_tac_toe_assests/"

    c = [(80,80),(200,80),(320,80),
        (80,200),(200,200),(320,200),
        (80,320),(200,320),(320,320)]
    pos = 4
    win_mark = [ [c[0], c[1], c[2]] , [c[3], c[4], c[5]] , [c[6], c[7], c[8]] ,
                [c[0], c[3], c[6]] , [c[1], c[4], c[7]] ,[c[2], c[5], c[8]] ,
                [c[0], c[4], c[8]] , [c[2], c[4], c[6]] ]

    put = pygame.mixer.Sound(PATH + "pong.ogg")
    no_put = pygame.mixer.Sound(PATH + "sfx_hit.wav")
    win_sound = pygame.mixer.Sound(PATH + "sfx_die.wav")

    game_font = pygame.font.Font(PATH + 'PoetsenOne-Regular.ttf',30)
    score_font = pygame.font.Font(PATH + '04B_19.TTF',50)

    o = pygame.image.load(PATH + 'circle.png').convert()
    o = pygame.transform.scale(o,(80,80))
    o_rect = o.get_rect(center = (0,0))

    x = pygame.image.load(PATH + 'cross.png').convert()
    x = pygame.transform.scale(x,(80,80))
    x_rect = x.get_rect(center = (0,0))

    box = pygame.image.load(PATH + 'box.png').convert()
    box = pygame.transform.scale(box,(100,100))

    mark, x_marks, o_marks, chance = [], set(), set(), 0
    p1, p2, t = 0, 0, 0

    def draw_lines():
        length, breadth = 3, 360
        line1 = pygame.Rect(120+20, 0+20, length, breadth)
        line2 = pygame.Rect(240+20, 0+20, length, breadth)
        line3 = pygame.Rect(0+20, 120+20, breadth, length)
        line4 = pygame.Rect(0+20, 240+20, breadth, length)
        pygame.draw.rect(screen, white, line1)
        pygame.draw.rect(screen, white, line2)
        pygame.draw.rect(screen, white, line3)
        pygame.draw.rect(screen, white, line4)
        
    def draw_names():
        player_1_name = game_font.render(f'{player_1}', True, (255, 255, 0))
        screen.blit(player_1_name,(45,390))
        player_2_name= game_font.render(f'{player_2}', True, (255,128,0))
        screen.blit(player_2_name,(290,390))
    def draw_x():
        x_mark = [mark[i] for i in range(0,len(mark),2)]
        for i in x_mark:
            x_rect.center = i
            screen.blit(x, x_rect)
        if len(mark) % 2 == 0:
            screen.blit(x, (160,420))      
    def draw_o():
        o_mark = [mark[i] for i in range(1,len(mark),2)]
        for i in o_mark:
            o_rect.center = i
            screen.blit(o, o_rect)
        if len(mark) % 2 != 0:
            screen.blit(o, (160,420))            
    def draw_box():
        global box_rect
        box_rect = box.get_rect(center = c[pos])
        screen.blit(box, box_rect)
    def draw_score():
        p1_score = score_font.render(f'{p1}', False, (255, 255, 255))
        screen.blit(p1_score,(60,440))
        p2_score = score_font.render(f'{p2}', False, (255, 255, 255))
        screen.blit(p2_score,(310,440))
    def win():
        global p1, p2
        for i in win_mark:
            if set(i).issubset(x_marks):
                p1 += 1
                return player_1
            elif set(i).issubset(o_marks):
                p2 += 1
                return player_2
        return False
    def tie_condition():
        global t
        if len(mark) == 9:
            t = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if box_rect.center not in mark:
                        mark.append(box_rect.center)
                        if chance % 2:
                            o_marks.add(box_rect.center)
                        else:
                            x_marks.add(box_rect.center)
                        chance += 1
                        pygame.mixer.Sound.play(put)
                    else:
                        pygame.mixer.Sound.play(no_put)
                            
                if event.key == pygame.K_LEFT:
                    if pos - 1 < 0: pass
                    else: pos -= 1
                if event.key == pygame.K_RIGHT:
                    if pos + 1 > 8: pass
                    else: pos += 1
                if event.key == pygame.K_UP:
                    if pos - 3 < 0: pass
                    else: pos -= 3
                if event.key == pygame.K_DOWN:
                    if pos + 3 > 8: pass
                    else: pos += 3

        game_state = win()
        screen.fill(grey)
        draw_lines()
        draw_box()
        draw_score()
        draw_names()
        draw_x()
        draw_o()
        tie_condition()
        
        if t == 1:
            mark = []
            x_marks, o_marks, chance = set(), set(), 0
            tie = score_font.render('Tie  Tie  Tie', True, (255,0,0))
            screen.blit(tie,(50,180))
            pygame.mixer.Sound.play(win_sound)
        
        if game_state:
            pygame.mixer.Sound.play(win_sound)
            mark = []
            x_marks, o_marks, chance = set(), set(), 0
        
        pygame.display.flip()
        clock.tick(120)
        
        if game_state or t:
            time.sleep(2)
            t = 0
main()
