import pygame, queue
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
        TS_txt1 = FONT.render('{}min'.format(self.min), True, BLACK, self.color)
        TS_txt2 = FONT.render('{}sec'.format(self.sec), True, BLACK, self.color)
        TS_txt3 = FONT.render('x {}'.format(self.time), True, BLACK, self.color)
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

def makemap():
    map = [[0 for i in range(21)] for k in range(21)]
    for y in [0,20]:
        for x in range(21):
            map[y][x] = 'x'; map[x][y] = 'x'
    return map

# 격자점에 사각형 그리기
def draw_grid():
    for x in range(19):
        for y in range(19):
            center_x = GAP + x*CELL_SIZE
            center_y = GAP + y*CELL_SIZE
            grid_rect = pygame.Rect(0,0,40,40)
            grid_rect.center = (center_x, center_y)
            grid_rects.append(grid_rect)
            # pygame.draw.rect(screen, BLACK, grid_rect, 5)

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
                self.time_txt = FONT.render('{0}:{1}   {2}times'\
                    .format(self.min, int(curr_sec), self.chance), True, self.clk_color)
                if self.chance == 0:
                    result_txt = FONT.render("{0} Time Over! {1} Wins!!".format(self.name, self.opp.name),\
                        True, self.opp.color, BLUE)
                    rect = result_txt.get_rect(center=(screen_width/2,screen_height/2))
                    screen.blit(result_txt, rect)
                    START = 0
                    running = False
                    break
                self.sec = self.o_sec
                if curr_sec <= 0.01:
                    self.chance -= 1
                    start_time = pygame.time.get_ticks()
            else:
                self.time_txt = FONT.render('{0}:{1}'.format(self.min, int(curr_sec)), True, self.clk_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    START = 0
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if giveup.collidepoint(event.pos):
                        time_run = False
                        result_txt = FONT.render("{0} Wins Without Counting!!".format(self.opp.name), True, self.opp.color, BLUE)
                        rect = result_txt.get_rect(center=(screen_width/2,screen_height/2))
                        screen.blit(result_txt, rect)
                        START = 0
                        break
                    for grid_rect in grid_rects:
                        if grid_rect.collidepoint(event.pos):
                            pos = grid_rect.center
                            x = (pos[0] - GAP)/CELL_SIZE
                            y = (pos[1] - GAP)/CELL_SIZE
                            if map[int(y+1)][int(x+1)] == 0 or\
                                map[int(y+1)][int(x+1)] == -self.num:
                                self.sec = curr_sec
                                time_run = False
                                self.placement(int(x+1), int(y+1), pos)
                            elif map[int(y+1)][int(x+1)] == self.num*(-1): break
                            break
                    else: break
                if time_run == False:
                    break
            if START == 0:
                running = False
                break
            draw_start_screen()
            draw_grid()
            for player in players:
                screen.blit(player.capture_txt, player.capture_pos)
                screen.blit(player.time_txt, (player.pos))
                for position in player.stones:
                    pygame.draw.circle(screen, player.color, position, 15)
            pygame.display.update() 

# 흑/백 대국자 클래스
class Player(Timer):
    def __init__(self, min, sec, over_sec, chance, pos, num, color, clock_color, capture_pos, name):
        super().__init__(min, sec, over_sec, chance, pos, color, clock_color)
        self.name = name    
        self.stones = []
        self.killed = []
        self.alive = []
        self.num = num
        self.over_counting = None
        self.q = queue.LifoQueue()
        self.capture = 0
        self.capture_txt = FONT.render('Captured Stone: {0}'.format(self.capture), True, BROWN)
        self.capture_pos = capture_pos
        self.opp = None
        self.map = makemap()
        
    def placement(self, x, y, pos):
        global map
        # print("before placement:\n",map)
        map[y][x] = self.num
        self.stones.append(pos)
        self.find_num(x,y)
        self.restore()
        self.remove_stones()
        self.capture += len(self.killed)
        self.capture_txt = FONT.render('Captured Stone: {0}'.format(self.capture), True, BROWN)
        self.check_ko((x,y))
        for player in players:
            player.check_place()
        for player in players:
            player.check_place2()
        for (a,b) in ko_pos:
            map[b][a] = -self.num
        # print("after placement:\n", map, "\nko_pos:", ko_pos)

    def isValid(self,x,y):
        global map
        if map[y][x] == self.num or map[y][x] == 'x' : return False # self.num, 'x'
        elif map[y][x] == 0 or map[y][x] == -1 or map[y][x] == -2\
             or map[y][x] == self.opp.num: return True   # 0, self.opp.num

    def check_death(self, result=True):
        global map
        for row_idx, row in enumerate(map):
            for col_idx, col in enumerate(row):
                if result == True:
                    if col == '.' :
                        self.alive.append((col_idx, row_idx)); map[row_idx][col_idx] = 'a'
                else:
                    if col == '.' : 
                        self.killed.append((col_idx, row_idx)); map[row_idx][col_idx] = 'd'

    def check_Liberty(self, pos=None):  # False: 따먹힘 True: 살아있음.
        global map
        if pos:
            self.q.put(pos)
        while self.q.qsize() != 0:
            here = self.q.get()
            (a,b) = here
            if map[b][a] == 0 or map[b][a] == -1 or map[b][a] == -2 : return True
            else:
                map[b][a] = '.'
                if self.isValid(a,b+1) : self.q.put((a,b+1))
                if self.isValid(a,b-1) : self.q.put((a,b-1))
                if self.isValid(a+1,b) : self.q.put((a+1,b))
                if self.isValid(a-1,b) : self.q.put((a-1,b))
        return False

    def find_num(self,x,y):
        for (a,b) in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
            if map[b][a] == self.opp.num:
                self.q = queue.LifoQueue()
                result = self.check_Liberty((a,b))
                self.check_death(result)

    def restore(self):
        global map
        for (x,y) in self.killed:
            map[y][x] = 0
        for (x,y) in self.alive:
            map[y][x] = self.opp.num

    def remove_stones(self):
        if len(self.killed) != 0:
            for (x,y) in self.killed:
                pos = (GAP+(x-1)*CELL_SIZE, GAP+(y-1)*CELL_SIZE)
                for player in players:
                    if pos in player.stones:
                        player.stones.remove(pos)

    def check_ko(self, pos):
        global map, ko_pos
        ko_pos = []
        if len(self.killed) == 1:
            for (x,y) in self.killed:
                map[y][x] = self.opp.num
                self.opp.q = queue.LifoQueue()
                if not self.opp.check_Liberty((pos[0], pos[1])):
                    self.opp.check_death()
                    if len(self.opp.alive) == 1:
                        ko_pos.append((x,y))
                else:
                    self.opp.check_death()
                map[y][x] = 0
                self.opp.restore()
                self.opp.dead = []; self.opp.alive = []      


    # 착수 금지 : 0 인 곳에 두면 곧바로 죽는 경우
    # 착수 금지 풀기 : 1. 다른 곳에 활로가 생겨 둘 수 있게 된 경우                
    def check_place(self):
        global map
        self.killed = []; self.alive = []
        for row_idx, row in enumerate(map):
            for col_idx, col in enumerate(row):
                if col == 0 or col == -self.num:
                    self.q = queue.LifoQueue()
                    map[row_idx][col_idx] = self.opp.num
                    if not self.check_Liberty((col_idx, row_idx)):
                        map[row_idx][col_idx] = -self.num
                    else:
                        map[row_idx][col_idx] = 0
                self.check_death()
                self.restore()
                        
    # 착수 금지 풀기 : 2. 돌을 따낼 수 있는 경우
    def check_place2(self):
        global map
        self.killed = []; self.alive = []
        for row_idx, row in enumerate(map):
            for col_idx, col in enumerate(row):
                if col == -(self.opp.num):
                    for (x,y) in [(col_idx+1,row_idx), (col_idx-1,row_idx),\
                        (col_idx,row_idx+1), (col_idx,row_idx-1)]:
                        map[row_idx][col_idx] = self.num
                        if map[y][x] == self.opp.num:
                            self.q = queue.LifoQueue()
                            if self.check_Liberty((x,y)):
                                self.check_death()
                                self.restore()
                                self.killed = []; self.alive = []
                            else:
                                map[row_idx][col_idx] = 0
                                self.check_death()
                                self.restore()
                                self.killed = []; self.alive = []
                                break
                        map[row_idx][col_idx] = -(self.opp.num)  

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

# game font
FONT = pygame.font.Font(None, 40)

# 사석
CAPTURED = 0

# 시작할때 변수. 시작 전 = 0, 시작 후 = 1
START = 0
TOTAL_NUM = 0

# 바둑판 데이터
map = makemap()
grid_rects=[]

# 패싸움 위치 저장
ko_pos = []

# 대국자 클래스 저장 리스트
players = []

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
                        black = Player(sel[0],0, sel[1], sel[2], (BOARD_SIZE,PLAYER_HEIGHT+40), 1, BLACK, WHITE, (BOARD_SIZE,PLAYER_HEIGHT), "Black")
                        white = Player(sel[0],0, sel[1], sel[2], (BOARD_SIZE,INFO_HEIGHT+PLAYER_HEIGHT+40), 2, WHITE, BLACK, (BOARD_SIZE, INFO_HEIGHT+PLAYER_HEIGHT), "White")
                        players =[black, white]
                        black.opp = white
                        white.opp = black
                        ts = True
                if start.collidepoint(event.pos):
                    if ts == True:
                        START = 1

    draw_start_screen()
    while START == 1:
        black.time_running()
        if START != 1: break
        white.time_running()

    pygame.display.update()

#pygame 종료
pygame.time.delay(5000)
pygame.quit()