import pygame
import random
pygame.init()

w = 864
h = 936
fps = 60
clock = pygame.time.Clock()
ground_scroll = 0
scrolling = 4
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False


font = pygame.font.SysFont('Bauhaus 93', 50)
white = (255,255,255)
sc = pygame.display.set_mode((w,h))
pygame.display.set_caption('KUS')
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')
button_image = pygame.image.load('img/restart.png')
game = True
flying = False
game_over = False

def draw_text(text,font,text_col,x,y):
    img = font.render(text, True, text_col)
    sc.blit(img, (x,y))


def reset():
    pipe_group.empty()
    bird.rect.x = 100
    bird.rect.y = h/2
    score = 0
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        for i in range(1,4):
            self.images.append(pygame.image.load(f'img/bird{i}.png'))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0
        self.speed = 0
        self.clicked = False


    def update(self):
        if flying:
            self.speed +=0.5
            if self.rect.bottom < 768:
                self.rect.y +=self.speed
        
        if game_over == False:
            udar = 5
            self.counter+=1
            if self.counter>udar:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            if pygame.key.get_pressed()[pygame.K_SPACE] == True and self.clicked==False:
                self.speed = -6
                self.clicked = True
            if pygame.key.get_pressed()[pygame.K_SPACE]== False:
                self.clicked = False


            self.image = pygame.transform.rotate(self.images[self.index], self.speed* -3)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y-pipe_gap/2]
        if position == -1:
            self.rect.topleft = [x,y +pipe_gap/2]


    def update(self):
        self.rect.x -= scrolling
        if self.rect.right < 0:
            self.kill() 


class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True:
                action = True
        sc.blit(self.image, (self.rect.x, self.rect.y))
        return action
    
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

bird = Bird(100,h/2)
bird_group.add(bird)

button = Button(w/2-50, h/2-100, button_image)

while game:
    clock.tick(fps)
    sc.blit(bg,(0,0))
    bird_group.draw(sc)
    bird_group.update()
    pipe_group.draw(sc)


    if game_over ==False and flying == True:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_h = random.randint(-100,100)
            btm_pipe = Pipe(w, h/2 + pipe_h, -1)
            top_pipe = Pipe(w, h/2 + pipe_h, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        pipe_group.update()
        ground_scroll-=scrolling
        if abs(ground_scroll)>35:
            ground_scroll = 0


    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe = False

    draw_text(str(score), font,white,int(w/2), 50)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or bird.rect.top < 0:
        game_over = True
    if bird.rect.bottom >= 768:
        game_over = True
        flying = False
    
    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and flying== False and game_over ==False:
            flying = True
    
    sc.blit(ground, (ground_scroll, 768))

    pygame.display.update()

pygame.quit()