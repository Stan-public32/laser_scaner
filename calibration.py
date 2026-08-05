import numpy as np

def mask_calc(radius, width, height):
    mask2 = np.full((width, height), 0, dtype=np.uint8)
    center = (height // 2, width // 2)
    yy, xx = np.ogrid[:height, :width]
    dist_sq = (xx - center[1]) ** 2 + (yy - center[0]) ** 2
    mask2[dist_sq <= radius ** 2] = 255
    return mask2

def get_min_max(int_sect):
    min_max = []
    if int_sect[0][0] > int_sect[1][0]:
        min_max.append((int_sect[1][0], int_sect[0][0]))
    else:
        min_max.append((int_sect[0][0], int_sect[1][0]))
    if int_sect[0][1] > int_sect[1][1]:
        min_max.append((int_sect[1][1], int_sect[0][1]))
    else:
        min_max.append((int_sect[0][1], int_sect[1][1]))
    return min_max

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
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    a = 0.0
    b = 0.0
    mx = 0.0
    my = 0.0
    sxx = 0.0
    syy = 0.0
    sxy = 0.0
    check = 0.0
    coords = [[0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0]]
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
        if len(numbers) == 12:
            for i in range(12):
                coords[i//3][i%3] = numbers[i]
            for i in range(4):
                mx += float(coords[i][0]) / 4.0
                my += float(coords[i][1]) / 4.0
            for i in range(4):
                sxx += (float(coords[i][0]-mx) ** 2)
                syy += (float(coords[i][1]-my) ** 2)
                sxy += (float(coords[i][0]-mx) * float(coords[i][1]-my))
            check = sxy
            flag = 1
        else:
            print(f"Ошибка: прочитано {len(numbers)} чисел, а ожидалось 6.")
            flag = 0
    if flag == 1 and check != 0:
        temp = (sxx + syy - ((sxx-syy)**2 + 4*sxy*sxy)**0.5) / 2.0
        a = sxy
        b = temp - sxx
        c = (-1.0) * (a*mx + b*my)
        a = a / c
        b = b / c
        x1 = float(coords[0][0])
        x2 = float(coords[3][0])
        y1 = (-1.0) * (a * x1 + 1.0) / b
        y2 = (-1.0) * (a * x2 + 1.0) / b
    intersections = get_line_intersections(x1, y1, x2, y2, width, height)
    xx = np.array([coords[0][0], coords[1][0], coords[2][0], coords[3][0]])
    zz = np.array([coords[0][2], coords[1][2], coords[2][2], coords[3][2]])
    mtrx = np.vstack([xx ** 3, xx ** 2, xx, np.ones_like(xx)]).T
    cfs = np.linalg.solve(mtrx, zz)
    return a, b, flag, intersections, cfs

def get_z(k, l, m, n, x):
    z = float(k) * (float(x)**3) + float(l) * (float(x)**2) + float(m) * float(x) + float(n)
    return z

def get_dist(x1, y1, x2, y2, x0, y0):
    dist = abs((float(x2)-float(x1))*(float(y1)-float(y0)) - (float(x1)-float(x0))*(float(y2)-float(y1))) / (((float(x2) - float(x1))**2 + (float(y2) - float(y1)**2))**0.5)
    return dist
