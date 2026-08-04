import math


def get_line_intersections(x1, y1, x2, y2, width, height):
    eps = 1e-9
    points = []
    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)
    width = float(width)
    height = float(height)
    dx = float(x2 - x1)
    dy = float(y2 - y1)
    if abs(dx) > eps and abs(dy) > eps:
        t = (0.0 - x1) / dx
        y = y1 + t * dy
        if 0 <= y <= height-1:
            points.append((0, int(y)))
        t = (width-1 - x1) / dx
        y = y1 + t * dy
        if 0 <= y <= height-1:
            points.append((int(width-1), int(y)))
        t = (0 - y1) / dy
        x = x1 + t * dx
        if 0 <= x <= width-1:
            points.append((int(x), 0))
        t = (height - y1) / dy
        x = x1 + t * dx
        if 0 <= x <= width-1:
            points.append((int(x), int(height-1)))
    # Если получилось больше двух точек (например, при совпадении с углами),
    # оставляем две крайние по параметру t вдоль направления прямой.
    if len(points) > 2:
        # Вычисляем параметр t для каждой точки
        if abs(dx) > eps:
            t_values = [(float(p[0]) - x1) / dx for p in points]
        else:  # dy != 0
            t_values = [(float(p[1]) - y1) / dy for p in points]
        # Сортируем по t и берём первую и последнюю
        sorted_points = sorted(zip(t_values, points), key=lambda pair: pair[0])
        points = [sorted_points[0][1], sorted_points[-1][1]]
    return points

def get_params(width, height):
    numbers = []
    a = 0
    b = 0
    check = 0
    x1 = 0
    y1 = 0
    z1 = 0
    x2 = 0
    y2 = 0
    z2 = 0
    try:
        flag = -1
        with open('data.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                for part in parts:
                    numbers.append(float(part))
    except FileNotFoundError:
        print("Ошибка: файл не найден.")
        flag = 0
    except ValueError:
        print("Ошибка: в файле есть нечисловые данные.")
        flag = 0
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        flag = 0
    else:
        # Проверяем, что получилось ровно 6 чисел
        if len(numbers) == 6:
            x1 = float(numbers[0])
            y1 = float(numbers[1])
            z1 = float(numbers[2])
            x2 = float(numbers[3])
            y2 = float(numbers[4])
            z2 = float(numbers[5])
            check = (x1*y2 - x2*y1)
            flag = 1
        else:
            print(f"Ошибка: прочитано {len(numbers)} чисел, а ожидалось 6.")
            flag = 0
    if flag == 1 and check != 0:
        a = (y2*(z1-1) - y1*(z2-1))/(x1*y2 - x2*y1)
        b = (x1*(z2-1) - x2*(z1-1))/(x1*y2 - x2*y1)
    intersections = get_line_intersections(x1, y1, x2, y2, width, height)
    return a, b, flag, intersections

def get_z(a, b, x, y):
    z = float(a) * float(x) + float(b) * float(y) + 1.0
    return z

def get_dist(x1, y1, x2, y2, x0, y0):
    dist = abs((float(x2)-float(x1))*(float(y1)-float(y0)) - (float(x1)-float(x0))*(float(y2)-float(y1))) / (((float(x2) - float(x1))**2 + (float(y2) - float(y1)**2))**0.5)
    return dist

