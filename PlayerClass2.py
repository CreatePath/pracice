import pygame
# 클래스/함수 정의
# 텍스트 입력창 클래스
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

# 버튼 클래스
class Button:
    def __init__(self, x, y, w, h, text_color, color, text=''):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.text_color = text_color
        self.color = color
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text = FONT.render(self.text, True, self.text_color)
        screen.blit(text, (self.rect.x, self.rect.y+BUTTON_HEIGHT/2))
    
    def collidepoint(self, pos):
        if self.rect.collidepoint(pos):
            return True


# 시작 화면
def draw_start_screen():
    global buttons
    # 바둑판 그리기
    pygame.draw.rect(screen, BROWN, [0,0,BOARD_SIZE,BOARD_SIZE])
    for y in range(19):
        pygame.draw.line(screen, BLACK, (GAP,y*CELL_SIZE+GAP), (BOARD_SIZE+GAP-CELL_SIZE, y*CELL_SIZE+GAP))
    for x in range(19):
        pygame.draw.line(screen, BLACK, (x*CELL_SIZE + GAP, GAP), (x*CELL_SIZE+GAP, BOARD_SIZE+GAP-CELL_SIZE))
    for x in [3,9,15]:
        for y in [3,9,15]:
            pygame.draw.circle(screen, BLACK, (x*CELL_SIZE + GAP,y*CELL_SIZE+GAP), 5)
    # 대국자 정보 
    pygame.draw.rect(screen, BLACK, [BOARD_SIZE, 0, PLAYER_WIDTH, INFO_HEIGHT])
    pygame.draw.rect(screen, WHITE, [BOARD_SIZE, INFO_HEIGHT, PLAYER_WIDTH, INFO_HEIGHT])
    text = FONT.render('Captured Stone: {0}'.format(CAPTURED), True, BROWN)
    screen.blit(text, (BOARD_SIZE, PLAYER_HEIGHT))
    screen.blit(text, (BOARD_SIZE, INFO_HEIGHT + PLAYER_HEIGHT))
    for i in inputbox:
        i.draw(screen)
    if START == 0:
        for button in buttons:
            button.draw()
    else:
        if start in buttons:
            buttons.pop()
        if giveup not in buttons:
            buttons.append(giveup)
        for button in buttons:
            button.draw()

# timer class
class Timer:
    def __init__(self, min, sec, pos, color=(255,255,255)):
        self.min = min
        self.sec = sec
        self.color = color
        self.pos = pos
        self.time_txt = FONT.render('{0}:{1}'.format(self.min, int(self.sec)), True, self.color)

    def time_running(self):
        global running, players, START
        start_time = pygame.time.get_ticks()
        time_run = True
        while time_run:
            elapsed_sec = (pygame.time.get_ticks()-start_time)/1000
            curr_sec = self.sec - elapsed_sec
            if self.min <= 0 and curr_sec <= 0:
                running = False
                break
            elif curr_sec <= 0:
                self.min -= 1
                start_time = pygame.time.get_ticks()
                self.sec = 60
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if giveup.collidepoint(event.pos):
                        self.sec = curr_sec
                        time_run = False
                        if TOTAL_NUM%2 == 1:
                            result_txt = FONT.render("Black Wins Without Counting!!", True, BLACK, WHITE)
                            rect = result_txt.get_rect(center=(screen_width/2,screen_height/2))
                        else:
                            result_txt = FONT.render("White Wins Without Counting!!", True, WHITE, BLACK)
                            rect = result_txt.get_rect(center=(screen_width/2,screen_height/2))
                        screen.blit(result_txt, rect)
                        running = False
                        START = 0
                        break
            if running == False:
                START = 0
                break
            self.time_txt = FONT.render('{0}:{1}'.format(self.min, int(curr_sec)), True, self.color)
            draw_start_screen()
            for player in players:
                screen.blit(player.time_txt, (player.pos))
            pygame.display.update() 

# 흑/백 사용자 클래스
class Player(Timer):
    def __init__(self, min, sec, pos, color=(255, 255, 255)):
        super().__init__(min, sec, pos, color)

    def turn(self):
        self.time_running()
        
    def placement(self, pos):
        pass

# pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 1200
screen_height = 760
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 이름
pygame.display.set_caption('바둑')

# 전역 변수 설정
# color
BLUE = (0,204,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
BROWN = (255,153,0)
RED = (255,0,51)
MINT = (0,255,204)

# board
GAP = 20
CELL_SIZE = 40
BOARD_SIZE = 760

# button size
INFO_HEIGHT = 280
PLAYER_WIDTH = 440
PLAYER_HEIGHT = 40
BUTTON_WIDTH = 145
BUTTON_HEIGHT = 200
GIVEUP_WIDTH = 150

# inputbox color
COLOR_INACTIVE = BLUE
COLOR_ACTIVE = MINT
FONT = pygame.font.Font(None, 40)

# 사석
CAPTURED = 0

# 시작할때 변수. 시작 전 = 0, 시작 후 = 1
START = 0

# 총 수순
TOTAL_NUM = 1

# 바둑판 데이터
map = [[0 for i in range(19)] for j in range(19)]

# 대국자 정보 입력창
p1 = InputBox(BOARD_SIZE, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 'BLACK: ')
p2 = InputBox(BOARD_SIZE, INFO_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, 'WHITE: ')
inputbox = [p1,p2]

# 계가/무르기/시작,기권 버튼 생성
counting = Button(BOARD_SIZE, screen_height-BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, BLUE, 'Counting')
move_back = Button(BOARD_SIZE+BUTTON_WIDTH, screen_height-BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, MINT, 'Move Back')
start = Button(screen_width-GIVEUP_WIDTH, screen_height-BUTTON_HEIGHT, GIVEUP_WIDTH, BUTTON_HEIGHT, RED, BLACK, 'Start')
giveup = Button(screen_width-GIVEUP_WIDTH, screen_height-BUTTON_HEIGHT, GIVEUP_WIDTH, BUTTON_HEIGHT, RED, BLACK, 'Give Up')
buttons = [counting, move_back, start]

# player class 호출
black = Player(10,0, (BOARD_SIZE,PLAYER_HEIGHT+40), WHITE)
white = Player(10,0, (BOARD_SIZE,INFO_HEIGHT+PLAYER_HEIGHT+40), BLACK)
players =[black, white]

# 이벤트 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for i in inputbox:
            if START == 0:
                i.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if START == 0:
                if start.collidepoint(event.pos):
                    START = 1

    draw_start_screen()
    while START == 1:
        black.turn()
        white.turn()

    pygame.display.update()

#pygame 종료
pygame.time.delay(2000)
pygame.quit()