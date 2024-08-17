from random import randint
import pygame as pg

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля и клавиша завершения:
pg.display.set_caption("Змейка. Нажмите ESC для выхода.")

# Настройка времени:
clock = pg.time.Clock()

# Словарь поворотов
TURNS = {
    (pg.K_UP, RIGHT): UP,
    (pg.K_UP, LEFT): UP,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT,
}

"""Базовый класс"""


class GameObject:
    """Инициальзация"""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw_cell(self):
        """Отрисовка клетки"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

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
        self.draw_cell()


"""Производный класс змея"""


class Snake(GameObject):
    """Инициализация"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def update_direction(self, next_direction):
        """Метод обновления направления после нажатия на кнопку"""
        if next_direction:
            self.direction = next_direction

    def move(self):
        """Обновление позиции змеи и её удлинение"""
        x, y = self.positions[0][0], self.positions[0][1]
        self.positions.insert(
            0,
            (
                (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
            ),
        )
        self.last = self.positions[-1]
        self.positions.pop(-1)

    def draw(self):
        """Отрисовка змеи"""
        for position in self.positions[:-1]:
            self.position = position
            self.draw_cell()

        # Отрисовка головы змейки
        self.position = self.positions[0]
        self.draw_cell()

        # Затирание последнего сегмента
        if self.last:
            if type(self.last) is list:
                for last in self.last:
                    last_rect = pg.Rect(last, (GRID_SIZE, GRID_SIZE))
                    pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            else:
                last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
                pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Геттер для головы змеи"""
        return self.positions[0]

    def reset(self):
        """Возврощение змеи к исходному состоянию"""
        self.last = self.positions if hasattr(self, "positions") else []
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Обработка действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT or (
            event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
        ):
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            next_direction = TURNS.get(
                (event.key, game_object.direction), game_object.direction
            )
            game_object.update_direction(next_direction)


def main():
    """Главная функция"""
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    apple.randomize_position()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if apple.position == snake.get_head_position():
            while apple.position in snake.positions:
                apple.randomize_position()
            snake.positions.append(snake.last)
        if snake.get_head_position() in snake.positions[1:-1]:
            snake.reset()
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == "__main__":
    main()
