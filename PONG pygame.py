import pygame
from pygame.locals import *
import time

# Initialization
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60
MARGIN = 10
PADDLE_WIDTH = 20
BALL_RADIUS = 8
BUTTON_WIDTH = 225
BUTTON_HEIGHT = 50
BUTTON_ELEVATION = 6
FONT_SIZE = 35

# Colors
BACKGROUND_COLOR = "black"
TEXT_COLOR_WHITE = "white"
TEXT_COLOR_PINK = "pink"
TEXT_COLOR_OLIVE = "olive"
TEXT_COLOR_BLUE = "blue"
TEXT_COLOR_YELLOW = "yellow"
BUTTON_COLOR_TOP = "#00224D"
BUTTON_COLOR_BOTTOM = "#FFDB00"

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pongg')
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont('Cooper Black', 42)
font1 = pygame.font.SysFont('Goudy Stout', 50)
font2 = pygame.font.SysFont('Impact', FONT_SIZE)
font3 = pygame.font.SysFont('Forte',35)
font4 = pygame.font.SysFont('Berlin Sans FB Demi',50)
font5 = pygame.font.SysFont('Goudy Stout', 60)
# Button Class
class Button:
    def __init__(self, screen, text, width, height, pos, elevation, font, onclick):
        self.screen = screen
        self.font = font
        self.onClick = onclick
        self.pressed = False
        self.elevation = elevation
        self.dynamicElevation = elevation
        self.original_y_pos = pos[1]
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_rect.center = pos
        self.top_color = BUTTON_COLOR_TOP
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = BUTTON_COLOR_BOTTOM
        self.text_surf = self.font.render(text, True, "#F9E400")
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
    
    def draw(self):
        self.top_rect.y = self.original_y_pos - self.dynamicElevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamicElevation
        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=20)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=20)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_Click()

    def check_Click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = BUTTON_COLOR_TOP
            if pygame.mouse.get_pressed()[0]:
                self.dynamicElevation = 0
                self.pressed = True
            else:
                self.dynamicElevation = self.elevation
                if self.pressed:
                    self.onClick()
                    self.pressed = False
        else:
            self.dynamicElevation = self.elevation
            self.top_color = BUTTON_COLOR_TOP

# Game States
gamestate = {"oneplayer": False, "twoplayer": True}
gameactive = False

def oneplayer():
    global gameactive
    gameactive = True
    pygame.rect
    gamestate["oneplayer"] = True
    gamestate["twoplayer"] = False

def twoplayer():
    global gameactive
    gameactive = True
    gamestate["oneplayer"] = False
    gamestate["twoplayer"] = True

# Buttons
button1 = Button(screen, "Single Player", BUTTON_WIDTH, BUTTON_HEIGHT, (600, 300), BUTTON_ELEVATION, font3, oneplayer)
button2 = Button(screen, "Multi Player", BUTTON_WIDTH, BUTTON_HEIGHT, (600, 380), BUTTON_ELEVATION, font3, twoplayer)

# Game variables
live_ball = False
c_score = 0
p_score = 0
speed_inc = 0
winner = 0

class Paddle:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, PADDLE_WIDTH, self.height)
        self.speed = 5

    def move(self, keyup, keydown):
        key = pygame.key.get_pressed()
        if key[keyup] and self.rect.top > MARGIN:
            self.y -= self.speed
        if key[keydown] and self.rect.bottom < SCREEN_HEIGHT:
            self.y += self.speed
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(screen, "#F8EDE3", self.rect)
    
    def dec(self):
        self.rect.height = max(self.height - 10, 40)  # Minimum height

    def ai(self):
        if self.rect.centery < pong.rect.top and self.rect.bottom < SCREEN_HEIGHT:
            self.y += self.speed
        if self.rect.centery > pong.rect.top and self.rect.top > MARGIN:
            self.y -= self.speed
        self.rect.y = self.y

class Ball:
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        if self.rect.top < MARGIN - 3 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1
        if self.rect.colliderect(player_paddle.rect) or self.rect.colliderect(cpu_paddle.rect):
            self.speed_x *= -1
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.right > SCREEN_WIDTH:
            self.winner = -1
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        return self.winner

    def draw(self):
        pygame.draw.circle(screen, "white", (self.rect.centerx, self.rect.centery), BALL_RADIUS)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.speed_x = -5
        self.speed_y = 5
        self.winner = 0

# Create paddles and ball
cpu_paddle = Paddle(SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2, 100)
player_paddle = Paddle(20, SCREEN_HEIGHT // 2, 100)
pong = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

def draw_board():
    screen.fill(BACKGROUND_COLOR)
    

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, [x, y])

def handle_events():
    global gameactive, live_ball
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
            live_ball = True
            pong.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

def adjust_ball_speed():
    global speed_inc
    if speed_inc > 50:
        speed_inc = 0
        if pong.speed_x < 0:
            pong.speed_x -= 0.5   
        if pong.speed_x > 0:
            pong.speed_x += 0.5
        if pong.speed_y < 0:
            pong.speed_y -= 0.5   
        if pong.speed_y > 0:
            pong.speed_y += 0.5

def game_loop():
    global live_ball, winner, c_score, p_score,gameactive
    while True:
        clock.tick(FPS)
        
        if not gameactive:
            
            screen.fill("black")
            pygame.draw.circle(screen,"white",(600,350),200)
            draw_text('P              nG', font5, "#F9E400", 325, 300)
            pygame.draw.line(screen,"white",(50,340),(320,340),5)
            pygame.draw.line(screen,"white",(960,340),(1180,340),5)
            button1.draw()
            button2.draw()
        else:
            if gamestate["oneplayer"] :
                draw_board()
                pygame.draw.circle(screen,"#211951",(600,350),200)
                draw_text(f' {c_score}', font, "#FF204E", 570,200)
                draw_text(f' {p_score}', font, "#FF204E",570,450)
                
                #draw_text(f'Ball Speed: {abs(pong.speed_x)}', font, TEXT_COLOR_PINK, 80, 50)
            
                draw_text('P              nG', font5, "#FF204E", 325, 300)
                pygame.draw.line(screen,"white",(50,340),(320,340),5)
                pygame.draw.line(screen,"white",(960,340),(1180,340),5)

            elif gamestate["twoplayer"]:
                draw_board()
                pygame.draw.circle(screen,"#481E14",(600,350),200)
                draw_text(f' {c_score}', font, "#00FFD1", 570,200)
                draw_text(f' {p_score}', font, "#00FFD1",570,450)
                
                #draw_text(f'Ball Speed: {abs(pong.speed_x)}', font, TEXT_COLOR_PINK, 80, 50)
            
                draw_text('P              nG', font5, "#00FFD1", 325, 300)
                pygame.draw.line(screen,"white",(50,340),(320,340),5)
                pygame.draw.line(screen,"white",(960,340),(1180,340),5)
            player_paddle.draw()
            cpu_paddle.draw()
            if gamestate["oneplayer"]:
                cpu_paddle.ai()
            elif gamestate["twoplayer"]:
                cpu_paddle.move(pygame.K_UP, pygame.K_DOWN)
            player_paddle.move(pygame.K_w, pygame.K_s)

            if live_ball:
                winner = pong.move()
                if winner == 0:
                    pong.draw()
                else:
                    live_ball = False
                    if winner == 1:
                        p_score += 1
                    elif winner == -1:
                        c_score += 1
            else:
                if winner == 0:
                    draw_text('CLICK ANYWHERE TO START', font2, TEXT_COLOR_OLIVE, 450, 300)
                elif winner == 1:
                    if gamestate["oneplayer"]:
                        draw_text('CPU SCORED', font, "#FF204E", 462, 315)
                    elif gamestate["twoplayer"]:
                        draw_text('P 2 SCORED', font, "#00FFD1", 462, 315)
                    if p_score == 5:
                        if gamestate["oneplayer"]:
                            img = font4.render("CPU WON", True,"red")
                        elif gamestate["twoplayer"]:
                            img = font4.render("P 2 WON", True,"#00FFD1")
                        screen.blit(img, [478,370])
                        pygame.display.update() 
                        time.sleep(2)
                        gameactive = False     
                elif winner == -1:
                    draw_text('YOU SCORED', font, TEXT_COLOR_YELLOW, 462, 315)
                    if c_score == 5 :
                        draw_text('YOU WON', font4, "#00FFD1", 478, 370)
                        pygame.display.update() 
                        time.sleep(2)
                        gameactive = False
                
        pygame.display.update()
        handle_events()

game_loop()