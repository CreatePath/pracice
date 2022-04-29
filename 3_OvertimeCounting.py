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

# 제한시간 선택 박스 클래스
class TS:
    def __init__(self, min, sec, time, color):
        self.min = min
        self.sec = sec
        self.time = time
        self.color = color

    def TS_draw(self, pos):
        TS_txt1 = FONT.render('{}min'.format(self.min), True, BLACK)
        TS_txt2 = FONT.render('{}sec'.format(self.sec), True, BLACK)
        TS_txt3 = FONT.render('x {}'.format(self.time), True, BLACK)
        self.rect = pygame.Rect(0,0,100,200)
        self.rect.center = pos
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(TS_txt1, (pos[0]-50+5, pos[1]-50))
        screen.blit(TS_txt2, (pos[0]-50+5, pos[1]-50+40))
        screen.blit(TS_txt3, (pos[0]-50+5, pos[1]-50+80))

    def time_select(self):
        return (self.min, self.sec, self.time)

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
        if ts == False:
            TS1.TS_draw((screen_width/2 - 100, screen_height/2))
            TS2.TS_draw((screen_width/2, screen_height/2))
            TS3.TS_draw((screen_width/2 + 100, screen_height/2))
        for button in buttons:
            button.draw()
    else:
        if start in buttons:
            buttons.pop()
        if giveup not in buttons:
            buttons.append(giveup)
        for button in buttons:
            button.draw()

# 격자점에 사각형 그리기
def draw_grid():
    for x in range(19):
        for y in range(19):
            center_x = GAP + x*CELL_SIZE
            center_y = GAP + y*CELL_SIZE
            grid_rect = pygame.Rect(0,0,30,30)
            grid_rect.center = (center_x, center_y)
            grid_rects.append(grid_rect)
            # pygame.draw.rect(screen, BLACK, grid_rect)

# timer class
class Timer:
    def __init__(self, min, sec, over_sec, chance, pos, color, clock_color):
        self.min = min
        self.sec = sec
        self.o_sec = over_sec
        self.chance = chance
        self.color = color
        self.clk_color = clock_color
        self.pos = pos
        self.time_txt = FONT.render('{0}:{1}'.format(self.min, int(self.sec)), True, self.clk_color)

    def time_running(self):
        global running, players, START
        start_time = pygame.time.get_ticks()
        time_run = True
        while time_run:
            elapsed_sec = (pygame.time.get_ticks()-start_time)/1000
            curr_sec = self.sec - elapsed_sec
            if self.min <= 0 and curr_sec <= 0:
                self.over_counting = True
                self.sec = self.o_sec
                start_time = pygame.time.get_ticks()
                self.min = 0
                continue
            elif curr_sec <= 0:
                self.min -= 1
                start_time = pygame.time.get_ticks()
                self.sec = 60
            if self.over_counting:
                if self.chance == 0:
                    if TOTAL_NUM%2 == 1:
                        result_txt = FONT.render("White Time Over! Black Wins!!", True, BLACK, BLUE)
                        rect = result_txt.get_rect(center=(screen_width/2,screen_height/2))
                    else:
                        result_txt = FONT.render("Black Time Over! White Wins", True, WHITE, BLUE)
                        rect = result_txt.get_rect(center=(screen_width/2,screen_height/2))
                    screen.blit(result_txt, rect)
                    running = False
                    START = 0
                    break
                self.sec = self.o_sec
                if curr_sec <= 0.001:
                    self.chance -= 1
                    start_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if giveup.collidepoint(event.pos):
                        self.sec = curr_sec
                        time_run = False
                        if TOTAL_NUM%2 == 1:
                            result_txt = FONT.render("Black Wins Without Counting!!", True, BLACK, BLUE)
                            rect = result_txt.get_rect(center=(screen_width/2,screen_height/2))
                        else:
                            result_txt = FONT.render("White Wins Without Counting!!", True, WHITE, BLUE)
                            rect = result_txt.get_rect(center=(screen_width/2,screen_height/2))
                        screen.blit(result_txt, rect)
                        running = False
                        break
                    for grid_rect in grid_rects:
                        if grid_rect.collidepoint(event.pos):
                            pos = grid_rect.center
                            x = (pos[0] - GAP)/CELL_SIZE
                            y = (pos[1] - GAP)/CELL_SIZE
                            # print(x,y) # 좌표값 입력 제대로 되는지 체크
                            if map[int(y)][int(x)] == 0:
                                # print(map[int(y)][int(x)])
                                self.placement(x, y, pos)
                                # print(map[int(y)][int(x)]) # 착수가 제대로 이루어 졌는지 체크
                                self.sec = curr_sec
                                time_run = False
                            break
                if time_run == False:
                    break
            if running == False:
                START = 0
                break
            if self.over_counting:
                self.time_txt = FONT.render('{0}:{1}   {2}times'.format(self.min, int(curr_sec), self.chance), True, self.clk_color)
            else:
                self.time_txt = FONT.render('{0}:{1}'.format(self.min, int(curr_sec)), True, self.clk_color)
            draw_start_screen()
            draw_grid()
            for player in players:
                screen.blit(player.time_txt, (player.pos))
                for position in player.stones:
                    pygame.draw.circle(screen, player.color, position, 15)
            pygame.display.update() 

# 흑/백 사용자 클래스
class Player(Timer):
    def __init__(self, min, sec, over_sec, chance, pos, num, color, clock_color):
        super().__init__(min, sec, over_sec, chance, pos, color, clock_color)
        self.stones = []
        self.num = num
        self.over_counting = None

    def turn(self):
        self.time_running()
        
    def placement(self, x, y, pos):
        global TOTAL_NUM, map
        map[int(y)][int(x)] = self.num
        self.stones.append(pos)
        TOTAL_NUM += 1
        print(map)
        
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

# time select
ts = False
TS1 = TS(30,30,3,RED)
TS2 = TS(10,20,3,MINT)
TS3 = TS(5,20,2,BLUE)
ts_lst = [TS1, TS2, TS3]

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
TOTAL_NUM = 0

# 바둑판 데이터
map = [[0 for i in range(19)] for j in range(19)]
grid_rects=[]

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
                for tsBox in ts_lst:
                    if tsBox.rect.collidepoint(event.pos):
                        sel = tsBox.time_select()
                        black = Player(sel[0],0, sel[1], sel[2], (BOARD_SIZE,PLAYER_HEIGHT+40), 1, BLACK, WHITE)
                        white = Player(sel[0],0, sel[1], sel[2], (BOARD_SIZE,INFO_HEIGHT+PLAYER_HEIGHT+40), 2, WHITE, BLACK)
                        players =[black, white]
                        ts = True
                if start.collidepoint(event.pos):
                    if ts:
                        START = 1

    draw_start_screen()
    while START == 1:
        black.turn()
        # print('a') # 턴이 잘 넘어가는지 확인.
        white.turn()

    pygame.display.update()

#pygame 종료
pygame.time.delay(2000)
pygame.quit()