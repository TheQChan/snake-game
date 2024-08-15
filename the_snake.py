from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()

"""Базовый класс"""


class GameObject:
    """Инициальзация"""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Метод для отрисовки"""
        pass


"""Производный класс яблоко"""


class Apple(GameObject):
    """Инициализация"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Случайная позиция для яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * 20,
            randint(0, GRID_HEIGHT - 1) * 20,
        )

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


"""Производный класс змея"""


class Snake(GameObject):
    """Инициализация"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, eat_flag):
        """Обновление позиции змеи и её удлинение"""
        self.positions.insert(
            0,
            (
                self.positions[0][0] + self.direction[0] * 20,
                self.positions[0][1] + self.direction[1] * 20,
            ),
        )
        position = self.positions[0]
        if position[0] >= SCREEN_WIDTH:
            position = (position[0] - SCREEN_WIDTH, position[1])
        elif position[0] < 0:
            position = (position[0] + SCREEN_WIDTH, position[1])
        elif position[1] < 0:
            position = (position[0], position[1] + SCREEN_HEIGHT)
        elif position[1] >= SCREEN_HEIGHT:
            position = (position[0], position[1] - SCREEN_HEIGHT)
        self.positions[0] = position
        if not eat_flag:
            self.last = self.positions[-1]
            self.positions.pop(-1)

    def draw(self):
        """Отрисовка змеи"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            if type(self.last) is list:
                for last in self.last:
                    last_rect = pygame.Rect(last, (GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            else:
                last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Геттер для головы змеи"""
        return self.positions[0]

    def reset(self):
        """Возврощение змеи к исходному состоянию"""
        self.last = self.positions
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Обработка действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    apple.randomize_position()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        if apple.position == snake.get_head_position():
            apple.randomize_position()
            snake.move(True)
        else:
            snake.move(False)
        if snake.get_head_position() in snake.positions[1:-1]:
            print(snake.positions)
            print(snake.get_head_position())
            snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
