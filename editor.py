import pygame
a = input('Начало есть?')
lvl = False
if a != '0':
    lvl = str(open(a, encoding="utf-8").read().strip()).split('\n')

    for el in range(len(lvl)):
        lvl[el] = lvl[el].split(', ')


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 20
        self.top = 20
        self.cell_size = 20

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, scr):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(scr, pygame.Color(255, 255, 255),
                                 (x * self.cell_size, y * self.cell_size,  self.cell_size,
                                  self.cell_size), 1)

    def render_rects(self):
        for y in range(40):
            for x in range(40):
                if str(self.board[y][x]).strip() == 'FLOOR':
                    pygame.draw.rect(screen, pygame.Color(255, 255, 255), (int(x) * 20, int(y) * 20, 20, 20), 0)
                elif str(self.board[y][x]).strip() == 'TRAP':
                    pygame.draw.rect(screen, pygame.Color(255, 0, 0), (int(x) * 20, int(y) * 20, 20, 20), 0)
                elif str(self.board[y][x]).strip() == 'EXIT':
                    pygame.draw.rect(screen, pygame.Color(0, 255, 0), (int(x) * 20, int(y) * 20, 20, 20), 0)

    def get_coords(self):
        self.x, self.y = event.pos
        return (self.x // self.cell_size, self.y // self.cell_size)


board = Board(40, 40)
if lvl:
    board.board = lvl

size = width, height = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Инициализация игры')
running = True
while running:
    for event in pygame.event.get():
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(board.get_coords())

        if event.type == pygame.MOUSEMOTION:
            x, y = board.get_coords()
        if keys[pygame.K_1]:
            board.board[y][x] = 'FLOOR'
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), (int(x) * 20, int(y) * 20, 20, 20), 0)
            print(x, y)
        elif keys[pygame.K_2]:
            board.board[y][x] = 'TRAP'
            pygame.draw.rect(screen, pygame.Color(255, 0, 0),
                             (x * board.cell_size, + y * board.cell_size, board.cell_size,
                              board.cell_size), 0)
        elif keys[pygame.K_3]:
            board.board[y][x] = 'EXIT'
            pygame.draw.rect(screen, pygame.Color(0, 255, 0),
                             (x * board.cell_size, + y * board.cell_size, board.cell_size,
                              board.cell_size), 0)
        elif keys[pygame.K_BACKSPACE]:
            board.board[y][x] = 0
    board.render_rects()
    board.render(screen)
    pygame.display.flip()

pygame.quit()

f = open(input(), encoding='utf-8', mode='w')
for i in board.board:
    print(str(i).replace(']', ' ').replace('[', ' '), file=f)
