import pygame
import sys
import random
from pygame.math import Vector2


class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback
        self.font = pygame.font.Font(None, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0),
                         (self.x, self.y, self.width, self.height), 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(-1, 0)
        self.new_block = False
        self.high_scores = []

    def draw(self, screen, top_bar_height):
        for block in self.body:
            block_rect = pygame.Rect(
                block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move(self):
        if self.new_block:
            self.body.insert(0, self.body[0] + self.direction)
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def add_block(self):
        self.new_block = True


class Food:
    def __init__(self):
        self.position = Vector2(random.randint(
            0, cell_number - 1), random.randint(0, cell_number - 1))

    def draw(self, screen, top_bar_height):

        food_rect = pygame.Rect(
            self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), food_rect)


class Star:
    def __init__(self):
        self.position = Vector2(-1, -1)  # Initialize the star off-screen
        self.active = False
        self.timer = 0

    def draw(self, screen, top_bar_height):
        if self.active:
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(
                self.position.x * cell_size, self.position.y * cell_size + top_bar_height, cell_size, cell_size))

    def new_position(self):
        self.position = Vector2(random.randint(
            0, cell_number - 1), random.randint(0, cell_number - 1))


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (cell_number * cell_size, cell_number * cell_size))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.game_state = "menu"
        self.high_scores = []
        self.top_bar_height = 30

    def run(self):
        self.is_game_over = False  # 이 변수를 추가하세요.
        while True:
            if self.game_state == "menu":
                self.show_menu()
            elif self.game_state == "game":
                self.handle_input()
                if not self.is_game_over:
                    self.snake.move()
                    self.check_collision()
                    self.check_fail()
                self.draw_elements()

                if self.is_game_over:
                    self.show_game_over_screen()  # 게임 오버 화면 추가
                pygame.display.flip()
                self.clock.tick(10)
            elif self.game_state == "high_scores":
                self.show_high_scores()

    def draw_elements(self):
        self.screen.fill((175, 215, 70))

        # Add this part to create a top bar and display the score on it
        top_bar_height = 30
        top_bar = pygame.Surface(
            (cell_number * cell_size, self.top_bar_height))
        top_bar.fill((0, 0, 0))

        score_font = pygame.font.Font(None, 25)
        score_surface = score_font.render(
            f"Score: {len(self.snake.body) - 3}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(midleft=(20, top_bar_height // 2))
        top_bar.blit(score_surface, score_rect)

        self.screen.blit(top_bar, (0, 0))

        # Update the snake and food draw methods to account for the top bar
        self.snake.draw(self.screen, self.top_bar_height)
        self.food.draw(self.screen, self.top_bar_height)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "menu"
                if event.key == pygame.K_SPACE and self.is_game_over:
                    self.snake = Snake()
                    self.food = Food()
                    self.is_game_over = False
                if event.key == pygame.K_UP:
                    if self.snake.direction.y != 1:
                        self.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if self.snake.direction.y != -1:
                        self.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    if self.snake.direction.x != 1:
                        self.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT:
                    if self.snake.direction.x != -1:
                        self.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_h and self.is_game_over:
                    self.show_high_scores()

    def show_menu(self):
        start_button = Button("Start Game", cell_number * cell_size / 4, cell_number *
                              cell_size / 2, cell_number * cell_size / 2, cell_size, self.start_game)
        high_scores_button = Button("High Scores", cell_number * cell_size / 4, cell_number *
                                    cell_size * 3 / 4, cell_number * cell_size / 2, cell_size, self.show_high_scores)

        while self.game_state == "menu":
            self.screen.fill((175, 215, 70))
            start_button.draw(self.screen)
            high_scores_button.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.is_clicked(mouse_pos):
                        start_button.callback()
                    if high_scores_button.is_clicked(mouse_pos):
                        high_scores_button.callback()

    def check_collision(self):
        if self.snake.body[0] == self.food.position:
            self.snake.add_block()
            self.food = Food()
        for block in self.snake.body[1:]:
            if block == self.food.position:
                self.food = Food()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.is_game_over = True
        score = len(self.snake.body) - 3
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)

    def show_game_over_screen(self):
        game_over_font = pygame.font.Font(None, 50)
        game_over_surface = game_over_font.render("Game Over", True, (0, 0, 0))
        game_over_rect = game_over_surface.get_rect(
            center=(cell_number * cell_size / 2, cell_number * cell_size / 4))
        self.screen.blit(game_over_surface, game_over_rect)

        restart_font = pygame.font.Font(None, 30)
        restart_surface = restart_font.render(
            "Press SPACE to restart", True, (0, 0, 0))
        restart_rect = restart_surface.get_rect(
            center=(cell_number * cell_size / 2, cell_number * cell_size * 3 / 8))
        self.screen.blit(restart_surface, restart_rect)

        score_font = pygame.font.Font(None, 40)
        score_surface = score_font.render(
            f"Score: {len(self.snake.body) - 3}", True, (0, 0, 0))
        score_rect = score_surface.get_rect(
            center=(cell_number * cell_size / 2, cell_number * cell_size / 2))
        self.screen.blit(score_surface, score_rect)

        back_to_menu_font = pygame.font.Font(None, 30)
        back_to_menu_surface = back_to_menu_font.render(
            "Press ESC to return to menu", True, (0, 0, 0))
        back_to_menu_rect = back_to_menu_surface.get_rect(
            center=(cell_number * cell_size / 2, cell_number * cell_size * 5 / 8))
        self.screen.blit(back_to_menu_surface, back_to_menu_rect)

        high_scores_font = pygame.font.Font(None, 30)
        high_scores_surface = high_scores_font.render(
            "Press H to see High Scores", True, (0, 0, 0))
        high_scores_rect = high_scores_surface.get_rect(
            center=(cell_number * cell_size / 2, cell_number * cell_size * 3 / 4))
        self.screen.blit(high_scores_surface, high_scores_rect)

    def start_game(self):
        self.snake = Snake()
        self.food = Food()
        self.is_game_over = False
        self.game_state = "game"

    def show_high_scores(self):
        self.game_state = "high_scores"

        while self.game_state == "high_scores":
            self.screen.fill((175, 215, 70))
            title_font = pygame.font.Font(None, 50)
            title_surface = title_font.render("High Scores", True, (0, 0, 0))
            title_rect = title_surface.get_rect(
                center=(cell_number * cell_size / 2, cell_number * cell_size / 6))
            self.screen.blit(title_surface, title_rect)

            for i, score in enumerate(self.high_scores[:5]):
                score_font = pygame.font.Font(None, 30)
                score_surface = score_font.render(
                    f"{i + 1}. {score}", True, (0, 0, 0))
                score_rect = score_surface.get_rect(
                    center=(cell_number * cell_size / 2, cell_number * cell_size * (i + 2) / 6))
                self.screen.blit(score_surface, score_rect)

            back_to_menu_font = pygame.font.Font(None, 30)
            back_to_menu_surface = back_to_menu_font.render(
                "Press ESC to return to menu", True, (0, 0, 0))
            back_to_menu_rect = back_to_menu_surface.get_rect(
                center=(cell_number * cell_size / 2, cell_number * cell_size * 5 / 6))
            self.screen.blit(back_to_menu_surface, back_to_menu_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game_state = "menu"

        pygame.display.flip()
        pygame.time.delay(7000)


cell_size = 30
cell_number = 20

game = Game()
game.run()
