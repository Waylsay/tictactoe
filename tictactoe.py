import pygame
import sys
import random

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
    
    # Запись данных 
    def update_board(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    # Проверка строк столбцов и диоганалей
    def is_winner(self, player):
        for i in range(self.size):
            if all([self.board[i][j] == player for j in range(self.size)]):
                return True
            if all([self.board[j][i] == player for j in range(self.size)]):
                return True
        if all([self.board[i][i] == player for i in range(self.size)]) or all([self.board[i][self.size - 1 - i] == player for i in range(self.size)]):
            return True
        return False
    
    # Проверка заполненности всех ячеек
    def is_full(self):
        return all([self.board[row][col] != ' ' for row in range(self.size) for col in range(self.size)])

class Game:
    def __init__(self, size):
        self.board = Board(size)
        self.current_player = 'X'
        self.size = size
        self.window_size = 300
        self.cell_size = self.window_size // size
        self.line_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.x_color = (0, 0, 255)
        self.o_color = (255, 0, 0)
        self.line_width = 5
        self.running = True
        self.result = None

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption('Крестики-нолики')
    
    # Рисуем доску
    def draw_board(self):
        self.screen.fill(self.bg_color)
        for row in range(1, self.size):
            pygame.draw.line(self.screen, self.line_color, (0, self.cell_size * row), (self.window_size, self.cell_size * row), self.line_width)
            pygame.draw.line(self.screen, self.line_color, (self.cell_size * row, 0), (self.cell_size * row, self.window_size), self.line_width)

    # Рисуем отметки игроков
    def draw_marks(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board.board[row][col] == 'X':
                    self.draw_x(row, col)
                elif self.board.board[row][col] == 'O':
                    self.draw_o(row, col)
    # Крестик
    def draw_x(self, row, col):
        start_pos = (col * self.cell_size, row * self.cell_size)
        end_pos = ((col + 1) * self.cell_size, (row + 1) * self.cell_size)
        pygame.draw.line(self.screen, self.x_color, start_pos, end_pos, self.line_width)
        start_pos = (col * self.cell_size, (row + 1) * self.cell_size)
        end_pos = ((col + 1) * self.cell_size, row * self.cell_size)
        pygame.draw.line(self.screen, self.x_color, start_pos, end_pos, self.line_width)
    # Нолик
    def draw_o(self, row, col):
        center = (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2)
        pygame.draw.circle(self.screen, self.o_color, center, self.cell_size // 2 - self.line_width, self.line_width)
    # Смена игрока
    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    # Проверка победы или ничьей
    def check_winner(self):
        if self.board.is_winner(self.current_player):
            self.result = f"Игрок {self.current_player} победил!"
            self.running = False
        elif self.board.is_full():
            self.result = "Ничья!"
            self.running = False
            

    def play(self):
        while self.running:
            # Ход компьютера
            if  self.current_player == 'O':
                        clicked_row = random.randint(0,grid_size-1)
                        clicked_col = random.randint(0,grid_size-1)
                        if self.board.update_board(clicked_row, clicked_col, self.current_player):
                            self.check_winner()
                            self.switch_player()
            # Ход игрока
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()      
                elif event.type == pygame.MOUSEBUTTONDOWN and self.running:
                    mouseX, mouseY = event.pos                     
                    clicked_row = mouseY // self.cell_size
                    clicked_col = mouseX // self.cell_size                    
                    if self.board.update_board(clicked_row, clicked_col, self.current_player):
                        self.check_winner()
                        self.switch_player()
            
            self.draw_board()
            self.draw_marks()
            pygame.display.flip()
        
        self.show_result()

    def show_result(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.screen.fill(self.bg_color)
            font = pygame.font.Font(None, 36)
            text = font.render(self.result, True, (0, 0, 0))
            text_info = font.render('нажмите Enter', True, (0, 0, 0))
            self.screen.blit(text, (self.window_size // 2 - text.get_width() // 2, self.window_size // 2 - text.get_height() // 2))
            self.screen.blit(text_info, (60, 180))
            pygame.display.flip()

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((300, 300))
        pygame.display.set_caption('Крестики-нолики')
        self.font = pygame.font.Font(None, 36)
        self.running = True
    
    # Выбор размера сетки игроком
    def draw_menu(self):
        self.screen.fill((255, 255, 255))
        menu_text = self.font.render('Выберете размер сетки', True, (0, 0, 0))
        menu_1 = self.font.render('3x3', True, (0, 0, 0))
        menu_2 = self.font.render('4x4', True, (0, 0, 0))
        menu_3 = self.font.render('5x5', True, (0, 0, 0))
        menu_4 = self.font.render('Выход', True, (255, 0, 0))
        self.screen.blit(menu_text, (10, 30))
        self.screen.blit(menu_1, (120, 80))
        self.screen.blit(menu_2, (120, 130))
        self.screen.blit(menu_3, (120, 180))
        self.screen.blit(menu_4, (100, 230))
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Проверка выбора размера сетки игроком
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    if 100 <= mouseX <= 180:
                        if 80 <= mouseY <= 110:
                            self.running = False
                            return 3
                        elif 130 <= mouseY <= 160:
                            self.running = False
                            return 4
                        elif 180 <= mouseY <= 210:
                            self.running = False
                            return 5
                        elif 230 <= mouseY <= 260:
                            pygame.quit()
                            sys.exit() 
            self.draw_menu()

if __name__ == "__main__":
    while True:
        menu = Menu()
        grid_size = menu.run()
        game = Game(grid_size)
        game.play()
