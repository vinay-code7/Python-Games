def main():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    import os
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
    import pygame, sys, random

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    clock = pygame.time.Clock()

    def ball_animation():
        global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
        
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= height:
            pygame.mixer.Sound.play(pong_sound)
            ball_speed_y *= -1
            
        if ball.left <= 0:
            pygame.mixer.Sound.play(score_sound)
            player_score += 1
            score_time = pygame.time.get_ticks()
            
        if ball.right >= width:
            pygame.mixer.Sound.play(score_sound)
            opponent_score += 1
            score_time = pygame.time.get_ticks()

        if ball.colliderect(player) and ball_speed_x > 0:
            pygame.mixer.Sound.play(pong_sound)
            if abs(ball.right - player.left) < 10:
                ball_speed_x *= -1
            elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
                ball_speed_y *= -1
            elif abs(ball.top- player.bottom) < 10 and ball_speed_y < 0:
                ball_speed_y *= -1
            
        if ball.colliderect(opponent) and ball_speed_x < 0:
            pygame.mixer.Sound.play(pong_sound)
            if abs(ball.left - opponent.right) < 10:
                ball_speed_x *= -1
            elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
                ball_speed_y *= -1
            elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
                ball_speed_y *= -1

    def player_animation():
        player.y += player_speed
        
        if player.top <= 0:
            player.top = 0
        if player.bottom >= height:
            player.bottom = height

    def opponent_animation():
        opponent.y += opponent_speed
        
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= height:
            opponent.bottom = height

    def ball_start():
        global ball_speed_y, ball_speed_x,score_time

        current_time = pygame.time.get_ticks()
        ball.center = (width//2, height//2)

        if current_time - score_time < 1000:
            number_three = game_font.render("3",False,light_grey)
            screen.blit(number_three,(width//2 - 5,height//2 + 30))
        if 1000 < current_time - score_time < 2000:
            number_two = game_font.render("2",False,light_grey)
            screen.blit(number_two,(width//2 - 5,height//2 + 30))
        if 2000 < current_time - score_time < 3000:
            number_one = game_font.render("1",False,light_grey)
            screen.blit(number_one,(width//2 - 5,height//2 + 30))

        if current_time - score_time < 3000:
            ball_speed_x, ball_speed_y = 0,0
        else:
            ball_speed_y = 4 * random.choice((-1,1))
            ball_speed_x = 4 * random.choice((-1,1))
            score_time = None
        
    width = 640
    height = 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Pong 2')

    ball = pygame.Rect(width//2 - 7, height//2 - 7, 15, 15)
    player = pygame.Rect(width - 10, height//2 - 35, 5, 70)
    opponent = pygame.Rect(5, height//2 - 35, 5, 70)

    bg_color = pygame.Color('grey12')
    light_grey = (200,200,200)

    ball_speed_x = 6 * random.choice((-1,1))
    ball_speed_y = 6 * random.choice((-1,1))
    player_speed = 0
    opponent_speed = 0

    player_score = 0
    opponent_score = 0
    game_font = pygame.font.Font(None,25)

    score_time = True

    pong_sound = pygame.mixer.Sound("pong_game_assests/pong.ogg")
    score_sound = pygame.mixer.Sound("pong_game_assests/score.ogg")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    opponent_speed += 5
                if event.key == pygame.K_w:
                    opponent_speed -= 5
                    
                if event.key == pygame.K_DOWN:
                    player_speed += 5
                if event.key == pygame.K_UP:
                    player_speed -= 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    opponent_speed -= 5
                if event.key == pygame.K_w:
                    opponent_speed += 5
                    
                if event.key == pygame.K_DOWN:
                    player_speed -= 5
                if event.key == pygame.K_UP:
                    player_speed += 5

        ball_animation()
        player_animation()
        opponent_animation()
        
        screen.fill(bg_color)
        pygame.draw.rect(screen,light_grey,player)
        pygame.draw.rect(screen,light_grey,opponent)
        pygame.draw.ellipse(screen,light_grey,ball)
        pygame.draw.aaline(screen,light_grey,(width//2,0),(width//2,height))

        if score_time:
            ball_start()
            
        player_text = game_font.render(f'{player_score}', False, light_grey)
        screen.blit(player_text,(345,235))

        opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
        screen.blit(opponent_text,(285,235))
        
        pygame.display.flip()
        clock.tick(60)
main()
