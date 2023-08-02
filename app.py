import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 10
BALL_SPEED_X, BALL_SPEED_Y = 5, 5
WINNING_SCORE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

class Paddle:
    def _init_(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        

    def move_up(self):
        self.rect.y -= PADDLE_SPEED
        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self):
        self.rect.y += PADDLE_SPEED
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self):
        pygame.draw.rect(win, WHITE, self.rect)

    # ... (same as before)

class Ball:
    def _init_(self):
      self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
      self.speed_x = BALL_SPEED_X
      self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def check_collision(self, paddle):
        return self.rect.colliderect(paddle.rect)

    def change_direction(self):
        self.speed_x *= -1
    def reset(self):
        self.rect.x = WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = HEIGHT // 2 - BALL_SIZE // 2
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def draw(self):
        pygame.draw.rect(win, WHITE, self.rect)    


def display_winner(winner):
    font = pygame.font.Font(None, 70)
    text = font.render(f"{winner} wins!", True, WHITE)
    win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    paddle_left = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    paddle_right = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball()

    score_left = 0
    score_right = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle_left.move_up()
        if keys[pygame.K_s]:
            paddle_left.move_down()
        if keys[pygame.K_UP]:
            paddle_right.move_up()
        if keys[pygame.K_DOWN]:
            paddle_right.move_down()

        ball.move()

        if ball.check_collision(paddle_left) or ball.check_collision(paddle_right):
            ball.change_direction()

        if ball.rect.left <= 0:
            score_right += 1
            ball.reset()
        if ball.rect.right >= WIDTH:
            score_left += 1
            ball.reset()

        win.fill(BLACK)
        pygame.draw.rect(win, WHITE, (WIDTH // 2, 0, 2, HEIGHT))
        paddle_left.draw()
        paddle_right.draw()
        ball.draw()

        font = pygame.font.Font(None, 50)
        text_left = font.render(str(score_left), True, WHITE)
        text_right = font.render(str(score_right), True, WHITE)
        win.blit(text_left, (WIDTH // 4, 20))
        win.blit(text_right, (3 * WIDTH // 4 - text_right.get_width(), 20))

        pygame.display.update()
        clock.tick(60)

        if score_left >= WINNING_SCORE:
            display_winner("Player 1")
            break
        elif score_right >= WINNING_SCORE:
            display_winner("Player 2")
            break

if _name_ == "_main_":
    main()