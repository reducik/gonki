import pygame  # Импортируем модуль pygame для создания игр
import sys  # Импортируем модуль sys для выхода из программы
import random  # Импортируем модуль random для генерации случайных чисел

# Инициализация Pygame
pygame.init()  # Инициализируем все модули pygame

# Параметры экрана
screen_width = 800  # Ширина экрана
screen_height = 600  # Высота экрана
screen = pygame.display.set_mode((screen_width, screen_height))  # Создаем окно с заданными размерами
pygame.display.set_caption("Гонки 2D")  # Устанавливаем заголовок окна

# Цвета
white = (255, 255, 255)  # Белый цвет
black = (0, 0, 0)  # Черный цвет
red = (255, 0, 0)  # Красный цвет
green = (0, 200, 0)  # Зеленый цвет
blue = (0, 0, 255)  # Синий цвет

# Загрузка изображений машин
player_image = pygame.image.load('car_1463810.png').convert_alpha()  # Загрузка изображения машины игрока с поддержкой прозрачности
enemy_image = pygame.image.load('car_16422421.png').convert_alpha()  # Загрузка изображения машины врага с поддержкой прозрачности

# Масштабирование изображений до нужного размера
player_image = pygame.transform.scale(player_image, (50, 85))  # Масштабируем изображение игрока до размеров 50x85
enemy_image = pygame.transform.scale(enemy_image, (50, 85))  # Масштабируем изображение врага до размеров 50x85

# Параметры игрока
player_pos = [screen_width // 2, screen_height - 2 * 85]  # Начальная позиция игрока

# Параметры врагов
enemy_speed = 8  # Скорость движения врагов
enemy_spawn_rate = 10  # Частота появления врагов (в кадрах)
enemies = []  # Список для хранения врагов

clock = pygame.time.Clock()  # Создаем объект для контроля времени

# Функция для рисования кнопок
def draw_button(screen, color, x, y, width, height, text, text_color):
    pygame.draw.ellipse(screen, color, (x, y, width, height))  # Рисуем окружность (эллипс)

    font = pygame.font.Font(None, 36)  # Устанавливаем шрифт и размер текста
    text_surf = font.render(text, True, text_color)  # Создаем поверхность с текстом
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))  # Получаем прямоугольник текста
    screen.blit(text_surf, text_rect)  # Отображаем текст на экране

# Функция для проверки клика по кнопке
def button_clicked(mouse_pos, button_pos, button_radius):
    if (mouse_pos[0] - button_pos[0])**2 + (mouse_pos[1] - button_pos[1])**2 <= button_radius**2:
        return True  # Если расстояние до центра кнопки меньше или равно радиусу кнопки, возвращаем True
    return False  # Иначе возвращаем False

# Отображение стартового меню
def start_menu():
    while True:
        screen.fill(white)  # Заполняем экран белым цветом

        # Рисуем кнопку "Start"
        draw_button(screen, green, 300, 200, 200, 100, "Start", white)

        # Рисуем кнопку "Exit"
        draw_button(screen, red, 300, 350, 200, 100, "Exit", white)

        pygame.display.update()  # Обновляем экран

        for event in pygame.event.get():  # Обрабатываем события
            if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                pygame.quit()  # Завершаем Pygame
                sys.exit()  # Завершаем выполнение программы
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Если было нажатие кнопки мыши
                mouse_pos = pygame.mouse.get_pos()  # Получаем позицию мыши
                if button_clicked(mouse_pos, (300 + 100, 200 + 50), 100):  # Проверяем клик по кнопке "Start"
                    return True  # Возвращаем True для начала игры
                elif button_clicked(mouse_pos, (300 + 100, 350 + 50), 100):  # Проверяем клик по кнопке "Exit"
                    pygame.quit()
                    sys.exit()

# Функция для создания нового врага
def create_enemy():
    x_pos = random.randint(0, screen_width - enemy_image.get_width())  # Случайная позиция по оси X в пределах экрана
    y_pos = -enemy_image.get_height()  # Начальная позиция по оси Y за пределами экрана
    return [x_pos, y_pos]  # Возвращаем координаты нового врага

# Функция для игрового экрана
def game_screen():
    global game_over, start_time
    frame_count = 0  # Счетчик кадров
    start_time = pygame.time.get_ticks()  # Время начала игры

    while not game_over:  # Пока игра не окончена
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                pygame.quit()  # Завершаем Pygame
                sys.exit()  # Завершаем выполнение программы

        keys = pygame.key.get_pressed()  # Получаем состояние всех клавиш

        if keys[pygame.K_LEFT]:  # Если нажата клавиша влево
            player_pos[0] -= 5  # Двигаем игрока влево
        if keys[pygame.K_RIGHT]:  # Если нажата клавиша вправо
            player_pos[0] += 5  # Двигаем игрока вправо
        if keys[pygame.K_UP]:  # Если нажата клавиша вверх
            player_pos[1] -= 5  # Двигаем игрока вверх
        if keys[pygame.K_DOWN]:  # Если нажата клавиша вниз
            player_pos[1] += 5  # Двигаем игрока вниз

        # Ограничиваем движение игрока пределами экрана
        if player_pos[0] < 0:
            player_pos[0] = 0
        if player_pos[0] > screen_width - player_image.get_width():
            player_pos[0] = screen_width - player_image.get_width()
        if player_pos[1] < 0:
            player_pos[1] = 0
        if player_pos[1] > screen_height - player_image.get_height():
            player_pos[1] = screen_height - player_image.get_height()

        screen.fill(white)  # Заполняем экран белым цветом

        # Генерация новых врагов
        frame_count += 1
        if frame_count % enemy_spawn_rate == 0:
            enemies.append(create_enemy())  # Добавляем нового врага в список

        # Обновление позиции врагов
        for enemy in enemies:
            enemy[1] += enemy_speed  # Двигаем врага вниз
            # Удаление врагов, вышедших за пределы экрана
            if enemy[1] > screen_height:
                enemies.remove(enemy)

        # Отображение спрайтов машин
        screen.blit(player_image, player_pos)  # Отображаем машину игрока
        for enemy in enemies:
            screen.blit(enemy_image, enemy)  # Отображаем врагов

        # Проверка столкновения
        for enemy in enemies:
            if player_pos[1] < enemy[1] + enemy_image.get_height() and player_pos[1] + player_image.get_height() > enemy[1]:
                if player_pos[0] < enemy[0] + enemy_image.get_width() and player_pos[0] + player_image.get_width() > enemy[0]:
                    game_over = True  # Если есть столкновение, завершаем игру

        # Отображение таймера на экране
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Вычисляем время с начала игры
        font = pygame.font.Font(None, 36)  # Создаем объект шрифта
        timer_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, black)  # Создаем текст таймера
        screen.blit(timer_text, (10, 10))  # Отображаем таймер на экране

        pygame.display.update()  # Обновляем экран
        clock.tick(30)  # Устанавливаем количество кадров в секунду

# Функция для экрана Game Over
def game_over_screen(game_time):
    while True:
        screen.fill(white)  # Заполняем экран белым цветом
        font = pygame.font.Font(None, 74)  # Создаем объект шрифта большого размера
        text = font.render("Game Over", True, red)  # Создаем текст "Game Over"
        text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 - 50))  # Получаем прямоугольник текста
        screen.blit(text, text_rect)  # Отображаем текст "Game Over" на экране

        # Отображение времени игры
        font = pygame.font.Font(None, 36)  # Создаем объект шрифта
        time_text = font.render(f"Time: {game_time:.2f} seconds", True, black)  # Создаем текст с временем игры
        time_text_rect = time_text.get_rect(center=(screen_width / 2, screen_height / 2 + 50))  # Получаем прямоугольник текста
        screen.blit(time_text, time_text_rect)  # Отображаем текст с временем игры на экране

        # Рисуем кнопку "Restart"
        draw_button(screen, green, 300, 400, 200, 100, "Restart", white)

        # Рисуем кнопку "Exit"
        draw_button(screen, red, 300, 520, 200, 100, "Exit", white)

        pygame.display.update()  # Обновляем экран

        for event in pygame.event.get():  # Обрабатываем события
            if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                pygame.quit()  # Завершаем Pygame
                sys.exit()  # Завершаем выполнение программы
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Если было нажатие кнопки мыши
                mouse_pos = pygame.mouse.get_pos()  # Получаем позицию мыши
                if button_clicked(mouse_pos, (300 + 100, 400 + 50), 100):  # Проверяем клик по кнопке "Restart"
                    return "restart"  # Возвращаем "restart" для перезапуска игры
                elif button_clicked(mouse_pos, (300 + 100, 520 + 50), 100):  # Проверяем клик по кнопке "Exit"
                    pygame.quit()  # Завершаем Pygame
                    sys.exit()  # Завершаем выполнение программы

# Запуск стартового меню
while True:
    if start_menu():  # Если кнопка "Start" была нажата
        game_over = False  # Игра не окончена
        enemies = []  # Сбрасываем список врагов
        player_pos = [screen_width // 2, screen_height - 2 * 85]  # Сбрасываем позицию игрока
        game_screen()  # Запускаем игровой экран
        end_time = pygame.time.get_ticks()  # Время окончания игры
        game_time = (end_time - start_time) / 1000  # Время игры в секундах
        action = game_over_screen(game_time)  # Показываем экран Game Over
        if action == "restart":  # Если выбрана перезагрузка
            continue  # Перезапускаем цикл
        else:
            pygame.quit()  # Завершаем Pygame
            sys.exit()  # Завершаем выполнение программы
    else:
        pygame.quit()  # Завершаем Pygame
        sys.exit()  # Завершаем выполнение программы
