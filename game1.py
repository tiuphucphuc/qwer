
import pygame, sys, random

from pygame.transform import rotate
#tao ham
def draw_an():
     screen.blit(an,(an_x_pos,650))
     screen.blit(an,(an_x_pos+500,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos-700))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes :
        #sua cho nay 1
        pipe.centerx -= 4
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600 :
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if chim_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if chim_rect.top <= -75 or chim_rect.bottom >= 650:
             return False
    return True
def rotate_chim(chim1):
    new_chim = pygame.transform.rotozoom(chim1,-chim_movement*3,1)
    return new_chim
def chim_animation():
    new_chim = chim_list[chim_index]
    new_chim_rect = new_chim.get_rect(center = (100,chim_rect.centery))
    return new_chim, new_chim_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,20 ,255))
        score_rect = score_surface.get_rect(center = (250,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,20 ,255))
        score_rect = score_surface.get_rect(center = (250,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,20 ,255))
        high_score_rect = score_surface.get_rect(center = (200,600))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen= pygame.display.set_mode((500,720))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)
#tao bien
trongluc = 0.15
chim_movement = 0
game_active = True
score =0
high_score = 0
#chen nen
bg = pygame.image.load('assets/2.png')
bg = pygame.transform.scale2x(bg) 
#chen san
an = pygame.image.load('assets/an.png')
an = pygame.transform.scale2x(an)
an_x_pos = 2
#tao chim
chim_down = pygame.transform.scale2x(pygame.image.load('assets/chim.png'))
chim_mid = pygame.transform.scale2x(pygame.image.load('assets/chim2.png'))
chim_up = pygame.transform.scale2x(pygame.image.load('assets/chim3.png'))
chim_list = [chim_down,chim_mid,chim_up]
chim_index = 0
chim = chim_list[chim_index]
#chim = pygame.image.load('assets/chim.png')
#chim = pygame.transform.scale2x(chim)
chim_rect =chim.get_rect(center = (100,300))
#tao timer cho chim
chimflap = pygame.USEREVENT + 1
pygame.time.set_timer(chimflap,200)

#tao ong
pipe_surface= pygame.image.load('assets/ong.png')
pipe_surface= pygame.transform.scale2x(pipe_surface)
pipe_list =[]
#tao timer
spawnpipe= pygame.USEREVENT
#sua cho nay
pygame.time.set_timer(spawnpipe, 1300)
pipe_height = [450,510,610,400,500,600]
#tao man hinh ket thuc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/4.png'))
game_over_rect = game_over_surface.get_rect(center=(250,360))
#chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
#while loop cua tro choi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                chim_movement = 0
                chim_movement =-4
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
                pipe_list.clear()
                chim_rect.center = (100,384)
                chim_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == chimflap:
            if chim_index < 2:
                chim_index +=1
            else:
                chim_index =0
            chim, chim_rect = chim_animation()

            

    screen.blit(bg,(-40,-350))
    if game_active:
        #chim
        chim_movement += trongluc
        rotated_chim = rotate_chim(chim)
        chim_rect.centery += chim_movement
        screen.blit(rotated_chim,chim_rect)
        game_active=check_collision(pipe_list)
        #ong
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.005
        score_display('main game')
        #sua cho nay
        score_sound_countdown -= 0.5
        if score_sound_countdown <=0:
            score_sound.play()
            score_sound_countdown =100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
    #san
    an_x_pos -= 1
    draw_an()
    if an_x_pos <= -500:
        an_x_pos =0
    pygame.display.update()
    clock.tick(120)
