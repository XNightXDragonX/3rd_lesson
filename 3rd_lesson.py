import os


def recipes_func(file_name):
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"Ошибка: файл '{file_name}' не найден.")
    cook_book = {}
    with open ('recipes.txt', encoding = 'utf-8') as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        dish_name = lines[i].strip()
        i += 1
        try:
            ingridients_count = int(lines[i].strip())
        except ValueError:
            raise ValueError(f"Ошибка: количество ингридиентов для блюда '{dish_name}' должно быть числом.")
        ingridients_count = int(lines[i].strip())
        i += 1
        ingridients = []
        j = 0
        while j < ingridients_count:
            ingridient_line = lines[i].strip()
            parts = ingridient_line.split('|')
            if len(parts) != 3:
                raise ValueError(f"Ошибка: некорректный формат строки ингридиента: '{ingridient_line}' для блюда '{dish_name}'. Ожидаемый формат:\n"
                                 f"Название ингредиента | Количество | Единица измерения")
            ingridient_name = parts[0].strip()
            try:
                quantity = int(parts[1].strip())
            except ValueError:
                raise ValueError(f"Ошибка: количество ингридиента '{ingridient_name}' должно быть числом.")
            measure = parts[2].strip()
            ingridients.append({
                'ingridient_name': ingridient_name,
                'quantity': quantity,
                'measure': measure
            })
            i += 1
            j += 1
        cook_book[dish_name] = ingridients
        i += 1
    return cook_book


def get_shop_list_by_dishes(dishes, person_count, finished_cook_book):
    if not isinstance(person_count, int) or person_count <= 0:
        raise ValueError("Ошибка: количество людей должно быть положительным числом.")
    shop_list = {}
    missing_dishes = []
    for dish in dishes:
        if dish in finished_cook_book:
            for ingridient in finished_cook_book[dish]:
                ingridient_name = ingridient['ingridient_name']
                quantity = ingridient['quantity'] * person_count
                measure = ingridient['measure']
                if ingridient_name in shop_list:
                    shop_list[ingridient_name]['quantity'] += quantity
                else:
                    shop_list[ingridient_name] = {'measure': measure, 'quantity': quantity}
        else:
            missing_dishes.append(dish)
    if missing_dishes:
        print(f"Внимание! Следующие блюда отстутствуют в книге рецептов: {', '.join(missing_dishes)}.")
    formatted_shop_list = "Список покупок:\n" + '\n'.join(
        [f"{name}: {data['quantity']} {data['measure']}" for name, data in shop_list.items()]
    )
    return formatted_shop_list


def merge_files(folder_name, file_names, output_file):
    file_data = []
    for file_name in file_names:
        file_path = os.path.join(folder_name, file_name)
        if not os.path.exists(file_path):
            print("Ошибка, файл '{file_path}' не найден. Он не будет учтён.")
            continue
        with open(file_path, encoding = 'utf-8') as f:
            lines = f.readlines()
        file_data.append((file_name, len(lines), lines))
    file_data.sort(key = lambda x: x[1])
    with open(output_file, 'w', encoding = 'utf-8') as output_f:
        for file_name, line_count, lines in file_data:
            output_f.write(f"===== {file_name} =====\n")
            output_f.write(f"{line_count}\n")
            output_f.writelines(lines)
            output_f.write("\n")


file_name = 'recipes.txt'
folder_name = 'files'
file_names = ['1.txt', '2.txt', '3.txt']
output_file = 'files/merged.txt'

try:
    finished_cook_book = recipes_func(file_name)
    finished_get_shop_list_by_dishes = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2, finished_cook_book)

    print(finished_cook_book)
    print(finished_get_shop_list_by_dishes)

    merge_files(folder_name, file_names, output_file)
except (FileNotFoundError, ValueError) as e:
    print(e)


