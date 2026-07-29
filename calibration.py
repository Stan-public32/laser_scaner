def get_params():
    numbers = []
    a = 0
    b = 0
    flag = -1
    check = 0
    x1 = 0
    y1 = 0
    z1 = 0
    x2 = 0
    y2 = 0
    z2 = 0
    try:
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
    return a, b, flag

def get_z(a, b, x, y):
    z = float(a) * float(x) + float(b) * float(y) + 1.0
    return z

