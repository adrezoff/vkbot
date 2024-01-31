import json

# Загрузка списка администраторов из JSON-файла
def load_admins():
    try:
        with open('admins/admins.json', 'r', encoding='cp1251') as file:
            return json.load(file)
    except FileNotFoundError:
        # Если файл не найден, вернем пустой список администраторов
        return {"list": []}


# Сохранение списка администраторов в JSON-файл
def save_admins(admins):
    with open('admins/admins.json', 'w', encoding='cp1251') as file:
        json.dump(admins, file, ensure_ascii=False, indent=4)


def add_admin(admin_id):
    admins = load_admins()
    admins_list = admins.get("list", [])
    if admin_id not in admins_list:
        admins_list.append(admin_id)
        admins["list"] = admins_list
        save_admins(admins)
        return True
    else:
        return False


def remove_admin(admin_id):
    admins = load_admins()
    admins_list = admins.get("list", [])
    if admin_id in admins_list:
        admins_list.remove(admin_id)
        admins["list"] = admins_list
        save_admins(admins)
        return True
    else:
        return False
