import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Гонки 2D")

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)

# Загрузка изображений машин
player_image = pygame.image.load('car_1463810.png').convert_alpha()
enemy_image = pygame.image.load('car_16422421.png').convert_alpha()

# Масштабирование изображений до нужного размера
player_image = pygame.transform.scale(player_image, (50, 85))
enemy_image = pygame.transform.scale(enemy_image, (50, 85))
fon = pygame.image.load('21455.png')
fon = pygame.transform.scale(fon, (screen_width, screen_height))
background = pygame.image.load('images.jpg')
background = pygame.transform.scale(fon, (screen_width, screen_height))
# Параметры игрока
player_pos = [screen_width // 2 - 100, screen_height - 2 * 85]

# Параметры врагов
enemy_speed = 8
enemy_spawn_rate = 10
enemies = []

# Константы для управления скоростью игрока
INITIAL_PLAYER_SPEED = 0
PLAYER_SPEED_INCREMENT = 1

# Параметры игры
finish_line_pos = screen_height // 4

clock = pygame.time.Clock()

# Функция для рисования кнопок с закругленными углами
def draw_button(screen, color, x, y, width, height, text, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=20)  # Рисуем прямоугольник с закругленными углами

    font = pygame.font.Font(None, 36)  # Устанавливаем шрифт и размер текста
    text_surf = font.render(text, True, text_color)  # Создаем поверхность с текстом
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))  # Получаем прямоугольник текста
    screen.blit(text_surf, text_rect)  # Отображаем текст на экране

# Функция для проверки клика по кнопке
def button_clicked(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)

# Отображение стартового меню
def start_menu():
    while True:
        screen.blit(fon, (0,0))  # Заполняем экран белым цветом

        # Рисуем кнопку "Level 1"
        level1_button_rect = pygame.Rect(300, 150, 200, 100)
        draw_button(screen, green, *level1_button_rect, "Level 1", white)

        # Рисуем кнопку "Level 2"
        level2_button_rect = pygame.Rect(300, 300, 200, 100)
        draw_button(screen, blue, *level2_button_rect, "Level 2", white)

        # Рисуем кнопку "Exit"
        exit_button_rect = pygame.Rect(300, 450, 200, 100)
        draw_button(screen, red, *exit_button_rect, "Exit", white)

        pygame.display.update()  # Обновляем экран

        for event in pygame.event.get():  # Обрабатываем события
            if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                pygame.quit()  # Завершаем Pygame
                sys.exit()  # Завершаем выполнение программы
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Если было нажатие кнопки мыши
                mouse_pos = pygame.mouse.get_pos()  # Получаем позицию мыши
                if button_clicked(mouse_pos, level1_button_rect):  # Проверяем клик по кнопке "Level 1"
                    start_game(level=1)  # Запускаем игру на первом уровне
                elif button_clicked(mouse_pos, level2_button_rect):  # Проверяем клик по кнопке "Level 2"
                    start_game(level=2)  # Запускаем игру на втором уровне
                elif button_clicked(mouse_pos, exit_button_rect):  # Проверяем клик по кнопке "Exit"
                    pygame.quit()
                    sys.exit()

# Функция для создания нового врага
def create_enemy():
    x_pos = random.randint(0, screen_width - enemy_image.get_width())
    y_pos = -enemy_image.get_height()
    return [x_pos, y_pos]

# Функция для игрового экрана первого уровня
def game_screen_level1():
    screen.blit(background, (0, 0))  # Заполняем экран белым цветом
    global game_over, start_time
    game_over = False  # Инициализируем game_over
    frame_count = 0
    start_time = pygame.time.get_ticks()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_pos[0] -= 5
        if keys[pygame.K_RIGHT]:
            player_pos[0] += 5
        if keys[pygame.K_UP]:
            player_pos[1] -= 5
        if keys[pygame.K_DOWN]:
            player_pos[1] += 5

        if player_pos[0] < 0:
            player_pos[0] = 0
        if player_pos[0] > screen_width - player_image.get_width():
            player_pos[0] = screen_width - player_image.get_width()
        if player_pos[1] < 0:
            player_pos[1] = 0
        if player_pos[1] > screen_height - player_image.get_height():
            player_pos[1] = screen_height - player_image.get_height()

        screen.fill(white)

        frame_count += 1
        if frame_count % enemy_spawn_rate == 0:
            enemies.append(create_enemy())

        # Проверка на наличие врагов перед их отрисовкой и обновлением позиций
        if len(enemies) > 0:
            for enemy in enemies:
                enemy[1] += enemy_speed
                if enemy[1] > screen_height:
                    enemies.remove(enemy)
                else:
                    screen.blit(enemy_image, enemy)

                # Проверка на столкновение с врагами
                if player_pos[1] < enemy[1] + enemy_image.get_height() and player_pos[1] + player_image.get_height() > enemy[1]:
                    if player_pos[0] < enemy[0] + enemy_image.get_width() and player_pos[0] + player_image.get_width() > enemy[0]:
                        game_over = True

        screen.blit(player_image, player_pos)

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, black)
        screen.blit(timer_text, (10, 10))

        pygame.display.update()
        clock.tick(30)

    game_over_screen(elapsed_time)

# Функция для игрового экрана второго уровня
def game_screen_level2():
    global game_over, car1_speed, car2_speed, car2_pos
    game_over = False  # Инициализируем game_over
    car1_pos = [screen_width // 2 - 200, screen_height - 2 * 85]  # Начальная позиция первой машины
    car2_pos = [screen_width // 2 + 100, screen_height - 2 * 85]  # Начальная позиция второй машины
    car1_speed = INITIAL_PLAYER_SPEED  # Начальная скорость первой машины
    car2_speed = 2  # Константная скорость второй машины

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    car1_speed += PLAYER_SPEED_INCREMENT  # Увеличиваем скорость первой машины при нажатии пробела

        screen.fill(white)  # Заполняем экран белым цветом

        # Обновление позиций машин
        car1_pos[1] -= car1_speed  # Перемещаем первую машину вверх на значение ее скорости
        car2_pos[1] -= car2_speed  # Перемещаем вторую машину вверх на значение ее скорости

        if car1_pos[1] <= finish_line_pos or car2_pos[1] <= finish_line_pos:
            game_over = True  # Игра заканчивается, когда одна из машин достигает финишной линии

        pygame.draw.line(screen, black, (screen_width // 2, 0), (screen_width // 2, screen_height), 5)  # Линия по центру экрана
        pygame.draw.line(screen, red, (0, finish_line_pos), (screen_width, finish_line_pos), 5)  # Финишная линия

        screen.blit(player_image, car1_pos)  # Отображаем первую машин
        screen.blit(player_image, car2_pos)  # Отображаем вторую машину

        pygame.display.update()
        clock.tick(30)  # Ограничиваем количество кадров в секунду

    winner = "Car 1" if car1_pos[1] <= finish_line_pos else "Car 2"  # Определяем победителя
    game_over_screen(winner)  # Отображаем экран окончания игры

# Функция для экрана Game Over
def game_over_screen(game_result):
    while True:
        screen.fill(white)
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, red)
        text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 - 100))  # Сместили текст вверх
        screen.blit(text, text_rect)

        if isinstance(game_result, float):
            font = pygame.font.Font(None, 36)
            time_text = font.render(f"Time: {game_result:.2f} seconds", True, black)
            time_text_rect = time_text.get_rect(center=(screen_width / 2, screen_height / 2 - 20))  # Сместили текст вверх
            screen.blit(time_text, time_text_rect)
        else:
            font = pygame.font.Font(None, 36)
            winner_text = font.render(f"Winner: {game_result}", True, black)
            winner_text_rect = winner_text.get_rect(center=(screen_width / 2, screen_height / 2 - 20))  # Сместили текст вверх
            screen.blit(winner_text, winner_text_rect)

        restart_button_rect2 = pygame.Rect(200, 300, 200, 100)  # Переместили кнопку вверх
        draw_button(screen, green, *restart_button_rect2, "Return to 2", white)

        restart_button_rect1 = pygame.Rect(425, 300, 200, 100)  # Переместили кнопку вверх
        draw_button(screen, green, *restart_button_rect1, "Return to 1", white)

        exit_button_rect = pygame.Rect(300, 450, 200, 100)  # Переместили кнопку вверх
        draw_button(screen, red, *exit_button_rect, "Exit", white)

        level2_button_rect = pygame.Rect(300, 50, 200, 100)
        draw_button(screen, blue, *level2_button_rect, "Назад", white)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_clicked(mouse_pos, restart_button_rect2):
                    start_game(level=2)
                if button_clicked(mouse_pos, restart_button_rect1):
                    start_game(level=1)
                if button_clicked(mouse_pos,  level2_button_rect ):
                    return "назад"
                elif button_clicked(mouse_pos, exit_button_rect):
                    pygame.quit()
                    sys.exit()

# Функция для запуска игры с выбранным уровнем
def start_game(level=1):
    global enemy_spawn_rate, game_over, enemies, player_pos

    if level == 1:
        enemy_spawn_rate = 10  # Уровень 1 - стандартные параметры
        game_screen_level1()
    elif level == 2:
        game_screen_level2()

# Запуск стартового меню
start_menu()
